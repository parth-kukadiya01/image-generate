import { Download, CheckCircle2, Loader2, LayoutGrid, Sparkles, AlertTriangle, Archive } from 'lucide-react';
import { downloadSessionZip, downloadBulkZip, API_BASE } from '../api';

/* ── individual image download (unchanged) ── */
const downloadImg = (url, label) => {
  const a = document.createElement('a');
  a.href = `${API_BASE}${url}`;
  a.download = `${label.replace(/[^a-z0-9]/gi, '_')}.jpg`;
  a.target = '_blank';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
};

export default function ResultsPanel({ mode, loading, results, bulkStatus, sessionId, bulkJobId }) {

  const isEmpty = !loading && !results;

  return (
    <div style={{ flex: 1, minHeight: 0, display: 'flex', flexDirection: 'column' }}>

      {/* ── Empty State ── */}
      {isEmpty && <EmptyState />}

      {/* ── Loading State ── */}
      {loading && (!results || (mode === 'single' || mode === 'social')) && <LoadingState mode={mode} />}

      {/* ── Single / Social Results ── */}
      {mode !== 'bulk' && Array.isArray(results) && (
        <div style={{ flex: 1, overflow: 'auto', padding: 0 }} className="thin-scroll">
          <ResultsHeader
            count={results.length}
            onDownloadAll={() => downloadSessionZip(sessionId, sessionId)}
          />
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: 16, padding: '0 0 24px' }}>
            {results.map((img, idx) => (
              <ImageCard key={idx} img={img} idx={idx} />
            ))}
          </div>
        </div>
      )}

      {/* ── Bulk Results ── */}
      {mode === 'bulk' && results?.status && (
        <div style={{ flex: 1, overflow: 'auto' }} className="thin-scroll">
          <BulkResultsPanel results={results} loading={loading} bulkJobId={bulkJobId} />
        </div>
      )}
    </div>
  );
}

function EmptyState() {
  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '60px 24px', textAlign: 'center' }}>
      <div style={{ position: 'relative', marginBottom: 32 }}>
        <div style={{ width: 100, height: 100, borderRadius: 28, background: '#fffbf0', border: '1px solid #e9c35c', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto', boxShadow: '0 4px 20px rgba(201,151,28,0.1)' }}>
          <LayoutGrid size={44} style={{ color: '#c9971c' }} strokeWidth={1} />
        </div>
      </div>
      <h3 style={{ fontFamily: 'Cormorant Garamond, serif', fontSize: 28, fontWeight: 400, color: '#1a1714', marginBottom: 10, letterSpacing: '0.02em' }}>
        Awaiting Your Creation
      </h3>
      <p style={{ fontSize: 13, color: '#6b6258', lineHeight: 1.7, maxWidth: 300 }}>
        Upload a jewelry reference image and configure your shoot. Our AI will craft a premium multi-angle campaign in seconds.
      </p>
      <div style={{ display: 'flex', gap: 24, marginTop: 36 }}>
        {[
          { icon: '📸', label: 'Multi-angle', sub: 'Up to 11 product views' },
          { icon: '👤', label: 'Model shots', sub: 'Editorial lifestyle' },
          { icon: '⚡', label: 'Fast output', sub: 'Under 2 minutes' },
        ].map(f => (
          <div key={f.label} style={{ textAlign: 'center' }}>
            <div style={{ fontSize: 24, marginBottom: 6 }}>{f.icon}</div>
            <div style={{ fontSize: 11, fontWeight: 700, color: '#3a342f', letterSpacing: '0.06em' }}>{f.label}</div>
            <div style={{ fontSize: 10, color: '#8a8275', marginTop: 2 }}>{f.sub}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function LoadingState({ mode }) {
  const steps = ['Analysing reference image...', 'Locking design fingerprint...', 'Crafting lighting & composition...', 'Rendering final imagery...'];
  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: 48 }}>
      {/* Animated ring */}
      <div style={{ position: 'relative', width: 90, height: 90, marginBottom: 36 }}>
        <svg style={{ position: 'absolute', inset: 0, animation: 'spin 1.8s linear infinite' }} viewBox="0 0 90 90">
          <circle cx="45" cy="45" r="38" fill="none" stroke="#ede9e1" strokeWidth="2" />
          <path d="M45 7 A38 38 0 0 1 83 45" fill="none" stroke="#c9971c" strokeWidth="2.5" strokeLinecap="round" />
        </svg>
        <div style={{ position: 'absolute', inset: 14, borderRadius: '50%', background: '#fffbf0', border: '1px solid #e9c35c', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Sparkles size={24} style={{ color: '#c9971c' }} />
        </div>
      </div>

      <h3 style={{ fontFamily: 'Cormorant Garamond, serif', fontSize: 26, fontWeight: 400, color: '#1a1714', marginBottom: 8, letterSpacing: '0.04em' }}>
        {mode === 'bulk' ? 'Processing Batch...' : 'Crafting Your Campaign'}
      </h3>
      <p style={{ fontSize: 12, color: '#6b6258', marginBottom: 32, letterSpacing: '0.06em' }}>
        AI is rendering photorealistic jewelry imagery
      </p>

      {/* Steps */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 10, width: '100%', maxWidth: 320 }}>
        {steps.map((step, i) => (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '8px 12px', borderRadius: 8, background: i === 0 ? '#fffbf0' : '#ffffff', border: `1px solid ${i === 0 ? '#d4a82a' : '#ede9e1'}` }}>
            {i === 0
              ? <Loader2 size={13} style={{ color: '#c9971c', flexShrink: 0, animation: 'spin 1s linear infinite' }} />
              : <div style={{ width: 13, height: 13, borderRadius: '50%', border: '1px solid #ccc8be', flexShrink: 0 }} />
            }
            <span style={{ fontSize: 11, color: i === 0 ? '#9a7015' : '#8a8275', fontWeight: i === 0 ? 600 : 400 }}>{step}</span>
          </div>
        ))}
      </div>

      {/* Progress Bar */}
      <div style={{ width: '100%', maxWidth: 320, height: 3, background: '#ede9e1', borderRadius: 99, overflow: 'hidden', marginTop: 28 }}>
        <div style={{ height: '100%', background: 'linear-gradient(90deg,#c9971c,#d4a82a)', borderRadius: 99, width: '40%', animation: 'progress-indeterminate 2s ease-in-out infinite' }} />
      </div>
    </div>
  );
}

function ResultsHeader({ count, onDownloadAll }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20, paddingBottom: 16, borderBottom: '1px solid #ede9e1' }}>
      <div>
        <h2 style={{ fontFamily: 'Cormorant Garamond, serif', fontSize: 26, fontWeight: 400, color: '#1a1714', marginBottom: 4 }}>Campaign Ready</h2>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <div style={{ width: 6, height: 6, borderRadius: '50%', background: '#16a34a', boxShadow: '0 0 8px rgba(22,163,74,0.4)' }} />
          <span style={{ fontSize: 11, color: '#15803d', fontWeight: 700, letterSpacing: '0.1em' }}>{count} IMAGES GENERATED</span>
        </div>
      </div>
      <button
        id="download-all-btn"
        onClick={onDownloadAll}
        className="btn-outline"
        style={{ display: 'flex', alignItems: 'center', gap: 7, padding: '9px 16px', borderRadius: 10, fontSize: 11, fontWeight: 700, letterSpacing: '0.1em' }}
      >
        <Download size={14} />
        DOWNLOAD ALL
      </button>
    </div>
  );
}

function ImageCard({ img, idx }) {
  return (
    <div className="img-card card-lift" style={{ position: 'relative', aspectRatio: '3/4' }}>
      <img
        src={`${API_BASE}${img.url}`}
        alt={img.label}
        style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }}
        loading="lazy"
      />
      {/* Overlay */}
      <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(180deg, transparent 45%, rgba(26,23,20,0.95) 100%)', pointerEvents: 'none' }} />
      {/* Shot number badge */}
      <div style={{ position: 'absolute', top: 12, left: 12, padding: '3px 9px', borderRadius: 99, background: 'rgba(255,255,255,0.9)', border: '1px solid #ede9e1', fontSize: 9, fontWeight: 800, color: '#8a6010', letterSpacing: '0.14em', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
        {String(idx + 1).padStart(2, '0')}
      </div>
      {/* Label + Download */}
      <div style={{ position: 'absolute', bottom: 0, left: 0, right: 0, padding: '12px 14px', display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', gap: 8 }}>
        <p style={{ fontSize: 11, fontWeight: 600, color: '#f8f6f2', lineHeight: 1.3, flex: 1, overflow: 'hidden', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical' }}>
          {img.label}
        </p>
        <button
          id={`download-img-${idx}`}
          onClick={() => downloadImg(img.url, img.label)}
          style={{ width: 32, height: 32, borderRadius: 8, background: 'rgba(255,255,255,0.95)', border: '1px solid #ede9e1', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', flexShrink: 0, transition: 'all 0.2s', boxShadow: '0 2px 8px rgba(0,0,0,0.15)' }}
          onMouseEnter={e => { e.currentTarget.style.background = '#ffffff'; e.currentTarget.style.borderColor = '#c9971c'; }}
          onMouseLeave={e => { e.currentTarget.style.background = 'rgba(255,255,255,0.95)'; e.currentTarget.style.borderColor = '#ede9e1'; }}
          title="Download image"
        >
          <Download size={14} style={{ color: '#1a1714' }} />
        </button>
      </div>
    </div>
  );
}

function BulkResultsPanel({ results, loading, bulkJobId }) {
  const isCompleted = results.status === 'completed';
  const isFailed = results.status === 'failed';
  const isProcessing = results.status === 'processing';
  
  const statusColor = isCompleted ? '#16a34a' : isFailed ? '#dc2626' : '#d97706';
  const statusBg = isCompleted ? '#f0fdf4' : isFailed ? '#fef2f2' : '#fffbeb';
  const statusBorder = isCompleted ? '#bbf7d0' : isFailed ? '#fecaca' : '#fde68a';

  return (
    <div>
      {/* Status Card */}
      <div className="card" style={{ display: 'flex', alignItems: 'center', gap: 16, padding: '16px 20px', borderRadius: 14, marginBottom: 20 }}>
        <div style={{ width: 44, height: 44, borderRadius: 12, background: statusBg, border: `1px solid ${statusBorder}`, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
          {isProcessing
            ? <Loader2 size={22} style={{ color: statusColor, animation: 'spin 1s linear infinite' }} />
            : isCompleted
            ? <CheckCircle2 size={22} style={{ color: statusColor }} />
            : <AlertTriangle size={22} style={{ color: statusColor }} />
          }
        </div>
        <div style={{ flex: 1 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
            <span style={{ fontSize: 13, fontWeight: 700, color: '#1a1714' }}>Bulk Job</span>
            <span style={{ padding: '2px 8px', borderRadius: 99, fontSize: 9, fontWeight: 800, letterSpacing: '0.1em', background: statusBg, border: `1px solid ${statusBorder}`, color: statusColor }}>
              {results.status?.toUpperCase()}
            </span>
          </div>
          <p style={{ fontSize: 12, color: '#6b6258' }}>{results.progress}</p>
        </div>
        {/* Download entire job as ZIP */}
        {isCompleted && bulkJobId && (
          <button
            id="download-bulk-zip-btn"
            onClick={() => downloadBulkZip(bulkJobId)}
            className="btn-outline"
            style={{ display: 'flex', alignItems: 'center', gap: 7, padding: '8px 14px', borderRadius: 10, fontSize: 11, fontWeight: 700, letterSpacing: '0.1em', flexShrink: 0 }}
          >
            <Archive size={14} />
            DOWNLOAD ALL ZIP
          </button>
        )}
      </div>

      {/* Results list */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        {results.results?.map((row, idx) => (
          <div key={idx} className="card" style={{ borderRadius: 14, overflow: 'hidden', padding: 0 }}>
            {/* Row Header */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '10px 16px', borderBottom: '1px solid #ede9e1', background: '#faf8f4' }}>
              <span style={{ fontSize: 9, fontWeight: 800, color: '#8a8275', letterSpacing: '0.16em' }}>ITEM #{row.row}</span>
              <span style={{ flex: 1 }} />
              <span className="pill-gold">{row.category}</span>
              {/* Per-product ZIP */}
              {row.success && (
                <button
                  onClick={() => downloadSessionZip(row.product_id, row.product_id)}
                  title="Download this product as ZIP"
                  style={{ display: 'flex', alignItems: 'center', gap: 5, padding: '4px 10px', borderRadius: 8, background: '#fffbf0', border: '1px solid #e9c35c', cursor: 'pointer', fontSize: 10, fontWeight: 700, color: '#9a7015', letterSpacing: '0.08em' }}
                >
                  <Archive size={11} />
                  ZIP
                </button>
              )}
            </div>
            {/* Row content */}
            <div style={{ padding: 12 }}>
              {row.success ? (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(90px, 1fr))', gap: 8 }}>
                  {row.shots?.map((img, si) => (
                    <div key={si} style={{ position: 'relative', borderRadius: 10, overflow: 'hidden', aspectRatio: '1/1', background: '#f5f2ec', border: '1px solid #ede9e1' }}>
                      <img src={`${API_BASE}${img.url}`} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover' }} loading="lazy" />
                      <div style={{ position: 'absolute', inset: 0, background: 'rgba(255,255,255,0)', transition: 'background 0.2s', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
                        onMouseEnter={e => { e.currentTarget.style.background = 'rgba(255,255,255,0.7)'; e.currentTarget.querySelector('button').style.opacity = 1; }}
                        onMouseLeave={e => { e.currentTarget.style.background = 'rgba(255,255,255,0)'; e.currentTarget.querySelector('button').style.opacity = 0; }}>
                        <button onClick={() => downloadImg(img.url, img.label || `shot_${si + 1}`)}
                          style={{ opacity: 0, transition: 'opacity 0.2s', background: '#ffffff', border: '1px solid #ede9e1', borderRadius: 6, width: 28, height: 28, display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', boxShadow: '0 2px 6px rgba(0,0,0,0.1)' }}>
                          <Download size={12} color="#1a1714" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '10px 12px', borderRadius: 8, background: '#fef2f2', border: '1px solid #fecaca' }}>
                  <AlertTriangle size={14} style={{ color: '#dc2626', flexShrink: 0 }} />
                  <span style={{ fontSize: 11, color: '#b91c1c' }}>{row.error}</span>
                </div>
              )}
            </div>
          </div>
        ))}

        {/* Processing skeleton */}
        {isProcessing && (
          <div style={{ borderRadius: 14, overflow: 'hidden', border: '1px solid #d4a82a', background: '#fffbf0', animation: 'pulse 2s ease infinite' }}>
            <div style={{ padding: '10px 16px', borderBottom: '1px solid #e9c35c', display: 'flex', alignItems: 'center', gap: 8 }}>
              <Loader2 size={12} style={{ color: '#c9971c', animation: 'spin 1s linear infinite' }} />
              <span style={{ fontSize: 10, color: '#9a7015', fontWeight: 700, letterSpacing: '0.14em' }}>SYNTHESIZING NEXT PIECE...</span>
            </div>
            <div style={{ padding: 12, display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 8 }}>
              {[1,2,3,4].map(i => (
                <div key={i} style={{ aspectRatio: '1/1', borderRadius: 10, background: '#f5f2ec', border: '1px solid #ede9e1' }} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
