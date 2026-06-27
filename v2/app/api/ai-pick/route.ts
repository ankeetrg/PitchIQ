import { generateAIPick } from "@/lib/ai";
import type { AIPickInput } from "@/lib/pitchiq-types";

export async function POST(request: Request) {
  const input = (await request.json()) as AIPickInput;
  const result = await generateAIPick(input);
  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    start(controller) {
      controller.enqueue(encoder.encode(JSON.stringify(result)));
      controller.close();
    },
  });

  return new Response(stream, {
    headers: {
      "content-type": "application/json; charset=utf-8",
    },
  });
}
