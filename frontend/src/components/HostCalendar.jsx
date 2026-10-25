import React, { useState } from "react";
import { useApp } from "../context/AppContext";
import {
  Calendar as CalendarIcon,
  Lock,
  Unlock,
  AlertCircle,
  CheckCircle2,
  Home,
  Clock,
  ShieldAlert,
} from "lucide-react";

export default function HostCalendar() {
  const {
    listings,
    bookings,
    availabilityBlocks,
    addAvailabilityBlock,
    removeAvailabilityBlock,
    user,
  } = useApp();

  const myListings = listings.filter((l) => l.host_id === user.id);
  const [selectedListingId, setSelectedListingId] = useState(
    myListings[0]?.id || listings[0]?.id
  );

  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [reason, setReason] = useState("Bảo trì định kỳ / Nghỉ gia đình");
  const [errorMsg, setErrorMsg] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  const currentListing = listings.find((l) => l.id === selectedListingId);

  // Filter bookings & blocks for selected listing
  const currentBookings = bookings.filter(
    (b) => b.listing_id === selectedListingId && b.status === "Confirmed"
  );
  const currentBlocks = availabilityBlocks.filter(
    (b) => b.listing_id === selectedListingId
  );

  const handleBlockDates = (e) => {
    e.preventDefault();
    setErrorMsg("");
    setSuccessMsg("");

    if (!startDate || !endDate) {
      setErrorMsg("Vui lòng chọn ngày bắt đầu và kết thúc!");
      return;
    }

    if (new Date(startDate) >= new Date(endDate)) {
      setErrorMsg("Ngày kết thúc phải sau ngày bắt đầu!");
      return;
    }

    const result = addAvailabilityBlock({
      listingId: selectedListingId,
      startDate,
      endDate,
      reason,
    });

    if (result.success) {
      setSuccessMsg("Đã chặn ngày thành công! Khách sẽ không thể đặt khoảng ngày này.");
      setStartDate("");
      setEndDate("");
    } else {
      setErrorMsg(result.error);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div>
        <h1 className="text-2xl sm:text-3xl font-black text-gray-900 flex items-center gap-2">
          <CalendarIcon className="w-8 h-8 text-[#FF385C]" />
          Lịch trống & Chặn ngày cho thuê
        </h1>
        <p className="text-xs sm:text-sm text-gray-500 mt-1">
          Quản lý ngày khả dụng, chủ động chặn ngày bận hoặc bảo trì chỗ ở (H07 / UC-06)
        </p>
      </div>

      {/* Select listing */}
      <div className="bg-white border border-gray-200 rounded-3xl p-5 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Home className="w-5 h-5 text-gray-500" />
          <span className="text-xs font-bold text-gray-700">Chọn phòng quản lý:</span>
        </div>
        <select
          value={selectedListingId}
          onChange={(e) => {
            setSelectedListingId(Number(e.target.value));
            setErrorMsg("");
            setSuccessMsg("");
          }}
          className="border border-gray-300 rounded-2xl px-4 py-2.5 text-xs sm:text-sm font-bold text-gray-900 bg-white outline-none focus:border-gray-900 w-full sm:w-auto"
        >
          {myListings.map((l) => (
            <option key={l.id} value={l.id}>
              {l.title} ({l.city})
            </option>
          ))}
        </select>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Form: Add Block (5 cols) */}
        <div className="lg:col-span-5">
          <div className="bg-white border border-gray-200 rounded-3xl p-6 shadow-sm space-y-5">
            <div className="flex items-center gap-2 pb-3 border-b border-gray-100">
              <Lock className="w-5 h-5 text-[#FF385C]" />
              <h3 className="font-bold text-gray-900 text-base">
                Thêm khoảng ngày muốn chặn
              </h3>
            </div>

            {errorMsg && (
              <div className="bg-red-50 border border-red-200 text-red-700 p-3 rounded-2xl text-xs flex items-start gap-2">
                <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5 text-red-600" />
                <span>{errorMsg}</span>
              </div>
            )}

            {successMsg && (
              <div className="bg-emerald-50 border border-emerald-200 text-emerald-700 p-3 rounded-2xl text-xs flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 flex-shrink-0 mt-0.5 text-emerald-600" />
                <span>{successMsg}</span>
              </div>
            )}

            <form onSubmit={handleBlockDates} className="space-y-4 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-bold text-gray-700 block mb-1">Từ ngày</label>
                  <input
                    type="date"
                    required
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    className="w-full border border-gray-300 rounded-xl p-2.5 font-semibold text-gray-900 outline-none"
                  />
                </div>
                <div>
                  <label className="font-bold text-gray-700 block mb-1">Đến ngày</label>
                  <input
                    type="date"
                    required
                    min={startDate}
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    className="w-full border border-gray-300 rounded-xl p-2.5 font-semibold text-gray-900 outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="font-bold text-gray-700 block mb-1">
                  Lý do chặn ngày (Ghi chú nội bộ)
                </label>
                <input
                  type="text"
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                  placeholder="Bảo trì, sửa chữa, kỳ nghỉ gia đình..."
                  className="w-full border border-gray-300 rounded-xl p-2.5 font-medium text-gray-800 outline-none"
                />
              </div>

              <div className="p-3 bg-amber-50/60 rounded-xl border border-amber-200 text-[11px] text-amber-900 flex items-start gap-2">
                <ShieldAlert className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
                <span>
                  Quy tắc BR-02: Không thể chặn ngày nếu khoảng ngày đó đã có đơn đặt phòng
                  xác nhận từ khách.
                </span>
              </div>

              <button
                type="submit"
                className="w-full bg-gray-900 hover:bg-black text-white font-bold py-3 rounded-xl text-xs shadow-md transition-all"
              >
                Khóa khoảng ngày này
              </button>
            </form>
          </div>
        </div>

        {/* Right Status: Bookings & Active Blocks (7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          {/* Active Blocks */}
          <div className="bg-white border border-gray-200 rounded-3xl p-6 shadow-sm space-y-4">
            <h3 className="font-bold text-gray-900 text-base flex items-center justify-between">
              <span>Các khoảng ngày đang bị chặn ({currentBlocks.length})</span>
              <span className="text-xs text-gray-400 font-normal">
                Khách không thể tìm thấy hoặc đặt
              </span>
            </h3>

            {currentBlocks.length === 0 ? (
              <p className="text-xs text-gray-400 py-4 text-center">
                Chưa có ngày nào bị chặn. Phòng đang mở lịch bình thường.
              </p>
            ) : (
              <div className="space-y-3">
                {currentBlocks.map((blk) => (
                  <div
                    key={blk.id}
                    className="flex items-center justify-between p-3.5 rounded-2xl bg-gray-50 border border-gray-200 text-xs"
                  >
                    <div className="space-y-0.5">
                      <p className="font-bold text-gray-900">
                        {blk.start_date} → {blk.end_date}
                      </p>
                      <p className="text-gray-500 text-[11px]">Lý do: {blk.reason}</p>
                    </div>

                    <button
                      onClick={() => removeAvailabilityBlock(blk.id)}
                      className="px-3 py-1.5 rounded-xl border border-gray-300 hover:bg-white text-gray-700 font-bold flex items-center gap-1 transition-colors"
                    >
                      <Unlock className="w-3.5 h-3.5 text-emerald-600" />
                      <span>Mở lại</span>
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Confirmed Guest Bookings */}
          <div className="bg-white border border-gray-200 rounded-3xl p-6 shadow-sm space-y-4">
            <h3 className="font-bold text-gray-900 text-base flex items-center justify-between">
              <span>Lịch khách đã đặt phòng ({currentBookings.length})</span>
              <span className="text-xs text-emerald-600 font-bold">● Đang giữ chỗ</span>
            </h3>

            {currentBookings.length === 0 ? (
              <p className="text-xs text-gray-400 py-4 text-center">
                Chưa có đơn đặt phòng nào trong khoảng thời gian tới.
              </p>
            ) : (
              <div className="space-y-3">
                {currentBookings.map((b) => (
                  <div
                    key={b.id}
                    className="p-3.5 rounded-2xl border border-emerald-100 bg-emerald-50/40 text-xs space-y-1"
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-mono font-bold text-emerald-900">
                        {b.booking_code}
                      </span>
                      <strong className="text-gray-900">
                        {b.total.toLocaleString("vi-VN")} ₫
                      </strong>
                    </div>
                    <p className="text-gray-700 font-semibold">
                      Lưu trú: {b.check_in} → {b.check_out} ({b.nights} đêm, {b.guests} khách)
                    </p>
                    <p className="text-gray-500 text-[11px]">
                      Thanh toán qua: {b.payment_method.toUpperCase()}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
