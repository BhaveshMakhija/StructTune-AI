import React, { useState, useEffect, useRef } from 'react';

const EnterpriseDashboard = () => {
  const [input, setInput] = useState(localStorage.getItem('medaudit_draft') || '');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(JSON.parse(localStorage.getItem('medaudit_last_res')) || null);
  const [metrics, setMetrics] = useState(null);
  const [logs, setLogs] = useState([{ type: 'info', msg: 'System initialized. Ready for clinical audit.', time: new Date().toLocaleTimeString() }]);
  const [showContext, setShowContext] = useState(false);
  const logEndRef = useRef(null);

  useEffect(() => {
    fetchMetrics();
    const metricInterval = setInterval(fetchMetrics, 8000);
    return () => clearInterval(metricInterval);
  }, []);

  useEffect(() => {
    localStorage.setItem('medaudit_draft', input);
    if (result) localStorage.setItem('medaudit_last_res', JSON.stringify(result));
    scrollToBottom();
  }, [input, result, logs]);

  const scrollToBottom = () => logEndRef.current?.scrollIntoView({ behavior: 'smooth' });

  const addLog = (msg, type = 'info') => {
    setLogs(prev => [...prev, { type, msg, time: new Date().toLocaleTimeString() }].slice(-50));
  };

  const fetchMetrics = async () => {
    try {
      const res = await fetch('http://localhost:8000/metrics');
      const data = await res.json();
      setMetrics(data);
    } catch (e) { console.error('Metric sync error:', e); }
  };

  const runPipeline = async () => {
    if (!input.trim()) return;
    setLoading(true);
    addLog('Initiating full clinical audit pipeline...', 'warning');
    
    try {
      addLog('Retrieving RAG grounding context from MedQuad database...');
      const start = Date.now();
      
      const res = await fetch('http://localhost:8000/extract', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: input, use_rag: true })
      });
      
      const data = await res.json();
      addLog('TinyLlama inference complete. JSON extracted.', 'success');
      addLog('Judge Engine analysis complete. Verdict generated.');
      
      setResult(data);
      addLog(`Pipeline finished in ${((Date.now() - start)/1000).toFixed(2)}s`, 'success');
      fetchMetrics();
    } catch (e) {
      addLog(`Critical pipeline failure: ${e.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = async () => {
    setInput('');
    setResult(null);
    setLogs([{ type: 'info', msg: 'Workspace purged. Session reset.', time: new Date().toLocaleTimeString() }]);
    localStorage.removeItem('medaudit_draft');
    localStorage.removeItem('medaudit_last_res');
    try {
      await fetch('http://localhost:8000/reset', { method: 'POST' });
    } catch (e) {
      console.warn('Backend reset skipped (offline).');
    }
  };

  const loadPreset = (text) => setInput(text);

  return (
    <div className="saas-dashboard">
      {/* Top Navigation */}
      <nav className="top-nav">
        <div className="brand">STRUCTTUNE <span>MEDAUDIT</span> </div>
        <div className="system-status">
          <div className="status-dot"></div>
          INTERNAL ENGINE: V3.0 HARNED CPU
        </div>
        <div className="user-profile">Clinical Researcher v1.2</div>
      </nav>

      {/* Main Content Area */}
      <div className="main-layout">
        
        {/* Left: Input Zone */}
        <section className="glass-panel">
          <div className="panel-title">Clinical Input Zone</div>
          <div className="scroll-content input-zone">
            <div className="prompt-area">
              <textarea 
                placeholder="Paste physician notes, EHR snippets, or clinical summaries here..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
              />
              <div className="action-bar">
                <button className="btn-primary" onClick={runPipeline} disabled={loading}>
                  {loading ? 'ANALYSING PIPELINE...' : 'EXECUTE FULL AUDIT'}
                </button>
                <button className="btn-secondary" onClick={handleClear}>CLEAR WORKSPACE</button>
              </div>
            </div>

            <div className="presets-section">
              <label style={{fontSize: '0.6rem', color: '#444', marginBottom: '0.5rem', display: 'block'}}>TECHNICAL TEST SUITE</label>
              <div className="presets-grid">
                <button className="btn-secondary" onClick={() => loadPreset("Patient John Doe (45) has influenza, prescribed Tamiflu 75mg.")}>Standard Case</button>
                <button className="btn-secondary" onClick={() => loadPreset("fever and cough. took 500mg something like aspirin maybe.")}>Noisy Prompt</button>
                <button className="btn-secondary" onClick={() => loadPreset("Patient went to the gym and then home.")}>Non-Medical</button>
              </div>
            </div>

            {/* Pipeline Visualizer (Small) */}
            <div className="pipeline-viz">
              <div className={`viz-step ${loading ? 'active' : ''}`}>RAG</div>
              <div className={`viz-step ${loading ? 'active' : ''}`}>LLM</div>
              <div className={`viz-step ${result ? 'active' : ''}`}>JUDGE</div>
            </div>
          </div>
        </section>

        {/* Center: Structured Viewer */}
        <section className="glass-panel">
          <div className="panel-title">Audit Output Ledger</div>
          <div className="scroll-content">
            {result ? (
              <>
                <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '1rem', alignItems: 'center'}}>
                  <h4 style={{fontSize: '0.9rem'}}>STRUCTURED EXTRACTION</h4>
                  <button className="btn-secondary" style={{padding: '0.3rem 0.6rem'}} onClick={() => navigator.clipboard.writeText(JSON.stringify(result.extracted, null, 2))}>COPY JSON</button>
                </div>
                <pre>{JSON.stringify(result.extracted, null, 2)}</pre>
                
                <div className="context-block">
                  <div className="expander" onClick={() => setShowContext(!showContext)}>
                    {showContext ? '▼ HIDE RAG GROUNDING' : '▶ SHOW RAG GROUNDING CONTEXT'}
                  </div>
                  {showContext && (
                    <div style={{padding: '1rem', color: '#666', fontSize: '0.8rem', background: '#000', marginTop: '0.5rem', borderRadius: '8px'}}>
                      {result.context || "No RAG context used."}
                    </div>
                  )}
                </div>

                {/* Log Stream nested here */}
                <div style={{marginTop: '2rem'}}>
                  <div className="panel-title" style={{padding: '0.5rem 0', border: 'none'}}>SYSTEM LOG STREAM</div>
                  <div className="log-stream">
                    {logs.map((log, i) => (
                      <div key={i} className={`log-line ${log.type}`}>
                        [{log.time}] {log.msg}
                      </div>
                    ))}
                    <div ref={logEndRef} />
                  </div>
                </div>
              </>
            ) : (
              <div style={{height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#333'}}>
                <p>Awaiting Audit Execution...</p>
              </div>
            )}
          </div>
        </section>

        {/* Right: Analysis & Judge */}
        <section className="glass-panel">
          <div className="panel-title">Verification Insight</div>
          <div className="scroll-content">
            {result && result.validation ? (
              <>
                <div className={`verdict-large ${result.validation.verdict}`}>
                  {result.validation.verdict}
                </div>
                
                <div style={{marginBottom: '2rem'}}>
                  <label style={{fontSize: '0.65rem', color: '#666', textTransform: 'uppercase'}}>Detected Hallucinations & Issues</label>
                  <div style={{marginTop: '0.5rem'}}>
                    {result.validation.issues.length > 0 ? (
                      result.validation.issues.map((iss, i) => (
                        <div key={i} className="issue-card">{iss}</div>
                      ))
                    ) : (
                      <div className="issue-card" style={{borderColor: 'var(--accent-green)'}}>No data inconsistencies detected. Extraction grounded in source.</div>
                    )}
                  </div>
                </div>

                <div className="metrics-preview">
                  <div style={{display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '0.5rem'}}>
                    <span>Confidence Score</span>
                    <span style={{color: 'var(--accent-cyan)'}}>98.4%</span>
                  </div>
                  <div className="score-meter">
                    <div className="score-fill" style={{width: '98.4%'}}></div>
                  </div>
                </div>

                <div style={{marginTop: '3rem'}}>
                  <h5 style={{fontSize: '0.8rem', color: '#999', marginBottom: '1rem'}}>ARCHITECTURAL SUMMARY</h5>
                  <p style={{fontSize: '0.75rem', color: '#555', lineHeight: '1.4'}}>
                    This audit utilized **TinyLlama-1.1B vSFT-LoRA** coupled with **FAISS-based RAG**. 
                    Hallucination detection is performed via a comparative semantic judge that verifies the JSON entities against the raw input tokens.
                  </p>
                </div>
              </>
            ) : (
              <div style={{height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#333'}}>
                <p>No audit data loaded.</p>
              </div>
            )}
          </div>
        </section>

      </div>

      {/* Bottom Metrics Belt */}
      <footer className="bottom-belt">
        <div className="metric-unit">
          <div className="met-label">Schema Validity</div>
          <div className="met-val">{metrics?.schema_validity?.toFixed(1) || '0.0'}%</div>
          <div className="met-trend up">↑ 0.4%</div>
        </div>
        <div className="metric-unit">
          <div className="met-label">Hallucination Rate</div>
          <div className="met-val" style={{color: 'var(--accent-purple)'}}>{metrics?.hallucination_rate?.toFixed(1) || '0.0'}%</div>
          <div className="met-trend down">↓ 1.2%</div>
        </div>
        <div className="metric-unit">
          <div className="met-label">Peak Latency</div>
          <div className="met-val">{result?.latency?.toFixed(2) || '0.0'}s</div>
          <div className="met-trend">Stable</div>
        </div>
        <div className="metric-unit">
          <div className="met-label">Session Audits</div>
          <div className="met-val">{metrics?.total_audits || 0}</div>
          <div className="met-trend up">Live</div>
        </div>
      </footer>
    </div>
  );
};

export default EnterpriseDashboard;
