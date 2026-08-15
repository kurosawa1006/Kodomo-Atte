import type {
  Attendance,
  AttendanceListParams,
  AttendanceWritePayload,
  AttendanceStatus,
  Children,
  PaginatedResponse,
  Parent,
  Staff,
  UserMe,
  UserRole,
} from "@/types";
import { toApiAttendanceStatus, todayIsoDate } from "@/lib/attendance";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export class ApiError extends Error {
  status: number;
  body: unknown;

  constructor(message: string, status: number, body: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.body = body;
  }
}

type QueryValue = string | number | boolean | null | undefined;
type QueryParams = Record<string, QueryValue>;

function buildUrl(path: string, query?: QueryParams): string {
  const normalized = path.startsWith("/") ? path : `/${path}`;
  const url = new URL(`${API_BASE_URL}${normalized}`);
  if (query) {
    Object.entries(query as QueryParams).forEach(([key, value]) => {
      if (value === undefined || value === null || value === "") return;
      url.searchParams.set(key, String(value));
    });
  }
  return url.toString();
}

async function request<T>(
  path: string,
  options: RequestInit & { query?: QueryParams } = {},
): Promise<T> {
  const { query, headers, ...rest } = options;
  const response = await fetch(buildUrl(path, query), {
    ...rest,
    headers: {
      "Content-Type": "application/json",
      ...headers,
    },
    cache: "no-store",
  });

  const text = await response.text();
  const data = text ? (JSON.parse(text) as unknown) : null;

  if (!response.ok) {
    const detail =
      typeof data === "object" && data && "detail" in data
        ? String((data as { detail: unknown }).detail)
        : response.statusText;
    throw new ApiError(detail || "API request failed", response.status, data);
  }

  return data as T;
}

export const api = {
  get<T>(path: string, query?: QueryParams | object) {
    return request<T>(path, { method: "GET", query: query as QueryParams | undefined });
  },
  post<T>(path: string, body?: unknown) {
    return request<T>(path, {
      method: "POST",
      body: body === undefined ? undefined : JSON.stringify(body),
    });
  },
  patch<T>(path: string, body?: unknown) {
    return request<T>(path, {
      method: "PATCH",
      body: body === undefined ? undefined : JSON.stringify(body),
    });
  },
};

export const nurseryApi = {
  getMe(role: UserRole, id: number) {
    return api.get<UserMe>("/me/", { role, id });
  },
  listChildren(params?: { class?: number | "all"; facility?: number; page?: number }) {
    return api.get<PaginatedResponse<Children>>("/children/", params);
  },
  getChild(id: number) {
    return api.get<Children>(`/children/${id}/`);
  },
  listStaff(params?: { page?: number }) {
    return api.get<PaginatedResponse<Staff>>("/staff/", params);
  },
  listParents(params?: { page?: number }) {
    return api.get<PaginatedResponse<Parent>>("/parents/", params);
  },
  listAttendances(params?: AttendanceListParams) {
    return api.get<PaginatedResponse<Attendance>>("/attendances/", params);
  },
  createAttendance(payload: AttendanceWritePayload) {
    return api.post<Attendance>("/attendances/", mapAttendancePayload(payload));
  },
  updateAttendance(id: number, payload: Partial<AttendanceWritePayload>) {
    return api.patch<Attendance>(`/attendances/${id}/`, mapAttendancePayload(payload, false));
  },
  confirmAttendance(id: number) {
    return api.post<Attendance>(`/attendances/${id}/confirm/`);
  },
};

function mapAttendancePayload(payload: Partial<AttendanceWritePayload>, ensureDate = true) {
  const body: Record<string, unknown> = { ...payload };
  if ("attendance_status" in payload && payload.attendance_status !== undefined) {
    body.attendance_status =
      payload.attendance_status === null
        ? null
        : toApiAttendanceStatus(payload.attendance_status as AttendanceStatus);
  }
  if (ensureDate && !body.date) {
    body.date = todayIsoDate();
  }
  return body;
}
