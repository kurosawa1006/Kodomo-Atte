"use client";

import { useEffect, useState } from "react";
import {
  AttendanceStatus,
  ATTENDANCE_STATUS_LABEL,
  type Attendance,
  type Children,
} from "@/types";
import { fromApiAttendanceStatus } from "@/lib/attendance";

export function StatusBadge({ attendance }: { attendance: Attendance | null }) {
  const status = attendance
    ? fromApiAttendanceStatus(attendance.attendance_status)
    : AttendanceStatus.Present;

  const styles: Record<AttendanceStatus, string> = {
    [AttendanceStatus.Present]: "bg-emerald-100 text-emerald-800",
    [AttendanceStatus.Late]: "bg-amber-100 text-amber-800",
    [AttendanceStatus.Absent]: "bg-rose-100 text-rose-800",
    [AttendanceStatus.RequestedCare]: "bg-sky-100 text-sky-800",
  };

  return (
    <span className={`inline-flex min-h-8 items-center rounded-full px-3 py-1 text-sm font-bold ${styles[status]}`}>
      {ATTENDANCE_STATUS_LABEL[status]}
    </span>
  );
}

export function ProfileCard({ child }: { child: Children }) {
  const classLabel = child.nursery_class_detail?.name ?? "クラス未設定";
  const subLabel = child.sub_class_detail?.name;

  return (
    <section className="rounded-3xl bg-gradient-to-br from-sky-500 to-sky-600 p-5 text-white shadow-md">
      <p className="text-xs font-semibold text-sky-100">お子さま</p>
      <p className="mt-1 text-2xl font-bold">{child.full_name}</p>
      <p className="mt-2 text-sm text-sky-50">
        {classLabel}
        {subLabel ? ` ・ ${subLabel}` : ""}
      </p>
      <p className="mt-1 text-xs text-sky-100">かな：{child.full_kana}</p>
    </section>
  );
}

export function DashboardSkeleton() {
  return (
    <div className="mx-auto max-w-md space-y-4 px-4 pb-28 pt-4">
      <div className="h-36 animate-pulse rounded-3xl bg-slate-200" />
      <div className="h-24 animate-pulse rounded-3xl bg-slate-200" />
      <div className="h-16 animate-pulse rounded-3xl bg-slate-200" />
      <div className="h-40 animate-pulse rounded-3xl bg-slate-200" />
    </div>
  );
}

export function Toast({
  message,
  type = "success",
  onClose,
}: {
  message: string;
  type?: "success" | "error";
  onClose: () => void;
}) {
  useEffect(() => {
    const timer = window.setTimeout(onClose, 4000);
    return () => window.clearTimeout(timer);
  }, [onClose]);

  const bg = type === "success" ? "bg-emerald-600" : "bg-rose-600";

  return (
    <div
      className={`fixed left-4 right-4 top-4 z-[80] mx-auto max-w-md rounded-2xl px-4 py-3 text-sm font-semibold text-white shadow-lg ${bg}`}
      role="alert"
    >
      {message}
    </div>
  );
}
