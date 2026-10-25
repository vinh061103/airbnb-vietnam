import React from "react";
import { useApp } from "../context/AppContext";
import {
  TrendingUp,
  DollarSign,
  CalendarCheck,
  Star,
  Users,
  PlusCircle,
  Home,
  ArrowUpRight,
  Luggage,
} from "lucide-react";

export default function HostDashboard() {
  const { listings, bookings, user, setCurrentView, setSelectedListingId } =
    useApp();

  // Filter listings & bookings of current host
  const hostListings = listings.filter((l) => l.host_id === user.id);
  const hostListingIds = hostListings.map((l) => l.id);

  const hostBookings = bookings.filter((b) =>
    hostListingIds.includes(b.listing_id)
  );

  const totalEarnings = hostBookings
    .filter((b) => b.status === "Confirmed" || b.status === "Completed")
    .reduce((sum, b) => sum + (b.subtotal || 0), 0);

  const confirmedBookingsCount = hostBookings.filter(
    (b) => b.status === "Confirmed"
  ).length;

  const avgRating =
    hostListings.length > 0
      ? (
          hostListings.reduce((sum, l) => sum + (l.rating || 5), 0) /
          hostListings.length
        ).toFixed(2)
      : "5.0";

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-gray-900 to-gray-800 rounded-3xl p-6 sm:p-8 text-white shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2">
          <span className="text-xs font-bold text-rose-400 uppercase tracking-widest bg-rose-950/60 px-3 py-1 rounded-full border border-rose-800">
            Bảng điều khiển chủ nhà
          </span>
          <h1 className="text-2xl sm:text-3xl font-black">
            Chào mừng trở lại, {user.full_name}!
          </h1>
          <p className="text-xs sm:text-sm text-gray-300 max-w-xl">
            Theo dõi tổng quan doanh thu, tình trạng các phòng cho thuê và đơn đặt phòng mới của khách hàng (H01 & H08).
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setCurrentView("host-new-listing")}
            className="bg-gradient-to-r from-[#FF385C] to-[#E00B41] hover:opacity-95 text-white font-bold py-3.5 px-6 rounded-2xl text-xs sm:text-sm flex items-center gap-2 shadow-lg transition-all active:scale-95"
          >
            <PlusCircle className="w-4 h-4" />
            Đăng phòng mới (UC-05)
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* KPI 1 */}
        <div className="bg-white border border-gray-200 rounded-3xl p-6 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-gray-500 uppercase">
              Tổng doanh thu
            </span>
            <div className="w-10 h-10 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <DollarSign className="w-5 h-5" />
            </div>
          </div>
          <p className="text-2xl font-black text-gray-900">
            {totalEarnings.toLocaleString("vi-VN")} ₫
          </p>
          <div className="flex items-center gap-1.5 text-xs text-emerald-600 font-semibold">
            <TrendingUp className="w-3.5 h-3.5" />
            <span>+18.5% so với tháng trước</span>
          </div>
        </div>

        {/* KPI 2 */}
        <div className="bg-white border border-gray-200 rounded-3xl p-6 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-gray-500 uppercase">
              Đơn đặt phòng mới
            </span>
            <div className="w-10 h-10 rounded-2xl bg-rose-50 text-[#FF385C] flex items-center justify-center">
              <CalendarCheck className="w-5 h-5" />
            </div>
          </div>
          <p className="text-2xl font-black text-gray-900">
            {confirmedBookingsCount} lượt
          </p>
          <p className="text-xs text-gray-500">Đã chốt giữ chỗ thành công</p>
        </div>

        {/* KPI 3 */}
        <div className="bg-white border border-gray-200 rounded-3xl p-6 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-gray-500 uppercase">
              Chỗ ở đang quản lý
            </span>
            <div className="w-10 h-10 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center">
              <Home className="w-5 h-5" />
            </div>
          </div>
          <p className="text-2xl font-black text-gray-900">
            {hostListings.length} căn
          </p>
          <p className="text-xs text-gray-500">
            {hostListings.filter((l) => l.status === "Published").length} căn đang hiển thị công khai
          </p>
        </div>

        {/* KPI 4 */}
        <div className="bg-white border border-gray-200 rounded-3xl p-6 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-gray-500 uppercase">
              Điểm đánh giá sao
            </span>
            <div className="w-10 h-10 rounded-2xl bg-amber-50 text-amber-500 flex items-center justify-center">
              <Star className="w-5 h-5 fill-current" />
            </div>
          </div>
          <p className="text-2xl font-black text-gray-900">{avgRating} / 5.0</p>
          <p className="text-xs text-amber-600 font-semibold">Đạt chuẩn Chủ nhà siêu cấp</p>
        </div>
      </div>

      {/* Monthly Earnings Chart Mockup */}
      <div className="bg-white border border-gray-200 rounded-3xl p-6 shadow-sm space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-gray-900">
              Biểu đồ tăng trưởng doanh thu 2026 (VND)
            </h3>
            <p className="text-xs text-gray-500">Thống kê theo 6 tháng gần nhất</p>
          </div>
          <span className="text-xs font-bold text-[#FF385C] bg-rose-50 px-3 py-1 rounded-full">
            Tỷ lệ lấp đầy: 84%
          </span>
        </div>

        {/* Bar chart representation */}
        <div className="grid grid-cols-6 gap-3 items-end h-48 pt-6 border-b border-gray-100">
          {[
            { month: "Tháng 5", amount: 14500000, height: "45%" },
            { month: "Tháng 6", amount: 22000000, height: "70%" },
            { month: "Tháng 7", amount: 28500000, height: "90%" },
            { month: "Tháng 8", amount: 25000000, height: "80%" },
            { month: "Tháng 9", amount: 19500000, height: "60%" },
            { month: "Tháng 10", amount: 32000000, height: "100%" },
          ].map((bar, i) => (
            <div key={i} className="flex flex-col items-center gap-2 h-full justify-end group">
              <span className="text-[10px] font-bold text-gray-600 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                {(bar.amount / 1000000).toFixed(1)} tr
              </span>
              <div
                style={{ height: bar.height }}
                className={`w-full rounded-2xl transition-all duration-300 group-hover:opacity-90 ${
                  i === 5
                    ? "bg-gradient-to-t from-[#FF385C] to-[#FF5A5F]"
                    : "bg-gray-200 group-hover:bg-gray-300"
                }`}
              />
              <span className="text-xs font-medium text-gray-500">{bar.month}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Access Grid: Listings & Recent Reservations */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Host Listings */}
        <div className="bg-white border border-gray-200 rounded-3xl p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-gray-100">
            <h3 className="font-bold text-gray-900 text-base">
              Chỗ ở của tôi ({hostListings.length})
            </h3>
            <button
              onClick={() => setCurrentView("host-listings")}
              className="text-xs font-bold text-[#FF385C] hover:underline"
            >
              Xem tất cả
            </button>
          </div>

          <div className="space-y-3">
            {hostListings.map((l) => (
              <div
                key={l.id}
                className="flex items-center justify-between p-3 rounded-2xl border border-gray-100 hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <img
                    src={l.cover_image}
                    alt={l.title}
                    className="w-14 h-14 rounded-xl object-cover"
                  />
                  <div>
                    <h4 className="font-bold text-gray-900 text-xs sm:text-sm line-clamp-1">
                      {l.title}
                    </h4>
                    <p className="text-[11px] text-gray-500">
                      {l.city} • {l.base_price.toLocaleString("vi-VN")} ₫ / đêm
                    </p>
                    <span
                      className={`inline-block text-[10px] font-bold px-2 py-0.5 rounded-full mt-1 ${
                        l.status === "Published"
                          ? "bg-emerald-50 text-emerald-700"
                          : "bg-gray-100 text-gray-600"
                      }`}
                    >
                      {l.status === "Published" ? "Đang xuất bản" : "Tạm ẩn"}
                    </span>
                  </div>
                </div>

                <button
                  onClick={() => {
                    setSelectedListingId(l.id);
                    setCurrentView("room-detail");
                  }}
                  className="p-2 text-gray-400 hover:text-gray-800"
                >
                  <ArrowUpRight className="w-5 h-5" />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Reservations */}
        <div className="bg-white border border-gray-200 rounded-3xl p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-gray-100">
            <h3 className="font-bold text-gray-900 text-base">
              Đơn đặt phòng gần đây ({hostBookings.length})
            </h3>
            <button
              onClick={() => setCurrentView("host-reservations")}
              className="text-xs font-bold text-[#FF385C] hover:underline"
            >
              Xem tất cả
            </button>
          </div>

          {hostBookings.length === 0 ? (
            <p className="text-xs text-gray-400 text-center py-8">
              Chưa có đơn đặt phòng nào vào các phòng của bạn.
            </p>
          ) : (
            <div className="space-y-3">
              {hostBookings.slice(0, 3).map((b) => (
                <div
                  key={b.id}
                  className="p-3 rounded-2xl border border-gray-100 space-y-1.5"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xs font-bold text-gray-900">
                      {b.booking_code}
                    </span>
                    <span className="text-[10px] font-bold bg-emerald-50 text-emerald-700 px-2 py-0.5 rounded-full">
                      {b.status}
                    </span>
                  </div>
                  <p className="text-xs text-gray-800 font-semibold line-clamp-1">
                    {b.listing_snapshot.title}
                  </p>
                  <div className="flex items-center justify-between text-xs text-gray-500">
                    <span>
                      {b.check_in} → {b.check_out} ({b.nights} đêm)
                    </span>
                    <strong className="text-[#FF385C]">
                      {b.total.toLocaleString("vi-VN")} ₫
                    </strong>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
