import React, { useState } from "react";
import { useApp } from "../context/AppContext";
import {
  Search,
  Menu,
  Heart,
  Luggage,
  MessageSquare,
  LayoutDashboard,
  Home,
  PlusCircle,
  Calendar,
  Compass,
  LogIn,
  UserPlus,
  LogOut,
  User,
  Building2,
} from "lucide-react";

export default function Navbar() {
  const {
    user,
    role,
    currentView,
    setCurrentView,
    wishlist,
    handleLogout,
  } = useApp();

  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Logo Airbnb */}
          <div
            onClick={() => {
              if (role === "host") {
                setCurrentView("host-dashboard");
              } else {
                setCurrentView("home");
              }
            }}
            className="flex items-center gap-2.5 cursor-pointer group flex-shrink-0"
          >
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-[#FF385C] to-[#E00B41] flex items-center justify-center text-white shadow-md group-hover:scale-105 transition-transform">
              <Compass className="w-6 h-6 stroke-[2.5]" />
            </div>
            <div className="flex flex-col">
              <span className="text-2xl font-black tracking-tight text-[#FF385C]">
                airbnb
              </span>
              <span className="text-xs -mt-0.5 font-bold text-gray-500 uppercase tracking-widest flex items-center gap-1">
                {role === "host" ? (
                  <span className="text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded font-extrabold">
                    Chủ sở hữu (Host)
                  </span>
                ) : (
                  <span>Khách hàng</span>
                )}
              </span>
            </div>
          </div>

          {/* Quick Search Bar (Customer Mode Only) */}
          {role === "customer" && currentView !== "home" && currentView !== "login" && currentView !== "register" && (
            <div
              onClick={() => setCurrentView("home")}
              className="hidden md:flex items-center border border-gray-300 rounded-full py-2.5 px-4 shadow-sm hover:shadow-md transition-shadow cursor-pointer divide-x divide-gray-200 text-sm font-semibold"
            >
              <span className="px-3 text-gray-900">Địa điểm bất kỳ</span>
              <span className="px-3 text-gray-900">Tuần bất kỳ</span>
              <div className="pl-3 flex items-center gap-2 text-gray-500">
                <span>Thêm khách</span>
                <div className="w-7 h-7 rounded-full bg-[#FF385C] flex items-center justify-center text-white">
                  <Search className="w-3.5 h-3.5 stroke-[3]" />
                </div>
              </div>
            </div>
          )}

          {/* Host Mode Navigation Tabs */}
          {role === "host" && (
            <div className="hidden lg:flex items-center gap-1.5 bg-gray-100 p-1.5 rounded-full text-sm font-bold">
              <button
                onClick={() => setCurrentView("host-dashboard")}
                className={`px-4 py-2 rounded-full transition-all ${
                  currentView === "host-dashboard"
                    ? "bg-white text-gray-900 shadow-sm"
                    : "text-gray-600 hover:text-gray-900"
                }`}
              >
                Tổng quan Doanh thu
              </button>
              <button
                onClick={() => setCurrentView("host-listings")}
                className={`px-4 py-2 rounded-full transition-all ${
                  currentView === "host-listings" || currentView === "host-new-listing"
                    ? "bg-white text-gray-900 shadow-sm"
                    : "text-gray-600 hover:text-gray-900"
                }`}
              >
                Chỗ ở của tôi
              </button>
              <button
                onClick={() => setCurrentView("host-reservations")}
                className={`px-4 py-2 rounded-full transition-all ${
                  currentView === "host-reservations"
                    ? "bg-white text-gray-900 shadow-sm"
                    : "text-gray-600 hover:text-gray-900"
                }`}
              >
                Đơn đặt phòng
              </button>
              <button
                onClick={() => setCurrentView("host-calendar")}
                className={`px-4 py-2 rounded-full transition-all ${
                  currentView === "host-calendar"
                    ? "bg-white text-gray-900 shadow-sm"
                    : "text-gray-600 hover:text-gray-900"
                }`}
              >
                Lịch trống & Chặn ngày
              </button>
            </div>
          )}

          {/* Right Actions */}
          <div className="flex items-center gap-2 sm:gap-3 flex-shrink-0">
            {/* If NOT logged in */}
            {!user ? (
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setCurrentView("login")}
                  className="flex items-center gap-1.5 text-sm font-bold text-gray-800 hover:bg-gray-100 px-4 py-2.5 rounded-full transition-colors border border-gray-300"
                >
                  <LogIn className="w-4 h-4" />
                  <span>Đăng nhập</span>
                </button>

                <button
                  onClick={() => setCurrentView("register")}
                  className="flex items-center gap-1.5 text-sm font-extrabold text-white bg-gradient-to-r from-[#FF385C] to-[#E00B41] hover:brightness-105 active:scale-95 px-5 py-2.5 rounded-full shadow-sm transition-all"
                >
                  <UserPlus className="w-4 h-4" />
                  <span>Đăng ký</span>
                </button>
              </div>
            ) : (
              /* If LOGGED IN */
              <>
                {/* Customer Shortcuts */}
                {role === "customer" && (
                  <>
                    <button
                      onClick={() => setCurrentView("wishlist")}
                      className="relative p-2.5 hover:bg-gray-100 rounded-full text-gray-700 transition-colors"
                      title="Danh sách yêu thích"
                    >
                      <Heart className="w-5 h-5 text-gray-700 hover:text-[#FF385C]" />
                      {wishlist.length > 0 && (
                        <span className="absolute top-1 right-1 w-4 h-4 bg-[#FF385C] text-white text-[10px] font-bold rounded-full flex items-center justify-center">
                          {wishlist.length}
                        </span>
                      )}
                    </button>

                    <button
                      onClick={() => setCurrentView("messages")}
                      className="relative p-2.5 hover:bg-gray-100 rounded-full text-gray-700 transition-colors"
                      title="Tin nhắn"
                    >
                      <MessageSquare className="w-5 h-5 text-gray-700" />
                      <span className="absolute top-1 right-1 w-2 h-2 bg-[#FF385C] rounded-full" />
                    </button>
                  </>
                )}

                {/* Host Messages */}
                {role === "host" && (
                  <button
                    onClick={() => setCurrentView("messages")}
                    className="relative p-2.5 hover:bg-gray-100 rounded-full text-gray-700 transition-colors"
                    title="Tin nhắn của chủ nhà"
                  >
                    <MessageSquare className="w-5 h-5 text-gray-700" />
                    <span className="absolute top-1 right-1 w-2 h-2 bg-[#FF385C] rounded-full" />
                  </button>
                )}

                {/* User Menu */}
                <div className="relative">
                  <button
                    onClick={() => setMenuOpen(!menuOpen)}
                    className="flex items-center gap-2 border border-gray-300 rounded-full p-1 pl-3 hover:shadow-md transition-shadow"
                  >
                    <Menu className="w-4 h-4 text-gray-600" />
                    <img
                      src={user.avatar_url || "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80"}
                      alt={user.full_name}
                      className="w-8 h-8 rounded-full object-cover border border-gray-200"
                    />
                  </button>

                  {/* Dropdown Menu */}
                  {menuOpen && (
                    <div
                      className="absolute right-0 mt-2 w-64 bg-white rounded-3xl shadow-2xl border border-gray-100 py-2.5 z-50 text-xs text-gray-700 animate-in fade-in slide-in-from-top-2"
                      onClick={() => setMenuOpen(false)}
                    >
                      <div className="px-5 py-3 border-b border-gray-100 bg-gray-50/50">
                        <p className="font-extrabold text-gray-900 text-sm truncate">{user.full_name}</p>
                        <p className="text-[11px] text-gray-500 truncate">{user.email}</p>
                        <span
                          className={`inline-block mt-1 px-2.5 py-0.5 text-[10px] font-bold rounded-full ${
                            role === "host"
                              ? "bg-emerald-100 text-emerald-800"
                              : "bg-rose-100 text-rose-800"
                          }`}
                        >
                          {role === "host" ? "Chủ sở hữu (Host Workspace)" : "Khách hàng"}
                        </span>
                      </div>

                      {role === "customer" ? (
                        <div className="py-1">
                          <button
                            onClick={() => setCurrentView("my-bookings")}
                            className="w-full text-left px-5 py-2.5 hover:bg-gray-50 flex items-center gap-3 font-semibold text-gray-800"
                          >
                            <Luggage className="w-4 h-4 text-gray-500" />
                            Chuyến đi của tôi (C07)
                          </button>
                          <button
                            onClick={() => setCurrentView("wishlist")}
                            className="w-full text-left px-5 py-2.5 hover:bg-gray-50 flex items-center gap-3 font-semibold text-gray-800"
                          >
                            <Heart className="w-4 h-4 text-gray-500" />
                            Danh sách yêu thích (C09)
                          </button>
                          <button
                            onClick={() => setCurrentView("messages")}
                            className="w-full text-left px-5 py-2.5 hover:bg-gray-50 flex items-center gap-3 font-semibold text-gray-800"
                          >
                            <MessageSquare className="w-4 h-4 text-gray-500" />
                            Tin nhắn trò chuyện (C10)
                          </button>
                        </div>
                      ) : (
                        <div className="py-1">
                          <button
                            onClick={() => setCurrentView("host-dashboard")}
                            className="w-full text-left px-5 py-2.5 hover:bg-gray-50 flex items-center gap-3 font-semibold text-gray-800"
                          >
                            <LayoutDashboard className="w-4 h-4 text-gray-500" />
                            Bảng điều khiển Doanh thu
                          </button>
                          <button
                            onClick={() => setCurrentView("host-listings")}
                            className="w-full text-left px-5 py-2.5 hover:bg-gray-50 flex items-center gap-3 font-semibold text-gray-800"
                          >
                            <Home className="w-4 h-4 text-gray-500" />
                            Chỗ ở của tôi ({20})
                          </button>
                          <button
                            onClick={() => setCurrentView("host-new-listing")}
                            className="w-full text-left px-5 py-2.5 hover:bg-gray-50 flex items-center gap-3 font-semibold text-gray-800"
                          >
                            <PlusCircle className="w-4 h-4 text-gray-500" />
                            Đăng phòng mới
                          </button>
                          <button
                            onClick={() => setCurrentView("host-calendar")}
                            className="w-full text-left px-5 py-2.5 hover:bg-gray-50 flex items-center gap-3 font-semibold text-gray-800"
                          >
                            <Calendar className="w-4 h-4 text-gray-500" />
                            Lịch trống & Chặn ngày
                          </button>
                        </div>
                      )}

                      <div className="border-t border-gray-100 my-1" />

                      <button
                        onClick={handleLogout}
                        className="w-full text-left px-5 py-2.5 hover:bg-red-50 text-red-600 font-bold flex items-center gap-3"
                      >
                        <LogOut className="w-4 h-4" />
                        Đăng xuất tài khoản
                      </button>
                    </div>
                  )}
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
