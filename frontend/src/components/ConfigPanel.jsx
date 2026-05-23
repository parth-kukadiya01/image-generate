import { useRef } from 'react';
import { UploadCloud, Image as ImageIcon, FileSpreadsheet, CheckCircle2, X, Link2 } from 'lucide-react';

const CATEGORIES = [
  { id: 'ring', label: 'Ring', emoji: '💍' },
  { id: 'necklace', label: 'Necklace', emoji: '📿' },
  { id: 'bracelet', label: 'Bracelet', emoji: '💎' },
  { id: 'earring', label: 'Earring', emoji: '✨' },
  { id: 'pendant', label: 'Pendant', emoji: '🔮' },
  { id: 'bangle', label: 'Bangle', emoji: '⭕' },
  { id: 'anklet', label: 'Anklet', emoji: '⛓️' },
  { id: 'brooch', label: 'Brooch', emoji: '🏵️' },
];

const s = {
  label: { fontSize: 10, fontWeight: 700, letterSpacing: '0.16em', color: '#8a6010', textTransform: 'uppercase', display: 'block', marginBottom: 10 },
  section: { marginBottom: 28 },
};

export default function ConfigPanel({
  mode, file, preview, isDragging, setIsDragging,
  category, setCategory, productName, setProductName,
  bulkUrl, setBulkUrl, selectedAngles, toggleAngle,
  availableCategories, socialScenes, categoriesError,
  loading, error, onGenerate, onFileSelect, onFileClear,
}) {
  const fileInputRef = useRef(null);

  const handleDrop = e => {
    e.preventDefault(); setIsDragging(false);
    if (e.dataTransfer.files?.[0]) onFileSelect(e.dataTransfer.files[0]);
  };

  const isShotsLoading = !socialScenes.length && !Object.keys(availableCategories).length && !categoriesError;

  const shots = mode === 'social'
    ? socialScenes
    : mode === 'single' && availableCategories[category]
      ? [
          ...(availableCategories[category]?.product || []).map(s => ({ ...s, group: 'Product Angle' })),
          ...(availableCategories[category]?.model || []).map(s => ({ ...s, group: 'Model Shot' }))
        ]
      : [];

  const canGenerate = mode === 'bulk' ? (file || bulkUrl.trim()) : !!file;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
      {/* ── Upload Section ── */}
      <div style={{ ...s.section, padding: '24px 24px 0' }}>
        {mode !== 'bulk' && (
          <div style={{ marginBottom: 18 }}>
            <label style={s.label}>Output Folder / Product ID</label>
            <input
              id="product-name-input"
              type="text"
              placeholder="e.g., Summer_Ring_01"
              value={productName}
              onChange={e => setProductName(e.target.value)}
              className="input-light"
              style={{ width: '100%', padding: '11px 14px', borderRadius: 10, fontSize: 13 }}
            />
          </div>
        )}

        <label style={s.label}>{mode === 'bulk' ? 'Data Source' : 'Reference Image'}</label>

        {mode === 'bulk' ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            <div style={{ position: 'relative' }}>
              <Link2 size={15} style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: '#b8b0a2' }} />
              <input
                id="bulk-url-input"
                type="url"
                placeholder="Google Sheets public URL..."
                value={bulkUrl}
                onChange={e => { setBulkUrl(e.target.value); onFileClear(); }}
                className="input-light"
                style={{ width: '100%', padding: '11px 14px 11px 36px', borderRadius: 10, fontSize: 13 }}
              />
            </div>
            <div style={{ textAlign: 'center', fontSize: 10, color: '#b8b0a2', letterSpacing: '0.12em', fontWeight: 600 }}>— OR UPLOAD FILE —</div>
            <BulkDropZone file={file} isDragging={isDragging} setIsDragging={setIsDragging}
              onDrop={handleDrop} onClick={() => fileInputRef.current?.click()} onClear={onFileClear} />
            <input ref={fileInputRef} type="file" accept=".xlsx,.xls,.csv" style={{ display: 'none' }}
              onChange={e => { onFileSelect(e.target.files[0]); setBulkUrl(''); }} />
          </div>
        ) : (
          <>
            <ImageDropZone preview={preview} isDragging={isDragging} setIsDragging={setIsDragging}
              onDrop={handleDrop} onClick={() => fileInputRef.current?.click()} onClear={onFileClear} />
            <input ref={fileInputRef} type="file" accept="image/*" style={{ display: 'none' }}
              onChange={e => onFileSelect(e.target.files[0])} />
          </>
        )}
      </div>

      <div className="divider" />

      {/* ── Category ── */}
      <div style={{ ...s.section, padding: '20px 24px 0' }}>
        <label style={s.label}>Product Category</label>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
          {CATEGORIES.map(cat => {
            const active = category === cat.id;
            return (
              <button
                key={cat.id}
                id={`cat-${cat.id}`}
                onClick={() => { setCategory(cat.id); }}
                className={`cat-chip ${active ? 'active' : ''}`}
                style={{
                  display: 'flex', alignItems: 'center', gap: 8,
                  padding: '9px 12px', borderRadius: 10, fontSize: 12, fontWeight: 600,
                }}
              >
                <span style={{ fontSize: 16 }}>{cat.emoji}</span>
                {cat.label}
                {active && <div className="dot-gold" style={{ marginLeft: 'auto' }} />}
              </button>
            );
          })}
        </div>
      </div>

      <div className="divider" />

      {/* ── Shots / Angles / Backgrounds ── */}
      {mode !== 'bulk' && (
        <>
          <div style={{ padding: '20px 24px 0' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 10 }}>
              <label style={{ ...s.label, marginBottom: 0 }}>
                {mode === 'social' ? 'Background & Scene' : 'Angle & Perspective'}
              </label>
              <span style={{ fontSize: 10, color: selectedAngles.length ? '#c9971c' : '#8a6010', fontWeight: 700 }}>
                {selectedAngles.length ? `${selectedAngles.length} selected` : 'Auto (4 best)'}
              </span>
            </div>
            
            {isShotsLoading ? (
              <div style={{ padding: '30px 0', textAlign: 'center' }}>
                <Spinner color="#c9971c" />
                <p style={{ fontSize: 11, color: '#8a8275', marginTop: 10, fontWeight: 500 }}>Fetching studio options...</p>
              </div>
            ) : categoriesError ? (
              <div style={{ padding: '20px', textAlign: 'center', background: '#fef2f2', borderRadius: 12, border: '1px solid #fecaca' }}>
                <X size={18} style={{ color: '#dc2626', marginBottom: 8 }} />
                <p style={{ fontSize: 11, color: '#b91c1c', fontWeight: 600, marginBottom: 10 }}>Failed to load configuration</p>
                <button 
                  onClick={() => window.location.reload()}
                  style={{ fontSize: 10, padding: '5px 12px', borderRadius: 6, background: '#ffffff', border: '1px solid #fecaca', color: '#dc2626', cursor: 'pointer', fontWeight: 700 }}
                >
                  RETRY
                </button>
              </div>
            ) : shots.length > 0 ? (
              <>
                <p style={{ fontSize: 11, color: '#8a6010', marginBottom: 12, lineHeight: 1.5, opacity: 0.8 }}>
                  {mode === 'social' 
                    ? 'Select creative backgrounds for your editorial shoot.'
                    : 'Select specific product or model angles, or leave empty for AI selection.'}
                </p>
                <div className="thin-scroll" style={{ maxHeight: 280, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 5, paddingRight: 4 }}>
                  {shots.map((shot, idx) => {
                    const active = selectedAngles.includes(shot.key);
                    const showGroup = idx === 0 || shots[idx-1].group !== shot.group;
                    
                    return (
                      <div key={shot.key}>
                        {mode === 'single' && shot.group && showGroup && (
                          <div style={{ fontSize: 9, fontWeight: 800, color: '#b8b0a2', letterSpacing: '0.1em', padding: '10px 0 6px', textTransform: 'uppercase' }}>
                            {shot.group}s
                          </div>
                        )}
                        <div
                          onClick={() => toggleAngle(shot.key)}
                          className={`angle-row ${active ? 'selected' : ''}`}
                          style={{
                            display: 'flex', alignItems: 'center', gap: 10,
                            padding: '8px 12px', borderRadius: 8,
                          }}
                        >
                          <div style={{
                            width: 16, height: 16, borderRadius: 4, flexShrink: 0,
                            background: active ? '#c9971c' : '#ffffff',
                            border: active ? 'none' : '1px solid #ccc8be',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                          }}>
                            {active && <CheckCircle2 size={12} color="#ffffff" strokeWidth={3} />}
                          </div>
                          <span style={{ fontSize: 11, color: active ? '#8a6010' : '#4a443e', fontWeight: active ? 600 : 500, flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                            {shot.label}
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </>
            ) : (
              <div style={{ padding: '20px 0', textAlign: 'center', background: '#fef2f2', borderRadius: 10, border: '1px solid #fecaca' }}>
                <p style={{ fontSize: 11, color: '#b91c1c' }}>No options available for this category.</p>
              </div>
            )}
          </div>
          <div className="divider" style={{ marginTop: 24 }} />
        </>
      )}

      {/* ── Generate Button ── */}
      <div style={{ padding: '20px 24px 24px' }}>
        {error && (
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: 10, padding: '10px 14px', borderRadius: 10, background: '#fef2f2', border: '1px solid #fecaca', marginBottom: 14 }}>
            <X size={14} style={{ color: '#dc2626', flexShrink: 0, marginTop: 1 }} />
            <p style={{ fontSize: 11, color: '#b91c1c', lineHeight: 1.5, fontWeight: 500 }}>{error}</p>
          </div>
        )}
        <button
          id="generate-btn"
          onClick={onGenerate}
          disabled={!canGenerate || loading}
          className="btn-gold"
          style={{ width: '100%', padding: '14px', borderRadius: 12, fontSize: 12, textTransform: 'uppercase' }}
        >
          {loading
            ? <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8 }}>
              <Spinner /> {mode === 'bulk' ? 'Processing...' : 'Generating...'}
            </span>
            : mode === 'bulk' ? '⚡ Run Bulk Export'
              : mode === 'social' ? '✦ Create Editorial'
                : '✦ Generate Campaign'
          }
        </button>
      </div>
    </div>
  );
}

function ImageDropZone({ preview, isDragging, setIsDragging, onDrop, onClick, onClear }) {
  return (
    <div
      onDragOver={e => { e.preventDefault(); setIsDragging(true); }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={onDrop}
      onClick={!preview ? onClick : undefined}
      className={`drop-zone ${isDragging ? 'dragging' : ''}`}
      style={{ borderRadius: 14, overflow: 'hidden', position: 'relative', aspectRatio: '1/1', cursor: preview ? 'default' : 'pointer' }}
    >
      {preview ? (
        <>
          <img src={preview} alt="Reference" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
          <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(180deg,transparent 50%,rgba(26,23,20,0.8) 100%)' }} />
          <button onClick={e => { e.stopPropagation(); onClear(); }}
            style={{ position: 'absolute', top: 10, right: 10, width: 28, height: 28, borderRadius: '50%', background: 'rgba(255,255,255,0.9)', border: '1px solid #ede9e1', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
            <X size={13} color="#1a1714" />
          </button>
          <button onClick={onClick}
            style={{ position: 'absolute', bottom: 10, left: '50%', transform: 'translateX(-50%)', padding: '6px 14px', borderRadius: 20, background: 'rgba(255,255,255,0.95)', border: '1px solid #ede9e1', cursor: 'pointer', fontSize: 10, color: '#1a1714', fontWeight: 600, letterSpacing: '0.1em', whiteSpace: 'nowrap', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
            Replace Image
          </button>
        </>
      ) : (
        <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 12 }}>
          <div style={{ width: 52, height: 52, borderRadius: 14, background: '#fffbf0', border: '1px solid #e9c35c', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <ImageIcon size={24} style={{ color: '#c9971c' }} />
          </div>
          <div style={{ textAlign: 'center' }}>
            <p style={{ fontSize: 13, fontWeight: 600, color: '#3a342f', marginBottom: 4 }}>Upload Reference Photo</p>
            <p style={{ fontSize: 11, color: '#8a8275' }}>Drag & drop or click to browse</p>
          </div>
          <div style={{ display: 'flex', gap: 6 }}>
            {['JPG', 'PNG', 'WEBP'].map(f => (
              <span key={f} style={{ padding: '2px 8px', borderRadius: 99, background: '#ffffff', border: '1px solid #ddd8ce', fontSize: 9, color: '#6b6258', fontWeight: 700, letterSpacing: '0.1em' }}>{f}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function BulkDropZone({ file, isDragging, setIsDragging, onDrop, onClick, onClear }) {
  return (
    <div
      onDragOver={e => { e.preventDefault(); setIsDragging(true); }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={onDrop}
      onClick={!file ? onClick : undefined}
      className={`drop-zone ${isDragging ? 'dragging' : ''}`}
      style={{ borderRadius: 12, padding: '20px', textAlign: 'center', cursor: file ? 'default' : 'pointer', position: 'relative' }}
    >
      {file ? (
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <FileSpreadsheet size={20} style={{ color: '#16a34a', flexShrink: 0 }} />
          <span style={{ fontSize: 12, color: '#16a34a', fontWeight: 600, flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{file.name}</span>
          <button onClick={e => { e.stopPropagation(); onClear(); }} style={{ background: 'none', border: 'none', cursor: 'pointer' }}>
            <X size={14} style={{ color: '#8a8275' }} />
          </button>
        </div>
      ) : (
        <>
          <UploadCloud size={22} style={{ color: '#b8b0a2', marginBottom: 6 }} />
          <p style={{ fontSize: 12, color: '#6b6258', fontWeight: 600 }}>Upload Excel / CSV</p>
          <p style={{ fontSize: 10, color: '#8a8275', marginTop: 3 }}>.xlsx · .xls · .csv</p>
        </>
      )}
    </div>
  );
}

function Spinner({ color = '#ffffff' }) {
  return (
    <svg width="14" height="14" viewBox="0 0 14 14" style={{ animation: 'spin 0.8s linear infinite' }}>
      <circle cx="7" cy="7" r="5.5" fill="none" stroke="rgba(0,0,0,0.1)" strokeWidth="1.5" />
      <path d="M7 1.5 A5.5 5.5 0 0 1 12.5 7" fill="none" stroke={color} strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  );
}
