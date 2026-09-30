import React, { useEffect, useRef, useState } from 'react';
import { Network } from 'vis-network';
import { DataSet } from 'vis-data';
import { 
  GitMerge, 
  Clock, 
  Layers, 
  FileWarning
} from 'lucide-react';

export default function JananiSecurityTab({ attackStories, evasionAlerts }) {
  const [selectedStory, setSelectedStory] = useState(null);
  const graphContainerRef = useRef(null);
  const networkRef = useRef(null);

  useEffect(() => {
    if (attackStories && attackStories.length > 0 && !selectedStory) {
      setSelectedStory(attackStories[0]);
    }
  }, [attackStories]);

  useEffect(() => {
    if (!graphContainerRef.current || !selectedStory || !selectedStory.graph_data) return;

    const graphData = selectedStory.graph_data;

    const visNodes = new DataSet(
      (graphData.nodes || []).map(node => ({
        id: node.id,
        label: node.label,
        shape: node.type === 'attacker' ? 'diamond' : node.type === 'honeypot' ? 'hexagon' : 'box',
        color: {
          background: node.type === 'attacker' ? '#FF5A3C' : node.type === 'honeypot' ? '#C2321B' : '#1A1A1A',
          border: '#FFFFFF',
          highlight: { background: '#FF5A3C', border: '#FFFFFF' }
        },
        font: { color: '#FFFFFF', face: 'Space Grotesk', size: 12 }
      }))
    );

    const visEdges = new DataSet(
      (graphData.edges || []).map(edge => ({
        id: edge.id,
        from: edge.from,
        to: edge.to,
        label: edge.label,
        color: { color: '#FF5A3C' },
        arrows: 'to',
        font: { color: '#A1A1A1', size: 10, align: 'top' },
        dashes: edge.dashes || false
      }))
    );

    const options = {
      nodes: { borderWidth: 2, shadow: true },
      edges: { width: 2, shadow: true, smooth: { type: 'curvedCW', roundness: 0.2 } },
      physics: { enabled: true, barnesHut: { gravitationalConstant: -3000, springLength: 120 } }
    };

    networkRef.current = new Network(graphContainerRef.current, { nodes: visNodes, edges: visEdges }, options);

    return () => {
      if (networkRef.current) {
        networkRef.current.destroy();
        networkRef.current = null;
      }
    };
  }, [selectedStory]);

  return (
    <div className="space-y-8">
      
      {/* Header Banner */}
      <div className="border-b border-white/10 pb-4">
        <div className="font-mono text-xs text-[#FF5A3C] tracking-[0.12em] uppercase">
          / JANANI MODULE / CORRELATION & ATTACK RECONSTRUCTION
        </div>
        <h2 className="text-2xl font-bold font-heading text-white mt-1">
          Cybersecurity <span className="text-[#FF5A3C]">Attack Topology Graph</span>
        </h2>
      </div>

      {/* Grid: Attack Stories + Interactive Graph */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column: Attack Campaigns */}
        <div className="space-y-4 font-mono text-xs">
          <div className="text-[#6B6B6B] uppercase tracking-wider">
            / CORRELATED CAMPAIGNS ({attackStories?.length || 0})
          </div>

          <div className="space-y-3">
            {attackStories && attackStories.length > 0 ? (
              attackStories.map((story, idx) => {
                const isSelected = selectedStory?.attacker_ip === story.attacker_ip;
                return (
                  <div
                    key={idx}
                    onClick={() => setSelectedStory(story)}
                    className={`tech-card p-4 cursor-pointer transition-all ${
                      isSelected ? 'tech-card-active' : ''
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="px-2 py-0.5 bg-[#FF5A3C] text-white font-bold text-[10px]">
                        {story.severity}
                      </span>
                      <span className="text-white font-bold">{story.attacker_ip}</span>
                    </div>

                    <h4 className="font-bold text-white font-heading text-sm">{story.title}</h4>
                    <p className="text-[#A1A1A1] text-[11px] mt-1 line-clamp-2">{story.description}</p>

                    <div className="flex items-center gap-1.5 mt-3 flex-wrap">
                      {story.mitre_tactics.map((tac, tIdx) => (
                        <span key={tIdx} className="px-2 py-0.5 bg-[#0F0F0F] text-slate-300 border border-white/10 text-[9px]">
                          {tac.split(' - ')[0]}
                        </span>
                      ))}
                    </div>
                  </div>
                );
              })
            ) : (
              <div className="tech-card p-6 text-center text-[#6B6B6B] italic">
                No attack campaigns correlated yet. Trigger simulation in Ashna tab.
              </div>
            )}
          </div>
        </div>

        {/* Center & Right Column: Vis-Network Graph & MITRE Timeline */}
        <div className="lg:col-span-2 space-y-6">
          {selectedStory ? (
            <>
              {/* Interactive Network Graph */}
              <div className="tech-card p-6 space-y-4">
                <div className="flex items-center justify-between font-mono text-xs">
                  <span className="text-white font-bold flex items-center gap-2">
                    <GitMerge className="w-4 h-4 text-[#FF5A3C]" />
                    ATTACK PATHWAY TOPOLOGY: {selectedStory.attacker_ip}
                  </span>
                  <span className="text-[#6B6B6B]">VIS-NETWORK ENGINE</span>
                </div>

                <div ref={graphContainerRef} id="vis-attack-graph"></div>
              </div>

              {/* MITRE ATT&CK Timeline */}
              <div className="tech-card p-6 space-y-4">
                <div className="font-mono text-xs text-[#FF5A3C] font-bold flex items-center gap-2">
                  <Clock className="w-4 h-4 text-[#FF5A3C]" />
                  MITRE ATT&CK STEP-BY-STEP RECONSTRUCTION TIMELINE
                </div>

                <div className="relative border-l border-white/10 ml-4 space-y-4 pl-6 font-mono text-xs">
                  {selectedStory.timeline_data.map((step, sIdx) => (
                    <div key={sIdx} className="relative">
                      <div className="absolute -left-[30px] top-1.5 w-2.5 h-2.5 bg-[#FF5A3C]"></div>
                      
                      <div className="p-3 bg-[#121212] border border-white/10 space-y-1">
                        <div className="flex items-center justify-between text-slate-400 text-[11px]">
                          <span className="text-[#FF5A3C] font-bold">STEP {step.step_index}: {step.mitre_tactic}</span>
                          <span>{step.timestamp}</span>
                        </div>

                        <div className="text-white">
                          <span className="text-[#FF5A3C] font-bold">{step.action}</span> {step.target}
                        </div>

                        {step.payload && (
                          <pre className="p-2 bg-[#0F0F0F] text-[#A1A1A1] text-[10px] overflow-x-auto border border-white/5">
                            {step.payload}
                          </pre>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          ) : (
            <div className="tech-card p-8 text-center text-[#6B6B6B] font-mono">
              Select a correlated attack story on the left to inspect topology graph.
            </div>
          )}
        </div>

      </div>

      {/* Log Tampering & Anti-Forensics Alerts */}
      <div className="tech-card p-6 border-t-2 border-t-[#FF5A3C] space-y-4">
        <div className="font-mono text-xs text-[#FF5A3C] font-bold flex items-center gap-2">
          <FileWarning className="w-4 h-4 text-[#FF5A3C]" />
          LOG TAMPERING & ANTI-FORENSICS EVASION ALERTS ({evasionAlerts?.length || 0})
        </div>

        <div className="space-y-3 font-mono text-xs">
          {evasionAlerts && evasionAlerts.length > 0 ? (
            evasionAlerts.map((alert, aIdx) => (
              <div key={aIdx} className="p-3.5 bg-[#121212] border border-white/10 space-y-1">
                <div className="flex items-center gap-3">
                  <span className="px-2 py-0.5 bg-[#C2321B] text-white font-bold text-[10px]">CRITICAL</span>
                  <span className="text-white font-bold">{alert.indicator_type}</span>
                  <span className="text-[#FF5A3C]">{alert.source_ip}</span>
                </div>
                <p className="text-[#A1A1A1]">{alert.description}</p>
              </div>
            ))
          ) : (
            <div className="text-[#6B6B6B] italic">No anti-forensics log tampering detected.</div>
          )}
        </div>
      </div>

    </div>
  );
}
