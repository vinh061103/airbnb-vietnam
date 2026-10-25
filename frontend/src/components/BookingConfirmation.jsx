import React from "react";
import { useApp } from "../context/AppContext";
import {
  CheckCircle2,
  Calendar,
  MapPin,
  Users,
  Copy,
  Luggage,
  MessageSquare,
  Compass,
} from "lucide-react";

export default function BookingConfirmation() {
  const { lastCreatedBooking, setCurrentView, startConversationWithHost, listings } =
    useApp();

  if (!lastCreatedBooking) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-16 text-center">
        <p className="text-gray-500 mb-4">Chưa có thông tin đơn đặt phòng gần đây.</p>
        <button
          onClick={() => setCurrentView("home")}
          className="px-6 py-2.5 bg-gray-900 text-white font-bold rounded-xl text-sm"
        >
          Khám phá phòng ngay
        </button>
      </div>
    );
  }

  const {
    booking_code,
    listing_snapshot,
    check_in,
    check_out,
    nights,
    guests,
    total,
    payment_method,
    listing_id,
  } = lastCreatedBooking;

  const currentListing = listings.find((l) => l.id === listing_id);

  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      <div className="bg-white border border-gray-200 rounded-3xl p-8 sm:p-10 shadow-xl text-center space-y-6">
        {/* Success Icon */}
        <div className="w-20 h-20 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto shadow-inner">
          <CheckCircle2 className="w-12 h-12 stroke-[2.5]" />
        </div>

        <div>
          <span className="text-xs font-bold text-emerald-600 uppercase tracking-widest bg-emerald-50 px-3 py-1 rounded-full">
            ● Đã xác nhận giữ chỗ thành công
          </span>
          <h1 className="text-3xl font-black text-gray-900 mt-3">
            Chúc mừng bạn, chuyến đi đã sẵn sàng!
          </h1>
          <p className="text-gray-500 text-sm mt-1">
            Mã đặt phòng duy nhất của bạn:{" "}
            <span className="font-mono font-bold text-gray-900 bg-gray-100 px-2 py-1 rounded-lg">
              {booking_code}
            </span>
          </p>
        </div>

        {/* Booking Card Details */}
        <div className="bg-gray-50 rounded-2xl p-6 text-left border border-gray-200 space-y-4">
          <div className="flex gap-4 items-center pb-4 border-b border-gray-200">
            <img
              src={listing_snapshot.cover_image}
              alt={listing_snapshot.title}
              className="w-20 h-20 rounded-xl object-cover shadow-sm flex-shrink-0"
            />
            <div>
              <h3 className="font-bold text-gray-900 text-sm sm:text-base line-clamp-1">
                {listing_snapshot.title}
              </h3>
              <p className="text-xs text-gray-500 flex items-center gap-1 mt-0.5">
                <MapPin className="w-3.5 h-3.5 text-[#FF385C]" />
                {listing_snapshot.address || listing_snapshot.city}
              </p>
              <p className="text-xs text-gray-600 mt-1">
                Chủ nhà: <strong>{listing_snapshot.host_name}</strong>
              </p>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 text-xs">
            <div>
              <span className="text-gray-500 block">Nhận phòng</span>
              <strong className="text-gray-900 text-sm">{check_in}</strong>
              <span className="text-gray-400 block text-[10px]">Từ 14:00</span>
            </div>
            <div>
              <span className="text-gray-500 block">Trả phòng</span>
              <strong className="text-gray-900 text-sm">{check_out}</strong>
              <span className="text-gray-400 block text-[10px]">Trước 12:00</span>
            </div>
            <div>
              <span className="text-gray-500 block">Số lượng khách</span>
              <strong className="text-gray-900 text-sm">{guests} khách</strong>
              <span className="text-gray-400 block text-[10px]">{nights} đêm</span>
            </div>
          </div>

          <div className="pt-3 border-t border-gray-200 flex justify-between items-center text-xs">
            <span className="text-gray-600">Phương thức thanh toán:</span>
            <span className="font-bold text-gray-900 uppercase">
              {payment_method === "vietqr"
                ? "Chuyển khoản VietQR"
                : payment_method === "credit_card"
                ? "Thẻ tín dụng / ghi nợ"
                : "Thanh toán tại chỗ nghỉ"}
            </span>
          </div>

          <div className="flex justify-between items-center text-sm font-black text-gray-900">
            <span>Tổng số tiền đã chốt:</span>
            <span className="text-[#FF385C] text-lg">
              {total.toLocaleString("vi-VN")} ₫
            </span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
          <button
            onClick={() => setCurrentView("my-bookings")}
            className="w-full sm:w-auto bg-gray-900 hover:bg-black text-white font-bold py-3.5 px-6 rounded-2xl text-xs flex items-center justify-center gap-2 shadow-md transition-all"
          >
            <Luggage className="w-4 h-4" />
            Xem các chuyến đi của tôi
          </button>

          {currentListing && (
            <button
              onClick={() => startConversationWithHost(currentListing)}
              className="w-full sm:w-auto bg-rose-50 text-[#FF385C] hover:bg-rose-100 font-bold py-3.5 px-6 rounded-2xl text-xs flex items-center justify-center gap-2 border border-rose-200 transition-all"
            >
              <MessageSquare className="w-4 h-4" />
              Nhắn tin với chủ nhà
            </button>
          )}

          <button
            onClick={() => setCurrentView("home")}
            className="w-full sm:w-auto border border-gray-300 hover:border-gray-900 text-gray-700 font-bold py-3.5 px-6 rounded-2xl text-xs flex items-center justify-center gap-2 transition-all"
          >
            <Compass className="w-4 h-4" />
            Khám phá thêm chỗ ở
          </button>
        </div>
      </div>
    </div>
  );
}
