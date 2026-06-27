import { AIParlayCard } from "@/components/pitchiq/AIParlayCard";
import { BettingIntelligence } from "@/components/pitchiq/BettingIntelligence";
import { DisclaimerBar } from "@/components/pitchiq/DisclaimerBar";
import { FantasyPicks } from "@/components/pitchiq/FantasyPicks";
import { Footer } from "@/components/pitchiq/Footer";
import { HeroGrid } from "@/components/pitchiq/HeroGrid";
import { LineMovementFeed } from "@/components/pitchiq/LineMovementFeed";
import { LiveMatchProvider } from "@/components/pitchiq/LiveMatchProvider";
import { LiveTicker } from "@/components/pitchiq/LiveTicker";
import { MobileBottomNav } from "@/components/pitchiq/MobileBottomNav";
import { Navbar } from "@/components/pitchiq/Navbar";
import { NewsAndAlerts } from "@/components/pitchiq/NewsAndAlerts";
import { NewsletterStrip } from "@/components/pitchiq/NewsletterStrip";
import { SportSwitcher } from "@/components/pitchiq/SportSwitcher";
import { SportsbookPromoBar } from "@/components/pitchiq/SportsbookPromoBar";
import { StandingsSchedule } from "@/components/pitchiq/StandingsSchedule";
import { StatsStrip } from "@/components/pitchiq/StatsStrip";

export default function Home() {
  return (
    <LiveMatchProvider>
      <DisclaimerBar />
      <LiveTicker />
      <Navbar />
      <SportSwitcher />
      <main>
        <HeroGrid />
        <SportsbookPromoBar />
        <StatsStrip />
        <StandingsSchedule />
        <FantasyPicks />
        <AIParlayCard />
        <BettingIntelligence />
        <LineMovementFeed />
        <NewsAndAlerts />
        <NewsletterStrip />
      </main>
      <Footer />
      <MobileBottomNav />
    </LiveMatchProvider>
  );
}
