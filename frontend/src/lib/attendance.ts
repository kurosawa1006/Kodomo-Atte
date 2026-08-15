import { AttendanceStatus } from "@/types";

/** Django API の attendance_status (null=出席, 1=遅刻, 2=早退, 3=欠席) */
export type ApiAttendanceStatus = 1 | 2 | 3 | null;

export function toApiAttendanceStatus(status: AttendanceStatus): ApiAttendanceStatus {
  switch (status) {
    case AttendanceStatus.Late:
      return 1;
    case AttendanceStatus.Absent:
      return 3;
    case AttendanceStatus.RequestedCare:
      return 3;
    default:
      return null;
  }
}

export function fromApiAttendanceStatus(status: number | null | undefined): AttendanceStatus {
  if (status === 1) return AttendanceStatus.Late;
  if (status === 3) return AttendanceStatus.Absent;
  if (status === 2) return AttendanceStatus.Late;
  return AttendanceStatus.Present;
}

export function todayIsoDate(): string {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Tokyo",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(new Date());
}

export function formatTodayJa(): string {
  return new Intl.DateTimeFormat("ja-JP", {
    timeZone: "Asia/Tokyo",
    year: "numeric",
    month: "long",
    day: "numeric",
    weekday: "short",
  }).format(new Date());
}

/** Django staff dashboard と同じクラスID → 年齢ラベル */
export const CLASS_AGE_LABELS: Record<number, string> = {
  1: "0歳",
  2: "1歳",
  3: "2歳",
  4: "3歳",
  5: "4歳",
  6: "5歳",
};

export function classAgeLabel(classId: number, fallbackName?: string): string {
  return CLASS_AGE_LABELS[classId] ?? fallbackName ?? `${classId}`;
}

export const REASON_PRESETS = [
  "発熱",
  "体調不良",
  "家庭の都合",
  "通院",
  "その他",
] as const;

export type ReasonPreset = (typeof REASON_PRESETS)[number];
