import React, { useState } from 'react';
import { 
  BrainCircuit, 
  RefreshCw, 
  ShieldCheck, 
  AlertTriangle, 
  CheckCircle2
} from 'lucide-react';

export default function RevantMLTab({ mlStatus, zeroDayCandidates, onRetrainModel }) {
  const [retraining, setRetraining] = useState(false);
  const [retrainMsg, setRetrainMsg] = useState(null);

  const handleRetrain = async () => {
    setRetraining(true);
    setRetrainMsg('Retraining Isolation Forest & Baseline Profiler...');
    try {
      await onRetrainModel();
      setRetrainMsg('ML baseline models retrained successfully.');
    } catch (err) {
      setRetrainMsg('Error: ' + err.message);
    } finally {
      setRetraining(false);
    }
  };

  return (
    <div className="space-y-8">
      
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/10 pb-4">
        <div>
          <div className="font-mono text-xs text-[#FF5A3C] tracking-[0.12em] uppercase">
            / REVANT MODULE / ZERO-DAY NOVELTY PROFILER
          </div>
          <h2 className="text-2xl font-bold font-heading text-white mt-1">
            AI/ML <span className="text-[#FF5A3C]">Anomaly Detector</span>
          </h2>
        </div>

        <button
          onClick={handleRetrain}
          disabled={retraining}
          className="btn-primary-tech"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${retraining ? 'animate-spin' : ''}`} />
          <span>{retraining ? 'RETRAINING...' : 'RETRAIN BASELINE MODEL'}</span>
        </button>
      </div>

      {retrainMsg && (
        <div className="p-3 bg-[#1A1A1A] border border-[#FF5A3C]/30 font-mono text-xs text-[#FF5A3C] flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-[#FF5A3C]" />
          {retrainMsg}
        </div>
      )}

      {/* Solid Red-Orange High-Impact Callout Card */}
      <div className="bg-[#FF5A3C] text-white p-6 rounded-[2px] shadow-[0_0_30px_rgba(255,90,60,0.3)] space-y-2">
        <div className="font-mono text-[11px] uppercase tracking-[0.12em] font-semibold text-black opacity-80">
          / TECHNICAL SCOPE & CONCEPT ENFORCEMENT
        </div>
        <h3 className="text-xl md:text-2xl font-bold font-heading">
          "Detection of previously unseen anomalous behaviour that may indicate zero-day activity"
        </h3>
        <p className="text-xs font-mono opacity-90">
          Unsupervised Isolation Forest feature extraction combined with Shannon entropy novelty scoring.
        </p>
      </div>

      {/* Stats Bento Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="tech-card p-5">
          <div className="font-mono text-[10px] text-[#A1A1A1] uppercase">ALGORITHM</div>
          <div className="font-mono text-sm font-bold text-white mt-2">IsolationForest + Scaler</div>
        </div>
        <div className="tech-card p-5">
          <div className="font-mono text-[10px] text-[#A1A1A1] uppercase">LOGS PROFILED</div>
          <div className="font-mono text-2xl font-bold text-white mt-2">{mlStatus?.total_logs_profiled || 0}</div>
        </div>
        <div className="tech-card p-5">
          <div className="font-mono text-[10px] text-[#A1A1A1] uppercase">ANOMALIES DETECTED</div>
          <div className="font-mono text-2xl font-bold text-[#FF5A3C] mt-2">{mlStatus?.anomalies_detected || 0}</div>
        </div>
        <div className="tech-card p-5">
          <div className="font-mono text-[10px] text-[#A1A1A1] uppercase">ZERO-DAY CANDIDATES</div>
          <div className="font-mono text-2xl font-bold text-white mt-2">{mlStatus?.zero_day_candidates || 0}</div>
        </div>
      </div>

      {/* Zero-Day Candidates Section */}
      <div className="space-y-4">
        <div className="font-mono text-xs text-[#6B6B6B] tracking-[0.08em] uppercase">
          / FLAGGED ZERO-DAY CANDIDATE ANOMALIES ({zeroDayCandidates?.length || 0})
        </div>

        <div className="space-y-4">
          {zeroDayCandidates && zeroDayCandidates.length > 0 ? (
            zeroDayCandidates.map((cand) => (
              <div 
                key={cand.id}
                className="tech-card p-6 border-l-4 border-l-[#FF5A3C] space-y-3 font-mono text-xs"
              >
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-white/10 pb-3">
                  <div className="flex items-center gap-3">
                    <span className="px-2 py-0.5 bg-[#FF5A3C] text-white font-bold text-[10px]">ZERO-DAY CANDIDATE</span>
                    <span className="text-white font-bold">{cand.log?.source_ip}</span>
                    <span className="text-[#6B6B6B]">{cand.log?.timestamp}</span>
                  </div>

                  <div className="flex items-center gap-4 text-[#A1A1A1]">
                    <span>ANOMALY SCORE: <strong className="text-white">{cand.anomaly_score}</strong></span>
                    <span>NOVELTY INDEX: <strong className="text-[#FF5A3C]">{cand.novelty_score}</strong></span>
                  </div>
                </div>

                <div>
                  <span className="text-[#FF5A3C] font-bold">{cand.log?.request_method}</span> {cand.log?.path}
                </div>

                {cand.log?.payload && (
                  <pre className="p-3 bg-[#0F0F0F] text-slate-300 text-[11px] border border-white/10 overflow-x-auto">
                    {cand.log.payload}
                  </pre>
                )}

                <div className="p-3 bg-[#1A1A1A] text-[#FF5A3C] border border-[#FF5A3C]/30 italic">
                  RATIONALE: {cand.detection_reason}
                </div>
              </div>
            ))
          ) : (
            <div className="tech-card p-8 text-center text-[#6B6B6B] font-mono italic">
              No zero-day candidate anomalies detected yet. Launch attack simulation in Ashna tab.
            </div>
          )}
        </div>
      </div>

    </div>
  );
}
