import React, { useState } from "react";
import { useApp } from "../context/AppContext";
import { api } from "../api/client";
import {
  User,
  Mail,
  Lock,
  Phone,
  Compass,
  AlertCircle,
  CheckCircle2,
  Building2,
  ArrowRight,
  ShieldCheck,
} from "lucide-react";

export default function RegisterPage() {
  const { setCurrentView, handleLoginSuccess } = useApp();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [role, setRole] = useState("customer"); // 'customer' | 'host'
  const [errorMsg, setErrorMsg] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg("");

    if (password !== confirmPassword) {
      setErrorMsg("Mật khẩu xác nhận không khớp!");
      return;
    }

    if (password.length < 6) {
      setErrorMsg("Mật khẩu phải có ít nhất 6 ký tự!");
      return;
    }

    setLoading(true);

    try {
      const res = await api.register({
        full_name: fullName,
        email,
        phone,
        password,
        role,
      });

      setLoading(false);
      alert(`Đăng ký tài khoản thành công với vai trò: ${role === 'host' ? 'Chủ sở hữu (Host)' : 'Khách hàng (Customer)'}!`);
      handleLoginSuccess(res.user, res.token);
    } catch (err) {
      setLoading(false);
      setErrorMsg(err.message || "Lỗi khi đăng ký tài khoản.");
    }
  };

  return (
    <div className="min-h-[85vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full bg-white border border-gray-200 rounded-3xl p-8 sm:p-10 shadow-xl space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="w-12 h-12 bg-gradient-to-tr from-[#FF385C] to-[#E00B41] text-white rounded-2xl flex items-center justify-center mx-auto shadow-md">
            <Compass className="w-7 h-7 stroke-[2.5]" />
          </div>
          <h2 className="text-2xl font-black text-gray-900 tracking-tight">
            Đăng ký tài khoản mới
          </h2>
          <p className="text-xs text-gray-500">
            Dữ liệu sẽ được lưu trực tiếp vào cơ sở dữ liệu SQLite
          </p>
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
          {/* Role Selection */}
          <div>
            <label className="font-bold text-gray-700 block mb-1.5">
              Bạn muốn tham gia với vai trò nào? *
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setRole("customer")}
                className={`p-3 rounded-2xl border text-left flex flex-col justify-between transition-all ${
                  role === "customer"
                    ? "border-[#FF385C] bg-rose-50/50 shadow-sm"
                    : "border-gray-200 hover:border-gray-300"
                }`}
              >
                <div className="flex items-center justify-between w-full">
                  <User className="w-4 h-4 text-[#FF385C]" />
                  {role === "customer" && <CheckCircle2 className="w-4 h-4 text-[#FF385C]" />}
                </div>
                <div className="mt-2">
                  <p className="font-bold text-gray-900">Khách hàng</p>
                  <p className="text-[10px] text-gray-500">Tìm & Đặt phòng</p>
                </div>
              </button>

              <button
                type="button"
                onClick={() => setRole("host")}
                className={`p-3 rounded-2xl border text-left flex flex-col justify-between transition-all ${
                  role === "host"
                    ? "border-emerald-600 bg-emerald-50/50 shadow-sm"
                    : "border-gray-200 hover:border-gray-300"
                }`}
              >
                <div className="flex items-center justify-between w-full">
                  <Building2 className="w-4 h-4 text-emerald-600" />
                  {role === "host" && <CheckCircle2 className="w-4 h-4 text-emerald-600" />}
                </div>
                <div className="mt-2">
                  <p className="font-bold text-gray-900">Chủ sở hữu (Host)</p>
                  <p className="text-[10px] text-gray-500">Đăng & Quản lý chỗ ở</p>
                </div>
              </button>
            </div>
          </div>

          <div>
            <label className="font-bold text-gray-700 block mb-1">Họ và tên *</label>
            <div className="relative">
              <User className="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Ví dụ: Nguyễn Văn An"
                className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-2xl text-xs font-semibold outline-none focus:border-gray-900 bg-white"
              />
            </div>
          </div>

          <div>
            <label className="font-bold text-gray-700 block mb-1">Email đăng nhập *</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
                className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-2xl text-xs font-semibold outline-none focus:border-gray-900 bg-white"
              />
            </div>
          </div>

          <div>
            <label className="font-bold text-gray-700 block mb-1">Số điện thoại</label>
            <div className="relative">
              <Phone className="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="0901234567"
                className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-2xl text-xs font-semibold outline-none focus:border-gray-900 bg-white"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="font-bold text-gray-700 block mb-1">Mật khẩu *</label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Ít nhất 6 ký tự"
                className="w-full px-3.5 py-2.5 border border-gray-300 rounded-2xl text-xs font-semibold outline-none focus:border-gray-900 bg-white"
              />
            </div>

            <div>
              <label className="font-bold text-gray-700 block mb-1">Nhập lại *</label>
              <input
                type="password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Xác nhận lại"
                className="w-full px-3.5 py-2.5 border border-gray-300 rounded-2xl text-xs font-semibold outline-none focus:border-gray-900 bg-white"
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
                <span>Hoàn tất đăng ký & Vào Workspace</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Switch to Login */}
        <div className="pt-4 border-t border-gray-100 text-center">
          <p className="text-xs text-gray-500">
            Đã có tài khoản?{" "}
            <button
              onClick={() => setCurrentView("login")}
              className="font-bold text-[#FF385C] hover:underline"
            >
              Đăng nhập ngay
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}
