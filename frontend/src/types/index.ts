export enum AttendanceStatus {
  Present = 1,
  Late = 2,
  Absent = 3,
  RequestedCare = 4,
}

export const ATTENDANCE_STATUS_LABEL: Record<AttendanceStatus, string> = {
  [AttendanceStatus.Present]: "通常登園",
  [AttendanceStatus.Late]: "遅刻登園",
  [AttendanceStatus.Absent]: "欠席",
  [AttendanceStatus.RequestedCare]: "希望保育",
};

export type Gender = "male" | "female" | "other";

export type UserRole = "parent" | "staff";

export interface Facility {
  id: number;
  name: string;
  postal_code: string;
  address: string;
  phone_number: string;
  capacity: number;
  is_active: boolean;
  is_deleted: boolean;
  created_at: string;
  updated_at: string;
}

export interface Class {
  id: number;
  name: string;
  description: string;
  facility: number;
  is_deleted: boolean;
}

export interface SubClass {
  id: number;
  name: string;
  description: string;
  facility: number;
  nursery_class: number;
  is_deleted: boolean;
}

export interface StaffRole {
  id: number;
  name: string;
  is_deleted: boolean;
}

export interface Staff {
  id: number;
  facility: number | null;
  staff_number: string;
  staff_role: number | null;
  staff_role_detail: StaffRole | null;
  last_name: string;
  first_name: string;
  last_name_kana: string;
  first_name_kana: string;
  full_name: string;
  full_kana: string;
  phone_number: string;
  postal_code: string;
  address: string;
  start_date: string | null;
  end_date: string | null;
  is_deleted: boolean;
  created_at: string;
  updated_at: string;
}

export interface Parent {
  id: number;
  facility: number | null;
  name: string;
  kana: string;
  phone_number: string;
  emergency_contact: string;
  postal_code: string;
  address: string;
  start_date: string | null;
  end_date: string | null;
  is_deleted: boolean;
  created_at: string;
  updated_at: string;
}

export interface Children {
  id: number;
  last_name: string;
  first_name: string;
  last_name_kana: string;
  first_name_kana: string;
  full_name: string;
  full_kana: string;
  birthday: string;
  gender: Gender;
  gender_display: string;
  facility: number | null;
  nursery_class: number | null;
  nursery_class_detail: Class | null;
  sub_class: number | null;
  sub_class_detail: SubClass | null;
  start_date: string | null;
  end_date: string | null;
  is_deleted: boolean;
  created_at: string;
  updated_at: string;
}

export interface Attendance {
  id: number;
  child: number;
  child_detail: Children;
  checked_by: number | null;
  checked_by_detail: Staff | null;
  date: string;
  attendance_status: number | null;
  attendance_status_display: string | null;
  reason: string;
  scheduled_arrival_time: string | null;
  note: string;
  is_confirmed: boolean;
  is_deleted: boolean;
  created_at: string;
  updated_at: string;
}

export interface AttendanceWritePayload {
  child: number;
  date?: string;
  attendance_status?: AttendanceStatus | null;
  reason?: string;
  scheduled_arrival_time?: string | null;
  note?: string;
  /** スタッフ確認済フラグ（API の is_confirmed） */
  is_confirmed?: boolean;
}

export interface UserMeParent {
  role: "parent";
  permissions: string[];
  profile: Parent;
  children: Children[];
}

export interface UserMeStaff {
  role: "staff";
  permissions: string[];
  profile: Staff;
}

export type UserMe = UserMeParent | UserMeStaff;

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface AttendanceListParams {
  date?: string;
  class?: number | "all";
  is_confirmed?: boolean;
  attendance_status?: AttendanceStatus;
  page?: number;
}
