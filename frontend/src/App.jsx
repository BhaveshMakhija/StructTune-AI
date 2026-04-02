import React, { useState, useEffect } from 'react'

function App() {
  const [instruction, setInstruction] = useState("Extract person name and city into JSON.")
  const [inputText, setInputText] = useState("Alice lives in London.")
  const [loading, setLoading] = useState(false)
  const [responses, setResponses] = useState({
    base: "No inference run yet",
    sft: "No inference run yet",
    dpo: "No inference run yet"
  })
  const [metrics, setMetrics] = useState(null)

  // Fetch metrics on mount
  useEffect(() => {
    fetch('/api/metrics')
      .then(res => res.json())
      .then(data => data.latest && setMetrics(data.latest))
      .catch(err => console.error("Metrics failed:", err))
  }, [])

  const handleInference = async () => {
    setLoading(true)
    const models = ['base', 'sft', 'dpo']
    const newResponses = { ...responses }

    for (const m of models) {
      try {
        const resp = await fetch('/api/infer', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ instruction, input_text: inputText, model_name: m })
        })
        const data = await resp.json()
        newResponses[m] = data.result || "Error in inference"
      } catch (e) {
        newResponses[m] = "Failed to reach backend"
      }
    }
    
    setResponses(newResponses)
    setLoading(false)
  }

  return (
    <div className="container">
      <header style={{ marginBottom: '40px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: 'bold' }}>StructTune AI Playground</h1>
          <p style={{ color: '#888' }}>Real-time JSON extraction parity</p>
        </div>
        {metrics && (
          <div className="card" style={{ padding: '12px 20px', fontSize: '0.8rem' }}>
            <span style={{ color: '#10b981' }}>Latest Accuracy: {(metrics.avg_field_accuracy * 100).toFixed(1)}%</span>
          </div>
        )}
      </header>

      {/* Inputs */}
      <section className="card" style={{ marginBottom: '32px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.75rem', color: '#666' }}>INSTRUCTION</label>
            <textarea 
              value={instruction}
              onChange={(e) => setInstruction(e.target.value)}
              style={{ width: '100%', background: '#000', color: '#fff', border: '1px solid #333', borderRadius: '8px', padding: '12px', minHeight: '80px' }}
            />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.75rem', color: '#666' }}>INPUT TEXT</label>
            <textarea 
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              style={{ width: '100%', background: '#000', color: '#fff', border: '1px solid #333', borderRadius: '8px', padding: '12px', minHeight: '80px' }}
            />
          </div>
        </div>
        <button 
          onClick={handleInference}
          disabled={loading}
          style={{
            marginTop: '20px',
            background: loading ? '#333' : '#fff',
            color: loading ? '#888' : '#000',
            padding: '12px 32px',
            borderRadius: '8px',
            border: 'none',
            fontWeight: '700',
            cursor: loading ? 'not-allowed' : 'pointer',
            transition: '0.2s all'
          }}>
          {loading ? 'Processing...' : 'Run Benchmarks'}
        </button>
      </section>

      {/* Comparison Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '20px' }}>
        {['base', 'sft', 'dpo'].map(m => (
          <div key={m} className="card" style={{ minHeight: '200px' }}>
            <h3 style={{ marginBottom: '16px', color: m === 'base' ? '#888' : m === 'sft' ? '#3b82f6' : '#10b981', fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '1px' }}>
              {m.toUpperCase()}
            </h3>
            <pre style={{ fontSize: '0.875rem', whiteSpace: 'pre-wrap', fontFamily: 'monospace', color: '#aaa' }}>
              {responses[m]}
            </pre>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App
