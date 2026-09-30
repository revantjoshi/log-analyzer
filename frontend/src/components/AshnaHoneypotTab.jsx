import React, { useState } from 'react';
import { 
  Flame, 
  Play, 
  CheckCircle2, 
  Radio
} from 'lucide-react';

export default function AshnaHoneypotTab({ honeypotLogs, onRunSimulation }) {
  const [selectedScenario, setSelectedScenario] = useState('web_sqli_campaign');
  const [simulating, setSimulating] = useState(false);
  const [simResult, setSimResult] = useState(null);

  const scenarios = [
    {
      key: 'web_sqli_campaign',
      name: 'WEB EXPLOITATION CAMPAIGN',
      ip: '198.51.100.44',
      desc: 'SQL Injection, XSS, and Path Traversal probes targeting web endpoints'
    },
    {
      key: 'ssh_brute_force',
      name: 'SSH BRUTE FORCE CAMPAIGN',
      ip: '203.0.113.88',
      desc: 'Automated SSH password brute force failures followed by root escalation probe'
    },
    {
      key: 'log_tampering',
      name: 'ANTI-FORENSICS & LOG EVASION',
      ip: '192.0.2.105',
      desc: 'Base64 obfuscated execution, negative timestamp jumps, and log erasure attempts'
    },
    {
      key: 'zero_day_unseen',
      name: 'PREVIOUSLY UNSEEN ANOMALOUS ACTIVITY',
      ip: '198.51.100.99',
      desc: 'High-entropy obfuscated payload exhibiting unclassified statistical feature profile'
    },
    {
      key: 'honeypot_trap',
      name: 'HONEYPOT DECOY INTERACTION',
      ip: '203.0.113.199',
      desc: 'Attacker probing emulated SSH and HTTP honeypot traps'
    }
  ];

  const handleSimulate = async () => {
    setSimulating(true);
    setSimResult('Injecting attack playbook events into log collector pipeline...');
    try {
      const res = await onRunSimulation(selectedScenario);
      setSimResult(`Executed playbook '${res.scenario.name}'. Processed ${res.generated_events_count} event logs.`);
    } catch (err) {
      setSimResult('Error: ' + err.message);
    } finally {
      setSimulating(false);
    }
  };

  return (
    <div className="space-y-8">
      
      {/* Header Banner */}
      <div className="border-b border-white/10 pb-4">
        <div className="font-mono text-xs text-[#FF5A3C] tracking-[0.12em] uppercase">
          / ASHNA MODULE / HONEYPOT TELEMETRY & ATTACK SIMULATOR
        </div>
        <h2 className="text-2xl font-bold font-heading text-white mt-1">
          Honeypot Decoy <span className="text-[#FF5A3C]">Infrastructure</span>
        </h2>
      </div>

      {/* Controlled Attack Simulator Panel */}
      <div className="tech-card p-6 border-t-2 border-t-[#FF5A3C] space-y-4">
        <div className="flex items-center justify-between font-mono text-xs">
          <span className="text-white font-bold flex items-center gap-2">
            <Radio className="w-4 h-4 text-[#FF5A3C]" />
            CONTROLLED ATTACK SCENARIO LAUNCHER
          </span>
          <span className="text-[#FF5A3C]">SAFE LOCAL SANDBOX</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 font-mono text-xs">
          {scenarios.map((sc) => {
            const isSelected = selectedScenario === sc.key;
            return (
              <div
                key={sc.key}
                onClick={() => setSelectedScenario(sc.key)}
                className={`tech-card p-4 cursor-pointer transition-all ${
                  isSelected ? 'tech-card-active' : ''
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[#FF5A3C] font-bold">{sc.ip}</span>
                  <span className="text-[10px] text-slate-500 uppercase">PLAYBOOK</span>
                </div>
                <h4 className="font-bold text-white font-heading text-xs mb-1">{sc.name}</h4>
                <p className="text-[#A1A1A1] text-[11px] leading-relaxed font-sans">{sc.desc}</p>
              </div>
            );
          })}
        </div>

        <div className="flex flex-col md:flex-row items-center justify-between gap-4 pt-2 font-mono text-xs">
          <span className="text-[#A1A1A1]">
            SELECTED PLAYBOOK: <strong className="text-white">{scenarios.find(s => s.key === selectedScenario)?.name}</strong>
          </span>

          <button
            onClick={handleSimulate}
            disabled={simulating}
            className="btn-primary-tech"
          >
            <Play className={`w-3.5 h-3.5 ${simulating ? 'animate-spin' : ''}`} />
            <span>{simulating ? 'INJECTING PLAYBOOK...' : 'TRIGGER SELECTED ATTACK SCENARIO'}</span>
          </button>
        </div>

        {simResult && (
          <div className="p-3 bg-[#121212] border border-[#FF5A3C]/30 text-xs font-mono text-[#FF5A3C] flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-[#FF5A3C]" />
            {simResult}
          </div>
        )}
      </div>

      {/* Honeypot Decoy Telemetry Table */}
      <div className="tech-card overflow-hidden font-mono text-xs">
        <div className="p-4 border-b border-white/10 flex items-center justify-between">
          <span className="text-white font-bold flex items-center gap-2">
            <Flame className="w-4 h-4 text-[#FF5A3C]" />
            ASHNA HONEYPOT DECOY TELEMETRY ({honeypotLogs?.length || 0})
          </span>
          <span className="text-[#6B6B6B]">SENSOR FEED</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs">
            <thead className="bg-[#121212] text-[#6B6B6B] uppercase border-b border-white/10 text-[10px]">
              <tr>
                <th className="p-3.5">TIMESTAMP</th>
                <th className="p-3.5">SENSOR NAME</th>
                <th className="p-3.5">ATTACKER IP</th>
                <th className="p-3.5">PORT</th>
                <th className="p-3.5">SERVICE</th>
                <th className="p-3.5">COMMAND / PAYLOAD</th>
                <th className="p-3.5">SESSION ID</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 text-[#A1A1A1]">
              {honeypotLogs && honeypotLogs.length > 0 ? (
                honeypotLogs.map((log) => (
                  <tr key={log.id} className="hover:bg-[#232323] transition-colors">
                    <td className="p-3.5 text-slate-500">
                      {log.timestamp ? log.timestamp.split('T')[1]?.substring(0, 8) || log.timestamp.substring(0, 10) : 'N/A'}
                    </td>
                    <td className="p-3.5 font-bold text-white">{log.honeypot_name}</td>
                    <td className="p-3.5 text-[#FF5A3C] font-bold">{log.attacker_ip}</td>
                    <td className="p-3.5 text-white">{log.target_port}</td>
                    <td className="p-3.5">
                      <span className="px-2 py-0.5 bg-[#0F0F0F] text-white border border-white/10 text-[10px]">
                        {log.service_emulated}
                      </span>
                    </td>
                    <td className="p-3.5 text-[#FF5A3C] max-w-xs truncate">
                      {log.command_executed || log.payload_attempt || 'N/A'}
                    </td>
                    <td className="p-3.5 text-slate-500 text-[11px]">{log.session_id}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="7" className="p-8 text-center text-[#6B6B6B] italic font-mono">
                    No honeypot telemetry recorded yet. Trigger simulation scenario above.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
