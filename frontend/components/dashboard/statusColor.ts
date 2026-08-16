/**
 * IoT 디바이스 및 시스템 상태에 따른 통일된 Tailwind CSS 색상 스타일 유틸리티
 */
export const statusColor = {
  on: "text-emerald-700 bg-emerald-50 border-emerald-200",
  off: "text-slate-500 bg-slate-50 border-slate-200",
  alert: "text-rose-700 bg-rose-50 border-rose-200 animate-pulse",
  warning: "text-amber-700 bg-amber-50 border-amber-200",
  info: "text-sky-700 bg-sky-50 border-sky-200",
  connecting: "text-amber-600 bg-amber-50 border-amber-200",
  disconnected: "text-gray-500 bg-gray-100 border-gray-200",
};

/**
 * 디바이스 상태 문자열에 맞는 스타일 클래스를 안전하게 반환합니다.
 */
export function getStatusBadgeClass(status: string | boolean | undefined): string {
  if (typeof status === "boolean") {
    return status ? statusColor.on : statusColor.off;
  }
  if (!status) return statusColor.off;

  const s = status.toLowerCase();
  if (s === "on" || s === "active" || s === "open" || s === "detected") return statusColor.on;
  if (s === "alert" || s === "danger" || s === "emergency") return statusColor.alert;
  if (s === "warning") return statusColor.warning;
  if (s === "connecting") return statusColor.connecting;
  return statusColor.off;
}
