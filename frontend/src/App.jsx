import React, { useState, useEffect } from 'react';

const MedAuditDashboard = () => {
  const [inputText, setInputText] = useState('');
  const [extraction, setExtraction] = useState(null);
  const [validation, setValidation] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchMetrics();
  }, []);

  const fetchMetrics = async () => {
    try {
      const res = await fetch('http://localhost:8000/metrics');
      const data = await res.json();
      setMetrics(data);
    } catch (e) {
      console.error("Failed to fetch metrics", e);
    }
  };

  const handleRun = async () => {
    setLoading(true);
    setExtraction(null);
    setValidation(null);
    try {
      const res = await fetch('http://localhost:8000/extract', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText, use_rag: true })
      });
      const data = await res.json();
      setExtraction(data);

      const valRes = await fetch('http://localhost:8000/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: inputText, extracted: data.extracted })
      });
      const valData = await valRes.json();
      setValidation(valData);
    } catch (e) {
      console.error("Extraction failed", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <header className="header">
        <h1>StructTune <span className="highlight">MedAudit</span></h1>
        <div className="tagline">Clinical Document Extraction + Validation System</div>
      </header>

      <div className="metrics-grid">
        <div className="metric-card">
          <label>Extraction Accuracy</label>
          <div className="value">{metrics?.extraction_accuracy?.toFixed(1) || '0.0'}%</div>
        </div>
        <div className="metric-card">
          <label>Hallucination Rate</label>
          <div className="value danger">{metrics?.hallucination_rate?.toFixed(1) || '0.0'}%</div>
        </div>
        <div className="metric-card">
          <label>Schema Validity</label>
          <div className="value success">{metrics?.schema_validity?.toFixed(1) || '0.0'}%</div>
        </div>
      </div>

      <main className="content">
        <section className="input-section card">
          <h3>Medical Text Input</h3>
          <textarea 
            placeholder="Paste clinical note here..." 
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
          />
          <button onClick={handleRun} disabled={loading || !inputText}>
            {loading ? 'Processing...' : 'Run Extraction'}
          </button>
        </section>

        <section className="output-grid">
          <div className="card json-viewer">
            <h3>Structured Output</h3>
            <pre>{extraction ? JSON.stringify(extraction.extracted, null, 2) : '// Result will appear here'}</pre>
          </div>

          <div className="card validation-panel">
            <h3>Validation Report</h3>
            {validation ? (
              <div className="val-content">
                <div className={`badge ${validation.verdict}`}>
                  {validation.verdict}
                </div>
                <ul className="issues">
                  {validation.issues.length > 0 ? (
                    validation.issues.map((iss, i) => <li key={i}>{iss}</li>)
                  ) : (
                    <li>No issues detected.</li>
                  )}
                </ul>
                <div className="val-type">Type: {validation.type}</div>
              </div>
            ) : (
              <p className="placeholder">Run extraction to see report</p>
            )}
          </div>
        </section>
      </main>
    </div>
  );
};

export default MedAuditDashboard;
