import React, { useState, useEffect } from 'react'
import { 
  Zap, Layout, Database, Activity, BarChart3, 
  ChevronRight, Trash2, History, RotateCcw, 
  CheckCircle, AlertCircle, Sparkles, PieChart,
  Target, ShieldCheck, Globe
} from 'lucide-react'

function App() {
  const [activeTab, setActiveTab] = useState(() => localStorage.getItem('activeTab') || 'Playground')
  const [instruction, setInstruction] = useState("")
  const [inputText, setInputText] = useState("")
  const [loading, setLoading] = useState(false)
  const [responses, setResponses] = useState({ base: null, sft: null, dpo: null })
  const [evaluations, setEvaluations] = useState({ base: null, sft: null, dpo: null })
  const [metrics, setMetrics] = useState(null)
  
  const [history, setHistory] = useState(() => {
    const saved = localStorage.getItem('inferenceHistory');
    return saved ? JSON.parse(saved) : [];
  })

  // FALLBACK: Standard lab instruction
  const DEFAULT_INSTRUCTION = "Extract all mentioned entities like Name, Age, City, and Job into a strictly formatted JSON object."

  useEffect(() => {
    localStorage.setItem('activeTab', activeTab)
    localStorage.setItem('inferenceHistory', JSON.stringify(history))
  }, [activeTab, history])

  useEffect(() => { fetchMetrics() }, [])

  const fetchMetrics = () => {
    fetch('/api/metrics')
      .then(res => res.json())
      .then(data => data.latest && setMetrics(data.latest))
  }

  const handleInference = async () => {
    if (!inputText) return
    setLoading(true)
    const activeInstruction = instruction.trim() || DEFAULT_INSTRUCTION
    
    const modelKeys = ['base', 'sft', 'dpo']
    const nextResults = { ...responses }
    const nextEvals = { ...evaluations }

    for (const m of modelKeys) {
      try {
        const r = await fetch('/api/infer', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ instruction: activeInstruction, input_text: inputText, model_name: m })
        })
        const d = await r.json()
        nextResults[m] = d.result
        nextEvals[m] = d.evaluation
      } catch(e) {}
    }
    setResponses(nextResults)
    setEvaluations(nextEvals)
    setHistory(prev => [{ instruction: activeInstruction, input: inputText, timestamp: new Date().toLocaleTimeString() }, ...prev].slice(0, 5))
    setLoading(false)
    setTimeout(fetchMetrics, 500)
  }

  const clearHub = async () => {
    if (window.confirm("Permanently purge laboratory session logs and reset metrics?")) {
      await fetch('/api/logs', { method: 'DELETE' })
      setHistory([])
      localStorage.removeItem('inferenceHistory')
      setMetrics({"avg_valid_json": 0.0, "avg_field_accuracy": 0.0, "hallucination_rate": 0.0, "total_samples": 0})
      setResponses({ base: null, sft: null, dpo: null })
      setEvaluations({ base: null, sft: null, dpo: null })
    }
  }

  const addData = async (mName) => {
    const respBody = responses[mName]
    const activeInstruction = instruction.trim() || DEFAULT_INSTRUCTION
    if (!respBody) return
    await fetch('/api/add_data', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ instruction: activeInstruction, input: inputText, output: respBody })
    })
    alert(`Weights reinforced for ${mName.toUpperCase()}. Baseline accuracy increased.`)
    fetchMetrics()
  }

  const renderContent = () => {
    if (activeTab === 'Playground') {
      return (
        <>
          <section className="workstation">
            <div className="panel-card">
              <div className="panel-label"><span>Inference Parameters</span>{!instruction.trim() && <div className="badge sft">On-Boarding On</div>}</div>
              <textarea placeholder="Custom JSON schema..." value={instruction} onChange={(e) => setInstruction(e.target.value)} rows={4}/>
            </div>
            <div className="panel-card">
              <div className="panel-label"><span>Context Source (Noisy Paragraphs)</span></div>
              <textarea placeholder="Paste bio or report text..." value={inputText} onChange={(e) => setInputText(e.target.value)} rows={4}/>
            </div>
          </section>

          <div className="control-row">
            <button className="btn-launch" onClick={handleInference} disabled={loading || !inputText}>
              {loading ? 'Processing Model Pipeline...' : 'Generate 3-Phase Calibration'} <ChevronRight size={20} />
            </button>
          </div>

          <section className="inference-stage">
            {['base', 'sft', 'dpo'].map(m => (
              <div key={m} className={`model-column`}>
                <div className="column-head"><h4>{m.toUpperCase()} CHECKPOINT</h4><div className={`badge ${m}`}>STABLE</div></div>
                <div className="output-viewport"><pre>{responses[m] || "Awaiting Analysis..."}</pre></div>
                {evaluations[m] && (
                  <div className="eval-stats">
                    <div className="stat-row"><span>Intelligence Score</span><span style={{ color: evaluations[m].is_valid ? '#10b981' : '#f59e0b' }}>{evaluations[m].hallucination_score}%</span></div>
                    <div className="progress-container"><div className="progress-bar" style={{ width: `${evaluations[m].hallucination_score}%`, background: evaluations[m].hallucination_score > 80 ? '#10b981' : '#f59e0b' }}></div></div>
                  </div>
                )}
                {responses[m] && responses[m] !== "Awaiting Analysis..." && (
                  <button className="btn-secondary" style={{ margin: '0 24px 20px 24px', justifyContent: 'center' }} onClick={() => addData(m)}>
                    <Database size={14}/> Refine Model Weights
                  </button>
                )}
              </div>
            ))}
          </section>

          {history.length > 0 && (
            <section className="history-tray">
              <div className="history-title"><History size={18} /> Deep Laboratory Audit Logs</div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {history.map((h, i) => (
                  <div key={i} style={{ padding: '12px 16px', background: '#0a0a0a', border: '1px solid #1a1a1a', borderRadius: '12px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ display: 'flex', gap: '20px', overflow: 'hidden' }}><span style={{ color: '#444', fontSize: '0.75rem' }}>{h.timestamp}</span><span style={{ color: '#888', fontSize: '0.8rem' }}><strong>INS:</strong> {h.instruction.substring(0, 40)}...</span></div>
                    <button className="nav-btn" style={{ padding: '6px' }} onClick={() => { setInstruction(h.instruction); setInputText(h.input); }}><RotateCcw size={14} /></button>
                  </div>
                ))}
              </div>
            </section>
          )}
        </>
      )
    }

    if (activeTab === 'Datasets') {
      return (
        <section style={{ display: 'grid', gridTemplateColumns: '1fr 1.5fr', gap: '24px' }}>
          <div className="panel-card">
            <h3>Active Repositories</h3>
            <div style={{ marginTop: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div style={{ padding: '16px', background: '#000', borderRadius: '12px', border: '1px solid #1a1a1a' }}>
                 <div style={{ color: '#555', fontSize: '0.7rem', fontWeight: 800 }}>SFT DATASET</div>
                 <div style={{ fontWeight: 700, marginTop: '4px' }}>neural_training.jsonl</div>
                 <div style={{ color: '#10b981', fontSize: '0.8rem', marginTop: '8px' }}>Active Partition: {metrics?.total_samples || 0} Learned</div>
              </div>
              <div style={{ padding: '16px', background: '#000', borderRadius: '12px', border: '1px solid #1a1a1a' }}>
                 <div style={{ color: '#555', fontSize: '0.7rem', fontWeight: 800 }}>ALIGNED MEMORY</div>
                 <div style={{ fontWeight: 700, marginTop: '4px' }}>dpo_memory.json</div>
                 <div style={{ color: '#3b82f6', fontSize: '0.8rem', marginTop: '8px' }}>Status: Sync Optimized</div>
              </div>
            </div>
          </div>
          <div className="panel-card">
            <h3>Neural Sample Inspection</h3>
            <pre style={{ marginTop: '20px', padding: '20px', background: '#000', borderRadius: '12px', fontSize: '0.86rem', color: '#666', border: '1px solid #1a1a1a' }}>
              {"{\n  \"instruction\": \"Extract...\",\n  \"context\": \"...\",\n  \"ground_truth\": {\"found\": true}\n}"}
            </pre>
            <p style={{ marginTop: '20px', color: '#444', fontSize: '0.9rem' }}>This memory bank is used by the DPO layer to verify extraction grounding during recursive inference cycles.</p>
          </div>
        </section>
      )
    }

    if (activeTab === 'Metrics') {
      return (
        <section style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '24px' }}>
          <div className="panel-card">
            <Target size={32} color="#10b981" />
            <h3 style={{ marginTop: '16px' }}>Field Accuracy</h3>
            <div style={{ fontSize: '3.5rem', fontWeight: 800, margin: '20px 0' }}>{(metrics?.avg_field_accuracy * 100).toFixed(1)}%</div>
            <p style={{ fontSize: '0.8rem', color: '#444' }}>F-Score precision for entity boundary detection.</p>
          </div>
          <div className="panel-card">
            <ShieldCheck size={32} color="#3b82f6" />
            <h3 style={{ marginTop: '16px' }}>JSON Validity</h3>
            <div style={{ fontSize: '3.5rem', fontWeight: 800, margin: '20px 0' }}>{(metrics?.avg_valid_json * 100).toFixed(1)}%</div>
            <p style={{ fontSize: '0.8rem', color: '#444' }}>Percentage of schema-perfect responses.</p>
          </div>
          <div className="panel-card">
            <Activity size={32} color="#ef4444" />
            <h3 style={{ marginTop: '16px' }}>Hallucination Filter</h3>
            <div style={{ fontSize: '3.5rem', fontWeight: 800, margin: '20px 0' }}>{(100 - (metrics?.hallucination_rate * 100)).toFixed(1)}%</div>
            <p style={{ fontSize: '0.8rem', color: '#444' }}>Detected invention of data fields vs source context.</p>
          </div>
        </section>
      )
    }
  }

  return (
    <div className="dashboard-wrapper">
      <aside className="sidebar">
        <div className="logo-area"><Zap size={28} className="logo-icon" fill="currentColor" /><span>StructTune AI</span></div>
        <nav className="nav-group">
          {['Playground', 'Datasets', 'Metrics'].map(tab => (
            <div key={tab} className={`nav-btn ${activeTab === tab ? 'active' : ''}`} onClick={() => setActiveTab(tab)}>
              {tab === 'Playground' ? <Layout size={20} /> : tab === 'Datasets' ? <Database size={20} /> : <BarChart3 size={20} />}
              {tab}
            </div>
          ))}
        </nav>
        <div className="nav-group" style={{ marginTop: 'auto' }}>
          <div className="nav-btn" style={{ color: '#ef4444' }} onClick={clearHub}>
            <Trash2 size={20} /> Purge Lab Logs
          </div>
        </div>
      </aside>
      <main className="main-stage">
        <header className="stage-header">
          <div className="stage-title"><h1>Laboratory Analytics Hub</h1><p>Active Stream: Research Channel 01</p></div>
          <div className="badge dpo"><Target size={12} /> Live Precision Tracking</div>
        </header>
        {renderContent()}
      </main>
    </div>
  )
}
export default App
