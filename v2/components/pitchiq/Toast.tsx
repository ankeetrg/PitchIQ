"use client";

import { AnimatePresence, motion } from "framer-motion";
import { createContext, useCallback, useContext, useMemo, useRef, useState } from "react";

type ToastTone = "success" | "info" | "warning";

interface ToastState {
  id: number;
  message: string;
  tone: ToastTone;
}

interface ToastContextValue {
  showToast: (message: string, tone?: ToastTone) => void;
}

const ToastContext = createContext<ToastContextValue | null>(null);

const toneClasses: Record<ToastTone, string> = {
  success: "border-green-border bg-green-dim text-green",
  info: "border-blue/30 bg-blue-dim text-blue",
  warning: "border-gold-border bg-gold-dim text-gold",
};

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toast, setToast] = useState<ToastState | null>(null);
  const timerRef = useRef<number | null>(null);

  const showToast = useCallback((message: string, tone: ToastTone = "success") => {
    if (timerRef.current) {
      window.clearTimeout(timerRef.current);
    }

    const id = Date.now();
    setToast({ id, message, tone });
    timerRef.current = window.setTimeout(() => {
      setToast((current) => (current?.id === id ? null : current));
    }, 2800);
  }, []);

  const value = useMemo(() => ({ showToast }), [showToast]);

  return (
    <ToastContext.Provider value={value}>
      {children}
      <AnimatePresence>
        {toast ? (
          <motion.div
            key={toast.id}
            initial={{ opacity: 0, y: 24, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.96 }}
            transition={{ duration: 0.22 }}
            className="fixed bottom-6 left-1/2 z-[500] w-[min(92vw,420px)] -translate-x-1/2 rounded-lg border bg-[var(--surf)] px-4 py-3 text-center text-sm font-semibold shadow-[var(--shadow)]"
          >
            <span className={`inline-flex rounded-md border px-3 py-1.5 ${toneClasses[toast.tone]}`}>
              {toast.message}
            </span>
          </motion.div>
        ) : null}
      </AnimatePresence>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const context = useContext(ToastContext);

  if (!context) {
    throw new Error("useToast must be used inside ToastProvider");
  }

  return context;
}
