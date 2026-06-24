import { getMatchesByTeam, toTeamSlug } from "./matches";

export interface TeamGuide {
  slug: string;
  teamSlug: string;
  name: string;
  flagCode: string;
  title: string;
  description: string;
  strengths: string[];
  questions: string[];
  fantasyTargets: string[];
  bettingAngle: string;
}

export const TEAM_GUIDES: TeamGuide[] = [
  {
    slug: "usa-guide",
    teamSlug: "usa",
    name: "USA",
    flagCode: "us",
    title: "USA World Cup 2026 Team Guide",
    description:
      "The USMNT has home-field pressure, real attacking speed, and a group-stage path that demands clean starts.",
    strengths: ["Transition pace", "Home crowd edge", "Wide attackers who can press"],
    questions: ["Can the back line defend set pieces?", "Who owns the final ball?", "Does the midfield control knockout-level games?"],
    fantasyTargets: ["Christian Pulisic", "Folarin Balogun", "Weston McKennie"],
    bettingAngle:
      "USA futures will carry public tax. The better angle is match-by-match: watch first-half pressure and set-piece markets.",
  },
  {
    slug: "brazil-guide",
    teamSlug: "brazil",
    name: "Brazil",
    flagCode: "br",
    title: "Brazil World Cup 2026 Team Guide",
    description:
      "Brazil still has the tournament's highest ceiling. Vinicius Jr. changes the matchup before the first whistle.",
    strengths: ["Elite one-v-one attackers", "Deep forward rotation", "Fullbacks who can tilt the field"],
    questions: ["Can Brazil defend counters cleanly?", "Who starts at the nine?", "Does the midfield protect leads?"],
    fantasyTargets: ["Vinicius Jr.", "Rodrygo", "Alisson"],
    bettingAngle:
      "Brazil moneylines are rarely cheap. Look for team total and player-shot markets when opponents sit deep.",
  },
  {
    slug: "france-guide",
    teamSlug: "france",
    name: "France",
    flagCode: "fr",
    title: "France World Cup 2026 Team Guide",
    description:
      "France owns the cleanest blend of pace, depth, and knockout experience. The floor is high. The ceiling is brutal.",
    strengths: ["Vertical runners everywhere", "Tournament-tested core", "Set-piece size"],
    questions: ["Does the midfield stay healthy?", "Can the fullbacks handle elite wingers?", "Who carries chance creation beyond Mbappe?"],
    fantasyTargets: ["Kylian Mbappe", "Antoine Griezmann", "Theo Hernandez"],
    bettingAngle:
      "France often gives better value in score-first, win-to-nil, and player goal markets than the straight moneyline.",
  },
];

const TEAM_GUIDE_BY_SLUG = new Map(TEAM_GUIDES.map((guide) => [guide.slug, guide]));

export function getTeamGuideBySlug(slug: string): TeamGuide | undefined {
  return TEAM_GUIDE_BY_SLUG.get(slug);
}

export function getTeamGuideMatches(guide: TeamGuide) {
  return getMatchesByTeam(toTeamSlug(guide.teamSlug));
}
