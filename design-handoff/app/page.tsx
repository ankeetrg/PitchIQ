import { DisclaimerBar } from "@/components/pitchiq/DisclaimerBar";
import { LiveTicker } from "@/components/pitchiq/LiveTicker";
import { Navbar } from "@/components/pitchiq/Navbar";
import { SportSwitcher } from "@/components/pitchiq/SportSwitcher";
import { FeaturedMatch } from "@/components/pitchiq/FeaturedMatch";
import { SideWidgets } from "@/components/pitchiq/SideWidgets";
import { SportsbookPromo } from "@/components/pitchiq/SportsbookPromo";
import { StatsStrip } from "@/components/pitchiq/StatsStrip";
import { StandingsSchedule } from "@/components/pitchiq/StandingsSchedule";
import { FantasyPicks } from "@/components/pitchiq/FantasyPicks";
import { ParlayCard } from "@/components/pitchiq/ParlayCard";
import { BettingIntelligence } from "@/components/pitchiq/BettingIntelligence";
import { LineMovement } from "@/components/pitchiq/LineMovement";
import { NewsAndAlerts } from "@/components/pitchiq/NewsAndAlerts";
import { Newsletter } from "@/components/pitchiq/Newsletter";
import { Footer } from "@/components/pitchiq/Footer";
import { MobileNav } from "@/components/pitchiq/MobileNav";
import { Toast } from "@/components/pitchiq/Toast";
import { CricketModal } from "@/components/pitchiq/CricketModal";
import { Reveal } from "@/components/pitchiq/Reveal";

export default function Home() {
  return (
    <>
      <DisclaimerBar />
      <LiveTicker />
      <Navbar />
      <SportSwitcher />

      <main className="page">
        <div className="w">
          <Reveal className="hero-grid">
            <FeaturedMatch />
            <SideWidgets />
          </Reveal>
        </div>

        <SportsbookPromo />
        <StatsStrip />

        <div className="w">
          <StandingsSchedule />
          <FantasyPicks />
          <ParlayCard />
          <BettingIntelligence />
          <LineMovement />
          <NewsAndAlerts />
        </div>

        <Newsletter />
      </main>

      <Footer />
      <MobileNav />
      <Toast />
      <CricketModal />
    </>
  );
}
