import React, { useState } from "react";
import { useApp } from "../context/AppContext";
import {
  CalendarCheck,
  CheckCircle,
  Clock,
  XCircle,
  MapPin,
  Users,
  DollarSign,
  Search,
} from "lucide-react";

export default function HostReservations() {
  const { listings, bookings, user } = useApp();

  const myListings = listings.filter((l) => l.host_id === user.id);
  const myListingIds = myListings.map((l) => l.id);

  const [filterStatus, setFilterStatus] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");

  const hostBookings = bookings.filter((b) => myListingIds.includes(b.listing_id));

  const filtered = hostBookings.filter((b) => {
    if (filterStatus !== "all" && b.status !== filterStatus) return false;
    if (
      searchTerm &&
      !b.booking_code.toLowerCase().includes(searchTerm.toLowerCase()) &&
      !b.listing_snapshot.title.toLowerCase().includes(searchTerm.toLowerCase())
    ) {
      return false;
    }
    return true;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-gray-900 flex items-center gap-2">
            <CalendarCheck className="w-8 h-8 text-[#FF385C]" />
            Quản lý đơn đặt phòng của khách
          </h1>
          <p className="text-xs sm:text-sm text-gray-500 mt-1">
            Theo dõi tất cả lượt khách đã đặt vào các chỗ ở của bạn (H05 & H06)
          </p>
        </div>

        {/* Search & Filter */}
        <div className="flex flex-wrap items-center gap-2 w-full sm:w-auto">
          <div className="relative flex-1 sm:w-64">
            <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Tìm mã đơn, tên chỗ ở..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-xl text-xs outline-none focus:border-gray-900 bg-white"
            />
          </div>

          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="border border-gray-300 rounded-xl px-3 py-2 text-xs font-bold text-gray-800 bg-white outline-none"
          >
            <option value="all">Tất cả trạng thái</option>
            <option value="Confirmed">Đã xác nhận</option>
            <option value="Completed">Đã hoàn thành</option>
            <option value="Cancelled">Đã hủy</option>
          </select>
        </div>
      </div>

      {filtered.length === 0 ? (
        <div className="bg-white border border-gray-200 rounded-3xl p-12 text-center space-y-3">
          <CalendarCheck className="w-12 h-12 text-gray-300 mx-auto" />
          <h3 className="font-bold text-gray-900 text-base">
            Không tìm thấy đơn đặt phòng nào phù hợp
          </h3>
          <p className="text-xs text-gray-500">
            Hãy điều chỉnh từ khóa tìm kiếm hoặc bộ lọc trạng thái.
          </p>
        </div>
      ) : (
        <div className="bg-white border border-gray-200 rounded-3xl shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-gray-50 border-b border-gray-200 text-gray-500 font-bold uppercase tracking-wider">
                <tr>
                  <th className="px-6 py-4">Mã đơn & Chỗ ở</th>
                  <th className="px-6 py-4">Ngày lưu trú</th>
                  <th className="px-6 py-4">Khách & Số đêm</th>
                  <th className="px-6 py-4">Số tiền thu</th>
                  <th className="px-6 py-4">Trạng thái</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {filtered.map((b) => (
                  <tr key={b.id} className="hover:bg-gray-50/80 transition-colors">
                    <td className="px-6 py-4">
                      <div className="space-y-1">
                        <span className="font-mono font-bold text-gray-900 bg-gray-100 px-2 py-0.5 rounded text-[11px]">
                          {b.booking_code}
                        </span>
                        <p className="font-bold text-gray-900 text-xs sm:text-sm line-clamp-1">
                          {b.listing_snapshot.title}
                        </p>
                        <p className="text-gray-400 text-[11px] flex items-center gap-1">
                          <MapPin className="w-3 h-3" />
                          {b.listing_snapshot.city}
                        </p>
                      </div>
                    </td>

                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="font-semibold text-gray-900 block">
                        {b.check_in} → {b.check_out}
                      </span>
                      <span className="text-gray-400 text-[10px]">
                        Đặt lúc: {new Date(b.created_at).toLocaleDateString("vi-VN")}
                      </span>
                    </td>

                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="font-semibold text-gray-800 block">
                        {b.guests} khách
                      </span>
                      <span className="text-gray-500">{b.nights} đêm</span>
                    </td>

                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="font-extrabold text-[#FF385C] text-sm block">
                        {b.total.toLocaleString("vi-VN")} ₫
                      </span>
                      <span className="text-[10px] text-gray-400 uppercase">
                        {b.payment_method}
                      </span>
                    </td>

                    <td className="px-6 py-4 whitespace-nowrap">
                      {b.status === "Confirmed" && (
                        <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
                          <CheckCircle className="w-3 h-3" /> Đã xác nhận
                        </span>
                      )}
                      {b.status === "Completed" && (
                        <span className="inline-flex items-center gap-1 text-[11px] font-bold text-blue-700 bg-blue-50 px-2.5 py-1 rounded-full border border-blue-200">
                          <Clock className="w-3 h-3" /> Đã hoàn tất
                        </span>
                      )}
                      {b.status === "Cancelled" && (
                        <span className="inline-flex items-center gap-1 text-[11px] font-bold text-red-700 bg-red-50 px-2.5 py-1 rounded-full border border-red-200">
                          <XCircle className="w-3 h-3" /> Đã hủy
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
