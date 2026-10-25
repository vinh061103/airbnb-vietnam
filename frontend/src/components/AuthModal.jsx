import React, { useState } from "react";
import { useApp } from "../context/AppContext";
import { SAMPLE_ACCOUNTS, INITIAL_USER, INITIAL_HOST } from "../data/initialData";
import {
  X,
  User,
  Building2,
  CheckCircle2,
  Lock,
  Mail,
  ShieldCheck,
  ArrowRight,
  Sparkles,
} from "lucide-react";

export default function AuthModal({ isOpen, onClose }) {
  const { user, setUser, switchRole } = useApp();

  const [activeTab, setActiveTab] = useState("quick"); // 'quick' | 'form'
  const [formMode, setFormMode] = useState("login"); // 'login' | 'register'
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [selectedRole, setSelectedRole] = useState("customer"); // 'customer' | 'host'

  if (!isOpen) return null;

  const handleSelectAccount = (account) => {
    if (account.id === 1) {
      setUser({
        ...INITIAL_USER,
        currentRole: "customer",
      });
      switchRole("customer");
    } else {
      setUser({
        ...INITIAL_HOST,
        currentRole: "host",
      });
      switchRole("host");
    }
    onClose();
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    if (!email || !password) {
      alert("Vui lòng điền đầy đủ email và mật khẩu!");
      return;
    }

    const newUser = {
      id: Date.now(),
      full_name: fullName || (email.split("@")[0].toUpperCase()),
      email,
      avatar_url:
        selectedRole === "host"
          ? "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=300&q=80"
          : "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80",
      currentRole: selectedRole,
      isHost: selectedRole === "host",
      createdAt: new Date().toISOString().split("T")[0],
    };

    setUser(newUser);
    switchRole(selectedRole);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-in fade-in">
      <div className="bg-white rounded-3xl w-full max-w-lg shadow-2xl overflow-hidden border border-gray-100 flex flex-col max-h-[92vh]">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-[#FF385C]" />
            <h3 className="font-extrabold text-gray-900 text-base">
              Đăng nhập & Phân quyền Workspace
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 rounded-full text-gray-400 hover:text-gray-700 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab switch */}
        <div className="px-6 pt-4 pb-2 flex border-b border-gray-100 gap-2 bg-gray-50/50">
          <button
            onClick={() => setActiveTab("quick")}
            className={`flex-1 py-2 text-xs font-bold rounded-xl transition-all ${
              activeTab === "quick"
                ? "bg-white text-gray-900 shadow-sm border border-gray-200"
                : "text-gray-500 hover:text-gray-900"
            }`}
          >
            ⚡ Đăng nhập 1-Click (2 Vai trò)
          </button>
          <button
            onClick={() => setActiveTab("form")}
            className={`flex-1 py-2 text-xs font-bold rounded-xl transition-all ${
              activeTab === "form"
                ? "bg-white text-gray-900 shadow-sm border border-gray-200"
                : "text-gray-500 hover:text-gray-900"
            }`}
          >
            🔐 Email & Mật khẩu
          </button>
        </div>

        {/* Body Content */}
        <div className="p-6 overflow-y-auto space-y-5">
          {activeTab === "quick" ? (
            <div className="space-y-4">
              <p className="text-xs text-gray-500">
                Chọn ngay một trong hai tài khoản mẫu được cấu hình sẵn theo đặc tả SRS để kiểm thử toàn diện cả 2 giao diện:
              </p>

              {/* Account 1: Customer */}
              <div
                onClick={() => handleSelectAccount(SAMPLE_ACCOUNTS[0])}
                className={`p-4 rounded-2xl border-2 cursor-pointer transition-all flex items-start gap-4 ${
                  user.email === "an.nguyen@example.com"
                    ? "border-[#FF385C] bg-rose-50/40 shadow-sm"
                    : "border-gray-200 hover:border-gray-400 hover:bg-gray-50"
                }`}
              >
                <img
                  src={SAMPLE_ACCOUNTS[0].avatar_url}
                  alt="Customer"
                  className="w-14 h-14 rounded-2xl object-cover border-2 border-white shadow-sm flex-shrink-0"
                />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <h4 className="font-bold text-gray-900 text-sm">
                      {SAMPLE_ACCOUNTS[0].full_name}
                    </h4>
                    <span className="text-[10px] font-black uppercase tracking-wider text-rose-700 bg-rose-100 px-2 py-0.5 rounded-full">
                      Customer
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 truncate mt-0.5">
                    {SAMPLE_ACCOUNTS[0].email}
                  </p>
                  <p className="text-xs text-gray-600 mt-2 line-clamp-2 leading-relaxed">
                    Trải nghiệm tìm phòng, đặt phòng nhanh, quét mã VietQR, xem vé đơn đặt, danh sách yêu thích & gửi đánh giá sau lưu trú.
                  </p>
                  <div className="mt-3 flex items-center gap-1.5 text-xs font-bold text-[#FF385C]">
                    <span>Vào Customer Workspace</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </div>
                </div>
              </div>

              {/* Account 2: Host */}
              <div
                onClick={() => handleSelectAccount(SAMPLE_ACCOUNTS[1])}
                className={`p-4 rounded-2xl border-2 cursor-pointer transition-all flex items-start gap-4 ${
                  user.email === "thao.le@homestay.vn"
                    ? "border-[#FF385C] bg-rose-50/40 shadow-sm"
                    : "border-gray-200 hover:border-gray-400 hover:bg-gray-50"
                }`}
              >
                <img
                  src={SAMPLE_ACCOUNTS[1].avatar_url}
                  alt="Host"
                  className="w-14 h-14 rounded-2xl object-cover border-2 border-white shadow-sm flex-shrink-0"
                />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <h4 className="font-bold text-gray-900 text-sm">
                      {SAMPLE_ACCOUNTS[1].full_name}
                    </h4>
                    <span className="text-[10px] font-black uppercase tracking-wider text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded-full">
                      Host Workspace
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 truncate mt-0.5">
                    {SAMPLE_ACCOUNTS[1].email}
                  </p>
                  <p className="text-xs text-gray-600 mt-2 line-clamp-2 leading-relaxed">
                    Quản lý 14 chỗ ở khắp Việt Nam, biểu đồ doanh thu triệu đồng, theo dõi đơn đặt của khách, quản lý lịch trống và chặn ngày bận.
                  </p>
                  <div className="mt-3 flex items-center gap-1.5 text-xs font-bold text-emerald-600">
                    <span>Vào Host Workspace</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <form onSubmit={handleFormSubmit} className="space-y-4 text-xs">
              <div className="flex bg-gray-100 p-1 rounded-xl">
                <button
                  type="button"
                  onClick={() => setFormMode("login")}
                  className={`flex-1 py-1.5 font-bold rounded-lg transition-all ${
                    formMode === "login" ? "bg-white text-gray-900 shadow-sm" : "text-gray-500"
                  }`}
                >
                  Đăng nhập
                </button>
                <button
                  type="button"
                  onClick={() => setFormMode("register")}
                  className={`flex-1 py-1.5 font-bold rounded-lg transition-all ${
                    formMode === "register" ? "bg-white text-gray-900 shadow-sm" : "text-gray-500"
                  }`}
                >
                  Đăng ký mới
                </button>
              </div>

              {formMode === "register" && (
                <div>
                  <label className="font-bold text-gray-700 block mb-1">
                    Họ và tên của bạn
                  </label>
                  <input
                    type="text"
                    required
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="Nguyễn Văn A"
                    className="w-full border border-gray-300 rounded-xl px-3.5 py-2.5 text-xs outline-none focus:border-gray-900"
                  />
                </div>
              )}

              <div>
                <label className="font-bold text-gray-700 block mb-1">Email</label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="email@example.com"
                    className="w-full pl-9 pr-3.5 py-2.5 border border-gray-300 rounded-xl text-xs outline-none focus:border-gray-900"
                  />
                </div>
              </div>

              <div>
                <label className="font-bold text-gray-700 block mb-1">Mật khẩu</label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full pl-9 pr-3.5 py-2.5 border border-gray-300 rounded-xl text-xs outline-none focus:border-gray-900"
                  />
                </div>
              </div>

              <div>
                <label className="font-bold text-gray-700 block mb-1.5">
                  Chọn vai trò khởi đầu
                </label>
                <div className="grid grid-cols-2 gap-3">
                  <button
                    type="button"
                    onClick={() => setSelectedRole("customer")}
                    className={`p-3 rounded-xl border text-left flex items-center justify-between ${
                      selectedRole === "customer"
                        ? "border-[#FF385C] bg-rose-50 text-gray-900 font-bold"
                        : "border-gray-200 text-gray-600"
                    }`}
                  >
                    <span>Khách đặt phòng</span>
                    {selectedRole === "customer" && (
                      <CheckCircle2 className="w-4 h-4 text-[#FF385C]" />
                    )}
                  </button>

                  <button
                    type="button"
                    onClick={() => setSelectedRole("host")}
                    className={`p-3 rounded-xl border text-left flex items-center justify-between ${
                      selectedRole === "host"
                        ? "border-emerald-600 bg-emerald-50 text-gray-900 font-bold"
                        : "border-gray-200 text-gray-600"
                    }`}
                  >
                    <span>Chủ nhà (Host)</span>
                    {selectedRole === "host" && (
                      <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                    )}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                className="w-full mt-2 bg-gradient-to-r from-[#FF385C] to-[#E00B41] hover:opacity-95 text-white font-extrabold py-3 rounded-xl text-xs shadow-md transition-all active:scale-95"
              >
                {formMode === "login" ? "Đăng nhập ngay" : "Tạo tài khoản & Bắt đầu"}
              </button>
            </form>
          )}
        </div>

        {/* Footer info */}
        <div className="px-6 py-3 bg-gray-50 border-t border-gray-100 flex items-center justify-between text-[11px] text-gray-500">
          <span className="flex items-center gap-1">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
            Bảo mật phân quyền RBAC
          </span>
          <span>Dữ liệu lưu tự động vào trình duyệt</span>
        </div>
      </div>
    </div>
  );
}
