import React, { useState } from 'react'

function App() {
  const [instruction, setInstruction] = useState("Extract person name and city into JSON.")
  const [inputText, setInputText] = useState("Alice lives in London.")
  const [responses, setResponses] = useState({
    base: "Base output placeholder",
    sft: "SFT output placeholder",
    dpo: "DPO output placeholder"
  })

  return (
    <div className="container">
      <header style={{ marginBottom: '40px' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 'bold' }}>StructTune AI Playground</h1>
        <p style={{ color: '#888' }}>Compare fine-tuning improvements in real-time</p>
      </header>

      {/* Inputs Section */}
      <section className="card" style={{ marginBottom: '32px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.875rem' }}>Instruction</label>
            <textarea 
              value={instruction}
              onChange={(e) => setInstruction(e.target.value)}
              style={{ width: '100%', background: '#000', color: '#fff', border: '1px solid #333', borderRadius: '8px', padding: '12px', minHeight: '80px' }}
            />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.875rem' }}>Text Input</label>
            <textarea 
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              style={{ width: '100%', background: '#000', color: '#fff', border: '1px solid #333', borderRadius: '8px', padding: '12px', minHeight: '80px' }}
            />
          </div>
        </div>
        <button style={{
          marginTop: '20px',
          background: '#fff',
          color: '#000',
          padding: '12px 24px',
          borderRadius: '8px',
          border: 'none',
          fontWeight: '600',
          cursor: 'pointer'
        }}>
          Run Inference
        </button>
      </section>

      {/* Comparison Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '20px' }}>
        <div className="card">
          <h3 style={{ marginBottom: '12px', color: '#888', fontSize: '0.75rem', textTransform: 'uppercase' }}>Base Model</h3>
          <pre style={{ fontSize: '0.875rem', whiteSpace: 'pre-wrap' }}>{responses.base}</pre>
        </div>
        <div className="card" style={{ border: '1px solid #3b82f6' }}>
          <h3 style={{ marginBottom: '12px', color: '#3b82f6', fontSize: '0.75rem', textTransform: 'uppercase' }}>SFT LoRA</h3>
          <pre style={{ fontSize: '0.875rem', whiteSpace: 'pre-wrap' }}>{responses.sft}</pre>
        </div>
        <div className="card" style={{ border: '1px solid #10b981' }}>
          <h3 style={{ marginBottom: '12px', color: '#10b981', fontSize: '0.75rem', textTransform: 'uppercase' }}>DPO Optimized</h3>
          <pre style={{ fontSize: '0.875rem', whiteSpace: 'pre-wrap' }}>{responses.dpo}</pre>
        </div>
      </div>
    </div>
  )
}

export default App
