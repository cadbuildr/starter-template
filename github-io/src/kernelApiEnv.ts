import { CADBUILDR_KERNEL_API_BASE_URL } from "@cadbuildr/cad-kernel-r3f";

/** Resolved origin for kernel-api (Vite env override or production default). No trailing slash. */
export function resolveKernelApiBaseUrl(): string {
  const raw = import.meta.env.VITE_KERNEL_API_BASE_URL?.trim();
  if (raw) {
    return raw.replace(/\/$/, "");
  }
  return CADBUILDR_KERNEL_API_BASE_URL.replace(/\/$/, "");
}
