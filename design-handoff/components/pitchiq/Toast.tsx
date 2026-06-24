"use client";

import { useApp } from "@/app/providers";

export function Toast() {
  const { toast } = useApp();
  return (
    <div className={`toast${toast.show ? " show" : ""}`} role="status" aria-live="polite">
      <span>{toast.msg}</span>
    </div>
  );
}
