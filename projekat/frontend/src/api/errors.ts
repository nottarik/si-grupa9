// Turn any thrown API/axios error into a readable message for the user.
// Prefers the backend's human-readable `detail` (FastAPI), then a Pydantic
// validation message, and otherwise the provided friendly fallback — never the
// raw "Request failed with status code 4XX" or an HTTP status code.
export function readableError(err: unknown, fallback = "Something went wrong. Please try again."): string {
  const resp = (err as { response?: { data?: { detail?: unknown } } })?.response;
  const detail = resp?.data?.detail;
  if (typeof detail === "string" && detail.trim()) return detail;
  if (Array.isArray(detail) && detail[0]?.msg) return String(detail[0].msg);
  return fallback;
}
