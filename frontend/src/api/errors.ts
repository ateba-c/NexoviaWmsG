import axios from "axios";

export function getApiErrorMessage(error: unknown, fallback: string) {
  if (axios.isAxiosError(error)) {
    const payload = error.response?.data;
    if (typeof payload === "string" && payload.trim()) {
      return payload;
    }
    if (payload && typeof payload === "object") {
      for (const value of Object.values(payload as Record<string, unknown>)) {
        if (typeof value === "string" && value.trim()) {
          return value;
        }
        if (Array.isArray(value) && typeof value[0] === "string" && value[0].trim()) {
          return value[0];
        }
      }
    }
  }
  if (error instanceof Error && error.message.trim()) {
    return error.message;
  }
  return fallback;
}
