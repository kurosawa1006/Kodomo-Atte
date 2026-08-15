"use client";

import { Suspense, useCallback, useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import AttendanceCheckCard from "@/components/staff/AttendanceCheckCard";
import { Toast } from "@/components/parent/ParentDashboardParts";
import { ApiError, nurseryApi } from "@/lib/api";
import {
  formatTodayJa,
  fromApiAttendanceStatus,
  classAgeLabel,
  todayIsoDate,
  toApiAttendanceStatus,
} from "@/lib/attendance";
import {
  AttendanceStatus,
  type Attendance,
  type Children,
  type Class,
  type PaginatedResponse,
  type UserMeStaff,
} from "@/types";

type ClassFilter = "all" | number;
type ToastState = { message: string; type: "success" | "error" } | null;

async function fetchAllPages<T>(
  fetchPage: (page: number) => Promise<PaginatedResponse<T>>,
): Promise<T[]> {
  const first = await fetchPage(1);
  const items = [...first.results];
  const pageSize = first.results.length || 100;
  const totalPages = Math.max(1, Math.ceil(first.count / pageSize));
  for (let page = 2; page <= totalPages; page += 1) {
    const next = await fetchPage(page);
    items.push(...next.results);
  }
  return items;
}

function statusDisplayLabel(status: AttendanceStatus): string {
  switch (status) {
    case AttendanceStatus.Late:
      return "遅刻";
    case AttendanceStatus.Absent:
      return "欠席";
    case AttendanceStatus.RequestedCare:
      return "希望保育";
    default:
      return "出席";
  }
}

export default function StaffAttendancePage() {
  return (
    <Suspense fallback={<StaffAttendanceSkeleton />}>
      <StaffAttendanceContent />
    </Suspense>
  );
}

function StaffAttendanceContent() {
  const searchParams = useSearchParams();
  const staffId = Number(searchParams.get("staff") ?? "1");

  const [loading, setLoading] = useState(true);
  const [me, setMe] = useState<UserMeStaff | null>(null);
  const [children, setChildren] = useState<Children[]>([]);
  const [attendances, setAttendances] = useState<Attendance[]>([]);
  const [classFilter, setClassFilter] = useState<ClassFilter>("all");
  const [busyIds, setBusyIds] = useState<Set<number>>(new Set());
  const [toast, setToast] = useState<ToastState>(null);

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const profile = await nurseryApi.getMe("staff", staffId);
      if (profile.role !== "staff") {
        throw new Error("スタッフプロファイルではありません");
      }
      setMe(profile);

      const [childList, attendanceList] = await Promise.all([
        fetchAllPages((page) => nurseryApi.listChildren({ page })),
        fetchAllPages((page) =>
          nurseryApi.listAttendances({ date: todayIsoDate(), page }),
        ),
      ]);

      setChildren(childList);
      setAttendances(attendanceList);
    } catch (error) {
      const message =
        error instanceof ApiError ? error.message : "データの取得に失敗しました";
      setToast({ message, type: "error" });
    } finally {
      setLoading(false);
    }
  }, [staffId]);

  useEffect(() => {
    void loadData();
  }, [loadData]);

  const classTabs = useMemo(() => {
    const map = new Map<number, Class>();
    children.forEach((child) => {
      if (child.nursery_class_detail) {
        map.set(child.nursery_class_detail.id, child.nursery_class_detail);
      }
    });
    return Array.from(map.values()).sort((a, b) => a.id - b.id);
  }, [children]);

  const filteredChildren = useMemo(() => {
    if (classFilter === "all") return children;
    return children.filter((child) => child.nursery_class === classFilter);
  }, [children, classFilter]);

  const attendanceByChild = useMemo(() => {
    const map = new Map<number, Attendance>();
    attendances.forEach((item) => map.set(item.child, item));
    return map;
  }, [attendances]);

  const summary = useMemo(() => {
    const total = filteredChildren.length;
    let late = 0;
    let absent = 0;
    filteredChildren.forEach((child) => {
      const record = attendanceByChild.get(child.id);
      const status = record
        ? fromApiAttendanceStatus(record.attendance_status)
        : AttendanceStatus.Present;
      if (status === AttendanceStatus.Late) late += 1;
      if (status === AttendanceStatus.Absent || status === AttendanceStatus.RequestedCare) {
        absent += 1;
      }
    });
    const present = Math.max(total - late - absent, 0);
    return { total, present, late, absent };
  }, [filteredChildren, attendanceByChild]);

  const unconfirmed = useMemo(() => {
    return filteredChildren
      .map((child) => ({ child, attendance: attendanceByChild.get(child.id) ?? null }))
      .filter(({ attendance }) => {
        if (!attendance || attendance.is_confirmed) return false;
        const status = fromApiAttendanceStatus(attendance.attendance_status);
        return status === AttendanceStatus.Late || status === AttendanceStatus.Absent;
      })
      .sort((a, b) => {
        const sa = fromApiAttendanceStatus(a.attendance!.attendance_status);
        const sb = fromApiAttendanceStatus(b.attendance!.attendance_status);
        if (sa !== sb) return sa - sb;
        return a.child.full_kana.localeCompare(b.child.full_kana, "ja");
      });
  }, [filteredChildren, attendanceByChild]);

  const setBusy = (childId: number, on: boolean) => {
    setBusyIds((prev) => {
      const next = new Set(prev);
      if (on) next.add(childId);
      else next.delete(childId);
      return next;
    });
  };

  const replaceAttendance = (updated: Attendance) => {
    setAttendances((prev) => {
      const index = prev.findIndex(
        (item) => item.id === updated.id || item.child === updated.child,
      );
      if (index === -1) return [...prev, updated];
      const next = [...prev];
      next[index] = updated;
      return next;
    });
  };

  const removeAttendanceForChild = (childId: number) => {
    setAttendances((prev) => prev.filter((item) => item.child !== childId));
  };

  const runOptimistic = async (
    child: Children,
    optimistic: Attendance | null,
    request: () => Promise<Attendance | null>,
    successMessage: string,
  ) => {
    const previous = attendanceByChild.get(child.id) ?? null;
    setBusy(child.id, true);
    if (optimistic) replaceAttendance(optimistic);
    else removeAttendanceForChild(child.id);

    try {
      const result = await request();
      if (result) replaceAttendance(result);
      else removeAttendanceForChild(child.id);
      setToast({ message: successMessage, type: "success" });
    } catch (error) {
      if (previous) replaceAttendance(previous);
      else removeAttendanceForChild(child.id);
      const message =
        error instanceof ApiError ? error.message : "更新に失敗しました";
      setToast({ message, type: "error" });
    } finally {
      setBusy(child.id, false);
    }
  };

  const buildOptimistic = (
    child: Children,
    current: Attendance | null,
    patch: Partial<Attendance>,
  ): Attendance => {
    const now = new Date().toISOString();
    if (current) {
      return { ...current, ...patch, updated_at: now };
    }
    return {
      id: -child.id,
      child: child.id,
      child_detail: child,
      checked_by: me?.profile.id ?? null,
      checked_by_detail: me?.profile ?? null,
      date: todayIsoDate(),
      attendance_status: null,
      attendance_status_display: null,
      reason: "",
      scheduled_arrival_time: null,
      note: "",
      is_confirmed: false,
      is_deleted: false,
      created_at: now,
      updated_at: now,
      ...patch,
    };
  };

  const handleConfirm = (child: Children) => {
    const current = attendanceByChild.get(child.id);
    if (!current || current.id < 0) return;
    void runOptimistic(
      child,
      buildOptimistic(child, current, { is_confirmed: true }),
      async () => nurseryApi.updateAttendance(current.id, { is_confirmed: true }),
      `${child.full_name}さんを確認済みにしました`,
    );
  };

  const handleSetStatus = (
    child: Children,
    status: AttendanceStatus,
    successMessage: string,
  ) => {
    const current = attendanceByChild.get(child.id) ?? null;
    // 記録なし＝出席扱いのため、出席への変更は API 不要
    if (!current && status === AttendanceStatus.Present) {
      setToast({ message: successMessage, type: "success" });
      return;
    }

    const apiStatus = toApiAttendanceStatus(status);
    const optimistic = buildOptimistic(child, current, {
      attendance_status: apiStatus,
      attendance_status_display: statusDisplayLabel(status),
      is_confirmed:
        status === AttendanceStatus.Present ? true : (current?.is_confirmed ?? false),
    });

    void runOptimistic(
      child,
      status === AttendanceStatus.Present && current
        ? { ...optimistic, attendance_status: null }
        : optimistic,
      async () => {
        const payload = {
          attendance_status: status,
          is_confirmed: status === AttendanceStatus.Present ? true : undefined,
        };
        if (current && current.id > 0) {
          return nurseryApi.updateAttendance(current.id, payload);
        }
        return nurseryApi.createAttendance({
          child: child.id,
          date: todayIsoDate(),
          ...payload,
        });
      },
      successMessage,
    );
  };

  if (loading) {
    return <StaffAttendanceSkeleton />;
  }

  return (
    <div className="mx-auto min-h-screen max-w-3xl pb-28">
      <header className="sticky top-0 z-40 border-b border-slate-100 bg-white/95 px-4 py-3 backdrop-blur">
        <p className="text-xs font-semibold text-sky-500">Staff</p>
        <h1 className="text-lg font-bold text-slate-900">出欠確認・承認</h1>
        <p className="text-xs text-slate-500">
          {formatTodayJa()}
          {me ? ` ／ ${me.profile.full_name}` : ""}
        </p>
      </header>

      <main className="space-y-5 px-4 pt-4">
        {toast ? (
          <Toast
            message={toast.message}
            type={toast.type}
            onClose={() => setToast(null)}
          />
        ) : null}

        <section>
          <p className="mb-2 text-xs font-semibold text-slate-500">本日の集計</p>
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
            <SummaryTile label="全園児" value={summary.total} tone="slate" />
            <SummaryTile label="登園" value={summary.present} tone="emerald" />
            <SummaryTile label="欠席" value={summary.absent} tone="rose" highlight />
            <SummaryTile label="遅刻" value={summary.late} tone="amber" />
          </div>
        </section>

        <section>
          <div className="-mx-4 flex gap-2 overflow-x-auto px-4 pb-1">
            <FilterChip
              active={classFilter === "all"}
              label="全体"
              onClick={() => setClassFilter("all")}
            />
            {classTabs.map((item) => (
              <FilterChip
                key={item.id}
                active={classFilter === item.id}
                label={classAgeLabel(item.id, item.name)}
                onClick={() => setClassFilter(item.id)}
              />
            ))}
          </div>
        </section>

        <section>
          <div className="mb-3 flex items-center justify-between gap-3 rounded-2xl bg-rose-50 px-3 py-2 ring-1 ring-rose-200">
            <h2 className="text-base font-bold text-rose-700">未確認の保護者連絡（欠席・遅刻）</h2>
            <span className="shrink-0 rounded-full bg-rose-600 px-3 py-1 text-xs font-bold text-white">
              {unconfirmed.length}件
            </span>
          </div>
          {unconfirmed.length === 0 ? (
            <div className="rounded-3xl bg-white px-4 py-10 text-center shadow-sm ring-1 ring-slate-100">
              <p className="text-sm font-semibold text-slate-700">未確認の連絡はありません</p>
              <p className="mt-1 text-xs text-slate-500">
                欠席・遅刻の連絡があるとここに表示されます
              </p>
            </div>
          ) : (
            <ul className="space-y-3">
              {unconfirmed.map(({ child, attendance }) => (
                <li key={`unconfirmed-${child.id}`}>
                  <AttendanceCheckCard
                    child={child}
                    attendance={attendance}
                    variant="unconfirmed"
                    busy={busyIds.has(child.id)}
                    onConfirm={() => handleConfirm(child)}
                    onSetPresent={() =>
                      handleSetStatus(
                        child,
                        AttendanceStatus.Present,
                        `${child.full_name}さんを出席に変更しました`,
                      )
                    }
                    onSetAbsent={() =>
                      handleSetStatus(
                        child,
                        AttendanceStatus.Absent,
                        `${child.full_name}さんを欠席に変更しました`,
                      )
                    }
                    onSetLate={() =>
                      handleSetStatus(
                        child,
                        AttendanceStatus.Late,
                        `${child.full_name}さんを遅刻に変更しました`,
                      )
                    }
                  />
                </li>
              ))}
            </ul>
          )}
        </section>

        <section>
          <div className="mb-3 flex items-center justify-between">
            <h2 className="text-base font-bold text-slate-800">園児ごとの出欠</h2>
            <span className="text-xs font-semibold text-slate-500">
              {filteredChildren.length}名
            </span>
          </div>
          <ul className="grid gap-3 sm:grid-cols-2">
            {filteredChildren.map((child) => {
              const attendance = attendanceByChild.get(child.id) ?? null;
              return (
                <li key={child.id}>
                  <AttendanceCheckCard
                    child={child}
                    attendance={attendance}
                    busy={busyIds.has(child.id)}
                    onConfirm={() => handleConfirm(child)}
                    onSetPresent={() =>
                      handleSetStatus(
                        child,
                        AttendanceStatus.Present,
                        `${child.full_name}さんを出席に変更しました`,
                      )
                    }
                    onSetAbsent={() =>
                      handleSetStatus(
                        child,
                        AttendanceStatus.Absent,
                        `${child.full_name}さんを欠席に変更しました`,
                      )
                    }
                    onSetLate={() =>
                      handleSetStatus(
                        child,
                        AttendanceStatus.Late,
                        `${child.full_name}さんを遅刻に変更しました`,
                      )
                    }
                  />
                </li>
              );
            })}
          </ul>
        </section>
      </main>

      <nav className="fixed bottom-0 left-0 right-0 z-50 border-t border-slate-200 bg-white/95 backdrop-blur">
        <div className="mx-auto grid max-w-3xl grid-cols-4">
          <a
            href={`/staff/attendance?staff=${staffId}`}
            className="flex min-h-14 flex-col items-center justify-center gap-0.5 text-sky-600"
          >
            <span className="text-[11px] font-semibold">ホーム</span>
          </a>
          <span className="flex min-h-14 flex-col items-center justify-center gap-0.5 text-slate-500">
            <span className="text-[11px] font-semibold">出欠一覧</span>
          </span>
          <span className="flex min-h-14 flex-col items-center justify-center gap-0.5 text-slate-400">
            <span className="text-[11px] font-semibold">連絡帳</span>
          </span>
          <span className="flex min-h-14 flex-col items-center justify-center gap-0.5 text-slate-400">
            <span className="text-[11px] font-semibold">設定</span>
          </span>
        </div>
      </nav>
    </div>
  );
}

function SummaryTile({
  label,
  value,
  tone,
  highlight = false,
}: {
  label: string;
  value: number;
  tone: "slate" | "emerald" | "rose" | "amber";
  highlight?: boolean;
}) {
  const tones = {
    slate: "bg-slate-100 text-slate-700",
    emerald: "bg-emerald-50 text-emerald-800",
    rose: "bg-rose-50 text-rose-800",
    amber: "bg-amber-50 text-amber-800",
  };
  return (
    <div
      className={`rounded-2xl px-3 py-3 text-center ${tones[tone]} ${
        highlight ? "ring-2 ring-rose-300" : ""
      }`}
    >
      <p className="text-[11px] font-semibold opacity-80">{label}</p>
      <p className={`mt-1 text-xl font-bold ${highlight ? "text-rose-700" : ""}`}>{value}</p>
    </div>
  );
}

function FilterChip({
  label,
  active,
  onClick,
}: {
  label: string;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`inline-flex min-h-12 shrink-0 items-center rounded-full px-4 text-sm font-semibold ${
        active
          ? "bg-sky-500 text-white"
          : "bg-white text-slate-600 ring-1 ring-slate-200"
      }`}
    >
      {label}
    </button>
  );
}

function StaffAttendanceSkeleton() {
  return (
    <div className="mx-auto max-w-3xl space-y-4 px-4 pb-28 pt-4">
      <div className="h-16 animate-pulse rounded-2xl bg-slate-200" />
      <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
        <div className="h-20 animate-pulse rounded-2xl bg-slate-200" />
        <div className="h-20 animate-pulse rounded-2xl bg-slate-200" />
        <div className="h-20 animate-pulse rounded-2xl bg-slate-200" />
        <div className="h-20 animate-pulse rounded-2xl bg-slate-200" />
      </div>
      <div className="h-12 animate-pulse rounded-full bg-slate-200" />
      <div className="h-40 animate-pulse rounded-3xl bg-slate-200" />
      <div className="h-40 animate-pulse rounded-3xl bg-slate-200" />
      <div className="h-40 animate-pulse rounded-3xl bg-slate-200" />
    </div>
  );
}
