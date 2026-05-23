import { useState, useEffect } from 'react';
import Header from './components/Header';
import ConfigPanel from './components/ConfigPanel';
import ResultsPanel from './components/ResultsPanel';
import ComboPanel, { COMBO_FLOWS } from './components/ComboPanel';
import ComboResultsPanel from './components/ComboResultsPanel';
import {
  fetchCategories,
  generateImages,
  startBulkGeneration,
  getBulkStatus,
  generateCombo,
} from './api';

export default function App() {
  const [mode, setMode] = useState('single');
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [category, setCategory] = useState('ring');
  const [productName, setProductName] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [bulkUrl, setBulkUrl] = useState('');
  const [bulkJobId, setBulkJobId] = useState(null);
  const [bulkStatus, setBulkStatus] = useState(null);
  const [availableCategories, setAvailableCategories] = useState({});
  const [socialScenes, setSocialScenes] = useState([]);
  const [categoriesError, setCategoriesError] = useState(false);
  const [selectedAngles, setSelectedAngles] = useState([]);
  const [lastSessionId, setLastSessionId] = useState(null); // tracks server-returned session_id for ZIP download

  // ── Combo flow state ─────────────────────────────────────────────────────
  const [selectedFlow, setSelectedFlow] = useState(null);        // 'bridal_trio' | 'classic_set'
  const [comboFiles, setComboFiles] = useState([null, null, null]);     // one File per piece
  const [comboPreviews, setComboPreviews] = useState([null, null, null]); // blob URLs
  const [comboResults, setComboResults] = useState(null);

  /* ── Fetch categories on mount ── */
  useEffect(() => {
    fetchCategories()
      .then(data => {
        setAvailableCategories(data.categories || {});
        setSocialScenes(data.social_scenes || []);
        setCategoriesError(false);
      })
      .catch(err => {
        console.error('Failed to load categories', err);
        setCategoriesError(true);
      });
  }, []);

  /* ── Revoke preview blob URLs ── */
  useEffect(() => () => { if (preview) URL.revokeObjectURL(preview); }, [preview]);

  /* ── Bulk polling ── */
  useEffect(() => {
    if (!bulkJobId || bulkStatus === 'completed' || bulkStatus === 'failed') return;
    const id = setInterval(async () => {
      try {
        const data = await getBulkStatus(bulkJobId);
        setBulkStatus(data.status);
        setResults(data);
        if (data.status === 'completed' || data.status === 'failed') {
          setLoading(false);
          clearInterval(id);
        }
      } catch { /* network hiccup — keep polling */ }
    }, 3000);
    return () => clearInterval(id);
  }, [bulkJobId, bulkStatus]);

  /* ── Mode change: reset state ── */
  const handleModeChange = newMode => {
    setMode(newMode);
    setFile(null);
    setPreview(null);
    setResults(null);
    setError(null);
    setSelectedAngles([]);
    setBulkUrl('');
    setBulkJobId(null);
    setBulkStatus(null);
    setLastSessionId(null);
    // Reset combo state
    setSelectedFlow(null);
    setComboFiles([null, null, null]);
    setComboPreviews([null, null, null]);
    setComboResults(null);
  };

  /* ── File select ── */
  const handleFileSelect = selectedFile => {
    if (!selectedFile) return;
    setError(null);
    setResults(null);
    if (mode === 'bulk') {
      if (/\.(xlsx|xls|csv)$/.test(selectedFile.name)) {
        setFile(selectedFile); setPreview(null);
        setBulkJobId(null);
      } else {
        setError('Please select a valid Excel or CSV file (.xlsx, .xls, .csv).');
      }
    } else {
      if (selectedFile.type.startsWith('image/')) {
        setFile(selectedFile);
        setPreview(URL.createObjectURL(selectedFile));
      } else {
        setError('Please select a valid image file (JPG, PNG, WEBP).');
      }
    }
  };

  /* ── File clear ── */
  const handleFileClear = () => {
    setFile(null);
    setPreview(null);
    setResults(null);
    setError(null);
  };

  /* ── Toggle shot angle ── */
  const toggleAngle = key => {
    setSelectedAngles(prev =>
      prev.includes(key) ? prev.filter(k => k !== key) : [...prev, key]
    );
  };

  /* ── Generate ── */
  const handleGenerate = async () => {
    const canGenerate = mode === 'bulk' ? (file || bulkUrl.trim()) : !!file;
    if (!canGenerate) {
      setError(
        mode === 'bulk'
          ? 'Please upload an Excel file or provide a Google Sheets URL.'
          : 'Please upload a reference image.'
      );
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      if (mode === 'bulk') {
        setBulkStatus('starting');
        const data = await startBulkGeneration({
          category,
          file: file || null,
          url: bulkUrl.trim() || null,
        });
        if (data.status === 'success') {
          setBulkJobId(data.job_id);
        } else {
          setError('Bulk generation failed to start.');
          setLoading(false);
        }
      } else {
        const data = await generateImages({
          category,
          file,
          productId:     productName.trim() || undefined,
          selectedShots: selectedAngles,
          mode:          mode === 'social' ? 'social' : 'standard',
        });
        if (data.status === 'success') {
          setResults(data.images);
          setLastSessionId(data.session_id); // save real folder name for ZIP
        } else {
          setError('Generation failed. Please try again.');
        }
        setLoading(false);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred during generation.');
      setLoading(false);
    }
  };

  /* ── Combo Generate ── */
  const handleComboGenerate = async () => {
    if (!selectedFlow) {
      setError('Please select a combo flow first.');
      return;
    }
    const flow = COMBO_FLOWS[selectedFlow];
    const allUploaded = flow.pieces.every((_, i) => !!comboFiles[i]);
    if (!allUploaded) {
      setError('Please upload a reference image for every piece in the combo.');
      return;
    }
    setLoading(true);
    setError(null);
    setComboResults(null);
    try {
      const data = await generateCombo({
        flowId:    selectedFlow,
        productId: productName.trim() || undefined,
        files:     comboFiles,
      });
      if (data.status === 'success') {
        setComboResults(data);
      } else {
        setError('Combo generation failed. Please try again.');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred during combo generation.');
    } finally {
      setLoading(false);
    }
  };


  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', position: 'relative', overflow: 'hidden' }}>

      {/* ── Background Elements ── */}
      <div aria-hidden="true" style={{ position: 'fixed', inset: 0, pointerEvents: 'none', zIndex: 0, overflow: 'hidden', background: '#f8f6f2' }}>
         <div style={{ position: 'absolute', top: '-10%', left: '-5%', width: '60%', height: '60%', background: 'radial-gradient(circle, rgba(201,151,28,0.04) 0%, transparent 65%)', borderRadius: '50%', animation: 'orb-drift 18s ease-in-out infinite' }} />
         <div style={{ position: 'absolute', bottom: '-20%', right: '-10%', width: '50%', height: '50%', background: 'radial-gradient(circle, rgba(212,168,42,0.03) 0%, transparent 70%)', borderRadius: '50%', animation: 'orb-drift 24s ease-in-out infinite reverse' }} />
      </div>

      {/* ── Header ── */}
      <Header mode={mode} onModeChange={handleModeChange} />

      {/* ── Main Layout ── */}
      <div style={{ flex: 1, display: 'flex', position: 'relative', zIndex: 1, overflow: 'hidden' }}>

        {/* ── Left Sidebar / Config ── */}
        <aside className="sidebar thin-scroll" style={{
          width: 340,
          flexShrink: 0,
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column',
        }}>
          {/* Sidebar header */}
          <div style={{ padding: '20px 24px 16px', borderBottom: '1px solid #ede9e1', background: '#faf8f4' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <div className="dot-gold" />
              <span style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.2em', color: '#8a8275', textTransform: 'uppercase' }}>Configuration</span>
            </div>
          </div>

          {mode === 'combo' ? (
            <ComboPanel
              selectedFlow={selectedFlow}
              setSelectedFlow={setSelectedFlow}
              comboFiles={comboFiles}
              setComboFiles={setComboFiles}
              comboPreviews={comboPreviews}
              setComboPreviews={setComboPreviews}
              productName={productName}
              setProductName={setProductName}
              loading={loading}
              error={error}
              onGenerate={handleComboGenerate}
            />
          ) : (
            <ConfigPanel
              mode={mode}
              file={file}
              preview={preview}
              isDragging={isDragging}
              setIsDragging={setIsDragging}
              category={category}
              setCategory={cat => { setCategory(cat); setSelectedAngles([]); }}
              productName={productName}
              setProductName={setProductName}
              bulkUrl={bulkUrl}
              setBulkUrl={setBulkUrl}
              selectedAngles={selectedAngles}
              toggleAngle={toggleAngle}
              availableCategories={availableCategories}
              socialScenes={socialScenes}
              categoriesError={categoriesError}
              loading={loading}
              error={error}
              onGenerate={handleGenerate}
              onFileSelect={handleFileSelect}
              onFileClear={handleFileClear}
            />
          )}

          {/* Sidebar footer info */}
          <div style={{ marginTop: 'auto', padding: '16px 24px', borderTop: '1px solid #ede9e1', background: '#faf8f4' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              <FeatureTile icon="🔒" text="Design-locked fidelity" sub="Identical stone & metal rendering" />
              <FeatureTile icon="🎯" text="Editorial quality" sub="Cartier / Bvlgari standard" />
              <FeatureTile icon="⚡" text="Gemini 2.5 Flash" sub="Next-gen image generation" />
            </div>
          </div>
        </aside>

        {/* ── Right Panel / Results ── */}
        <main style={{ flex: 1, overflow: 'auto', padding: '28px 32px', display: 'flex', flexDirection: 'column' }} className="thin-scroll">
          {/* Results panel header context */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 24 }}>
            <div>
              <h2 style={{ fontFamily: 'Cormorant Garamond, serif', fontSize: 34, fontWeight: 500, color: '#1a1714', letterSpacing: '0.02em', lineHeight: 1.2 }}>
                {mode === 'single' ? 'Studio Output' : mode === 'social' ? 'Editorial Suite' : mode === 'combo' ? 'Combo Campaign' : 'Batch Export'}
              </h2>
              <p style={{ fontSize: 13, color: '#6b6258', marginTop: 4 }}>
                {mode === 'single' && 'Multi-angle product & model photography'}
                {mode === 'social' && 'Lifestyle & editorial creative scenes'}
                {mode === 'combo' && 'Multi-piece matched jewelry campaign'}
                {mode === 'bulk'  && 'Automated batch processing from spreadsheet'}
              </p>
            </div>
            <ModeInfoBadge mode={mode} />
          </div>

          <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            {mode === 'combo' ? (
              <ComboResultsPanel
                loading={loading}
                results={comboResults}
                flowLabel={selectedFlow ? COMBO_FLOWS[selectedFlow]?.label : ''}
              />
            ) : (
              <ResultsPanel
                mode={mode}
                loading={loading}
                results={results}
                bulkStatus={bulkStatus}
                sessionId={lastSessionId}
                bulkJobId={bulkJobId}
              />
            )}
          </div>
        </main>
      </div>

      {/* ── Footer ── */}
      <footer style={{ position: 'relative', zIndex: 10, background: '#ffffff', borderTop: '1px solid #ede9e1', padding: '14px 32px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span style={{ fontSize: 10, color: '#8a8275', letterSpacing: '0.14em', fontWeight: 600 }}>
          © 2026 RIOLLS LUXURY SYSTEMS · AI PHOTOGRAPHY ENGINE
        </span>
        <div style={{ display: 'flex', gap: 20 }}>
          {['GDPR COMPLIANT', 'ISO 27001', 'ENTERPRISE GRADE'].map(tag => (
            <span key={tag} style={{ fontSize: 9, color: '#b8b0a2', letterSpacing: '0.16em', fontWeight: 700 }}>{tag}</span>
          ))}
        </div>
      </footer>
    </div>
  );
}

function FeatureTile({ icon, text, sub }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
      <div style={{ width: 32, height: 32, borderRadius: 8, background: '#fffbf0', border: '1px solid #e9c35c', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 14, flexShrink: 0 }}>
        {icon}
      </div>
      <div>
        <p style={{ fontSize: 11, fontWeight: 700, color: '#3a342f' }}>{text}</p>
        <p style={{ fontSize: 10, color: '#8a8275', marginTop: 1 }}>{sub}</p>
      </div>
    </div>
  );
}

function ModeInfoBadge({ mode }) {
  const info = {
    single: { color: '#c9971c', label: 'STUDIO MODE',  sub: 'Up to 11 product angles + model shots' },
    social: { color: '#8b5cf6', label: 'CREATIVE MODE', sub: '30+ backgrounds & lifestyle scenes' },
    combo:  { color: '#e85d9c', label: 'COMBO MODE',   sub: 'Bridal Trio · Classic Set campaigns' },
    bulk:   { color: '#16a34a', label: 'BULK MODE',    sub: 'Excel / Google Sheets batch processing' },
  }[mode] || { color: '#c9971c', label: 'MODE', sub: '' };

  return (
    <div style={{ textAlign: 'right' }}>
      <div style={{ fontSize: 9, fontWeight: 800, letterSpacing: '0.2em', color: info.color, marginBottom: 3 }}>{info.label}</div>
      <div style={{ fontSize: 11, color: '#6b6258' }}>{info.sub}</div>
    </div>
  );
}
