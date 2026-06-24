import { NextResponse } from "next/server";
import { z } from "zod";

// Email capture only. Do NOT store betting behavior or personalize odds (see CLAUDE.md).
export const runtime = "nodejs";

const SubscribeSchema = z.object({
  email: z.string().trim().toLowerCase().email().max(254),
  // Honeypot: real users leave this empty; bots tend to fill every field.
  company: z.string().max(0).optional(),
});

// Naive in-memory limiter — resets on cold start and is per-instance only.
// TODO: rate-limit with a shared store (Upstash/Redis) before this sees real traffic.
const HITS = new Map<string, { count: number; resetAt: number }>();
const WINDOW_MS = 60_000;
const MAX_PER_WINDOW = 5;

function rateLimited(key: string, now: number): boolean {
  const entry = HITS.get(key);
  if (!entry || now > entry.resetAt) {
    HITS.set(key, { count: 1, resetAt: now + WINDOW_MS });
    return false;
  }
  entry.count += 1;
  return entry.count > MAX_PER_WINDOW;
}

/**
 * Hand off the subscription to whatever email provider is configured.
 * Stubbed behind an env check so the route is safe to ship before a provider
 * is chosen. Idempotent by contract: providers dedupe by email, and re-subscribing
 * an existing address must succeed without error.
 */
async function subscribe(email: string): Promise<void> {
  const endpoint = process.env.NEWSLETTER_API_URL;
  const apiKey = process.env.NEWSLETTER_API_KEY;

  // No provider wired yet — accept the signup so the UI works, but make it loud
  // in logs that nothing is being persisted. Never log the email itself.
  if (!endpoint || !apiKey) {
    console.warn("[newsletter] no provider configured — signup accepted but not stored");
    return;
  }

  const res = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({ email, source: "getpitchiq.net" }),
  });

  // 409 = already subscribed; treat as success to stay idempotent.
  if (!res.ok && res.status !== 409) {
    throw new Error(`provider responded ${res.status}`);
  }
}

export async function POST(req: Request) {
  try {
    const ip =
      req.headers.get("x-forwarded-for")?.split(",")[0]?.trim() || "unknown";
    const now = Date.now();
    if (rateLimited(ip, now)) {
      return NextResponse.json(
        { ok: false, error: "Too many requests. Try again shortly." },
        { status: 429 },
      );
    }

    const body = await req.json().catch(() => null);
    const parsed = SubscribeSchema.safeParse(body);
    if (!parsed.success) {
      return NextResponse.json(
        { ok: false, error: "Please enter a valid email address." },
        { status: 400 },
      );
    }

    // Honeypot tripped — pretend success, store nothing.
    if (parsed.data.company) {
      return NextResponse.json({ ok: true });
    }

    await subscribe(parsed.data.email);
    return NextResponse.json({ ok: true });
  } catch (err) {
    console.error("[newsletter] subscribe failed:", (err as Error).message);
    return NextResponse.json(
      { ok: false, error: "Subscription is temporarily unavailable." },
      { status: 502 },
    );
  }
}
