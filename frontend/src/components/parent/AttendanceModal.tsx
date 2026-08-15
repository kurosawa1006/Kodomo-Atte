"use client";

import { useState, useTransition } from "react";
import {
  AttendanceStatus,
  type Attendance,
  type AttendanceWritePayload,
  type Children,
} from "@/types";
import { ApiError, nurseryApi } from "@/lib/api";
import { REASON_PRESETS, todayIsoDate } from "@/lib/attendance";

type AttendanceType = "absent" | "late";

interface AttendanceModalProps {
  open: boolean;
  child: Children;
  existingAttendance: Attendance | null;
  onClose: () => void;
  onSuccess: (attendance: Attendance) => void;
  onError: (message: string) => void;
}

export default function AttendanceModal({
  open,
  child,
  existingAttendance,
  onClose,
  onSuccess,
  onError,
}: AttendanceModalProps) {
  const [type, setType] = useState<AttendanceType>("absent");
  const [scheduledArrivalTime, setScheduledArrivalTime] = useState("09:00");
  const [reasonPreset, setReasonPreset] = useState<string>(REASON_PRESETS[0]);
  const [reasonCustom, setReasonCustom] = useState("");
  const [note, setNote] = useState("");
  const [isPending, startTransition] = useTransition();

  if (!open) return null;

  const reason =
    reasonPreset === "その他" ? reasonCustom.trim() : reasonPreset;

  const handleSubmit = () => {
    if (!reason) {
      onError("理由を入力してください");
      return;
    }

    const payload: AttendanceWritePayload = {
      child: child.id,
      date: todayIsoDate(),
      attendance_status:
        type === "late" ? AttendanceStatus.Late : AttendanceStatus.Absent,
      reason,
      note: note.trim(),
      scheduled_arrival_time:
        type === "late" ? `${scheduledArrivalTime}:00`.slice(0, 8) : null,
      is_confirmed: false,
    };

    startTransition(async () => {
      try {
        const result = existingAttendance
          ? await nurseryApi.updateAttendance(existingAttendance.id, payload)
          : await nurseryApi.createAttendance(payload);
        onSuccess(result);
        onClose();
      } catch (error) {
        const message =
          error instanceof ApiError
            ? error.message
            : "連絡の送信に失敗しました";
        onError(message);
      }
    });
  };

  return (
    <div className="fixed inset-0 z-[70]" role="dialog" aria-modal="true">
      <button
        type="button"
        className="absolute inset-0 bg-slate-900/40"
        aria-label="閉じる"
        onClick={onClose}
      />
      <div className="absolute inset-x-0 bottom-0 mx-auto max-w-md rounded-t-3xl bg-white px-4 pb-8 pt-5 shadow-xl">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-base font-bold text-slate-900">欠席・遅刻連絡</h2>
          <button
            type="button"
            onClick={onClose}
            className="flex min-h-12 min-w-12 items-center justify-center rounded-xl text-slate-500"
            aria-label="閉じる"
          >
            ✕
          </button>
        </div>

        <div className="max-h-[70vh] space-y-5 overflow-y-auto">
          <div>
            <p className="mb-2 text-xs font-semibold text-slate-500">区分</p>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => setType("absent")}
                className={`min-h-12 rounded-2xl px-4 text-sm font-bold ${
                  type === "absent"
                    ? "bg-rose-500 text-white"
                    : "bg-rose-50 text-rose-700"
                }`}
              >
                欠席
              </button>
              <button
                type="button"
                onClick={() => setType("late")}
                className={`min-h-12 rounded-2xl px-4 text-sm font-bold ${
                  type === "late"
                    ? "bg-amber-500 text-white"
                    : "bg-amber-50 text-amber-800"
                }`}
              >
                遅刻
              </button>
            </div>
          </div>

          {type === "late" && (
            <div>
              <label htmlFor="scheduled_arrival_time" className="mb-2 block text-xs font-semibold text-slate-500">
                予定登園時間
              </label>
              <input
                id="scheduled_arrival_time"
                type="time"
                value={scheduledArrivalTime}
                onChange={(e) => setScheduledArrivalTime(e.target.value)}
                className="min-h-12 w-full rounded-2xl border border-slate-200 px-4 text-sm"
              />
            </div>
          )}

          <div>
            <label htmlFor="reason_preset" className="mb-2 block text-xs font-semibold text-slate-500">
              理由
            </label>
            <select
              id="reason_preset"
              value={reasonPreset}
              onChange={(e) => setReasonPreset(e.target.value)}
              className="min-h-12 w-full rounded-2xl border border-slate-200 px-4 text-sm"
            >
              {REASON_PRESETS.map((preset) => (
                <option key={preset} value={preset}>
                  {preset}
                </option>
              ))}
            </select>
            {reasonPreset === "その他" && (
              <input
                type="text"
                value={reasonCustom}
                onChange={(e) => setReasonCustom(e.target.value)}
                placeholder="理由を入力"
                className="mt-2 min-h-12 w-full rounded-2xl border border-slate-200 px-4 text-sm"
              />
            )}
          </div>

          <div>
            <label htmlFor="note" className="mb-2 block text-xs font-semibold text-slate-500">
              特記事項
            </label>
            <textarea
              id="note"
              value={note}
              onChange={(e) => setNote(e.target.value)}
              rows={3}
              placeholder="園への連絡事項があれば入力"
              className="w-full rounded-2xl border border-slate-200 px-4 py-3 text-sm"
            />
          </div>

          <button
            type="button"
            disabled={isPending}
            onClick={handleSubmit}
            className="flex min-h-14 w-full items-center justify-center rounded-2xl bg-sky-500 px-4 text-base font-bold text-white disabled:opacity-60"
          >
            {isPending ? "送信中..." : "連絡を送信する"}
          </button>
        </div>
      </div>
    </div>
  );
}
