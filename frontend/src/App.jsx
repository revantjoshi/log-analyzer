import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import OverviewTab from './components/OverviewTab';
import LogStreamTab from './components/LogStreamTab';
import RevantMLTab from './components/RevantMLTab';
import JananiSecurityTab from './components/JananiSecurityTab';
import AshnaHoneypotTab from './components/AshnaHoneypotTab';
import ReportTab from './components/ReportTab';

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');
  
  // State from Backend APIs
  const [systemInfo, setSystemInfo] = useState(null);
  const [logs, setLogs] = useState([]);
  const [mlStatus, setMlStatus] = useState(null);
  const [zeroDayCandidates, setZeroDayCandidates] = useState([]);
  const [attackStories, setAttackStories] = useState([]);
  const [evasionAlerts, setEvasionAlerts] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [honeypotLogs, setHoneypotLogs] = useState([]);
  const [summaryReport, setSummaryReport] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchAllData = async () => {
    try {
      const [
        sysRes,
        logsRes,
        mlRes,
        zdRes,
        secRes,
        evRes,
        alRes,
        hpRes,
        repRes
      ] = await Promise.all([
        fetch('/api/v1/system/info').then(r => r.ok ? r.json() : null).catch(() => null),
        fetch('/api/v1/logs?per_page=100').then(r => r.ok ? r.json() : null).catch(() => null),
        fetch('/api/v1/ml/status').then(r => r.ok ? r.json() : null).catch(() => null),
        fetch('/api/v1/ml/zero-day-candidates').then(r => r.ok ? r.json() : null).catch(() => null),
        fetch('/api/v1/security/attack-stories').then(r => r.ok ? r.json() : null).catch(() => null),
        fetch('/api/v1/security/evasion-alerts').then(r => r.ok ? r.json() : null).catch(() => null),
        fetch('/api/v1/security/alerts').then(r => r.ok ? r.json() : null).catch(() => null),
        fetch('/api/v1/honeypot/logs').then(r => r.ok ? r.json() : null).catch(() => null),
        fetch('/api/v1/security/summary-report').then(r => r.ok ? r.json() : null).catch(() => null)
      ]);

      if (sysRes) setSystemInfo(sysRes);
      if (logsRes && logsRes.logs) setLogs(logsRes.logs);
      if (mlRes) setMlStatus(mlRes);
      if (zdRes && zdRes.candidates) setZeroDayCandidates(zdRes.candidates);
      if (secRes && secRes.stories) setAttackStories(secRes.stories);
      if (evRes && evRes.alerts) setEvasionAlerts(evRes.alerts);
      if (alRes) setAlerts(alRes);
      if (hpRes && hpRes.logs) setHoneypotLogs(hpRes.logs);
      if (repRes) setSummaryReport(repRes);
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAllData();
    const interval = setInterval(fetchAllData, 6000); // refresh every 6 seconds
    return () => clearInterval(interval);
  }, []);

  const handleUploadFile = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch('/api/v1/logs/upload', {
      method: 'POST',
      body: formData
    });
    if (!res.ok) throw new Error('Failed to upload log file');
    await fetchAllData();
  };

  const handleIngestLog = async (rawText) => {
    const res = await fetch('/api/v1/logs/ingest', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ raw_text: rawText })
    });
    if (!res.ok) throw new Error('Failed to ingest log');
    await fetchAllData();
  };

  const handleRunSimulation = async (scenarioKey) => {
    const res = await fetch('/api/v1/honeypot/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenario_key: scenarioKey })
    });
    if (!res.ok) throw new Error('Failed to run attack simulation');
    const data = await res.json();
    await fetchAllData();
    return data;
  };

  const handleRetrainModel = async () => {
    const res = await fetch('/api/v1/ml/retrain', { method: 'POST' });
    if (!res.ok) throw new Error('Failed to retrain model');
    await fetchAllData();
  };

  return (
    <div className="min-h-screen bg-[#07090e] text-slate-100 flex flex-col">
      <Navbar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        systemInfo={systemInfo} 
      />

      <main className="flex-1 max-w-7xl w-full mx-auto p-6">
        {activeTab === 'overview' && (
          <OverviewTab
            mlStatus={mlStatus}
            attackStories={attackStories}
            alerts={alerts}
            honeypotLogs={honeypotLogs}
            logsCount={logs.length}
            onSelectTab={setActiveTab}
          />
        )}

        {activeTab === 'logs' && (
          <LogStreamTab
            logs={logs}
            onUploadFile={handleUploadFile}
            onIngestLog={handleIngestLog}
          />
        )}

        {activeTab === 'ml' && (
          <RevantMLTab
            mlStatus={mlStatus}
            zeroDayCandidates={zeroDayCandidates}
            onRetrainModel={handleRetrainModel}
          />
        )}

        {activeTab === 'security' && (
          <JananiSecurityTab
            attackStories={attackStories}
            evasionAlerts={evasionAlerts}
          />
        )}

        {activeTab === 'honeypot' && (
          <AshnaHoneypotTab
            honeypotLogs={honeypotLogs}
            onRunSimulation={handleRunSimulation}
          />
        )}

        {activeTab === 'report' && (
          <ReportTab
            summaryReport={summaryReport}
          />
        )}
      </main>

      <footer className="border-t border-white/5 py-4 text-center text-xs text-slate-500 bg-[#07090e]">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between px-6 gap-2">
          <span>AI-Powered Intelligent Log Analyzer • Final Year Engineering Project</span>
          <span className="font-mono">Revant (AI/ML) | Janani (Cybersecurity) | Ashna (Honeypot Infrastructure)</span>
        </div>
      </footer>
    </div>
  );
}
