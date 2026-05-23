import { useRef, useState } from 'react';
import { Image as ImageIcon, X, CheckCircle2, Layers } from 'lucide-react';

/* ── Combo Flow definitions (mirrors backend) ───────────────────────────── */
export const COMBO_FLOWS = {
  bridal_trio: {
    label: 'Bridal Trio',
    tagline: 'Ring · Earring · Necklace',
    description: 'The complete bridal jewelry set — ring, earring, and necklace generated together as a matched campaign.',
    pieces: ['ring', 'earring', 'necklace'],
    emojis: ['💍', '✨', '📿'],
    accent: '#c9971c',
    accentSoft: '#fffbf0',
    accentBorder: '#e9c35c',
  },
  classic_set: {
    label: 'Classic Set',
    tagline: 'Necklace · Bracelet · Earring',
    description: 'A timeless jewelry trio — necklace, bracelet, and earring composed into a unified editorial campaign.',
    pieces: ['necklace', 'bracelet', 'earring'],
    emojis: ['📿', '💎', '✨'],
    accent: '#8b5cf6',
    accentSoft: '#f5f3ff',
    accentBorder: '#c4b5fd',
  },
};

const PIECE_LABELS = {
  ring:      'Ring',
  earring:   'Earring',
  necklace:  'Necklace',
  bracelet:  'Bracelet',
};

const s = {
  label: {
    fontSize: 10, fontWeight: 700, letterSpacing: '0.16em',
    color: '#8a6010', textTransform: 'uppercase', display: 'block', marginBottom: 10,
  },
};

/* ── Main Component ─────────────────────────────────────────────────────── */
export default function ComboPanel({
  selectedFlow, setSelectedFlow,
  comboFiles, setComboFiles,
  comboPreviews, setComboPreviews,
  productName, setProductName,
  loading, error,
  onGenerate,
}) {
  const flow = selectedFlow ? COMBO_FLOWS[selectedFlow] : null;

  const handleFlowSelect = (flowId) => {
    setSelectedFlow(flowId);
    setComboFiles([null, null, null]);
    setComboPreviews([null, null, null]);
  };

  const handleFileSelect = (index, file) => {
    if (!file || !file.type.startsWith('image/')) return;
    const newFiles = [...comboFiles];
    const newPreviews = [...comboPreviews];
    // revoke old blob URL
    if (newPreviews[index]) URL.revokeObjectURL(newPreviews[index]);
    newFiles[index] = file;
    newPreviews[index] = URL.createObjectURL(file);
    setComboFiles(newFiles);
    setComboPreviews(newPreviews);
  };

  const handleFileClear = (index) => {
    const newFiles = [...comboFiles];
    const newPreviews = [...comboPreviews];
    if (newPreviews[index]) URL.revokeObjectURL(newPreviews[index]);
    newFiles[index] = null;
    newPreviews[index] = null;
    setComboFiles(newFiles);
    setComboPreviews(newPreviews);
  };

  const allUploaded = flow && flow.pieces.every((_, i) => !!comboFiles[i]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>

      {/* ── Product ID ── */}
      <div style={{ padding: '24px 24px 0', marginBottom: 20 }}>
        <label style={s.label}>Output Folder / Product ID</label>
        <input
          id="combo-product-name-input"
          type="text"
          placeholder="e.g., BridalSet_Spring2026"
          value={productName}
          onChange={e => setProductName(e.target.value)}
          className="input-light"
          style={{ width: '100%', padding: '11px 14px', borderRadius: 10, fontSize: 13 }}
        />
      </div>

      <div className="divider" />

      {/* ── Flow Selector ── */}
      <div style={{ padding: '20px 24px 0' }}>
        <label style={s.label}>Select Combo Flow</label>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {Object.entries(COMBO_FLOWS).map(([flowId, flowDef]) => {
            const isActive = selectedFlow === flowId;
            return (
              <button
                key={flowId}
                id={`combo-flow-${flowId}`}
                onClick={() => handleFlowSelect(flowId)}
                style={{
                  display: 'flex', alignItems: 'flex-start', gap: 12,
                  padding: '14px 16px', borderRadius: 12, textAlign: 'left',
                  cursor: 'pointer', transition: 'all 0.2s ease',
                  background: isActive ? flowDef.accentSoft : '#ffffff',
                  border: `1.5px solid ${isActive ? flowDef.accentBorder : '#e8e3dc'}`,
                  boxShadow: isActive ? `0 2px 12px ${flowDef.accent}18` : 'none',
                }}
              >
                {/* Emoji stack */}
                <div style={{
                  display: 'flex', gap: 2, fontSize: 18, flexShrink: 0, paddingTop: 1,
                }}>
                  {flowDef.emojis.map((em, i) => (
                    <span key={i}>{em}</span>
                  ))}
                </div>

                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <span style={{
                      fontSize: 13, fontWeight: 700, color: isActive ? flowDef.accent : '#1a1714',
                    }}>
                      {flowDef.label}
                    </span>
                    {isActive && (
                      <CheckCircle2 size={16} style={{ color: flowDef.accent, flexShrink: 0 }} />
                    )}
                  </div>
                  <div style={{ fontSize: 11, color: '#8a8275', marginTop: 2, fontWeight: 600 }}>
                    {flowDef.tagline}
                  </div>
                  <div style={{ fontSize: 10, color: '#b0a898', marginTop: 4, lineHeight: 1.4 }}>
                    {flowDef.description}
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      <div className="divider" style={{ marginTop: 20 }} />

      {/* ── Per-piece Upload Zones ── */}
      {flow ? (
        <div style={{ padding: '20px 24px 0' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 14 }}>
            <label style={{ ...s.label, marginBottom: 0 }}>Reference Images</label>
            <span style={{
              fontSize: 10, color: allUploaded ? '#16a34a' : '#c9971c', fontWeight: 700,
            }}>
              {comboFiles.filter(Boolean).length}/{flow.pieces.length} uploaded
            </span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {flow.pieces.map((category, i) => (
              <PieceUploadSlot
                key={`${selectedFlow}-${i}`}
                index={i}
                emoji={flow.emojis[i]}
                label={PIECE_LABELS[category] || category}
                preview={comboPreviews[i]}
                accent={flow.accent}
                onSelect={(file) => handleFileSelect(i, file)}
                onClear={() => handleFileClear(i)}
              />
            ))}
          </div>
        </div>
      ) : (
        <div style={{ padding: '20px 24px', textAlign: 'center' }}>
          <div style={{
            width: 48, height: 48, borderRadius: 12,
            background: '#f5f3f0', border: '1px solid #e8e3dc',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            margin: '0 auto 12px',
          }}>
            <Layers size={22} style={{ color: '#b8b0a2' }} />
          </div>
          <p style={{ fontSize: 12, color: '#8a8275', fontWeight: 500, lineHeight: 1.5 }}>
            Select a combo flow above to<br />upload your reference images.
          </p>
        </div>
      )}

      <div className="divider" style={{ marginTop: 20 }} />

      {/* ── Generate Button ── */}
      <div style={{ padding: '20px 24px 24px' }}>
        {error && (
          <div style={{
            display: 'flex', alignItems: 'flex-start', gap: 10,
            padding: '10px 14px', borderRadius: 10,
            background: '#fef2f2', border: '1px solid #fecaca', marginBottom: 14,
          }}>
            <X size={14} style={{ color: '#dc2626', flexShrink: 0, marginTop: 1 }} />
            <p style={{ fontSize: 11, color: '#b91c1c', lineHeight: 1.5, fontWeight: 500 }}>{error}</p>
          </div>
        )}
        <button
          id="combo-generate-btn"
          onClick={onGenerate}
          disabled={!allUploaded || loading}
          className="btn-gold"
          style={{ width: '100%', padding: '14px', borderRadius: 12, fontSize: 12, textTransform: 'uppercase' }}
        >
          {loading
            ? <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8 }}>
                <Spinner /> Generating All Pieces…
              </span>
            : `✦ Generate ${flow ? flow.label : 'Combo'}`
          }
        </button>
        {flow && (
          <p style={{ fontSize: 10, color: '#b0a898', textAlign: 'center', marginTop: 8, lineHeight: 1.5 }}>
            {flow.pieces.length} jewelry pieces × 4 shots each = ~{flow.pieces.length * 4} total images
          </p>
        )}
      </div>
    </div>
  );
}

/* ── Per-piece Upload Slot ───────────────────────────────────────────────── */
function PieceUploadSlot({ index, emoji, label, preview, accent, onSelect, onClear }) {
  const fileInputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) onSelect(file);
  };

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
      {/* Piece label */}
      <div style={{
        width: 36, height: 36, borderRadius: 10, flexShrink: 0,
        background: preview ? '#fffbf0' : '#f5f3f0',
        border: `1.5px solid ${preview ? accent : '#e8e3dc'}`,
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
      }}>
        <span style={{ fontSize: 16 }}>{emoji}</span>
      </div>

      {/* Drop zone */}
      <div
        onDragOver={e => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        onClick={!preview ? () => fileInputRef.current?.click() : undefined}
        style={{
          flex: 1, borderRadius: 10, overflow: 'hidden', position: 'relative',
          border: `1.5px ${isDragging ? 'solid' : 'dashed'} ${preview ? accent : isDragging ? accent : '#ccc8be'}`,
          background: isDragging ? '#fffbf0' : preview ? '#faf8f4' : '#ffffff',
          cursor: preview ? 'default' : 'pointer',
          transition: 'all 0.18s ease',
          minHeight: 52,
          display: 'flex', alignItems: 'center',
        }}
      >
        {preview ? (
          <>
            {/* Thumbnail */}
            <img
              src={preview}
              alt={label}
              style={{ width: 52, height: 52, objectFit: 'cover', flexShrink: 0 }}
            />
            <div style={{ flex: 1, padding: '0 10px' }}>
              <p style={{ fontSize: 11, fontWeight: 700, color: '#3a342f' }}>{label}</p>
              <p style={{ fontSize: 10, color: '#16a34a', marginTop: 2 }}>✓ Image ready</p>
            </div>
            {/* Change + Clear */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 4, paddingRight: 8 }}>
              <button
                onClick={() => fileInputRef.current?.click()}
                title="Replace image"
                style={{
                  background: 'none', border: '1px solid #ddd8ce', borderRadius: 6,
                  cursor: 'pointer', padding: '3px 7px', fontSize: 9, color: '#6b6258', fontWeight: 700,
                }}
              >
                Change
              </button>
              <button
                onClick={e => { e.stopPropagation(); onClear(); }}
                title="Remove image"
                style={{
                  background: 'none', border: '1px solid #fecaca', borderRadius: 6,
                  cursor: 'pointer', padding: '3px 7px', fontSize: 9, color: '#dc2626', fontWeight: 700,
                }}
              >
                Clear
              </button>
            </div>
          </>
        ) : (
          <div style={{ width: '100%', display: 'flex', alignItems: 'center', gap: 10, padding: '10px 14px' }}>
            <ImageIcon size={18} style={{ color: '#c9971c', flexShrink: 0 }} />
            <div>
              <p style={{ fontSize: 11, fontWeight: 700, color: '#3a342f' }}>{label} Reference</p>
              <p style={{ fontSize: 10, color: '#8a8275', marginTop: 1 }}>
                {isDragging ? 'Drop here…' : 'Click or drag & drop image'}
              </p>
            </div>
          </div>
        )}
      </div>

      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        style={{ display: 'none' }}
        onChange={e => onSelect(e.target.files[0])}
      />
    </div>
  );
}

function Spinner() {
  return (
    <svg width="14" height="14" viewBox="0 0 14 14" style={{ animation: 'spin 0.8s linear infinite' }}>
      <circle cx="7" cy="7" r="5.5" fill="none" stroke="rgba(255,255,255,0.3)" strokeWidth="1.5" />
      <path d="M7 1.5 A5.5 5.5 0 0 1 12.5 7" fill="none" stroke="#ffffff" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  );
}
