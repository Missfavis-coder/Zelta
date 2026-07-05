
import WhyZelta from "@/components /home/demo";
import HeroSection from "@/components /home/hero";
import Navbar from "@/components /home/navbar";
import Why from "@/components /home/why";
import IntroTab from "@/components /IntroTab";
import HowItWorks from "@/components /home/how-it-works";
import Footer from "@/components /home/footer";
import Companies from "@/components /home/built-on";
import Demo from "@/components /home/demo";
import Testimonies from "@/components /home/testimonies";

export default function Home() {
  return (
    <div className="bg-background text-white">
      <Navbar />
      <HeroSection/>
      <Companies/>
      <Why/>
      <HowItWorks/>
      <Testimonies/>
      <Demo/>
      <Footer/>
    </div>
  );
}
