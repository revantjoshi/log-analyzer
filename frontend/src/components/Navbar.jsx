import React from 'react';
import { 
  Activity, 
  Database, 
  BrainCircuit, 
  GitMerge, 
  Flame, 
  FileText,
  Square
} from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab }) {
  const tabs = [
    { id: 'overview', label: 'OVERVIEW', icon: Activity },
    { id: 'logs', label: 'LOG STREAM', icon: Database },
    { id: 'ml', label: 'REVANT: AI PROFILER', icon: BrainCircuit },
    { id: 'security', label: 'JANANI: ATTACK GRAPH', icon: GitMerge },
    { id: 'honeypot', label: 'ASHNA: HONEYPOT', icon: Flame },
    { id: 'report', label: 'INCIDENT REPORT', icon: FileText }
  ];

  return (
    <header className="sticky top-0 z-50 bg-[#0F0F0F]/95 backdrop-blur-md border-b border-white/10 px-6 py-4">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        
        {/* Logo & Eyebrow */}
        <div className="flex items-center gap-4">
          <div className="w-9 h-9 bg-[#FF5A3C] text-white flex items-center justify-center font-mono text-sm font-bold shadow-[0_0_15px_rgba(255,90,60,0.4)]">
            LA
          </div>
          <div>
            <div className="text-[10px] font-mono tracking-[0.12em] text-[#FF5A3C] uppercase">
              / UNIFIED / INTELLIGENT / LOG ANALYZER
            </div>
            <h1 className="text-xl font-bold font-heading text-white tracking-tight flex items-center gap-2">
              CYBERSECURITY <span className="text-[#FF5A3C]">PLATFORM</span>
            </h1>
          </div>
        </div>

        {/* Team Module Contributors Tags */}
        <div className="flex items-center gap-2 flex-wrap">
          <span className="font-mono text-[10px] uppercase px-2.5 py-1 bg-[#1A1A1A] text-[#A1A1A1] border border-white/10">
            REVANT • <span className="text-[#FF5A3C]">AI/ML</span>
          </span>
          <span className="font-mono text-[10px] uppercase px-2.5 py-1 bg-[#1A1A1A] text-[#A1A1A1] border border-white/10">
            JANANI • <span className="text-[#FF5A3C]">CYBER</span>
          </span>
          <span className="font-mono text-[10px] uppercase px-2.5 py-1 bg-[#1A1A1A] text-[#A1A1A1] border border-white/10">
            ASHNA • <span className="text-[#FF5A3C]">HONEYPOT</span>
          </span>
          <div className="flex items-center gap-1.5 px-3 py-1 bg-[#1A1A1A] border border-[#FF5A3C]/40 text-[10px] font-mono text-white">
            <span className="w-2 h-2 rounded-full bg-[#FF5A3C] animate-pulse"></span>
            SOC ACTIVE
          </div>
        </div>

      </div>

      {/* Tech Eyebrow Navigation Bar */}
      <div className="max-w-7xl mx-auto mt-4 pt-3 border-t border-white/5 flex items-center gap-2 overflow-x-auto pb-1 scrollbar-none">
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-3.5 py-2 font-mono text-[11px] tracking-wider transition-all duration-200 whitespace-nowrap rounded-[2px] ${
                isActive
                  ? 'bg-[#FF5A3C] text-white font-semibold shadow-[0_0_15px_rgba(255,90,60,0.35)]'
                  : 'bg-[#1A1A1A] text-[#A1A1A1] hover:text-white hover:border-[#FF5A3C]/50 border border-white/5'
              }`}
            >
              <div className={`w-2 h-2 ${isActive ? 'bg-white' : 'bg-[#FF5A3C]'}`} />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>
    </header>
  );
}
