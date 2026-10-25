import React from "react";
import { useApp } from "../context/AppContext";
import {
  Home,
  PlusCircle,
  Eye,
  EyeOff,
  Calendar,
  ExternalLink,
  MapPin,
  Star,
} from "lucide-react";

export default function HostListings() {
  const {
    listings,
    user,
    setCurrentView,
    setSelectedListingId,
    toggleListingStatus,
  } = useApp();

  const myListings = listings.filter((l) => l.host_id === user.id);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-gray-900 flex items-center gap-2">
            <Home className="w-8 h-8 text-[#FF385C]" />
            Quản lý chỗ ở của tôi
          </h1>
          <p className="text-xs sm:text-sm text-gray-500 mt-1">
            Danh sách tất cả phòng/biệt thự bạn đang sở hữu và quản lý (H02 / FR-08)
          </p>
        </div>

        <button
          onClick={() => setCurrentView("host-new-listing")}
          className="bg-gradient-to-r from-[#FF385C] to-[#E00B41] hover:opacity-95 text-white font-bold py-3 px-6 rounded-2xl text-xs sm:text-sm flex items-center gap-2 shadow-md transition-all active:scale-95"
        >
          <PlusCircle className="w-4 h-4" />
          Đăng phòng mới (UC-05)
        </button>
      </div>

      {myListings.length === 0 ? (
        <div className="bg-white border border-gray-200 rounded-3xl p-12 text-center space-y-4 max-w-xl mx-auto mt-6">
          <div className="w-16 h-16 bg-rose-50 text-[#FF385C] rounded-full flex items-center justify-center mx-auto">
            <Home className="w-8 h-8" />
          </div>
          <h3 className="font-bold text-gray-900 text-lg">
            Bạn chưa có chỗ ở nào trên hệ thống
          </h3>
          <p className="text-xs text-gray-500">
            Bắt đầu đăng căn hộ, biệt thự hoặc homestay của bạn để tiếp cận hàng ngàn khách hàng tiềm năng.
          </p>
          <button
            onClick={() => setCurrentView("host-new-listing")}
            className="bg-gray-900 hover:bg-black text-white font-bold py-3 px-6 rounded-2xl text-xs shadow-md transition-all"
          >
            Đăng chỗ ở đầu tiên ngay
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {myListings.map((l) => (
            <div
              key={l.id}
              className="bg-white border border-gray-200 rounded-3xl overflow-hidden shadow-sm hover:shadow-md transition-all flex flex-col"
            >
              <div className="relative aspect-video w-full bg-gray-100">
                <img
                  src={l.cover_image}
                  alt={l.title}
                  className="w-full h-full object-cover"
                />
                <span
                  className={`absolute top-3 left-3 text-[10px] font-black uppercase px-2.5 py-1 rounded-full shadow-sm ${
                    l.status === "Published"
                      ? "bg-emerald-500 text-white"
                      : "bg-gray-800 text-white"
                  }`}
                >
                  {l.status === "Published" ? "Đang xuất bản" : "Đã tạm ẩn"}
                </span>

                <div className="absolute top-3 right-3 bg-white/90 backdrop-blur-sm px-2 py-0.5 rounded-full flex items-center gap-1 text-xs font-bold text-gray-900 shadow">
                  <Star className="w-3.5 h-3.5 fill-current" />
                  <span>{l.rating ? l.rating.toFixed(2) : "Mới"}</span>
                </div>
              </div>

              <div className="p-5 flex-1 flex flex-col justify-between space-y-4">
                <div className="space-y-1">
                  <span className="text-[10px] font-bold text-gray-400 uppercase">
                    {l.property_type} • {l.capacity} khách
                  </span>
                  <h3 className="font-bold text-gray-900 text-sm line-clamp-2">
                    {l.title}
                  </h3>
                  <p className="text-xs text-gray-500 flex items-center gap-1">
                    <MapPin className="w-3.5 h-3.5 text-gray-400" />
                    {l.address}
                  </p>
                  <p className="text-base font-black text-gray-900 pt-1">
                    {l.base_price.toLocaleString("vi-VN")} ₫
                    <span className="text-xs text-gray-500 font-normal"> / đêm</span>
                  </p>
                </div>

                {/* Actions */}
                <div className="pt-3 border-t border-gray-100 flex items-center justify-between gap-2 text-xs">
                  <button
                    onClick={() => toggleListingStatus(l.id)}
                    className={`flex items-center gap-1 px-3 py-2 rounded-xl font-bold border transition-colors ${
                      l.status === "Published"
                        ? "border-gray-200 text-gray-700 hover:bg-gray-50"
                        : "border-emerald-200 text-emerald-700 bg-emerald-50 hover:bg-emerald-100"
                    }`}
                  >
                    {l.status === "Published" ? (
                      <>
                        <EyeOff className="w-3.5 h-3.5" />
                        <span>Tạm ẩn</span>
                      </>
                    ) : (
                      <>
                        <Eye className="w-3.5 h-3.5" />
                        <span>Công khai</span>
                      </>
                    )}
                  </button>

                  <button
                    onClick={() => setCurrentView("host-calendar")}
                    className="flex items-center gap-1 px-3 py-2 rounded-xl border border-gray-200 text-gray-700 hover:bg-gray-50 font-bold transition-colors"
                  >
                    <Calendar className="w-3.5 h-3.5 text-[#FF385C]" />
                    <span>Lịch trống</span>
                  </button>

                  <button
                    onClick={() => {
                      setSelectedListingId(l.id);
                      setCurrentView("room-detail");
                    }}
                    className="flex items-center gap-1 px-3 py-2 rounded-xl bg-gray-900 hover:bg-black text-white font-bold transition-colors"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                    <span>Xem</span>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
