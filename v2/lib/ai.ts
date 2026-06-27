import { FALLBACK_AI_PICK } from "./pitchiq-data";
import type { AIPickInput, AIPickResult } from "./pitchiq-types";

export const AI_PICK_PROMPT = `You are PitchIQ, an expert World Cup 2026 soccer analyst.
Return strict JSON with keys: winProbability, recommendation, confidence, topFantasyPicks, riskNotes.
Use the provided form, head-to-head, injuries, and odds. Clearly avoid guarantees and keep all betting language educational.`;

const ANTHROPIC_URL = "https://api.anthropic.com/v1/messages";
const MODEL = "claude-sonnet-4-6";
const cache = new Map<string, { expires: number; result: AIPickResult }>();

interface AnthropicContentBlock {
  type?: string;
  text?: string;
}

interface AnthropicMessageResponse {
  content?: AnthropicContentBlock[];
}

function isAIPickResult(value: unknown): value is AIPickResult {
  const result = value as Partial<AIPickResult>;
  return (
    typeof result.winProbability === "number" &&
    typeof result.recommendation === "string" &&
    typeof result.confidence === "number" &&
    Array.isArray(result.topFantasyPicks) &&
    Array.isArray(result.riskNotes)
  );
}

function buildUserPrompt(input: AIPickInput) {
  return JSON.stringify(
    {
      matchId: input.matchId,
      matchContext: input.matchContext,
      form: input.form,
      h2h: input.h2h,
      injuries: input.injuries,
      odds: input.odds,
    },
    null,
    2,
  );
}

export async function generateAIPick(input: AIPickInput): Promise<AIPickResult> {
  const cached = cache.get(input.matchId);
  if (cached && cached.expires > Date.now()) {
    return cached.result;
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    cache.set(input.matchId, { expires: Date.now() + 300_000, result: FALLBACK_AI_PICK });
    return FALLBACK_AI_PICK;
  }

  try {
    const response = await fetch(ANTHROPIC_URL, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": apiKey,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: MODEL,
        max_tokens: 700,
        temperature: 0.2,
        system: AI_PICK_PROMPT,
        messages: [
          {
            role: "user",
            content: buildUserPrompt(input),
          },
        ],
      }),
      next: { revalidate: 300 },
    });

    if (!response.ok) {
      return FALLBACK_AI_PICK;
    }

    const data = (await response.json()) as AnthropicMessageResponse;
    const text = data.content?.find((block) => block.type === "text")?.text;

    if (!text) {
      return FALLBACK_AI_PICK;
    }

    const parsed = JSON.parse(text) as unknown;
    const result = isAIPickResult(parsed) ? parsed : FALLBACK_AI_PICK;
    cache.set(input.matchId, { expires: Date.now() + 300_000, result });
    return result;
  } catch {
    return FALLBACK_AI_PICK;
  }
}
