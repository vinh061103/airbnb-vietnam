import React, { useState } from "react";
import { useApp } from "../context/AppContext";
import {
  Search,
  MapPin,
  Calendar,
  Users,
  SlidersHorizontal,
  X,
  AlertCircle,
  CheckCircle2,
} from "lucide-react";

export default function HeroSearch({ onOpenFilter }) {
  const {
    searchParams,
    setSearchParams,
    setActiveSearch,
    setCurrentView,
  } = useApp();

  const [activeTab, setActiveTab] = useState(null); // 'where' | 'checkin' | 'checkout' | 'guests'
  const [errorMessage, setErrorMessage] = useState("");

  const popularCities = [
    "Hồ Chí Minh",
    "Hà Nội",
    "Đà Lạt",
    "Đà Nẵng",
    "Phú Quốc",
    "Hội An",
    "Sa Pa",
    "Nha Trang",
    "Vũng Tàu",
    "Ninh Bình",
    "Quy Nhơn",
    "Huế",
    "Mộc Châu",
  ];

  const todayStr = new Date().toISOString().split("T")[0];

  const handleSearch = () => {
    setErrorMessage("");

    const missing = [];
    if (!searchParams.city || !searchParams.city.trim() || searchParams.city === "Tất cả điểm đến") {
      missing.push("Địa điểm");
    }
    if (!searchParams.checkIn) {
      missing.push("Ngày nhận phòng");
    }
    if (!searchParams.checkOut) {
      missing.push("Ngày trả phòng");
    }

    if (missing.length > 0) {
      setErrorMessage(
        `Vui lòng chọn đầy đủ: ${missing.join(", ")} và Số lượng khách trước khi bấm Tìm kiếm!`
      );
      if (!searchParams.city || searchParams.city === "Tất cả điểm đến") {
        setActiveTab("where");
      } else if (!searchParams.checkIn) {
        setActiveTab("checkin");
      } else if (!searchParams.checkOut) {
        setActiveTab("checkout");
      }
      return;
    }

    // Check date logic
    const start = new Date(searchParams.checkIn);
    const end = new Date(searchParams.checkOut);
    if (end <= start) {
      setErrorMessage("Ngày trả phòng phải sau ngày nhận phòng ít nhất 1 đêm!");
      setActiveTab("checkout");
      return;
    }

    const nights = Math.max(
      1,
      Math.round((end - start) / (1000 * 60 * 60 * 24))
    );

    // Set active search state
    setActiveSearch({
      city: searchParams.city.trim(),
      checkIn: searchParams.checkIn,
      checkOut: searchParams.checkOut,
      guests: searchParams.guests || 1,
      nights,
    });

    setActiveTab(null);
    setErrorMessage("");
    // Navigate to Search Results page
    setCurrentView("search-results");
  };

  const clearSelection = () => {
    setSearchParams((prev) => ({
      ...prev,
      city: "",
      checkIn: "",
      checkOut: "",
      guests: 1,
    }));
    setErrorMessage("");
  };

  return (
    <div className="relative py-4 px-3 sm:px-4">
      <div className="max-w-5xl mx-auto">
        {/* Main Pill Search Bar */}
        <div className="bg-white rounded-full shadow-lg hover:shadow-xl border border-gray-200 p-2 sm:p-2.5 flex flex-col md:flex-row items-center transition-all">
          {/* Destination */}
          <div
            className={`flex-1 w-full px-4 sm:px-6 py-2 rounded-full cursor-pointer transition-colors ${
              activeTab === "where" ? "bg-gray-100 ring-2 ring-rose-300" : "hover:bg-gray-50"
            }`}
            onClick={() => {
              setErrorMessage("");
              setActiveTab(activeTab === "where" ? null : "where");
            }}
          >
            <div className="flex items-center gap-1.5 text-[#FF385C]">
              <MapPin className="w-4 h-4" />
              <span className="text-xs font-extrabold uppercase tracking-wider text-gray-800">
                1. Địa điểm
              </span>
            </div>
            <p className="text-sm font-bold text-gray-900 truncate mt-0.5">
              {searchParams.city || "Chọn điểm đến (Hồ Chí Minh, Đà Lạt...)"}
            </p>
          </div>

          <div className="hidden md:block w-px h-8 bg-gray-200" />

          {/* Check-in */}
          <div
            className={`w-full md:w-40 lg:w-44 px-3 sm:px-4 py-2 rounded-full cursor-pointer transition-colors ${
              activeTab === "checkin" ? "bg-gray-100 ring-2 ring-rose-300" : "hover:bg-gray-50"
            }`}
            onClick={() => {
              setErrorMessage("");
              setActiveTab(activeTab === "checkin" ? null : "checkin");
            }}
          >
            <div className="flex items-center gap-1.5 text-[#FF385C]">
              <Calendar className="w-4 h-4" />
              <span className="text-xs font-extrabold uppercase tracking-wider text-gray-800">
                2. Nhận phòng
              </span>
            </div>
            <input
              type="date"
              min={todayStr}
              value={searchParams.checkIn}
              onChange={(e) => {
                setErrorMessage("");
                setSearchParams((prev) => ({ ...prev, checkIn: e.target.value }));
              }}
              className="w-full text-sm font-bold text-gray-900 bg-transparent outline-none cursor-pointer mt-0.5"
            />
          </div>

          <div className="hidden md:block w-px h-8 bg-gray-200" />

          {/* Check-out */}
          <div
            className={`w-full md:w-40 lg:w-44 px-3 sm:px-4 py-2 rounded-full cursor-pointer transition-colors ${
              activeTab === "checkout" ? "bg-gray-100 ring-2 ring-rose-300" : "hover:bg-gray-50"
            }`}
            onClick={() => {
              setErrorMessage("");
              setActiveTab(activeTab === "checkout" ? null : "checkout");
            }}
          >
            <div className="flex items-center gap-1.5 text-[#FF385C]">
              <Calendar className="w-4 h-4" />
              <span className="text-xs font-extrabold uppercase tracking-wider text-gray-800">
                3. Trả phòng
              </span>
            </div>
            <input
              type="date"
              min={searchParams.checkIn || todayStr}
              value={searchParams.checkOut}
              onChange={(e) => {
                setErrorMessage("");
                setSearchParams((prev) => ({ ...prev, checkOut: e.target.value }));
              }}
              className="w-full text-sm font-bold text-gray-900 bg-transparent outline-none cursor-pointer mt-0.5"
            />
          </div>

          <div className="hidden md:block w-px h-8 bg-gray-200" />

          {/* Guests & Action Buttons */}
          <div className="w-full md:w-auto pl-3 pr-1 py-1 flex items-center justify-between gap-2 sm:gap-3 flex-shrink-0">
            <div
              className={`cursor-pointer px-3 py-1.5 rounded-full transition-colors ${
                activeTab === "guests" ? "bg-gray-100 ring-2 ring-rose-300" : "hover:bg-gray-50"
              }`}
              onClick={() => {
                setErrorMessage("");
                setActiveTab(activeTab === "guests" ? null : "guests");
              }}
            >
              <div className="flex items-center gap-1.5 text-[#FF385C]">
                <Users className="w-4 h-4" />
                <span className="text-xs font-extrabold uppercase tracking-wider text-gray-800">
                  4. Khách
                </span>
              </div>
              <p className="text-sm font-bold text-gray-900 whitespace-nowrap mt-0.5">
                {searchParams.guests} khách
              </p>
            </div>

            {/* Filter icon button */}
            {onOpenFilter && (
              <button
                onClick={onOpenFilter}
                className="p-2.5 rounded-full hover:bg-gray-100 border border-gray-200 text-gray-700 transition-colors flex-shrink-0"
                title="Bộ lọc nâng cao"
              >
                <SlidersHorizontal className="w-4 h-4" />
              </button>
            )}

            {/* Red Search Pill Button */}
            <button
              onClick={handleSearch}
              className="bg-gradient-to-r from-[#FF385C] to-[#E00B41] hover:brightness-105 active:scale-95 text-white font-extrabold py-3 px-5 sm:px-6 rounded-full flex items-center gap-2 shadow-md transition-all flex-shrink-0 whitespace-nowrap text-sm"
            >
              <Search className="w-4 h-4 stroke-[2.5]" />
              <span>Tìm kiếm</span>
            </button>
          </div>
        </div>

        {/* Validation Error Banner */}
        {errorMessage && (
          <div className="mt-3.5 bg-rose-50 border border-rose-300 rounded-2xl p-3 sm:p-4 text-rose-800 flex items-center justify-between gap-3 shadow-md animate-in fade-in slide-in-from-top-2">
            <div className="flex items-center gap-2.5">
              <AlertCircle className="w-5 h-5 flex-shrink-0 text-[#FF385C]" />
              <p className="text-xs sm:text-sm font-bold">{errorMessage}</p>
            </div>
            <button
              onClick={() => setErrorMessage("")}
              className="p-1 rounded-full hover:bg-rose-100 text-rose-600 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* Dropdown Destination Picker */}
        {activeTab === "where" && (
          <div className="absolute left-1/2 -translate-x-1/2 top-24 w-full max-w-xl bg-white rounded-3xl shadow-2xl border border-gray-100 p-5 z-40 animate-in fade-in zoom-in-95">
            <div className="flex items-center justify-between mb-3 pb-2 border-b border-gray-100">
              <span className="text-xs font-bold uppercase tracking-wider text-gray-700">
                1. Chọn điểm đến tại Việt Nam
              </span>
              <button
                onClick={() => setActiveTab(null)}
                className="p-1 hover:bg-gray-100 rounded-full text-gray-400 hover:text-gray-700"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Text input to search or type custom city */}
            <div className="relative mb-3">
              <input
                type="text"
                placeholder="Gõ tên thành phố hoặc chọn bên dưới..."
                value={searchParams.city}
                onChange={(e) =>
                  setSearchParams((prev) => ({ ...prev, city: e.target.value }))
                }
                className="w-full pl-9 pr-4 py-2.5 rounded-xl border border-gray-200 text-sm font-semibold focus:border-[#FF385C] focus:ring-1 focus:ring-[#FF385C] outline-none"
              />
              <Search className="w-4 h-4 text-gray-400 absolute left-3 top-3" />
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 max-h-56 overflow-y-auto pr-1">
              {popularCities.map((c) => (
                <button
                  key={c}
                  onClick={() => {
                    setSearchParams((prev) => ({
                      ...prev,
                      city: c,
                    }));
                    setActiveTab("checkin"); // Auto step to next
                  }}
                  className={`text-left px-3 py-2.5 rounded-xl text-xs font-semibold transition-all flex items-center gap-2 ${
                    searchParams.city === c
                      ? "bg-rose-50 text-[#FF385C] border border-rose-300 font-bold"
                      : "hover:bg-gray-50 text-gray-700 border border-gray-100"
                  }`}
                >
                  <MapPin className="w-3.5 h-3.5 text-gray-400 flex-shrink-0" />
                  <span className="truncate">{c}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Dropdown Guests Picker */}
        {activeTab === "guests" && (
          <div className="absolute right-4 top-24 w-72 bg-white rounded-3xl shadow-2xl border border-gray-100 p-5 z-40 animate-in fade-in zoom-in-95">
            <div className="flex items-center justify-between pb-3 border-b border-gray-100">
              <div>
                <p className="font-semibold text-gray-900 text-sm">Số lượng khách</p>
                <p className="text-xs text-gray-500">Từ 1 tuổi trở lên</p>
              </div>
              <div className="flex items-center gap-3">
                <button
                  disabled={searchParams.guests <= 1}
                  onClick={() =>
                    setSearchParams((prev) => ({
                      ...prev,
                      guests: Math.max(1, prev.guests - 1),
                    }))
                  }
                  className="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center text-gray-600 disabled:opacity-40 disabled:cursor-not-allowed hover:border-gray-900 font-bold"
                >
                  -
                </button>
                <span className="font-bold text-gray-900 text-sm w-4 text-center">
                  {searchParams.guests}
                </span>
                <button
                  disabled={searchParams.guests >= 20}
                  onClick={() =>
                    setSearchParams((prev) => ({
                      ...prev,
                      guests: prev.guests + 1,
                    }))
                  }
                  className="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center text-gray-600 disabled:opacity-40 disabled:cursor-not-allowed hover:border-gray-900 font-bold"
                >
                  +
                </button>
              </div>
            </div>
            <button
              onClick={() => setActiveTab(null)}
              className="mt-4 w-full bg-gray-900 text-white font-semibold py-2.5 rounded-xl text-xs hover:bg-black transition-colors"
            >
              Xác nhận số khách ({searchParams.guests} khách)
            </button>
          </div>
        )}

        {/* Quick Clear helper if any field is filled */}
        {(searchParams.city || searchParams.checkIn || searchParams.checkOut) && (
          <div className="mt-2.5 flex items-center justify-center gap-2 text-xs text-gray-500">
            <span>Thông tin đang chọn:</span>
            {searchParams.city && (
              <span className="bg-gray-100 px-2.5 py-0.5 rounded-full font-semibold text-gray-800">
                📍 {searchParams.city}
              </span>
            )}
            {searchParams.checkIn && (
              <span className="bg-gray-100 px-2.5 py-0.5 rounded-full font-semibold text-gray-800">
                📅 {searchParams.checkIn}
              </span>
            )}
            {searchParams.checkOut && (
              <span className="bg-gray-100 px-2.5 py-0.5 rounded-full font-semibold text-gray-800">
                → {searchParams.checkOut}
              </span>
            )}
            <button
              onClick={clearSelection}
              className="text-[#FF385C] font-bold hover:underline ml-2"
            >
              Xóa thông tin
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
