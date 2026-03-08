import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { UploadCloud, Image as ImageIcon, Sparkles, Loader2, CheckCircle2, FileSpreadsheet, LayoutGrid } from 'lucide-react';

const CATEGORIES = [
  { id: 'ring', label: 'Ring', icon: '💍' },
  { id: 'necklace', label: 'Necklace', icon: '📿' },
  { id: 'bracelet', label: 'Bracelet', icon: '💫' },
  { id: 'earring', label: 'Earring', icon: '✨' },
  { id: 'pendant', label: 'Pendant', icon: '🔮' },
  { id: 'bangle', label: 'Bangle', icon: '⭕' },
  { id: 'anklet', label: 'Anklet', icon: '⛓️' },
  { id: 'brooch', label: 'Brooch', icon: '🏵️' },
];

function App() {
  const [isBulkMode, setIsBulkMode] = useState(false);

  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [category, setCategory] = useState('ring');
  const [isDragging, setIsDragging] = useState(false);

  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  // Bulk specific states
  const [bulkUrl, setBulkUrl] = useState('');
  const [bulkJobId, setBulkJobId] = useState(null);
  const [bulkStatus, setBulkStatus] = useState(null);

  const fileInputRef = useRef(null);

  const API_URL = 'http://localhost:8000';

  // Clean up object URL on unmount
  useEffect(() => {
    return () => {
      if (preview) URL.revokeObjectURL(preview);
    };
  }, [preview]);

  // Polling effect for bulk job
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
    if (file) {
      formData.append('file', file);
    }
    if (isBulkMode && bulkUrl) {
      formData.append('url', bulkUrl);
    }
    formData.append('category', category); // acts as default category for bulk

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
          timeout: 120000,
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
    <div className="min-h-screen bg-slate-50 relative overflow-hidden font-sans pb-20">

      {/* Premium Background Elements */}
      <div className="absolute top-0 inset-x-0 h-96 bg-gradient-to-br from-indigo-900 via-slate-800 to-indigo-950 -z-10 animate-gradient-x" />
      <div className="absolute -top-32 -left-32 w-96 h-96 bg-white/10 rounded-full blur-3xl" />
      <div className="absolute top-16 -right-32 w-80 h-80 bg-indigo-500/20 rounded-full blur-3xl animate-pulse-slow" />

      <div className="max-w-6xl mx-auto px-4 py-12 md:py-20 relative z-10">

        {/* Header */}
        <div className="text-center mb-16 space-y-4">
          <div className="inline-flex items-center justify-center p-3 bg-white/10 backdrop-blur-md rounded-2xl mb-4 border border-white/20 shadow-xl">
            <Sparkles className="w-8 h-8 text-indigo-300" />
          </div>
          <h1 className="text-5xl md:text-6xl font-extrabold text-white tracking-tight">
            Lumina <span className="text-indigo-300 font-light italic">Studio</span>
          </h1>
          <p className="text-indigo-100/80 text-lg md:text-xl max-w-2xl mx-auto font-light">
            Transform a single jewelry photo or batch process an Excel file into stunning photorealistic campaigns instantly.
          </p>
        </div>

        {/* Action Toggle */}
        <div className="flex justify-center mb-8">
          <div className="bg-white/20 backdrop-blur-md p-1.5 rounded-2xl border border-white/10 flex shadow-lg">
            <button
              onClick={() => { setIsBulkMode(false); setFile(null); setPreview(null); }}
              className={`flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all ${!isBulkMode ? 'bg-white text-indigo-900 shadow-md' : 'text-indigo-50 hover:bg-white/10'}`}
            >
              <ImageIcon size={18} />
              Single Image
            </button>
            <button
              onClick={() => { setIsBulkMode(true); setFile(null); setPreview(null); }}
              className={`flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all ${isBulkMode ? 'bg-white text-indigo-900 shadow-md' : 'text-indigo-50 hover:bg-white/10'}`}
            >
              <FileSpreadsheet size={18} />
              Bulk Excel
            </button>
          </div>
        </div>

        {/* Main Content Area */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">

          {/* Controls Column (Left) */}
          <div className="lg:col-span-4 space-y-6">
            <div className="glass rounded-3xl p-6 md:p-8 relative overflow-hidden group transition-all duration-300 hover:shadow-2xl">

              <h2 className="text-xl font-semibold mb-6 flex items-center text-slate-800">
                <span className="bg-indigo-100 text-indigo-700 w-8 h-8 rounded-full flex items-center justify-center mr-3 text-sm">1</span>
                Upload {isBulkMode ? "Excel List" : "Image"}
              </h2>

              {/* Dropzone OR URL Input (Bulk Mode) */}
              {isBulkMode ? (
                <div className="space-y-4">
                  <div className="relative">
                    <input
                      type="url"
                      placeholder="Paste Google Sheets Public URL..."
                      value={bulkUrl}
                      onChange={(e) => {
                        setBulkUrl(e.target.value);
                        setFile(null); // Clear file if URL is entered
                        setError(null);
                      }}
                      className="w-full px-4 py-3 pl-12 rounded-xl border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white shadow-sm transition-all"
                    />
                    <FileSpreadsheet className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
                  </div>

                  <div className="flex items-center gap-4 text-slate-400">
                    <div className="h-px bg-slate-200 flex-1"></div>
                    <span className="text-sm font-medium uppercase tracking-wider">or upload file</span>
                    <div className="h-px bg-slate-200 flex-1"></div>
                  </div>

                  <div
                    className={`border-2 border-dashed rounded-2xl p-6 text-center transition-all duration-200 cursor-pointer flex flex-col items-center justify-center ${isDragging ? 'border-indigo-500 bg-indigo-50/50' :
                      file ? 'border-indigo-400 bg-indigo-50/20' : 'border-slate-300 hover:border-indigo-400 hover:bg-slate-50/50'
                      }`}
                    onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                    onDragLeave={() => setIsDragging(false)}
                    onDrop={handleDrop}
                    onClick={() => fileInputRef.current?.click()}
                  >
                    <input
                      type="file"
                      ref={fileInputRef}
                      className="hidden"
                      accept=".xlsx,.xls,.csv"
                      onChange={(e) => {
                        handleFile(e.target.files[0]);
                        setBulkUrl(''); // Clear URL if file is chosen
                      }}
                    />
                    {file ? (
                      <div className="space-y-3 py-2">
                        <div className="w-12 h-12 bg-emerald-50 rounded-full flex items-center justify-center mx-auto text-emerald-500 shadow-sm">
                          <CheckCircle2 size={24} strokeWidth={2} />
                        </div>
                        <div className="text-slate-800 font-medium break-all px-4">{file.name}</div>
                        <p className="text-xs text-slate-400">Click to replace</p>
                      </div>
                    ) : (
                      <div className="space-y-3 py-2">
                        <div className="w-12 h-12 bg-indigo-50 rounded-full flex items-center justify-center mx-auto text-indigo-500 shadow-sm">
                          <UploadCloud size={24} strokeWidth={2} />
                        </div>
                        <div className="text-slate-600">
                          <span className="font-semibold text-indigo-600">Upload Excel/CSV</span>
                        </div>
                        <p className="text-xs text-slate-400">with 'Image Prompt' or 'URL' columns</p>
                      </div>
                    )}
                  </div>
                </div>
              ) : (
                <div
                  className={`border-2 border-dashed rounded-2xl p-8 text-center transition-all duration-200 cursor-pointer flex flex-col items-center justify-center ${isDragging ? 'border-indigo-500 bg-indigo-50/50' :
                    preview ? 'border-slate-200 bg-slate-50' : 'border-slate-300 hover:border-indigo-400 hover:bg-slate-50/50'
                    }`}
                  onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                  onDragLeave={() => setIsDragging(false)}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current?.click()}
                >
                  <input
                    type="file"
                    ref={fileInputRef}
                    className="hidden"
                    accept={"image/jpeg, image/png, image/webp"}
                    onChange={(e) => handleFile(e.target.files[0])}
                  />

                  {preview ? (
                    <div className="relative w-full aspect-square rounded-xl overflow-hidden shadow-inner group/img">
                      <img src={preview} alt="Preview" className="w-full h-full object-cover transition-transform duration-500 group-hover/img:scale-105" />
                      <div className="absolute inset-0 bg-black/40 opacity-0 group-hover/img:opacity-100 transition-opacity flex items-center justify-center">
                        <span className="text-white font-medium flex items-center gap-2"><UploadCloud size={18} /> Replace</span>
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-4 py-6">
                      <div className="w-16 h-16 bg-indigo-50 rounded-full flex items-center justify-center mx-auto text-indigo-500 shadow-sm">
                        <ImageIcon size={32} strokeWidth={1.5} />
                      </div>
                      <div className="text-slate-600">
                        <span className="font-semibold text-indigo-600">Click to upload</span> or drag and drop
                      </div>
                      <p className="text-xs text-slate-400">PNG, JPG, WEBP (Max 5MB)</p>
                    </div>
                  )}
                </div>
              )}

              {/* Category Selection */}
              <div className="mt-8">
                <h2 className="text-xl font-semibold mb-4 flex items-center text-slate-800">
                  <span className="bg-indigo-100 text-indigo-700 w-8 h-8 rounded-full flex items-center justify-center mr-3 text-sm">2</span>
                  {isBulkMode ? "Default Category" : "Select Category"}
                </h2>
                {isBulkMode && <p className="text-xs text-slate-500 mb-3">If Excel row has a 'category' column, it will override this default.</p>}
                <div className="grid grid-cols-2 gap-3">
                  {CATEGORIES.map(cat => (
                    <button
                      key={cat.id}
                      onClick={() => setCategory(cat.id)}
                      className={`py-3 px-4 rounded-xl flex items-center gap-2 text-left transition-all duration-200 border ${category === cat.id
                        ? 'bg-indigo-600 text-white border-indigo-600 shadow-md shadow-indigo-200'
                        : 'bg-slate-50 text-slate-600 border-slate-200 hover:border-indigo-300 hover:bg-white'
                        }`}
                    >
                      <span className="text-lg">{cat.icon}</span>
                      <span className="font-medium text-sm">{cat.label}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Actions */}
              <div className="mt-8">
                <button
                  onClick={handleGenerate}
                  disabled={(!file && !bulkUrl && isBulkMode) || (!file && !isBulkMode) || loading}
                  className={`w-full py-4 rounded-xl flex items-center justify-center gap-2 font-semibold text-lg transition-all duration-300 shadow-lg ${((!file && !bulkUrl && isBulkMode) || (!file && !isBulkMode))
                    ? 'bg-slate-100 text-slate-400 cursor-not-allowed shadow-none'
                    : loading
                      ? 'bg-indigo-400 text-white cursor-wait relative overflow-hidden'
                      : 'bg-indigo-600 hover:bg-indigo-700 text-white hover:shadow-indigo-500/30 hover:-translate-y-0.5'
                    }`}
                >
                  {loading ? (
                    <>
                      <Loader2 className="animate-spin" size={20} />
                      {isBulkMode ? "Starting Bulk..." : "Generating Magic..."}
                      <div className="absolute inset-x-0 bottom-0 h-1 bg-indigo-500">
                        <div className="h-full bg-white/50 animate-[pulse_2s_ease-in-out_infinite] w-1/3 rounded-r-full"></div>
                      </div>
                    </>
                  ) : (
                    <>
                      <Sparkles size={20} />
                      {isBulkMode ? "Process Bulk List" : "Generate Collection"}
                    </>
                  )}
                </button>
                {error && (
                  <p className="mt-3 text-sm text-red-500 flex items-center gap-1.5 justify-center">
                    <span className="w-1.5 h-1.5 rounded-full bg-red-500 inline-block animate-pulse"></span>
                    {error}
                  </p>
                )}
              </div>
            </div>
          </div>

          {/* Results Area (Right) */}
          <div className="lg:col-span-8">
            <div className={`glass rounded-3xl p-6 md:p-8 min-h-[600px] transition-all duration-500 flex flex-col ${!results && !loading ? 'items-center justify-center border-dashed border-2' : ''
              }`}>

              {loading && !results && (
                <div className="flex flex-col items-center justify-center h-full space-y-8 animate-in fade-in duration-500 w-full min-h-[400px]">
                  <div className="relative w-24 h-24">
                    <div className="absolute inset-0 rounded-full border-4 border-indigo-100"></div>
                    <div className="absolute inset-0 rounded-full border-4 border-indigo-600 border-t-transparent animate-spin"></div>
                    <Sparkles className="absolute inset-0 m-auto text-indigo-400 animate-pulse-slow" size={32} />
                  </div>
                  <div className="text-center space-y-2">
                    <h3 className="text-2xl font-bold text-slate-800">Crafting your collection</h3>
                    <p className="text-slate-500 flex items-center justify-center gap-2">
                      <Loader2 size={16} className="animate-spin" /> Analyzing design details, materials & angles...
                    </p>
                    <p className="text-xs text-slate-400 mt-2 italic">This may take up to 60 seconds.</p>
                  </div>
                </div>
              )}

              {!loading && !results && !error && (
                <div className="opacity-60 text-center max-w-sm mx-auto">
                  <div className="w-24 h-24 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-6 text-slate-300">
                    <LayoutGrid size={48} strokeWidth={1} />
                  </div>
                  <h3 className="text-xl font-medium text-slate-700 mb-2">Awaiting Masterpiece</h3>
                  <p className="text-slate-500 text-sm">Upload an image and select a category to generate 6 premium product and lifestyle angles.</p>
                </div>
              )}

              {/* Bulk Mode Live Results */}
              {isBulkMode && results && results.status && (
                <div className="animate-in slide-in-from-bottom-8 fade-in duration-700">
                  <div className="flex items-center justify-between mb-6 bg-slate-100 p-4 rounded-2xl border border-slate-200">
                    <div className="flex items-center gap-4">
                      {results.status === 'processing' ? (
                        <Loader2 className="animate-spin text-indigo-600" size={24} />
                      ) : results.status === 'failed' ? (
                        <div className="w-4 h-4 rounded-full bg-red-500"></div>
                      ) : (
                        <CheckCircle2 className="text-emerald-500" size={28} />
                      )}
                      <div>
                        <h2 className="text-lg font-bold text-slate-800 flex items-center gap-3">
                          Bulk Generation: <span className="capitalize">{results.status}</span>
                        </h2>
                        <p className="text-sm text-slate-600 font-medium">{results.progress}</p>
                      </div>
                    </div>
                  </div>

                  {results.results && results.results.length > 0 && (
                    <div className="space-y-8">
                      {results.results.map((rowResult, rowIdx) => (
                        <div key={rowIdx} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                          <div className="flex items-center justify-between mb-4 border-b pb-3">
                            <div>
                              <span className="px-2.5 py-1 bg-indigo-50 text-indigo-700 text-xs font-bold rounded-full mr-3">Row {rowResult.row}</span>
                              <span className="text-slate-600 font-medium text-sm truncate max-w-[200px] inline-block align-bottom">{rowResult.url}</span>
                            </div>
                            <span className="px-3 py-1 bg-slate-100 text-slate-600 text-xs font-semibold rounded-full uppercase tracking-wider">
                              {rowResult.category}
                            </span>
                          </div>

                          {rowResult.success && rowResult.shots ? (
                            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
                              {rowResult.shots.map((img, idx) => (
                                <div key={idx} className="group relative rounded-xl overflow-hidden bg-slate-100 border border-slate-200 aspect-square group">
                                  <img
                                    src={`${API_URL}${img.url}`}
                                    alt={img.label}
                                    className="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                                  />
                                  <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/80 to-transparent p-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <p className="text-white text-[10px] truncate">{img.label}</p>
                                  </div>
                                </div>
                              ))}
                            </div>
                          ) : (
                            <div className="p-4 bg-red-50 text-red-600 rounded-xl text-sm font-medium">
                              Failed: {rowResult.error}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Loading Skeleton for the actively processing row */}
                  {results.status === 'processing' && (
                    <div className="mt-8 bg-indigo-50/50 p-6 rounded-2xl border border-indigo-100 shadow-sm relative overflow-hidden animate-pulse">
                      <div className="flex items-center mb-6 border-b border-indigo-200 pb-3">
                        <Loader2 className="animate-spin text-indigo-500 mr-3" size={20} />
                        <span className="text-indigo-700 font-semibold text-sm">Generating 6-angle collection... (approx 90 seconds/product)</span>
                      </div>
                      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
                        {[1, 2, 3, 4, 5, 6].map(i => (
                          <div key={`skeleton-${i}`} className="aspect-square bg-indigo-200/50 rounded-xl animate-pulse"></div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Single Mode Results */}
              {!isBulkMode && Array.isArray(results) && (
                <div className="animate-in slide-in-from-bottom-8 fade-in duration-700">
                  <div className="flex items-center justify-between mb-8">
                    <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-3">
                      <CheckCircle2 className="text-emerald-500" />
                      Generated Collection
                    </h2>
                    <span className="px-3 py-1 bg-indigo-50 text-indigo-700 text-xs font-semibold rounded-full uppercase tracking-wider">
                      {results.length} / 6 Shots
                    </span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {results.map((img, idx) => (
                      <div key={idx} className="group relative rounded-2xl overflow-hidden bg-slate-100 border border-slate-200 shadow-sm hover:shadow-xl transition-all duration-300 isolate">
                        <div className="aspect-[4/5] w-full bg-slate-200 animate-pulse relative -z-10" />
                        <img
                          src={`${API_URL}${img.url}`}
                          alt={img.label}
                          className="absolute top-0 left-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
                          onLoad={(e) => { e.target.previousSibling.style.display = 'none'; }}
                        />

                        {/* Label Badge */}
                        <div className="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent p-4 pt-12">
                          <p className="text-white font-medium text-sm translate-y-2 group-hover:translate-y-0 transition-transform">{img.label}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

export default App;
