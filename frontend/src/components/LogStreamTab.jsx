import React, { useState } from 'react';
import { 
  Database, 
  Search, 
  Upload, 
  Filter, 
  Eye, 
  AlertTriangle, 
  CheckCircle2
} from 'lucide-react';

export default function LogStreamTab({ logs, onUploadFile, onIngestLog }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [selectedLog, setSelectedLog] = useState(null);
  const [rawIngestText, setRawIngestText] = useState('');
  const [uploadMsg, setUploadMsg] = useState(null);

  const filteredLogs = (logs || []).filter((log) => {
    const matchesSearch = 
      (log.source_ip || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (log.path || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (log.payload || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (log.attack_category || '').toLowerCase().includes(searchTerm.toLowerCase());

    const matchesType = filterType === 'all' || log.log_type === filterType;
    return matchesSearch && matchesType;
  });

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setUploadMsg('Parsing log file...');
    try {
      await onUploadFile(file);
      setUploadMsg('File uploaded and analyzed successfully.');
    } catch (err) {
      setUploadMsg('Error: ' + err.message);
    }
  };

  const handleIngestSubmit = async (e) => {
    e.preventDefault();
    if (!rawIngestText.trim()) return;
    await onIngestLog(rawIngestText);
    setRawIngestText('');
  };

  return (
    <div className="space-y-8">
      
      {/* Eyebrow Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/10 pb-4">
        <div>
          <div className="font-mono text-xs text-[#FF5A3C] tracking-[0.12em] uppercase">
            / LOG INGESTION & FEATURE PARSER
          </div>
          <h2 className="text-2xl font-bold font-heading text-white mt-1">
            Real-Time System <span className="text-[#FF5A3C]">Log Feed</span>
          </h2>
        </div>

        <label className="btn-primary-tech cursor-pointer">
          <div className="w-2.5 h-2.5 bg-white"></div>
          <span>UPLOAD LOG FILE (.LOG/.TXT)</span>
          <input type="file" accept=".log,.txt" onChange={handleFileChange} className="hidden" />
        </label>
      </div>

      {uploadMsg && (
        <div className="p-3 bg-[#1A1A1A] border border-[#FF5A3C]/40 text-xs font-mono text-[#FF5A3C] flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-[#FF5A3C]" />
          {uploadMsg}
        </div>
      )}

      {/* Ingestion Input Bar */}
      <form onSubmit={handleIngestSubmit} className="tech-card p-4 flex flex-col md:flex-row gap-3">
        <input
          type="text"
          placeholder="PASTE RAW LOG STRING (E.G. 192.168.1.50 - - [30/SEP/2026] 'GET /ADMIN/CONFIG.PHP' 404)..."
          value={rawIngestText}
          onChange={(e) => setRawIngestText(e.target.value)}
          className="flex-1 bg-transparent border-b border-white/20 font-mono text-xs text-white placeholder-slate-600 px-3 py-2 focus:outline-none focus:border-[#FF5A3C]"
        />
        <button type="submit" className="btn-secondary-tech">
          <span>INGEST & ANALYZE LOG</span>
        </button>
      </form>

      {/* Filter Controls */}
      <div className="flex flex-col md:flex-row items-center justify-between gap-4 font-mono text-xs">
        <div className="relative flex-1 w-full max-w-md">
          <Search className="w-4 h-4 text-[#6B6B6B] absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="SEARCH IP, PATH, PAYLOAD, CATEGORY..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-[#1A1A1A] border border-white/10 pl-9 pr-4 py-2 text-white placeholder-slate-600 focus:outline-none focus:border-[#FF5A3C]"
          />
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto">
          <Filter className="w-4 h-4 text-[#FF5A3C]" />
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="bg-[#1A1A1A] border border-white/10 text-white px-3 py-2 focus:outline-none focus:border-[#FF5A3C]"
          >
            <option value="all">ALL SOURCES</option>
            <option value="web">WEB ACCESS LOGS</option>
            <option value="ssh">SSH AUTH LOGS</option>
            <option value="honeypot">HONEYPOT DECOY</option>
          </select>
        </div>
      </div>

      {/* Log Stream Table */}
      <div className="tech-card overflow-hidden">
        <div className="p-4 border-b border-white/10 flex items-center justify-between font-mono text-xs">
          <span className="text-[#FF5A3C] font-bold">/ LOG RECORDS ({filteredLogs.length})</span>
          <span className="text-[#6B6B6B]">PARSED & FEATURE SCORED</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs">
            <thead className="bg-[#121212] text-[#6B6B6B] uppercase border-b border-white/10 text-[10px]">
              <tr>
                <th className="p-3.5">TIME</th>
                <th className="p-3.5">SOURCE</th>
                <th className="p-3.5">SOURCE IP</th>
                <th className="p-3.5">METHOD / PATH</th>
                <th className="p-3.5">STATUS</th>
                <th className="p-3.5">CATEGORY</th>
                <th className="p-3.5">AI SCORE</th>
                <th className="p-3.5 text-right">ACTION</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 text-[#A1A1A1]">
              {filteredLogs.length > 0 ? (
                filteredLogs.map((log) => {
                  const isAnomaly = log.anomaly?.is_anomaly;
                  const isZeroDay = log.anomaly?.is_zero_day_candidate;
                  return (
                    <tr key={log.id} className="hover:bg-[#232323] transition-colors">
                      <td className="p-3.5 text-slate-500">
                        {log.timestamp ? log.timestamp.split('T')[1]?.substring(0, 8) || log.timestamp.substring(0, 10) : 'N/A'}
                      </td>
                      <td className="p-3.5">
                        <span className="uppercase text-[10px] px-2 py-0.5 bg-[#0F0F0F] text-white border border-white/10">
                          {log.log_type}
                        </span>
                      </td>
                      <td className="p-3.5 text-white font-bold">{log.source_ip}</td>
                      <td className="p-3.5 max-w-xs truncate text-slate-300">
                        <span className="text-[#FF5A3C] font-bold mr-1.5">{log.request_method}</span>
                        {log.path}
                      </td>
                      <td className="p-3.5">
                        <span className={`font-bold ${log.status_code >= 400 ? 'text-[#FF5A3C]' : 'text-emerald-400'}`}>
                          {log.status_code || 200}
                        </span>
                      </td>
                      <td className="p-3.5 text-slate-200">{log.attack_category}</td>
                      <td className="p-3.5">
                        {isZeroDay ? (
                          <span className="px-2 py-0.5 bg-[#C2321B] text-white text-[10px] font-bold">ZERO-DAY</span>
                        ) : isAnomaly ? (
                          <span className="text-[#FF5A3C] font-bold">ANOMALY ({log.anomaly?.anomaly_score})</span>
                        ) : (
                          <span className="text-slate-600">NORMAL</span>
                        )}
                      </td>
                      <td className="p-3.5 text-right">
                        <button
                          onClick={() => setSelectedLog(log)}
                          className="p-1 bg-[#1A1A1A] hover:bg-[#FF5A3C] hover:text-white border border-white/10 text-slate-300 transition-colors"
                        >
                          <Eye className="w-3.5 h-3.5" />
                        </button>
                      </td>
                    </tr>
                  );
                })
              ) : (
                <tr>
                  <td colSpan="8" className="p-8 text-center text-slate-600 italic font-mono">
                    No log records match current search filter.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Log Detail Inspector Modal */}
      {selectedLog && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="tech-card p-6 max-w-2xl w-full space-y-4 font-mono text-xs border-[#FF5A3C]/40">
            <div className="flex items-center justify-between border-b border-white/10 pb-3">
              <h3 className="font-bold text-white text-sm font-heading">LOG EVENT INSPECTOR</h3>
              <button onClick={() => setSelectedLog(null)} className="text-slate-400 hover:text-white">✕</button>
            </div>

            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-3 text-slate-300">
                <div>SOURCE IP: <span className="text-[#FF5A3C] font-bold">{selectedLog.source_ip}</span></div>
                <div>TYPE: <span className="text-white">{selectedLog.log_type}</span></div>
                <div>STATUS CODE: <span className="text-white">{selectedLog.status_code}</span></div>
                <div>CATEGORY: <span className="text-white">{selectedLog.attack_category}</span></div>
              </div>

              <div>
                <div className="text-slate-500 mb-1">TARGET ENDPOINT:</div>
                <pre className="p-3 bg-[#0F0F0F] text-[#FF5A3C] border border-white/10 overflow-x-auto">{selectedLog.path}</pre>
              </div>

              <div>
                <div className="text-slate-500 mb-1">PAYLOAD STRING:</div>
                <pre className="p-3 bg-[#0F0F0F] text-white border border-white/10 overflow-x-auto">{selectedLog.payload || 'NONE'}</pre>
              </div>

              {selectedLog.anomaly && (
                <div className="p-3 bg-[#1A1A1A] border border-[#FF5A3C]/30 space-y-1">
                  <div className="text-[#FF5A3C] font-bold">REVANT AI ANOMALY INDEX: {selectedLog.anomaly.anomaly_score}</div>
                  <div className="text-slate-300 italic">{selectedLog.anomaly.detection_reason}</div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
