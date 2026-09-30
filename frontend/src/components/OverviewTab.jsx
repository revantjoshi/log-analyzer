import React, { useState } from 'react';
import { 
  ArrowUpRight, 
  ShieldAlert, 
  BrainCircuit, 
  Flame, 
  Layers, 
  Activity,
  Check,
  ChevronRight
} from 'lucide-react';

export default function OverviewTab({ mlStatus, attackStories, alerts, honeypotLogs, logsCount, onSelectTab }) {
  const [activeChartTab, setActiveChartTab] = useState('Efficiency');

  const anomaliesCount = mlStatus?.anomalies_detected || 0;
  const zeroDayCount = mlStatus?.zero_day_candidates || 0;
  const hpCount = honeypotLogs?.length || 0;
  const campaignsCount = attackStories?.length || 0;

  return (
    <div className="space-y-16">
      
      {/* 1. HERO SECTION */}
      <div className="tech-card p-8 md:p-12 relative overflow-hidden glow-ambient-top">
        {/* Corner Crop Bracket Details */}
        <div className="absolute top-2 left-2 font-mono text-[10px] text-[#FF5A3C] opacity-60">+</div>
        <div className="absolute top-2 right-2 font-mono text-[10px] text-[#FF5A3C] opacity-60">+</div>
        <div className="absolute bottom-2 left-2 font-mono text-[10px] text-[#FF5A3C] opacity-60">+</div>
        <div className="absolute bottom-2 right-2 font-mono text-[10px] text-[#FF5A3C] opacity-60">+</div>

        <div className="max-w-4xl space-y-6">
          <div className="font-mono text-xs tracking-[0.12em] text-[#FF5A3C] uppercase flex items-center gap-2">
            <span>/ UNIFIED PLATFORM</span>
            <span>/ REAL-TIME ANOMALY PROFILING</span>
          </div>

          <h1 className="text-4xl md:text-6xl font-bold font-heading text-white tracking-tight leading-tight">
            Automated <span className="text-[#FF5A3C]">Threat Intelligence</span> & Log Analysis
          </h1>

          <p className="text-[#A1A1A1] text-base md:text-lg max-w-2xl leading-relaxed font-sans">
            A unified security operations framework parsing high-volume logs, extracting statistical features, modeling normal behavior baselines, and reconstructing multi-stage attack campaigns.
          </p>

          <div className="flex flex-wrap items-center gap-4 pt-4">
            <button 
              onClick={() => onSelectTab('logs')}
              className="btn-primary-tech"
            >
              <div className="w-2.5 h-2.5 bg-white"></div>
              <span>INSPECT LIVE LOG STREAM</span>
            </button>

            <button 
              onClick={() => onSelectTab('security')}
              className="btn-secondary-tech"
            >
              <span>VIEW ATTACK TOPOLOGY GRAPH</span>
              <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Wireframe Isometric SVG Background Asset */}
        <div className="absolute right-6 bottom-6 hidden lg:block opacity-20 pointer-events-none">
          <svg width="220" height="220" viewBox="0 0 100 100" fill="none" stroke="#FF5A3C" strokeWidth="0.8">
            <polygon points="50,10 90,30 90,70 50,90 10,70 10,30" />
            <line x1="50" y1="10" x2="50" y2="90" />
            <line x1="90" y1="30" x2="10" y2="70" />
            <line x1="10" y1="30" x2="90" y2="70" />
            <circle cx="50" cy="50" r="15" stroke="#FFFFFF" strokeWidth="0.5" />
          </svg>
        </div>
      </div>

      {/* 2. STATS BENTO GRID */}
      <div className="space-y-4">
        <div className="font-mono text-xs text-[#6B6B6B] tracking-[0.08em] uppercase">
          / SYSTEM METRICS & IMPACT TELEMETRY
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          
          <div className="tech-card p-6">
            <div className="font-mono text-[11px] text-[#A1A1A1] uppercase tracking-wider">Total Logs Parsed</div>
            <div className="text-4xl font-bold font-mono text-white mt-3">{logsCount || 25}</div>
            <div className="text-xs text-[#FF5A3C] font-mono mt-2">Real-time Stream Active</div>
          </div>

          <div className="tech-card p-6 border-l-2 border-l-[#FF5A3C]">
            <div className="font-mono text-[11px] text-[#FF5A3C] uppercase tracking-wider">REVANT • AI ANOMALIES</div>
            <div className="text-4xl font-bold font-mono text-white mt-3">{anomaliesCount}</div>
            <div className="text-xs text-[#A1A1A1] font-mono mt-2">
              Zero-Day Candidates: <span className="text-[#FF5A3C] font-bold">{zeroDayCount}</span>
            </div>
          </div>

          <div className="tech-card p-6">
            <div className="font-mono text-[11px] text-[#A1A1A1] uppercase tracking-wider">JANANI • ATTACK STORIES</div>
            <div className="text-4xl font-bold font-mono text-white mt-3">{campaignsCount}</div>
            <div className="text-xs text-[#A1A1A1] font-mono mt-2">MITRE ATT&CK Sequences</div>
          </div>

          <div className="tech-card p-6">
            <div className="font-mono text-[11px] text-[#A1A1A1] uppercase tracking-wider">ASHNA • HONEYPOT HITS</div>
            <div className="text-4xl font-bold font-mono text-white mt-3">{hpCount}</div>
            <div className="text-xs text-[#A1A1A1] font-mono mt-2">Decoy Traps Triggered</div>
          </div>

        </div>
      </div>

      {/* 3. THREE-COLUMN ARCHITECTURE MODULES */}
      <div className="space-y-6">
        <div className="font-mono text-xs text-[#6B6B6B] tracking-[0.08em] uppercase">
          / ARCHITECTURAL MODULE BREAKDOWN
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Revant Module */}
          <div className="tech-card p-6 flex flex-col justify-between">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-mono text-[10px] text-[#FF5A3C] uppercase tracking-wider">MODULE 01</span>
                <BrainCircuit className="w-5 h-5 text-[#FF5A3C]" />
              </div>
              <h3 className="text-xl font-bold font-heading text-white">REVANT: AI/ML Profiling</h3>
              <p className="text-xs text-[#A1A1A1] leading-relaxed font-sans">
                Extracts numerical feature vectors, models baseline normal system behavior with Isolation Forest, and flags statistical anomalies.
              </p>
              <div className="p-3 bg-[#0F0F0F] border border-white/5 font-mono text-[11px] text-[#FF5A3C]">
                "Detection of previously unseen anomalous behaviour that may indicate zero-day activity"
              </div>
            </div>

            <button 
              onClick={() => onSelectTab('ml')}
              className="btn-secondary-tech mt-6 w-full justify-between"
            >
              <span>ACCESS AI PROFILER</span>
              <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>

          {/* Janani Module */}
          <div className="tech-card p-6 flex flex-col justify-between">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-mono text-[10px] text-[#FF5A3C] uppercase tracking-wider">MODULE 02</span>
                <Layers className="w-5 h-5 text-[#FF5A3C]" />
              </div>
              <h3 className="text-xl font-bold font-heading text-white">JANANI: Attack Story</h3>
              <p className="text-xs text-[#A1A1A1] leading-relaxed font-sans">
                Correlates cross-source security logs into end-to-end MITRE ATT&CK story sequences, generates directed topology graphs, and detects log tampering.
              </p>
              <div className="p-3 bg-[#0F0F0F] border border-white/5 font-mono text-[11px] text-[#A1A1A1]">
                Interactive Directed Topology Graph & Anti-Forensics Analysis
              </div>
            </div>

            <button 
              onClick={() => onSelectTab('security')}
              className="btn-secondary-tech mt-6 w-full justify-between"
            >
              <span>ACCESS ATTACK GRAPH</span>
              <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>

          {/* Ashna Module */}
          <div className="tech-card p-6 flex flex-col justify-between">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-mono text-[10px] text-[#FF5A3C] uppercase tracking-wider">MODULE 03</span>
                <Flame className="w-5 h-5 text-[#FF5A3C]" />
              </div>
              <h3 className="text-xl font-bold font-heading text-white">ASHNA: Honeypot & Infra</h3>
              <p className="text-xs text-[#A1A1A1] leading-relaxed font-sans">
                Collects telemetry from emulated decoy services and provides a controlled attack simulator for safe local demonstration.
              </p>
              <div className="p-3 bg-[#0F0F0F] border border-white/5 font-mono text-[11px] text-[#A1A1A1]">
                5 Preset Attack Playbook Simulation Engine
              </div>
            </div>

            <button 
              onClick={() => onSelectTab('honeypot')}
              className="btn-secondary-tech mt-6 w-full justify-between"
            >
              <span>ACCESS HONEYPOT</span>
              <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>

        </div>
      </div>

      {/* 4. LIGHT CONTRAST PANEL: PIXEL-GRID COMPARISON CHART SECTION */}
      <div className="bg-[#E8E8E8] text-[#0F0F0F] p-8 md:p-12 rounded-[2px] space-y-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-black/10 pb-6">
          <div>
            <div className="font-mono text-xs text-[#6B6B6B] tracking-[0.08em] uppercase">
              / EFFICIENCY & METRICS BENCHMARK
            </div>
            <h2 className="text-3xl md:text-4xl font-bold font-heading text-[#0F0F0F] mt-1">
              A Better Way to Detect & Analyze Security Events
            </h2>
          </div>
          <p className="text-xs font-mono text-[#6B6B6B] max-w-sm">
            Comparing manual log searching vs. unified AI-powered feature profiling & graph reconstruction.
          </p>
        </div>

        {/* Chart Filter Tabs */}
        <div className="flex items-center gap-6 border-b border-black/10 pb-2">
          {['Productivity', 'Cost', 'Efficiency', 'Growth'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveChartTab(tab)}
              className={`font-mono text-xs uppercase tracking-wider pb-2 relative font-semibold transition-colors ${
                activeChartTab === tab ? 'text-[#FF5A3C]' : 'text-[#6B6B6B] hover:text-[#0F0F0F]'
              }`}
            >
              {tab}
              {activeChartTab === tab && (
                <div className="absolute bottom-0 left-0 right-0 h-[2px] bg-[#FF5A3C]"></div>
              )}
            </button>
          ))}
        </div>

        {/* Dot-Matrix Pixel Grid Visualization */}
        <div className="p-6 bg-white border border-black/10 rounded-[2px] space-y-4 font-mono">
          <div className="flex items-center justify-between text-[11px] text-[#6B6B6B]">
            <span>[BEFORE ANALYZER] MANUAL GREP / SYSLOG</span>
            <span>[AFTER UNIFIED ANALYZER] AI & GRAPH RECONSTRUCTION</span>
          </div>

          <div className="h-64 relative bg-[#F5F5F5] border border-dashed border-black/20 p-4 flex items-end justify-between overflow-hidden">
            {/* Grid background dots */}
            <div className="absolute inset-0 bg-[radial-gradient(#CCC_1px,transparent_1px)] [background-size:16px_16px]"></div>

            {/* Before state (Grey dots, lower efficiency) */}
            <div className="relative z-10 w-1/2 h-full flex items-end justify-around border-r border-dashed border-black/30 pr-4">
              <div className="w-3 bg-gray-400 h-[30%]"></div>
              <div className="w-3 bg-gray-400 h-[25%]"></div>
              <div className="w-3 bg-gray-400 h-[40%]"></div>
              <div className="w-3 bg-gray-400 h-[35%]"></div>
            </div>

            {/* After state (Red-Orange accent dots, 8x efficiency) */}
            <div className="relative z-10 w-1/2 h-full flex items-end justify-around pl-4">
              <div className="w-3 bg-[#FF5A3C] h-[75%]"></div>
              <div className="w-3 bg-[#FF5A3C] h-[85%]"></div>
              <div className="w-3 bg-[#FF5A3C] h-[95%]"></div>
              <div className="w-3 bg-[#FF5A3C] h-[90%]"></div>
            </div>
          </div>

          <div className="flex items-center justify-between text-xs text-[#0F0F0F] pt-2">
            <span>Average MTTR: <strong className="text-gray-600">4.5 Hours</strong></span>
            <span>AI Automated Detection: <strong className="text-[#FF5A3C]">&lt; 2 Seconds</strong></span>
          </div>
        </div>
      </div>

    </div>
  );
}
