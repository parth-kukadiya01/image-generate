import { Sparkles, Image as ImageIcon, FileSpreadsheet, Wand2, Layers } from 'lucide-react';

const MODES = [
  { id: 'single', label: 'Studio', icon: ImageIcon, desc: 'Single product shoot' },
  { id: 'social', label: 'Creative Scenes', icon: Wand2, desc: 'Editorial & lifestyle' },
  { id: 'combo', label: 'Combo', icon: Layers, desc: 'Multi-piece flow' },
  { id: 'bulk', label: 'Bulk', icon: FileSpreadsheet, desc: 'Excel batch process' },
];

export default function Header({ mode, setMode, onModeChange }) {
  return (
    <header className="header-bar relative z-10">
      {/* Top Bar */}
      <div className="flex items-center justify-between px-8 py-5 border-b border-[#ede9e1]">
        {/* Brand */}
        <div className="flex items-center gap-4">
          <div className="relative">
            <div className="w-10 h-10 rounded-xl flex items-center justify-center btn-gold">
              <span style={{ fontFamily: 'Cormorant Garamond, serif', fontWeight: 600, fontSize: 18, color: '#ffffff' }}>R</span>
            </div>
          </div>
          <div>
            <div style={{ fontFamily: 'Cormorant Garamond, serif', fontSize: 22, fontWeight: 600, letterSpacing: '0.06em', color: '#1a1714' }}>
              RIOLLS<span className="text-gold"> AI</span>
            </div>
            <div style={{ fontSize: 9, fontWeight: 700, letterSpacing: '0.22em', color: '#6b6258', textTransform: 'uppercase', marginTop: -2 }}>
              Photography Studio
            </div>
          </div>
        </div>

        {/* Status Badge */}
        <div className="hidden md:flex items-center gap-2 px-4 py-2 rounded-full" style={{ background: '#f0fdf4', border: '1px solid #bbf7d0' }}>
          <div className="dot-live" />
          <span style={{ fontSize: 11, fontWeight: 700, color: '#15803d', letterSpacing: '0.1em' }}>LIVE ENGINE</span>
        </div>

        {/* Powered by */}
        <div className="hidden lg:flex items-center gap-2">
          <Sparkles size={13} style={{ color: '#c9971c' }} />
          <span style={{ fontSize: 11, color: '#8a6010', letterSpacing: '0.08em', fontWeight: 500 }}>Powered by Gemini 2.5</span>
        </div>
      </div>

      {/* Mode Tabs */}
      <div className="flex items-end px-8 pt-0 gap-0">
        {MODES.map(({ id, label, icon: Icon }) => {
          const active = mode === id;
          return (
            <button
              key={id}
              id={`mode-tab-${id}`}
              onClick={() => onModeChange(id)}
              style={{
                display: 'flex', alignItems: 'center', gap: 8,
                padding: '14px 24px',
                fontFamily: 'Inter, sans-serif',
                fontSize: 13, fontWeight: active ? 700 : 500,
                color: active ? '#9a7015' : '#6b6258',
                borderBottom: active ? '2px solid #c9971c' : '2px solid transparent',
                marginBottom: -1,
                transition: 'all 0.2s ease',
                background: 'transparent', borderTop: 'none', borderLeft: 'none', borderRight: 'none', cursor: 'pointer',
                letterSpacing: '0.04em',
              }}
              onMouseEnter={e => { if (!active) e.currentTarget.style.color = '#3a342f'; }}
              onMouseLeave={e => { if (!active) e.currentTarget.style.color = '#6b6258'; }}
            >
              <Icon size={15} />
              {label}
              {active && (
                <span className="pill-gold ml-1">ACTIVE</span>
              )}
            </button>
          );
        })}
      </div>
    </header>
  );
}
