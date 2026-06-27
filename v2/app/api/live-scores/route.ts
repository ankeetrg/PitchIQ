import { getLiveScores } from "@/lib/espn";

export async function GET() {
  const matches = await getLiveScores();
  return Response.json(matches);
}
