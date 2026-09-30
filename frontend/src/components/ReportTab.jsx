import React, { useState } from 'react';
import { 
  FileText, 
  Download, 
  Copy, 
  CheckCircle2 
} from 'lucide-react';

export default function ReportTab({ summaryReport }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (!summaryReport) return;
    const text = JSON.stringify(summaryReport, null, 2);
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    if (!summaryReport) return;
    const text = JSON.stringify(summaryReport, null, 2);
    const blob = new Blob([text], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Cybersecurity_Log_Analyzer_Report_${new Date().toISOString().substring(0, 10)}.json`;
    a.click();
  };

  return (
    <div className="space-y-8 font-mono">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/10 pb-4">
        <div>
          <div className="text-xs text-[#FF5A3C] tracking-[0.12em] uppercase">
            / INCIDENT ENGINE / AUTOMATED SUMMARY REPORT
          </div>
          <h2 className="text-2xl font-bold font-heading text-white mt-1">
            Executive <span className="text-[#FF5A3C]">Cybersecurity Report</span>
          </h2>
        </div>

        <div className="flex items-center gap-3">
          <button onClick={handleCopy} className="btn-secondary-tech">
            <Copy className="w-3.5 h-3.5" />
            <span>{copied ? 'COPIED!' : 'COPY RAW JSON'}</span>
          </button>

          <button onClick={handleDownload} className="btn-primary-tech">
            <Download className="w-3.5 h-3.5" />
            <span>EXPORT INCIDENT REPORT</span>
          </button>
        </div>
      </div>

      {summaryReport ? (
        <div className="tech-card p-6 space-y-6 text-xs">
          
          {/* Metadata Block */}
          <div className="p-4 bg-[#121212] border border-white/10 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <span className="text-[#6B6B6B] block">REPORT TITLE:</span>
              <span className="font-bold text-white">{summaryReport.report_title}</span>
            </div>
            <div>
              <span className="text-[#6B6B6B] block">PLATFORM STATUS:</span>
              <span className="font-bold text-emerald-400">{summaryReport.platform_status}</span>
            </div>
            <div>
              <span className="text-[#6B6B6B] block">GENERATED AT:</span>
              <span className="text-[#FF5A3C]">{summaryReport.generated_at}</span>
            </div>
          </div>

          {/* Executive Summary Statement */}
          <div className="p-6 bg-[#1A1A1A] border-l-4 border-l-[#FF5A3C] text-slate-200 text-sm leading-relaxed font-sans">
            <h3 className="font-bold text-white font-heading text-base mb-2">EXECUTIVE SUMMARY STATEMENT</h3>
            <p>{summaryReport.executive_summary}</p>
          </div>

          {/* Metrics Summary Table */}
          <div className="space-y-3">
            <div className="text-[#6B6B6B] uppercase">/ KEY INCIDENT METRICS</div>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
              {Object.entries(summaryReport.metrics || {}).map(([key, val]) => (
                <div key={key} className="tech-card p-4">
                  <span className="text-[10px] text-[#A1A1A1] uppercase block truncate">
                    {key.replace(/_/g, ' ')}
                  </span>
                  <span className="text-2xl font-bold text-white font-mono mt-1 block">
                    {val}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Recommended Mitigations List */}
          <div className="space-y-3">
            <div className="text-[#FF5A3C] uppercase font-bold">/ RECOMMENDED INCIDENT RESPONSE MITIGATIONS</div>
            <ul className="space-y-2">
              {(summaryReport.recommended_mitigations || []).map((item, idx) => (
                <li key={idx} className="p-3 bg-[#121212] border border-white/10 text-slate-300 flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-[#FF5A3C] shrink-0" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>

        </div>
      ) : (
        <div className="tech-card p-8 text-center text-[#6B6B6B]">Loading executive report...</div>
      )}

    </div>
  );
}
