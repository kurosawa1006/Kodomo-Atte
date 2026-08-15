"use client";

import {
  AttendanceStatus,
  ATTENDANCE_STATUS_LABEL,
  type Attendance,
  type Children,
} from "@/types";
import { fromApiAttendanceStatus } from "@/lib/attendance";

type CardVariant = "unconfirmed" | "list";

type Props = {
  child: Children;
  attendance: Attendance | null;
  busy?: boolean;
  variant?: CardVariant;
  onConfirm: () => void;
  onSetPresent: () => void;
  onSetAbsent: () => void;
  onSetLate: () => void;
};

function statusStyles(status: AttendanceStatus): string {
  switch (status) {
    case AttendanceStatus.Late:
      return "bg-amber-100 text-amber-800";
    case AttendanceStatus.Absent:
      return "bg-rose-100 text-rose-800";
    case AttendanceStatus.RequestedCare:
      return "bg-sky-100 text-sky-800";
    default:
      return "bg-emerald-100 text-emerald-800";
  }
}

export default function AttendanceCheckCard({
  child,
  attendance,
  busy = false,
  variant = "list",
  onConfirm,
  onSetPresent,
  onSetAbsent,
  onSetLate,
}: Props) {
  const status = attendance
    ? fromApiAttendanceStatus(attendance.attendance_status)
    : AttendanceStatus.Present;
  const isPresent = status === AttendanceStatus.Present;
  const isLate = status === AttendanceStatus.Late;
  const isAbsent = status === AttendanceStatus.Absent;
  const needsConfirm = Boolean(attendance && !attendance.is_confirmed && !isPresent);
  const classLabel = child.nursery_class_detail?.name ?? "クラス未設定";
  const subLabel = child.sub_class_detail?.name;

  const shell =
    variant === "unconfirmed"
      ? "rounded-3xl bg-white p-4 shadow-md ring-2 ring-rose-200"
      : "rounded-3xl bg-white p-4 shadow-sm ring-1 ring-slate-100";

  return (
    <article className={shell}>
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="truncate text-lg font-bold text-slate-900">{child.full_name}</p>
          <p className="mt-1 text-xs text-slate-500">
            {classLabel}
            {subLabel ? ` / ${subLabel}` : ""}
          </p>
          <p className="mt-0.5 text-xs text-slate-400">{child.full_kana}</p>
        </div>
        <span
          className={`shrink-0 rounded-full px-3 py-1.5 text-xs font-bold ${statusStyles(status)}`}
        >
          {ATTENDANCE_STATUS_LABEL[status]}
        </span>
      </div>

      {attendance?.reason ? (
        <p className="mt-3 rounded-2xl bg-slate-50 px-3 py-2 text-sm text-slate-700">
          理由：{attendance.reason}
        </p>
      ) : null}

      {attendance?.scheduled_arrival_time ? (
        <p className="mt-2 text-sm text-slate-600">
          予定登園：{attendance.scheduled_arrival_time.slice(0, 5)}
        </p>
      ) : null}

      {attendance?.note ? (
        <p className="mt-2 text-sm text-slate-600">特記：{attendance.note}</p>
      ) : null}

      {attendance?.is_confirmed && !isPresent ? (
        <p className="mt-2 text-xs font-semibold text-emerald-600">確認済み</p>
      ) : null}

      <div className="mt-4 grid gap-2">
        {needsConfirm ? (
          <button
            type="button"
            disabled={busy}
            onClick={onConfirm}
            className="flex min-h-14 w-full items-center justify-center rounded-2xl bg-sky-500 px-4 text-base font-bold text-white shadow-sm active:bg-sky-600 disabled:opacity-60"
          >
            {busy ? "処理中…" : "確認済にする"}
          </button>
        ) : null}

        <div className="grid grid-cols-2 gap-2">
          {!isPresent ? (
            <button
              type="button"
              disabled={busy}
              onClick={onSetPresent}
              className="flex min-h-14 items-center justify-center rounded-2xl bg-emerald-500 px-3 text-sm font-bold text-white active:bg-emerald-600 disabled:opacity-60"
            >
              出席に変更
            </button>
          ) : (
            <button
              type="button"
              disabled={busy}
              onClick={onSetAbsent}
              className="flex min-h-14 items-center justify-center rounded-2xl bg-rose-500 px-3 text-sm font-bold text-white active:bg-rose-600 disabled:opacity-60"
            >
              欠席に変更
            </button>
          )}

          {!isLate ? (
            <button
              type="button"
              disabled={busy}
              onClick={onSetLate}
              className="flex min-h-14 items-center justify-center rounded-2xl bg-amber-500 px-3 text-sm font-bold text-white active:bg-amber-600 disabled:opacity-60"
            >
              遅刻に変更
            </button>
          ) : (
            <button
              type="button"
              disabled={busy}
              onClick={onSetAbsent}
              className="flex min-h-14 items-center justify-center rounded-2xl bg-rose-500 px-3 text-sm font-bold text-white active:bg-rose-600 disabled:opacity-60"
            >
              欠席に変更
            </button>
          )}
        </div>

        {isAbsent ? (
          <button
            type="button"
            disabled={busy}
            onClick={onSetLate}
            className="flex min-h-12 items-center justify-center rounded-2xl bg-white px-3 text-sm font-semibold text-amber-700 ring-1 ring-amber-200 active:bg-amber-50 disabled:opacity-60"
          >
            遅刻に変更
          </button>
        ) : null}
      </div>
    </article>
  );
}
