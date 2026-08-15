"use client";

import { Suspense, useCallback, useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import AttendanceModal from "@/components/parent/AttendanceModal";
import {
  DashboardSkeleton,
  ProfileCard,
  StatusBadge,
  Toast,
} from "@/components/parent/ParentDashboardParts";
import { ApiError, nurseryApi } from "@/lib/api";
import { formatTodayJa, todayIsoDate } from "@/lib/attendance";
import type { Attendance, Children, UserMeParent } from "@/types";

const NOTICES = [
  {
    title: "本日の持ち物について",
    body: "気温の変動があります。着替えとタオルを多めにお願いします。",
  },
  {
    title: "給食のお知らせ",
    body: "本日の給食はカレーライスです。アレルギー対応もご用意しています。",
  },
];

export default function ParentDashboardPage() {
  return (
    <Suspense fallback={<DashboardSkeleton />}>
      <ParentDashboardContent />
    </Suspense>
  );
}

function ParentDashboardContent() {
  const searchParams = useSearchParams();
  const parentId = Number(searchParams.get("parent") ?? "1");

  const [loading, setLoading] = useState(true);
  const [me, setMe] = useState<UserMeParent | null>(null);
  const [selectedChild, setSelectedChild] = useState<Children | null>(null);
  const [attendance, setAttendance] = useState<Attendance | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: "success" | "error" } | null>(null);

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const profile = await nurseryApi.getMe("parent", parentId);
      if (profile.role !== "parent") {
        throw new Error("保護者プロファイルではありません");
      }
      setMe(profile);
      const child = profile.children[0] ?? null;
      setSelectedChild(child);

      if (child) {
        const attendances = await nurseryApi.listAttendances({ date: todayIsoDate() });
        const todayRecord =
          attendances.results.find((item) => item.child === child.id) ?? null;
        setAttendance(todayRecord);
      } else {
        setAttendance(null);
      }
    } catch (error) {
      const message =
        error instanceof ApiError ? error.message : "データの取得に失敗しました";
      setToast({ message, type: "error" });
    } finally {
      setLoading(false);
    }
  }, [parentId]);

  useEffect(() => {
    void loadData();
  }, [loadData]);

  const classOptions = useMemo(
    () => me?.children.map((child) => ({ id: child.id, name: child.full_name })) ?? [],
    [me],
  );

  if (loading) {
    return <DashboardSkeleton />;
  }

  return (
    <div className="mx-auto min-h-screen max-w-md pb-28">
      <header className="sticky top-0 z-40 border-b border-slate-100 bg-white/95 px-4 py-3 backdrop-blur">
        <p className="text-xs font-semibold text-sky-500">Parent</p>
        <h1 className="text-lg font-bold text-slate-900">保護者ホーム</h1>
        <p className="text-xs text-slate-500">{formatTodayJa()}</p>
      </header>

      <main className="space-y-5 px-4 pt-4">
        {toast && (
          <Toast
            message={toast.message}
            type={toast.type}
            onClose={() => setToast(null)}
          />
        )}

        {!selectedChild ? (
          <div className="rounded-3xl bg-white p-6 text-center text-sm text-slate-500 shadow-sm ring-1 ring-slate-100">
            お子さまの登録がありません
          </div>
        ) : (
          <>
            {classOptions.length > 1 && (
              <div className="flex gap-2 overflow-x-auto pb-1">
                {classOptions.map((option) => (
                  <button
                    key={option.id}
                    type="button"
                    onClick={() => {
                      const child = me?.children.find((c) => c.id === option.id) ?? null;
                      setSelectedChild(child);
                      void (async () => {
                        const attendances = await nurseryApi.listAttendances({
                          date: todayIsoDate(),
                        });
                        setAttendance(
                          attendances.results.find((item) => item.child === option.id) ?? null,
                        );
                      })();
                    }}
                    className={`min-h-12 shrink-0 rounded-full px-4 text-sm font-semibold ${
                      selectedChild.id === option.id
                        ? "bg-sky-500 text-white"
                        : "bg-white text-slate-600 ring-1 ring-slate-200"
                    }`}
                  >
                    {option.name}
                  </button>
                ))}
              </div>
            )}

            <ProfileCard child={selectedChild} />

            <section className="rounded-3xl bg-white p-4 shadow-sm ring-1 ring-slate-100">
              <p className="text-xs font-semibold text-slate-500">本日の出欠</p>
              <div className="mt-3 flex flex-wrap items-center gap-2">
                <StatusBadge attendance={attendance} />
                {attendance?.reason && (
                  <span className="text-sm text-slate-600">理由：{attendance.reason}</span>
                )}
              </div>
              {attendance?.scheduled_arrival_time && (
                <p className="mt-2 text-sm text-slate-600">
                  予定登園：{attendance.scheduled_arrival_time.slice(0, 5)}
                </p>
              )}
              {attendance?.note && (
                <p className="mt-2 text-sm text-slate-600">特記：{attendance.note}</p>
              )}
              {attendance && (
                <p className="mt-2 text-xs font-semibold text-slate-500">
                  {attendance.is_confirmed ? "園側で確認済み" : "園側の確認待ち"}
                </p>
              )}
            </section>

            <button
              type="button"
              onClick={() => setModalOpen(true)}
              className="flex min-h-16 w-full items-center justify-center rounded-3xl bg-rose-500 px-4 text-base font-bold text-white shadow-md active:bg-rose-600"
            >
              欠席・遅刻の連絡をする
            </button>
            <p className="text-center text-xs text-slate-500">タップして10秒で連絡できます</p>
          </>
        )}

        <section>
          <h2 className="mb-3 text-base font-bold text-slate-800">園からのお便り</h2>
          <ul className="space-y-3">
            {NOTICES.map((notice) => (
              <li
                key={notice.title}
                className="rounded-3xl bg-white p-4 shadow-sm ring-1 ring-slate-100"
              >
                <p className="text-sm font-bold text-slate-900">{notice.title}</p>
                <p className="mt-2 text-sm leading-relaxed text-slate-600">{notice.body}</p>
              </li>
            ))}
          </ul>
        </section>
      </main>

      <nav className="fixed bottom-0 left-0 right-0 z-50 border-t border-slate-200 bg-white/95 backdrop-blur">
        <div className="mx-auto grid max-w-md grid-cols-4">
          <a href={`/parent/dashboard?parent=${parentId}`} className="flex min-h-14 flex-col items-center justify-center gap-0.5 text-sky-600">
            <span className="text-lg">🏠</span>
            <span className="text-[11px] font-semibold">ホーム</span>
          </a>
          <button
            type="button"
            onClick={() => setModalOpen(true)}
            className="flex min-h-14 flex-col items-center justify-center gap-0.5 text-slate-500"
          >
            <span className="text-lg">📝</span>
            <span className="text-[11px] font-semibold">連絡</span>
          </button>
          <a href="#notices" className="flex min-h-14 flex-col items-center justify-center gap-0.5 text-slate-500">
            <span className="text-lg">✉️</span>
            <span className="text-[11px] font-semibold">お便り</span>
          </a>
          <span className="flex min-h-14 flex-col items-center justify-center gap-0.5 text-slate-400">
            <span className="text-lg">👤</span>
            <span className="text-[11px] font-semibold">設定</span>
          </span>
        </div>
      </nav>

      {selectedChild && (
        <AttendanceModal
          open={modalOpen}
          child={selectedChild}
          existingAttendance={attendance}
          onClose={() => setModalOpen(false)}
          onSuccess={(updated) => {
            setAttendance(updated);
            setToast({ message: "連絡を送信しました", type: "success" });
          }}
          onError={(message) => setToast({ message, type: "error" })}
        />
      )}
    </div>
  );
}
