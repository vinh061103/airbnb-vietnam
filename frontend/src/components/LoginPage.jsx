import React, { useState } from "react";
import { useApp } from "../context/AppContext";
import { api } from "../api/client";
import { Lock, Mail, Compass, AlertCircle, ArrowRight, ShieldCheck, Sparkles } from "lucide-react";

export default function LoginPage() {
  const { setCurrentView, handleLoginSuccess } = useApp();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg("");
    setLoading(true);

    try {
      const res = await api.login(email, password);
      setLoading(false);
      handleLoginSuccess(res.user, res.token);
    } catch (err) {
      setLoading(false);
      setErrorMsg(err.message || "Email hoặc mật khẩu không chính xác!");
    }
  };

  const handleQuickFill = (demoEmail) => {
    setEmail(demoEmail);
    setPassword("123456");
    setErrorMsg("");
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full bg-white border border-gray-200 rounded-3xl p-8 sm:p-10 shadow-xl space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="w-12 h-12 bg-gradient-to-tr from-[#FF385C] to-[#E00B41] text-white rounded-2xl flex items-center justify-center mx-auto shadow-md">
            <Compass className="w-7 h-7 stroke-[2.5]" />
          </div>
          <h2 className="text-2xl font-black text-gray-900 tracking-tight">
            Đăng nhập tài khoản
          </h2>
          <p className="text-xs text-gray-500">
            Hệ thống tự động nhận diện và chuyển hướng vào đúng Workspace của bạn
          </p>
        </div>

        {/* Quick Demo Credentials Info */}
        <div className="bg-gray-50 p-4 rounded-2xl border border-gray-200 text-xs space-y-2">
          <div className="flex items-center gap-1.5 font-bold text-gray-800">
            <Sparkles className="w-4 h-4 text-[#FF385C]" />
            <span>Tài khoản có sẵn trong cơ sở dữ liệu SQLite:</span>
          </div>
          <div className="grid grid-cols-2 gap-2 pt-1">
            <button
              type="button"
              onClick={() => handleQuickFill("host@gmail.com")}
              className="p-2 text-left bg-white border border-emerald-200 rounded-xl hover:border-emerald-500 transition-colors"
            >
              <span className="block font-bold text-emerald-700">Chủ sở hữu (Host)</span>
              <span className="text-[10px] text-gray-500">host@gmail.com</span>
              <span className="block text-[10px] text-gray-400">MK: 123456</span>
            </button>

            <button
              type="button"
              onClick={() => handleQuickFill("customer@gmail.com")}
              className="p-2 text-left bg-white border border-rose-200 rounded-xl hover:border-rose-500 transition-colors"
            >
              <span className="block font-bold text-rose-700">Khách hàng</span>
              <span className="text-[10px] text-gray-500">customer@gmail.com</span>
              <span className="block text-[10px] text-gray-400">MK: 123456</span>
            </button>
          </div>
        </div>

        {/* Error Alert */}
        {errorMsg && (
          <div className="bg-red-50 border border-red-200 text-red-700 p-3.5 rounded-2xl text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0 text-red-600" />
            <span>{errorMsg}</span>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div>
            <label className="font-bold text-gray-700 block mb-1">Email đăng nhập</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="email@example.com"
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-2xl text-xs font-semibold outline-none focus:border-gray-900 bg-white"
              />
            </div>
          </div>

          <div>
            <label className="font-bold text-gray-700 block mb-1">Mật khẩu</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Nhập mật khẩu"
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-2xl text-xs font-semibold outline-none focus:border-gray-900 bg-white"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full mt-2 bg-gradient-to-r from-[#FF385C] to-[#E00B41] hover:brightness-105 active:scale-95 text-white font-extrabold py-3.5 px-4 rounded-2xl text-xs sm:text-sm shadow-md transition-all flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {loading ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <span>Đăng nhập</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Switch to Register */}
        <div className="pt-4 border-t border-gray-100 text-center">
          <p className="text-xs text-gray-500">
            Chưa có tài khoản?{" "}
            <button
              onClick={() => setCurrentView("register")}
              className="font-bold text-[#FF385C] hover:underline"
            >
              Đăng ký tài khoản mới ngay
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}
