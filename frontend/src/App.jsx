import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { 
  UploadCloud, 
  Image as ImageIcon, 
  Sparkles, 
  Loader2, 
  CheckCircle2, 
  FileSpreadsheet, 
  LayoutGrid,
  ChevronRight,
  Download,
  Shield,
  Zap
} from 'lucide-react';

const CATEGORIES = [
  { id: 'ring', label: 'Ring', icon: '💍' },
  { id: 'necklace', label: 'Necklace', icon: '📿' },
  { id: 'bracelet', label: 'Bracelet', icon: '💫' },
  { id: 'earring', label: 'Earring', icon: '✨' },
  { id: 'pendant', label: 'Pendant', icon: '🔮' },
  { id: 'pendant_set', label: 'Pendant Set', icon: '💎' },
  { id: 'bangle', label: 'Bangle', icon: '⭕' },
  { id: 'anklet', label: 'Anklet', icon: '⛓️' },
  { id: 'brooch', label: 'Brooch', icon: '🏵️' },
];

function App() {
  const [isBulkMode, setIsBulkMode] = useState(false);
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

  const fileInputRef = useRef(null);
  const API_URL = 'http://localhost:8000';

  useEffect(() => {
    return () => {
      if (preview) URL.revokeObjectURL(preview);
    };
  }, [preview]);

  useEffect(() => {
    let intervalId;
    if (bulkJobId && bulkStatus !== 'completed' && bulkStatus !== 'failed') {
      intervalId = setInterval(async () => {
        try {
          const res = await axios.get(`${API_URL}/api/bulk-status/${bulkJobId}`);
          setBulkStatus(res.data.status);
          setResults(res.data);
          if (res.data.status === 'completed' || res.data.status === 'failed') {
            setLoading(false);
            clearInterval(intervalId);
          }
        } catch (err) {
          console.error("Polling error", err);
        }
      }, 3000);
    }
    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [bulkJobId, bulkStatus]);

  const handleFile = (selectedFile) => {
    if (!selectedFile) return;
    if (isBulkMode) {
      if (selectedFile.name.match(/\.(xlsx|xls|csv)$/)) {
        setFile(selectedFile);
        setPreview(null);
        setError(null);
        setResults(null);
        setBulkJobId(null);
      } else {
        setError("Please select a valid Excel or CSV file.");
      }
    } else {
      if (selectedFile.type.startsWith('image/')) {
        setFile(selectedFile);
        setPreview(URL.createObjectURL(selectedFile));
        setError(null);
        setResults(null);
      } else {
        setError("Please select a valid image file.");
      }
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleGenerate = async () => {
    if (isBulkMode && !file && !bulkUrl) {
      setError("Please upload an Excel file or provide a Google Sheets URL.");
      return;
    }
    if (!isBulkMode && !file) {
      setError("Please upload an image.");
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    const formData = new FormData();
    if (file) formData.append('file', file);
    if (isBulkMode && bulkUrl) formData.append('url', bulkUrl);
    formData.append('category', category);
    
    if (!isBulkMode && productName.trim()) {
      formData.append('product_id', productName.trim());
    }

    try {
      if (isBulkMode) {
        setBulkStatus('starting');
        const response = await axios.post(`${API_URL}/api/bulk-generate`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        if (response.data.status === 'success') {
          setBulkJobId(response.data.job_id);
        } else {
          setError("Bulk generation failed to start.");
          setLoading(false);
        }
      } else {
        const response = await axios.post(`${API_URL}/api/generate`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
          timeout: 180000,
        });
        if (response.data.status === 'success') {
          setResults(response.data.images);
        } else {
          setError("Generation failed. Please try again.");
        }
        setLoading(false);
      }
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "An error occurred during generation.");
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#05070a] text-slate-100 flex flex-col font-sans selection:bg-indigo-500/30">
      
      {/* Background Ambience */}
      <div className="fixed inset-0 overflow-hidden -z-10 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-900/20 blur-[120px] rounded-full animate-pulse-slow" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-900/10 blur-[120px] rounded-full" />
      </div>

      <div className="max-w-7xl mx-auto px-6 py-12 w-full">
        
        {/* Header Section */}
        <header className="flex flex-col md:flex-row justify-between items-center mb-16 gap-8">
          <div className="space-y-4 text-center md:text-left">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs font-semibold tracking-wider text-indigo-300 uppercase">
              <Sparkles size={12} className="animate-pulse" />
              <span>Next-Gen Jewelry AI</span>
            </div>
            <h1 className="text-6xl font-extrabold tracking-tighter">
              Lumina <span className="text-gradient-gold">Studio</span>
            </h1>
            <p className="text-slate-400 text-lg max-w-xl font-medium leading-relaxed">
              Transform a single jewelry photo into stunning, photorealistic multi-angle campaigns for your high-end brand.
            </p>
          </div>

          <div className="flex bg-white/5 p-1 rounded-2xl border border-white/10 backdrop-blur-md shadow-2xl">
            <button
              onClick={() => { setIsBulkMode(false); setFile(null); setPreview(null); setResults(null); }}
              className={`px-8 py-3 rounded-xl font-bold transition-all flex items-center gap-2 ${!isBulkMode ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/20' : 'text-slate-400 hover:text-white'}`}
            >
              <ImageIcon size={18} />
              Single Image
            </button>
            <button
              onClick={() => { setIsBulkMode(true); setFile(null); setPreview(null); setResults(null); }}
              className={`px-8 py-3 rounded-xl font-bold transition-all flex items-center gap-2 ${isBulkMode ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/20' : 'text-slate-400 hover:text-white'}`}
            >
              <FileSpreadsheet size={18} />
              Bulk Excel
            </button>
          </div>
        </header>

        <main className="grid grid-cols-1 lg:grid-cols-12 gap-10">
          
          {/* Controls Panel */}
          <div className="lg:col-span-4 flex flex-col gap-8">
            <div className="glass rounded-[2rem] p-8 relative overflow-hidden group">
              
              <div className="flex items-center gap-4 mb-8">
                <div className="w-10 h-10 rounded-xl bg-indigo-500/20 flex items-center justify-center text-indigo-400 border border-indigo-500/30">
                  <span className="font-bold">01</span>
                </div>
                <h2 className="text-2xl font-bold tracking-tight">Configuration</h2>
              </div>

              {/* Upload Area */}
              <div className="space-y-6">
                {!isBulkMode && (
                  <div>
                    <label className="text-sm font-bold text-slate-500 uppercase tracking-widest block pl-1 mb-2">
                      Folder Name
                    </label>
                    <input
                      type="text"
                      placeholder="e.g., Summer_Collection_Ring_01"
                      value={productName}
                      onChange={(e) => setProductName(e.target.value)}
                      className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 px-5 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none placeholder:text-slate-600 font-medium mb-4"
                    />
                  </div>
                )}
                
                <label className="text-sm font-bold text-slate-500 uppercase tracking-widest block pl-1">
                  {isBulkMode ? "Data Source" : "Reference Image"}
                </label>
                
                {isBulkMode ? (
                  <div className="space-y-4">
                    <div className="relative group">
                      <input
                        type="url"
                        placeholder="Google Sheets Public URL..."
                        value={bulkUrl}
                        onChange={(e) => { setBulkUrl(e.target.value); setFile(null); setError(null); }}
                        className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none placeholder:text-slate-600 font-medium"
                      />
                      <FileSpreadsheet className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" size={20} />
                    </div>
                    <div className="flex items-center gap-3 py-2">
                       <div className="h-px bg-white/5 flex-1"></div>
                       <span className="text-[10px] font-black text-white/20 uppercase tracking-[0.3em]">OR</span>
                       <div className="h-px bg-white/5 flex-1"></div>
                    </div>
                    <div
                      className={`border-2 border-dashed rounded-3xl p-8 text-center transition-all cursor-pointer flex flex-col items-center justify-center ${isDragging ? 'border-indigo-500 bg-indigo-500/10' : 'border-white/10 hover:border-white/30 hover:bg-white/5'}`}
                      onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                      onDragLeave={() => setIsDragging(false)}
                      onDrop={handleDrop}
                      onClick={() => fileInputRef.current?.click()}
                    >
                      <input type="file" ref={fileInputRef} className="hidden" accept=".xlsx,.xls,.csv" onChange={(e) => { handleFile(e.target.files[0]); setBulkUrl(''); }} />
                      {file ? (
                        <div className="animate-in fade-in zoom-in duration-300">
                          <CheckCircle2 size={40} className="text-emerald-400 mx-auto mb-4" />
                          <p className="text-lg font-bold truncate max-w-[200px] mx-auto">{file.name}</p>
                        </div>
                      ) : (
                        <>
                          <div className="w-12 h-12 rounded-2xl bg-white/5 flex items-center justify-center text-slate-400 mb-4 group-hover:scale-110 transition-transform">
                            <UploadCloud size={24} />
                          </div>
                          <p className="font-bold text-slate-400">Click to upload spreadsheet</p>
                        </>
                      )}
                    </div>
                  </div>
                ) : (
                  <div
                    className={`border-2 border-dashed rounded-[2rem] overflow-hidden group/drop aspect-square relative cursor-pointer transition-all duration-500 ${isDragging ? 'border-indigo-500 bg-indigo-500/10' : 'border-white/10 hover:border-white/30 hover:bg-white/5'}`}
                    onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                    onDragLeave={() => setIsDragging(false)}
                    onDrop={handleDrop}
                    onClick={() => fileInputRef.current?.click()}
                  >
                    <input type="file" ref={fileInputRef} className="hidden" accept="image/*" onChange={(e) => handleFile(e.target.files[0])} />
                    {preview ? (
                      <div className="w-full h-full p-4 animate-in fade-in zoom-in duration-500 transition-all group-hover/drop:p-2">
                        <img src={preview} alt="Reference" className="w-full h-full object-cover rounded-2xl shadow-2xl" />
                        <div className="absolute inset-0 bg-indigo-900/60 opacity-0 group-hover/drop:opacity-100 flex items-center justify-center transition-all duration-300">
                           <div className="flex flex-col items-center gap-2">
                             <div className="w-12 h-12 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center">
                               <UploadCloud className="text-white" size={24} />
                             </div>
                             <span className="font-bold tracking-widest text-[10px] uppercase">Replace Image</span>
                           </div>
                        </div>
                      </div>
                    ) : (
                      <div className="w-full h-full flex flex-col items-center justify-center space-y-4 p-8">
                        <div className="w-16 h-16 rounded-3xl bg-indigo-500/10 flex items-center justify-center text-indigo-400 group-hover:scale-110 group-hover:bg-indigo-500/20 transition-all duration-300">
                           <ImageIcon size={32} />
                        </div>
                        <div className="text-center">
                           <p className="font-bold text-lg mb-1">Upload Product</p>
                           <p className="text-slate-500 text-sm">Drag and drop or click to browse</p>
                        </div>
                        <div className="flex gap-2 p-1 bg-white/5 rounded-full px-3 text-[10px] font-black text-indigo-400 border border-white/5">
                           <span>JPG</span>•<span>PNG</span>•<span>WEBP</span>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Category Step */}
              <div className="mt-12 space-y-6">
                <label className="text-sm font-bold text-slate-500 uppercase tracking-widest block pl-1">
                  Product Category
                </label>
                <div className="grid grid-cols-2 gap-3">
                  {CATEGORIES.map(cat => (
                    <button
                      key={cat.id}
                      onClick={() => setCategory(cat.id)}
                      className={`relative group h-14 rounded-2xl flex items-center gap-3 px-4 transition-all border ${category === cat.id 
                        ? 'bg-indigo-600 border-indigo-400 text-white shadow-lg shadow-indigo-600/30' 
                        : 'bg-white/5 border-white/10 text-slate-400 hover:bg-white/10 hover:border-white/20 hover:text-white'}`}
                    >
                      <span className="text-xl filter group-hover:scale-125 transition-transform duration-300">{cat.icon}</span>
                      <span className="font-bold text-sm">{cat.label}</span>
                      {category === cat.id && (
                        <div className="absolute right-3 w-1.5 h-1.5 rounded-full bg-white animate-pulse" />
                      )}
                    </button>
                  ))}
                </div>
              </div>

              {/* Generate Button */}
              <div className="mt-12">
                <button
                  onClick={handleGenerate}
                  disabled={((!file && !bulkUrl && isBulkMode) || (!file && !isBulkMode)) || loading}
                  className={`w-full py-5 rounded-[1.5rem] flex items-center justify-center gap-3 font-black text-lg tracking-wider transition-all relative overflow-hidden group ${
                    ((!file && !bulkUrl && isBulkMode) || (!file && !isBulkMode))
                      ? 'bg-white/5 text-slate-700 cursor-not-allowed border border-white/5'
                      : loading
                        ? 'bg-indigo-500/50 text-white cursor-wait px-12'
                        : 'bg-gradient-to-r from-indigo-700 to-indigo-500 hover:from-indigo-600 hover:to-indigo-400 text-white shadow-2xl shadow-indigo-900/40 hover:-translate-y-1'
                  }`}
                >
                  {loading ? (
                    <>
                      <Loader2 className="animate-spin" size={24} />
                      <span className="animate-pulse">{isBulkMode ? "PROCCESSING..." : "CRAFTING..."}</span>
                    </>
                  ) : (
                    <>
                      <Sparkles size={20} className="group-hover:rotate-12 transition-transform" />
                      <span>{isBulkMode ? "RUN BULK EXPORT" : "GENERATE CAMPAIGN"}</span>
                      <ChevronRight size={20} className="group-hover:translate-x-1 transition-transform opacity-50" />
                    </>
                  )}
                </button>
                {error && (
                  <div className="mt-4 p-4 bg-red-500/10 border border-red-500/20 rounded-2xl flex items-center gap-3 text-red-500 animate-in fade-in slide-in-from-top-2 duration-300">
                    <div className="w-1.5 h-1.5 rounded-full bg-red-500" />
                    <p className="text-xs font-bold leading-tight uppercase tracking-wide">{error}</p>
                  </div>
                )}
              </div>
            </div>

            {/* Extra Info Card */}
            <div className="glass rounded-[2rem] p-6 flex items-center gap-4 border-indigo-500/10">
               <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 flex items-center justify-center text-indigo-400">
                  <Shield size={22} />
               </div>
               <div>
                  <h4 className="font-bold text-sm">Ultra-Realistic Output</h4>
                  <p className="text-slate-500 text-[11px] font-medium leading-relaxed">Powered by proprietary vision-locked generative AI for jewelry consistency.</p>
               </div>
            </div>
          </div>

          {/* Results Main Area */}
          <div className="lg:col-span-8 flex flex-col h-full min-h-[800px]">
            <div className={`glass rounded-[2.5rem] p-4 md:p-8 flex-1 transition-all duration-700 relative flex flex-col ${!results && !loading ? 'items-center justify-center border-dashed border-2 border-white/5 bg-transparent shadow-none' : 'bg-white/[0.03]'}`}>
              
              {/* Dynamic Overlay for Empty State */}
              {!loading && !results && !error && (
                <div className="text-center space-y-8 animate-in fade-in duration-1000">
                  <div className="relative mx-auto w-32 h-32">
                    <div className="absolute inset-0 bg-indigo-500/20 rounded-full blur-3xl animate-pulse" />
                    <div className="relative w-full h-full rounded-[2rem] bg-white/5 border border-white/10 flex items-center justify-center text-indigo-400 rotate-12 hover:rotate-0 transition-transform duration-500 shadow-2xl">
                      <LayoutGrid size={48} strokeWidth={1} />
                    </div>
                  </div>
                  <div className="max-w-xs mx-auto">
                    <h3 className="text-2xl font-black tracking-tight mb-2">Awaiting Creation</h3>
                    <p className="text-slate-500 font-medium leading-relaxed">Upload your piece and let our Studio craft a premium 6-angle marketing collection in seconds.</p>
                  </div>
                </div>
              )}

              {/* Generating State */}
              {loading && !results && (
                <div className="flex flex-col items-center justify-center h-full w-full space-y-12 py-20 bg-indigo-950/20 rounded-[2rem] border border-indigo-500/10">
                   <div className="relative">
                      <div className="w-24 h-24 rounded-full border-[3px] border-indigo-500/10 border-t-indigo-500 animate-spin" />
                      <Sparkles className="absolute inset-0 m-auto text-indigo-300 animate-pulse" size={32} />
                   </div>
                   <div className="text-center space-y-4">
                      <p className="text-3xl font-black tracking-tighter text-white uppercase italic">Polishing Diamonds</p>
                      <div className="flex flex-col items-center gap-2">
                        <div className="flex items-center gap-2 text-indigo-400 font-bold tracking-widest text-xs uppercase">
                          <Zap size={14} className="fill-indigo-400" />
                          <span>AI Processing</span>
                        </div>
                        <p className="text-slate-500 text-sm max-w-sm font-medium leading-relaxed">
                          Applying realistic textures, materials, and lighting to 6 unique product and model angles...
                        </p>
                      </div>
                   </div>
                   <div className="w-64 h-1.5 bg-white/5 rounded-full overflow-hidden border border-white/5">
                      <div className="h-full bg-indigo-500 w-1/3 animate-[loading-bar_3s_infinite]" />
                   </div>
                </div>
              )}

              {/* Single Mode Gallery */}
              {!isBulkMode && Array.isArray(results) && (
                <div className="animate-in fade-in duration-1000 slide-in-from-bottom-5">
                   <div className="flex flex-col md:flex-row md:items-end justify-between mb-10 gap-4 pl-2">
                      <div className="space-y-1">
                        <h2 className="text-3xl font-black tracking-tighter">Campaign Preview</h2>
                        <div className="flex items-center gap-2 text-emerald-400 font-bold text-[10px] tracking-[0.2em] uppercase">
                          <CheckCircle2 size={12} />
                          <span>6 Images Ready for Marketplace</span>
                        </div>
                      </div>
                      <button className="flex items-center gap-2 px-6 py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-2xl text-[11px] font-black tracking-widest uppercase transition-all hover:scale-105 active:scale-95 group">
                         <Download size={14} className="group-hover:translate-y-0.5 transition-transform" />
                         Package All Assets
                      </button>
                   </div>

                   <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                      {results.map((img, idx) => (
                        <div key={idx} className="group relative rounded-[2rem] overflow-hidden bg-white/5 border border-white/10 aspect-[4/5] shadow-2xl transition-all duration-700 hover:-translate-y-2 hover:shadow-indigo-500/10 isolate">
                           <div className="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent opacity-100 z-10" />
                           <img 
                            src={`${API_URL}${img.url}`} 
                            alt={img.label} 
                            className="w-full h-full object-cover transition-transform duration-1000 group-hover:scale-110" 
                           />
                           
                           {/* Content Overlay */}
                           <div className="absolute inset-x-0 bottom-0 p-6 z-20 flex flex-col gap-3">
                              <span className="inline-flex w-fit px-2 py-1 rounded-lg bg-indigo-600/90 backdrop-blur-md text-[9px] font-black uppercase tracking-widest">
                                Angle {idx + 1}
                              </span>
                              <div className="flex items-end justify-between">
                                <p className="text-white font-bold leading-tight min-h-[2.5rem] flex items-end">{img.label}</p>
                                <button className="w-10 h-10 rounded-xl bg-white/10 backdrop-blur-md flex items-center justify-center text-white opacity-0 group-hover:opacity-100 translate-y-2 group-hover:translate-y-0 transition-all hover:bg-white hover:text-black">
                                   <Download size={18} />
                                </button>
                              </div>
                           </div>
                        </div>
                      ))}
                   </div>
                </div>
              )}

              {/* Bulk Mode Experience */}
              {isBulkMode && results && results.status && (
                <div className="animate-in fade-in duration-700 w-full space-y-10">
                   <div className="glass rounded-3xl p-6 flex flex-wrap items-center justify-between gap-6 border-indigo-500/20 bg-indigo-500/[0.02]">
                      <div className="flex items-center gap-6">
                        <div className={`w-16 h-16 rounded-[1.5rem] flex items-center justify-center relative ${results.status === 'processing' ? 'bg-indigo-500/20 text-indigo-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                           {results.status === 'processing' ? <Loader2 className="animate-spin" size={32} /> : <CheckCircle2 size={32} />}
                           {results.status === 'processing' && <div className="absolute top-0 right-0 w-3 h-3 bg-indigo-500 rounded-full animate-ping" />}
                        </div>
                        <div className="space-y-1">
                          <h3 className="text-xl font-black uppercase tracking-tighter flex items-center gap-3">
                            Bulk Operation: <span className={results.status === 'processing' ? "text-indigo-400" : "text-emerald-400 animate-pulse"}>{results.status}</span>
                          </h3>
                          <div className="flex items-center gap-3 bg-white/5 py-1 px-3 rounded-full w-fit">
                             <div className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse" />
                             <p className="text-xs font-black tracking-widest text-indigo-300 uppercase">{results.progress}</p>
                          </div>
                        </div>
                      </div>
                      
                      {results.status === 'completed' && (
                        <button className="px-8 py-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded-2xl font-black text-xs uppercase tracking-widest shadow-xl shadow-emerald-900/40 transition-all flex items-center gap-2">
                           <Download size={16} />
                           Export Entire Project
                        </button>
                      )}
                   </div>

                   {/* Bulk List Rendering */}
                   <div className="grid grid-cols-1 gap-8">
                      {results.results && results.results.map((rowResult, idx) => (
                        <div key={idx} className="glass rounded-[2rem] overflow-hidden border-white/5 group-hover:border-white/20 transition-all animate-in slide-in-from-left duration-500" style={{ animationDelay: `${idx * 100}ms` }}>
                           <div className="flex items-center justify-between px-8 py-4 bg-white/5 border-b border-white/5">
                              <div className="flex items-center gap-4">
                                <span className="text-[10px] font-black text-white/20 uppercase tracking-[0.2em]">Item #{rowResult.row}</span>
                                <h4 className="font-bold text-sm text-indigo-200">Processing Success</h4>
                              </div>
                              <span className="px-3 py-1 bg-white/10 rounded-lg text-[9px] font-black uppercase tracking-widest text-indigo-300">
                                {rowResult.category}
                              </span>
                           </div>
                           
                           <div className="p-6">
                              {rowResult.success ? (
                                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
                                  {rowResult.shots && rowResult.shots.map((img, sIdx) => (
                                    <div key={sIdx} className="aspect-square rounded-2xl overflow-hidden bg-white/5 border border-white/10 group/shot relative">
                                        <img src={`${API_URL}${img.url}`} alt="" className="w-full h-full object-cover group-hover/shot:scale-125 transition-transform duration-700" />
                                        <div className="absolute inset-0 bg-black/60 opacity-0 group-hover/shot:opacity-100 flex items-center justify-center transition-all">
                                           <Download size={14} className="text-white translate-y-2 group-hover/shot:translate-y-0 transition-transform" />
                                        </div>
                                    </div>
                                  ))}
                                </div>
                              ) : (
                                <div className="flex items-center gap-4 p-4 bg-red-500/10 border border-red-500/20 rounded-2xl">
                                   <div className="w-2 h-2 rounded-full bg-red-500" />
                                   <span className="text-xs font-bold text-red-400 uppercase tracking-widest leading-tight">Error: {rowResult.error}</span>
                                </div>
                              )}
                           </div>
                        </div>
                      ))}

                      {/* Active Row Skeleton */}
                      {results.status === 'processing' && (
                        <div className="glass rounded-[2rem] overflow-hidden border-indigo-500/30 animate-pulse">
                           <div className="px-8 py-4 bg-indigo-500/10 flex items-center justify-between">
                              <div className="flex items-center gap-3">
                                 <Loader2 size={14} className="animate-spin text-indigo-400" />
                                 <span className="text-[10px] font-black text-indigo-300 uppercase tracking-[0.2em]">Synthesizing next piece...</span>
                              </div>
                           </div>
                           <div className="p-6 grid grid-cols-2 lg:grid-cols-6 gap-3">
                              {[1,2,3,4,5,6].map(i => (
                                <div key={i} className="aspect-square rounded-2xl bg-indigo-500/5 border border-indigo-500/10" />
                              ))}
                           </div>
                        </div>
                      )}
                   </div>
                </div>
              )}
            </div>
          </div>
        </main>

        {/* Footer Details */}
        <footer className="mt-20 pt-12 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-8 px-4 opacity-50">
           <div className="flex items-center gap-6">
              <p className="text-[10px] font-black tracking-[0.2em] uppercase">© 2026 Lumina Luxury Systems</p>
           </div>
           <div className="flex items-center gap-8">
              <span className="text-[10px] font-bold tracking-widest text-indigo-400 hover:text-indigo-300 cursor-pointer transition-colors">GDPR COMPLIANT</span>
              <span className="text-[10px] font-bold tracking-widest text-indigo-400 hover:text-indigo-300 cursor-pointer transition-colors">ENTERPRISE CLOUD</span>
           </div>
        </footer>

      </div>

      <style>{`
        @keyframes loading-bar {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(300%); }
        }
        @keyframes pulse-slow {
          0%, 100% { opacity: 0.1; transform: scale(1); }
          50% { opacity: 0.3; transform: scale(1.1); }
        }
      `}</style>
    </div>
  );
}

export default App;
