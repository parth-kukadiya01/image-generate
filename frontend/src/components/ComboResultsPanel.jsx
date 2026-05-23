/**
 * ComboResultsPanel
 * Displays the generated images for each piece in the combo flow,
 * grouped by jewelry type with individual section headers.
 */
import { API_BASE } from '../api/client';
import { downloadSessionZip } from '../api/download';

const PIECE_LABELS = {
  ring:      { emoji: '💍', label: 'Ring' },
  earring:   { emoji: '✨', label: 'Earring' },
  necklace:  { emoji: '📿', label: 'Necklace' },
  bracelet:  { emoji: '💎', label: 'Bracelet' },
};

export default function ComboResultsPanel({ loading, results, flowLabel }) {
  if (loading) {
    return (
      <div style={{
        flex: 1, display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center', gap: 20, padding: '60px 0',
      }}>
        {/* Pulsing orbs */}
        <div style={{ position: 'relative', width: 80, height: 80 }}>
          {[0, 1, 2].map(i => (
            <div key={i} style={{
              position: 'absolute', inset: `${i * 8}px`,
              borderRadius: '50%',
              border: `1.5px solid ${i === 2 ? '#c9971c' : 'rgba(201,151,28,' + (0.15 + i * 0.12) + ')'}`,
              animation: `pulse-ring 2s ease-in-out ${i * 0.3}s infinite`,
            }} />
          ))}
          <div style={{
            position: 'absolute', inset: 28,
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #c9971c, #e9c35c)',
            boxShadow: '0 0 20px rgba(201,151,28,0.35)',
          }} />
        </div>
        <div style={{ textAlign: 'center' }}>
          <p style={{
            fontFamily: 'Cormorant Garamond, serif',
            fontSize: 22, fontWeight: 500, color: '#1a1714', marginBottom: 8,
          }}>
            Generating {flowLabel || 'Combo'}…
          </p>
          <p style={{ fontSize: 12, color: '#8a8275', lineHeight: 1.6 }}>
            All pieces are being generated simultaneously.<br />
            This typically takes 3–8 minutes.
          </p>
        </div>
        <ComboLoadingPieces />
      </div>
    );
  }

  if (!results || !results.pieces) {
    return (
      <div style={{
        flex: 1, display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center', gap: 16,
        padding: '60px 0', opacity: 0.55,
      }}>
        <div style={{ fontSize: 48 }}>💎✨📿</div>
        <div style={{ textAlign: 'center' }}>
          <p style={{
            fontFamily: 'Cormorant Garamond, serif',
            fontSize: 22, fontWeight: 500, color: '#1a1714', marginBottom: 6,
          }}>
            Combo Campaign Studio
          </p>
          <p style={{ fontSize: 12, color: '#8a8275', lineHeight: 1.6 }}>
            Select a flow, upload all reference images,<br />and generate a complete matched jewelry set.
          </p>
        </div>
      </div>
    );
  }

  const { pieces, session_id, flow_label } = results;
  const totalImages = pieces.reduce((sum, p) => sum + (p.images?.length || 0), 0);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 36 }}>

      {/* ── Top summary bar ── */}
      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '16px 20px', borderRadius: 14,
        background: 'linear-gradient(135deg, #fffbf0 0%, #fdf8ee 100%)',
        border: '1px solid #e9c35c',
        boxShadow: '0 2px 12px rgba(201,151,28,0.08)',
      }}>
        <div>
          <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.18em', color: '#c9971c', marginBottom: 4 }}>
            COMBO CAMPAIGN COMPLETE
          </div>
          <div style={{
            fontFamily: 'Cormorant Garamond, serif',
            fontSize: 22, fontWeight: 600, color: '#1a1714',
          }}>
            {flow_label || flowLabel}
          </div>
          <div style={{ fontSize: 11, color: '#8a8275', marginTop: 2 }}>
            {pieces.length} pieces · {totalImages} images generated
          </div>
        </div>
        {session_id && (
          <button
            id="combo-download-zip-btn"
            onClick={() => downloadSessionZip(session_id, `combo_${session_id}`)}
            style={{
              padding: '10px 18px', borderRadius: 10, cursor: 'pointer',
              background: 'linear-gradient(135deg, #c9971c 0%, #e9c35c 100%)',
              border: 'none', color: '#ffffff',
              fontSize: 11, fontWeight: 700, letterSpacing: '0.1em',
              boxShadow: '0 2px 8px rgba(201,151,28,0.3)',
              whiteSpace: 'nowrap',
            }}
          >
            ↓ Download All
          </button>
        )}
      </div>

      {/* ── Per-piece sections ── */}
      {pieces.map((piece, pi) => {
        const meta = PIECE_LABELS[piece.category] || { emoji: '💎', label: piece.category };
        return (
          <section key={pi}>
            {/* Section header */}
            <div style={{
              display: 'flex', alignItems: 'center', justifyContent: 'space-between',
              marginBottom: 16,
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <div style={{
                  width: 36, height: 36, borderRadius: 10,
                  background: '#fffbf0', border: '1.5px solid #e9c35c',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: 18, flexShrink: 0,
                }}>
                  {meta.emoji}
                </div>
                <div>
                  <h3 style={{
                    fontFamily: 'Cormorant Garamond, serif',
                    fontSize: 20, fontWeight: 600, color: '#1a1714', lineHeight: 1.2,
                  }}>
                    {meta.label}
                  </h3>
                  <p style={{ fontSize: 10, color: '#8a8275', marginTop: 1 }}>
                    {piece.images?.length || 0} shots generated
                  </p>
                </div>
              </div>
              {piece.session_id && (
                <button
                  id={`combo-dl-${piece.category}`}
                  onClick={() => downloadSessionZip(piece.session_id, `${meta.label.toLowerCase()}_${session_id}`)}
                  style={{
                    padding: '6px 14px', borderRadius: 8, cursor: 'pointer',
                    background: '#ffffff', border: '1px solid #e9c35c',
                    color: '#c9971c', fontSize: 10, fontWeight: 700,
                    letterSpacing: '0.1em',
                  }}
                >
                  ↓ ZIP
                </button>
              )}
            </div>

            {/* Image grid */}
            {piece.images && piece.images.length > 0 ? (
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
                gap: 12,
              }}>
                {piece.images.map((img, ii) => (
                  <ImageCard key={ii} img={img} />
                ))}
              </div>
            ) : (
              <div style={{
                padding: '24px', borderRadius: 12,
                background: '#fef2f2', border: '1px solid #fecaca',
                textAlign: 'center',
              }}>
                <p style={{ fontSize: 12, color: '#b91c1c', fontWeight: 500 }}>
                  Generation failed for this piece. Please retry.
                </p>
              </div>
            )}
          </section>
        );
      })}
    </div>
  );
}

function ImageCard({ img }) {
  const src = img.url.startsWith('http') ? img.url : `${API_BASE}${img.url}`;
  return (
    <div style={{
      borderRadius: 12, overflow: 'hidden', position: 'relative',
      background: '#f5f3f0', border: '1px solid #e8e3dc',
      boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
      transition: 'box-shadow 0.2s ease, transform 0.2s ease',
    }}
    onMouseEnter={e => {
      e.currentTarget.style.boxShadow = '0 8px 24px rgba(0,0,0,0.10)';
      e.currentTarget.style.transform = 'translateY(-2px)';
    }}
    onMouseLeave={e => {
      e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.04)';
      e.currentTarget.style.transform = 'translateY(0)';
    }}
    >
      <img
        src={src}
        alt={img.label}
        style={{ width: '100%', aspectRatio: '1/1', objectFit: 'cover', display: 'block' }}
        loading="lazy"
      />
      {/* Label overlay */}
      <div style={{
        position: 'absolute', bottom: 0, left: 0, right: 0,
        background: 'linear-gradient(transparent, rgba(26,23,20,0.82))',
        padding: '20px 10px 8px',
      }}>
        <p style={{
          fontSize: 10, color: '#ffffff', fontWeight: 600, textAlign: 'center',
          letterSpacing: '0.06em', lineHeight: 1.3,
        }}>
          {img.label}
        </p>
      </div>
      {/* Download single image */}
      <a
        href={src}
        download
        title="Download image"
        style={{
          position: 'absolute', top: 8, right: 8,
          width: 26, height: 26, borderRadius: '50%',
          background: 'rgba(255,255,255,0.9)', border: '1px solid #ede9e1',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 12, textDecoration: 'none', color: '#1a1714',
          boxShadow: '0 1px 4px rgba(0,0,0,0.08)',
        }}
      >
        ↓
      </a>
    </div>
  );
}

/* ── Loading piece pills ─────────────────────────────────────────────────── */
function ComboLoadingPieces() {
  const STEPS = ['Locking designs…', 'Generating shots…', 'Applying watermarks…'];
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 8, width: '100%', maxWidth: 280 }}>
      {STEPS.map((step, i) => (
        <div key={i} style={{
          display: 'flex', alignItems: 'center', gap: 10,
          padding: '8px 14px', borderRadius: 99,
          background: '#ffffff', border: '1px solid #e8e3dc',
          animation: `fade-in 0.4s ease ${i * 0.15}s both`,
        }}>
          <div style={{
            width: 6, height: 6, borderRadius: '50%',
            background: '#c9971c',
            animation: `pulse 1.5s ease ${i * 0.3}s infinite`,
          }} />
          <span style={{ fontSize: 11, color: '#6b6258', fontWeight: 500 }}>{step}</span>
        </div>
      ))}
    </div>
  );
}
