import { useState } from 'react';
import axios from 'axios';
import { Shield, Activity, Database, Zap, AlertCircle, RefreshCw, DollarSign, Wallet } from 'lucide-react';

function App() {
  const [clientId, setClientId] = useState('C001');
  const [income, setIncome] = useState(60000); // 默认年收入
  const [debt, setDebt] = useState(15000);    // 默认债务
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const runAnalysis = async () => {
    setLoading(true);
    setData(null); 
    try {
      // 关键：现在我们发送的是动态的 income 和 debt
      const response = await axios.post('http://127.0.0.1:8000/risk', {
        client_id: clientId,
        income: Number(income),
        debt: Number(debt)
      });

      console.log("Agent Response:", response.data);

      // 兼容性解析逻辑：无论后端给什么字段，全抓出来
      const result = response.data;
      if (result && (result.risk_level || result.decision || result.risk_score !== undefined)) {
        setData(result);
      }
    } catch (err) {
      console.error("API Error:", err);
      alert("Backend Connection Lost! Check 8000 port.");
    } finally {
      setLoading(false);
    }
  };

  // 辅助函数：智能提取分析文字
  const getReasoning = (d: any) => {
    const raw = d.explanation || d.audit_log || d.reasoning;
    if (Array.isArray(raw)) return raw[0];
    return raw || "No detailed reasoning provided by LLM.";
  };

  return (
    <div className="min-h-screen bg-slate-50 p-6 md:p-12 font-sans text-slate-900">
      <div className="max-w-6xl mx-auto">
        
        {/* Header */}
        <header className="flex items-center justify-between mb-10 border-b border-slate-200 pb-6">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-600 rounded-2xl shadow-xl shadow-blue-200 text-white">
              <Shield className="w-8 h-8" />
            </div>
            <div>
              <h1 className="text-2xl font-black tracking-tight">FinAgent Orchestrator</h1>
              <p className="text-slate-500 text-sm font-medium">Multi-Agent Risk Infrastructure</p>
            </div>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-emerald-50 text-emerald-600 rounded-full text-[10px] font-black border border-emerald-100 uppercase tracking-widest">
            <Zap className="w-3 h-3 fill-emerald-600" /> System Live
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
          
          {/* Controls Panel */}
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-white p-8 rounded-[2rem] shadow-sm border border-slate-200">
              <h2 className="text-xs font-black text-slate-400 uppercase mb-6 tracking-widest">Input Parameters</h2>
              
              <div className="space-y-6">
                {/* Client ID */}
                <div>
                  <label className="text-[10px] font-black text-slate-500 mb-2 block ml-1 uppercase">Client Identifier</label>
                  <input 
                    className="w-full p-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-blue-500 outline-none font-mono text-sm"
                    value={clientId} 
                    onChange={(e) => setClientId(e.target.value)} 
                  />
                </div>

                {/* Income Input */}
                <div>
                  <label className="text-[10px] font-black text-slate-500 mb-2 block ml-1 uppercase">Annual Income ($)</label>
                  <div className="relative">
                    <DollarSign className="absolute left-4 top-4 w-4 h-4 text-slate-400" />
                    <input 
                      type="number"
                      className="w-full p-4 pl-10 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-blue-500 outline-none font-bold"
                      value={income} 
                      onChange={(e) => setIncome(Number(e.target.value))} 
                    />
                  </div>
                </div>

                {/* Debt Input */}
                <div>
                  <label className="text-[10px] font-black text-slate-500 mb-2 block ml-1 uppercase">Total Debt ($)</label>
                  <div className="relative">
                    <Wallet className="absolute left-4 top-4 w-4 h-4 text-slate-400" />
                    <input 
                      type="number"
                      className="w-full p-4 pl-10 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-blue-500 outline-none font-bold text-rose-600"
                      value={debt} 
                      onChange={(e) => setDebt(Number(e.target.value))} 
                    />
                  </div>
                </div>

                <button 
                  onClick={runAnalysis}
                  disabled={loading}
                  className="w-full bg-slate-900 hover:bg-blue-700 text-white font-bold py-5 rounded-[1.5rem] transition-all flex items-center justify-center gap-3 disabled:bg-slate-300 shadow-2xl active:scale-95 mt-4"
                >
                  {loading ? <RefreshCw className="animate-spin w-5 h-5" /> : <Activity className="w-5 h-5" />}
                  {loading ? "CONSULTING AGENT..." : "EXECUTE ANALYSIS"}
                </button>
              </div>
            </div>
          </div>

          {/* Results Display */}
          <div className="lg:col-span-2">
            {data ? (
              <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  <div className="bg-white p-8 rounded-[2rem] border border-slate-200 shadow-sm relative overflow-hidden">
                    <div className={`absolute top-0 left-0 w-2 h-full ${(data.risk_level === 'LOW' || data.decision === 'APPROVE') ? 'bg-emerald-500' : 'bg-rose-500'}`}></div>
                    <p className="text-slate-400 text-xs font-black uppercase tracking-widest">Agent Decision</p>
                    <p className={`text-4xl font-black mt-3 ${(data.risk_level === 'LOW' || data.decision === 'APPROVE') ? 'text-emerald-600' : 'text-rose-600'}`}>
                      {data.risk_level || data.decision}
                    </p>
                  </div>
                  <div className="bg-white p-8 rounded-[2rem] border border-slate-200 shadow-sm text-center sm:text-left">
                    <p className="text-slate-400 text-xs font-black uppercase tracking-widest">Risk Score</p>
                    <p className="text-4xl font-black mt-3 text-slate-900">
                      {((data.risk_score || 0) * 100).toFixed(0)}%
                    </p>
                  </div>
                </div>

                <div className="bg-slate-900 rounded-[2.5rem] p-10 shadow-2xl border border-slate-800">
                  <div className="flex items-center gap-3 mb-8 border-b border-slate-800 pb-6">
                    <div className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></div>
                    <h4 className="text-blue-400 font-mono text-[10px] font-black uppercase tracking-[0.2em]">
                      // AGENT_AUDIT_TRAIL
                    </h4>
                  </div>
                  
                  <p className="text-slate-100 text-xl leading-relaxed italic font-serif">
                    "{getReasoning(data)}"
                  </p>

                  <div className="mt-10 flex items-center gap-6">
                    <div className="text-[10px] font-mono text-slate-500 uppercase">Input Params: DTI Ratio {((debt/income)*100).toFixed(1)}%</div>
                    <div className="flex-grow h-[1px] bg-slate-800"></div>
                    <div className="text-[10px] font-mono text-slate-500">SECURE NODE: {clientId}</div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="h-full min-h-[450px] border-2 border-dashed border-slate-200 rounded-[3rem] flex flex-col items-center justify-center text-slate-400 bg-white/50 backdrop-blur-sm">
                <AlertCircle className="w-16 h-16 mb-6 opacity-5 text-slate-900" />
                <p className="text-sm font-bold uppercase tracking-widest opacity-40">Awaiting Orchestration Command</p>
              </div>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}

export default App;