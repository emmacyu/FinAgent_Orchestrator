import { useState } from 'react';
import axios from 'axios';
import { Shield, Activity, Database, Zap, AlertCircle, RefreshCw } from 'lucide-react';

function App() {
  const [clientId, setClientId] = useState('C001');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const runAnalysis = async () => {
    setLoading(true);
    setData(null); 
    try {
      const response = await axios.post('http://127.0.0.1:8000/risk', {
        client_id: clientId,
        income: 60000.0,
        debt: 15000.0
      });

      console.log("Backend Response:", response.data);

      // 【核心解析逻辑】兼容你的后端 DEBUG 输出结构
      const result = response.data;
      
      // 只要返回了任何核心字段（risk_level, decision, 或 risk_score），就认为抓到了数据
      if (result && (result.risk_level || result.decision || result.risk_score !== undefined)) {
        setData(result);
      }
    } catch (err) {
      console.error("API Error:", err);
      alert("连接失败！请确保 FastAPI 后端在 8000 端口运行。");
    } finally {
      setLoading(false);
    }
  };

  // 辅助函数：智能提取分析文字（处理字符串或数组）
  const getReasoning = (d: any) => {
    const raw = d.explanation || d.audit_log || d.reasoning;
    if (Array.isArray(raw)) return raw[0]; // 如果是数组，取第一项
    return raw || "No analysis details provided by Agent.";
  };

  // 辅助函数：智能判断风险等级显示
  const getRiskDisplay = (d: any) => {
    return d.risk_level || d.decision || "N/A";
  };

  // 辅助函数：判断是否为低风险（用于变色）
  const isSafe = (d: any) => {
    const val = (d.risk_level || d.decision || "").toUpperCase();
    return val === 'LOW' || val === 'APPROVE' || val === 'SUCCESS';
  };

  return (
    <div className="min-h-screen bg-slate-50 p-6 md:p-12 font-sans text-slate-900">
      <div className="max-w-5xl mx-auto">
        
        {/* Header */}
        <header className="flex items-center justify-between mb-10 border-b border-slate-200 pb-6">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-600 rounded-xl shadow-lg shadow-blue-200">
              <Shield className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-black tracking-tight">FinAgent Orchestrator</h1>
              <p className="text-slate-500 text-sm font-medium">Enterprise MCP Risk Node</p>
            </div>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-emerald-50 text-emerald-600 rounded-full text-xs font-bold border border-emerald-100">
            <Zap className="w-3 h-3 fill-emerald-600" /> SYSTEM ONLINE
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Controls */}
          <div className="lg:col-span-1">
            <div className="bg-white p-6 rounded-3xl shadow-sm border border-slate-200">
              <h2 className="text-xs font-bold text-slate-400 uppercase mb-5 tracking-widest">Input Parameters</h2>
              <div className="space-y-4">
                <div>
                  <label className="text-[10px] font-black text-slate-400 mb-1 block">CLIENT_ID</label>
                  <input 
                    className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none font-mono text-sm"
                    value={clientId} 
                    onChange={(e) => setClientId(e.target.value)} 
                  />
                </div>
                <button 
                  onClick={runAnalysis}
                  disabled={loading}
                  className="w-full bg-slate-900 hover:bg-blue-700 text-white font-bold py-4 rounded-2xl transition-all flex items-center justify-center gap-3 disabled:bg-slate-300 shadow-xl shadow-slate-200 active:scale-95"
                >
                  {loading ? <RefreshCw className="animate-spin w-5 h-5" /> : <Database className="w-5 h-5" />}
                  {loading ? "MCP ANALYZING..." : "EXECUTE AGENT"}
                </button>
              </div>
            </div>
          </div>

          {/* Results Area */}
          <div className="lg:col-span-2">
            {data ? (
              <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="bg-white p-7 rounded-3xl border border-slate-200 shadow-sm relative overflow-hidden">
                    <div className={`absolute top-0 left-0 w-2 h-full ${isSafe(data) ? 'bg-emerald-500' : 'bg-rose-500'}`}></div>
                    <p className="text-slate-400 text-xs font-bold uppercase tracking-wider">Analysis Status</p>
                    <p className={`text-3xl font-black mt-2 ${isSafe(data) ? 'text-emerald-600' : 'text-rose-600'}`}>
                      {getRiskDisplay(data)}
                    </p>
                  </div>
                  <div className="bg-white p-7 rounded-3xl border border-slate-200 shadow-sm">
                    <p className="text-slate-400 text-xs font-bold uppercase tracking-wider">Confidence</p>
                    <p className="text-3xl font-black mt-2 text-slate-900">
                      {((data.risk_score || 0) * 100).toFixed(0)}%
                    </p>
                  </div>
                </div>

                {/* AI Reasoning / Audit Log */}
                <div className="bg-slate-900 rounded-[2.5rem] p-8 shadow-2xl">
                  <div className="flex items-center gap-2 mb-6 border-b border-slate-800 pb-4">
                    <Activity className="w-4 h-4 text-blue-400" />
                    <h4 className="text-blue-400 font-mono text-xs font-bold uppercase tracking-widest">// AGENT_AUDIT_LOG</h4>
                  </div>
                  <p className="text-slate-200 text-lg leading-relaxed italic pl-5 border-l-2 border-blue-500">
                    "{getReasoning(data)}"
                  </p>
                </div>
              </div>
            ) : (
              <div className="h-full min-h-[300px] border-2 border-dashed border-slate-200 rounded-[2.5rem] flex flex-col items-center justify-center text-slate-400 bg-white/50">
                {loading ? (
                  <Activity className="w-12 h-12 mb-4 animate-pulse text-blue-500" />
                ) : (
                  <AlertCircle className="w-12 h-12 mb-4 opacity-10" />
                )}
                <p className="font-medium text-sm tracking-wide">
                  {loading ? "Agent is pulling context from MCP tools..." : "Ready to Orchestrate. Enter Client ID."}
                </p>
              </div>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}

export default App;