import React, { useState } from "react";
import { useApp } from "../context/AppContext";
import confetti from "canvas-confetti";
import {
  ArrowLeft,
  ShieldCheck,
  CreditCard,
  QrCode,
  Building,
  CheckCircle2,
  Calendar,
  Users,
  AlertCircle,
  Copy,
  Lock,
} from "lucide-react";

export default function BookingCheckout() {
  const {
    pendingBookingData,
    setCurrentView,
    createBooking,
    user,
    listings,
    selectedListingId,
  } = useApp();

  const [paymentMethod, setPaymentMethod] = useState("vietqr"); // 'vietqr' | 'credit_card' | 'pay_at_property'
  const [isProcessing, setIsProcessing] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [copied, setCopied] = useState(false);

  // Fake Credit Card Form state
  const [cardNumber, setCardNumber] = useState("4532 •••• •••• 8899");
  const [cardExp, setCardExp] = useState("12/28");
  const [cardCvv, setCardCvv] = useState("888");

  const fallbackListing = listings.find((l) => l.id === selectedListingId) || listings[0];
  const effectiveData = pendingBookingData || {
    listing: fallbackListing,
    checkIn: "2026-11-15",
    checkOut: "2026-11-18",
    guests: 2,
    nights: 3,
    subtotal: (fallbackListing?.base_price || 1850000) * 3,
    serviceFee: Math.round((fallbackListing?.base_price || 1850000) * 3 * 0.08),
    tax: Math.round((fallbackListing?.base_price || 1850000) * 3 * 0.08),
    total:
      (fallbackListing?.base_price || 1850000) * 3 +
      Math.round((fallbackListing?.base_price || 1850000) * 3 * 0.16),
  };

  const {
    listing,
    checkIn,
    checkOut,
    guests,
    nights,
    subtotal,
    serviceFee,
    tax,
    total,
  } = effectiveData;

  const handleConfirmPayment = () => {
    setIsProcessing(true);
    setErrorMsg("");

    setTimeout(() => {
      const result = createBooking({
        listing,
        checkIn,
        checkOut,
        guests,
        paymentMethod,
      });

      setIsProcessing(false);

      if (result.success) {
        // Confetti celebration effect!
        try {
          confetti({
            particleCount: 120,
            spread: 80,
            origin: { y: 0.6 },
          });
        } catch (e) {
          console.log(e);
        }
        setCurrentView("confirmation");
      } else {
        setErrorMsg(result.error);
      }
    }, 1200);
  };

  const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=247-AIRBNBVN-${total}-BOOKING`;

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back button */}
      <button
        onClick={() => setCurrentView("room-detail")}
        className="mb-6 inline-flex items-center gap-2 text-sm font-bold text-gray-700 hover:text-gray-900"
      >
        <ArrowLeft className="w-4 h-4" /> Quay lại thông tin phòng
      </button>

      <h1 className="text-3xl font-black text-gray-900 mb-8">
        Yêu cầu đặt phòng & Thanh toán
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
        {/* Left Form: Payment Details (7 cols) */}
        <div className="lg:col-span-7 space-y-8">
          {/* Trip Summary */}
          <div className="bg-white border border-gray-200 rounded-3xl p-6 shadow-sm space-y-4">
            <h2 className="text-lg font-bold text-gray-900">Chuyến đi của bạn</h2>

            <div className="flex items-center justify-between py-2 border-b border-gray-100">
              <div>
                <p className="font-bold text-gray-900 text-sm">Ngày lưu trú</p>
                <p className="text-xs text-gray-600 mt-0.5">
                  {checkIn} đến {checkOut} ({nights} đêm)
                </p>
              </div>
              <button
                onClick={() => setCurrentView("room-detail")}
                className="text-xs font-bold text-gray-900 underline hover:text-[#FF385C]"
              >
                Chỉnh sửa
              </button>
            </div>

            <div className="flex items-center justify-between py-2">
              <div>
                <p className="font-bold text-gray-900 text-sm">Khách</p>
                <p className="text-xs text-gray-600 mt-0.5">{guests} khách</p>
              </div>
              <button
                onClick={() => setCurrentView("room-detail")}
                className="text-xs font-bold text-gray-900 underline hover:text-[#FF385C]"
              >
                Chỉnh sửa
              </button>
            </div>
          </div>

          {/* Payment Method Selector (FR-06) */}
          <div className="bg-white border border-gray-200 rounded-3xl p-6 shadow-sm space-y-5">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-bold text-gray-900">
                Phương thức thanh toán
              </h2>
              <span className="flex items-center gap-1 text-xs text-emerald-600 font-semibold bg-emerald-50 px-2.5 py-1 rounded-full">
                <Lock className="w-3 h-3" /> Bảo mật SSL 256-bit
              </span>
            </div>

            {/* Options tabs */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {/* VietQR */}
              <button
                type="button"
                onClick={() => setPaymentMethod("vietqr")}
                className={`p-4 rounded-2xl border text-left transition-all flex flex-col justify-between ${
                  paymentMethod === "vietqr"
                    ? "border-[#FF385C] bg-rose-50/40 text-gray-900 shadow-sm"
                    : "border-gray-200 text-gray-600 hover:border-gray-300"
                }`}
              >
                <QrCode className="w-6 h-6 text-[#FF385C] mb-2" />
                <div>
                  <p className="font-bold text-xs text-gray-900">Chuyển khoản VietQR</p>
                  <p className="text-[10px] text-gray-500 mt-0.5">Quét mã tiện lợi</p>
                </div>
              </button>

              {/* Credit Card */}
              <button
                type="button"
                onClick={() => setPaymentMethod("credit_card")}
                className={`p-4 rounded-2xl border text-left transition-all flex flex-col justify-between ${
                  paymentMethod === "credit_card"
                    ? "border-[#FF385C] bg-rose-50/40 text-gray-900 shadow-sm"
                    : "border-gray-200 text-gray-600 hover:border-gray-300"
                }`}
              >
                <CreditCard className="w-6 h-6 text-[#FF385C] mb-2" />
                <div>
                  <p className="font-bold text-xs text-gray-900">Thẻ Quốc Tế</p>
                  <p className="text-[10px] text-gray-500 mt-0.5">Visa, Mastercard</p>
                </div>
              </button>

              {/* Pay at property */}
              <button
                type="button"
                onClick={() => setPaymentMethod("pay_at_property")}
                className={`p-4 rounded-2xl border text-left transition-all flex flex-col justify-between ${
                  paymentMethod === "pay_at_property"
                    ? "border-[#FF385C] bg-rose-50/40 text-gray-900 shadow-sm"
                    : "border-gray-200 text-gray-600 hover:border-gray-300"
                }`}
              >
                <Building className="w-6 h-6 text-[#FF385C] mb-2" />
                <div>
                  <p className="font-bold text-xs text-gray-900">Tại chỗ nghỉ</p>
                  <p className="text-[10px] text-gray-500 mt-0.5">Tiền mặt / Thẻ</p>
                </div>
              </button>
            </div>

            {/* VietQR View */}
            {paymentMethod === "vietqr" && (
              <div className="bg-gradient-to-br from-gray-50 to-rose-50/30 p-5 rounded-2xl border border-rose-100 flex flex-col sm:flex-row items-center gap-6">
                <div className="bg-white p-3 rounded-2xl shadow-md border border-gray-100 text-center flex-shrink-0">
                  <img
                    src={qrUrl}
                    alt="VietQR Demo"
                    className="w-36 h-36 mx-auto rounded-lg"
                  />
                  <span className="text-[10px] font-bold text-emerald-600 mt-1 block">
                    ● Quét mã tự động khớp tiền
                  </span>
                </div>
                <div className="text-xs space-y-2 flex-1 w-full">
                  <p className="font-bold text-gray-900 text-sm">
                    Thông tin thanh toán ngân hàng
                  </p>
                  <div className="bg-white p-3 rounded-xl border border-gray-200 space-y-1">
                    <p className="text-gray-500">Ngân hàng: <span className="font-bold text-gray-900">MB Bank (Quân Đội)</span></p>
                    <p className="text-gray-500">Số tài khoản: <span className="font-bold text-[#FF385C]">090123456789</span></p>
                    <p className="text-gray-500">Người thụ hưởng: <span className="font-bold text-gray-900">AIRBNB VIETNAM OFFICIAL</span></p>
                    <p className="text-gray-500">
                      Số tiền:{" "}
                      <span className="font-extrabold text-[#FF385C]">
                        {total.toLocaleString("vi-VN")} ₫
                      </span>
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Credit Card Mock Form */}
            {paymentMethod === "credit_card" && (
              <div className="space-y-3 bg-gray-50 p-4 rounded-2xl border border-gray-200 text-xs">
                <div>
                  <label className="font-bold text-gray-700 block mb-1">
                    Số thẻ tín dụng / ghi nợ
                  </label>
                  <input
                    type="text"
                    value={cardNumber}
                    onChange={(e) => setCardNumber(e.target.value)}
                    className="w-full bg-white border border-gray-300 rounded-xl px-3 py-2.5 font-mono font-bold text-gray-800 outline-none focus:border-gray-900"
                  />
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="font-bold text-gray-700 block mb-1">
                      Hết hạn (MM/YY)
                    </label>
                    <input
                      type="text"
                      value={cardExp}
                      onChange={(e) => setCardExp(e.target.value)}
                      className="w-full bg-white border border-gray-300 rounded-xl px-3 py-2.5 font-mono font-bold text-gray-800 outline-none focus:border-gray-900"
                    />
                  </div>
                  <div>
                    <label className="font-bold text-gray-700 block mb-1">
                      CVV / CVC
                    </label>
                    <input
                      type="password"
                      value={cardCvv}
                      onChange={(e) => setCardCvv(e.target.value)}
                      className="w-full bg-white border border-gray-300 rounded-xl px-3 py-2.5 font-mono font-bold text-gray-800 outline-none focus:border-gray-900"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Pay at property View */}
            {paymentMethod === "pay_at_property" && (
              <div className="bg-blue-50/60 p-4 rounded-2xl border border-blue-200 text-xs text-blue-900 flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                <p>
                  Bạn sẽ thanh toán trực tiếp số tiền{" "}
                  <strong>{total.toLocaleString("vi-VN")} ₫</strong> cho chủ nhà khi nhận
                  chìa khóa phòng. Đơn đặt phòng vẫn được xác nhận và giữ lịch ngay lập tức!
                </p>
              </div>
            )}
          </div>

          {/* Cancellation Policy */}
          <div className="bg-white border border-gray-200 rounded-3xl p-6 shadow-sm space-y-3 text-xs text-gray-600">
            <h3 className="font-bold text-gray-900 text-sm">Chính sách hủy phòng</h3>
            <p>
              Hủy miễn phí trong vòng 48 giờ sau khi đặt phòng. Sau thời gian này, bạn sẽ
              được hoàn trả 50% tổng số tiền thanh toán theo quy định bảo vệ khách hàng của
              chúng tôi.
            </p>
          </div>

          {/* Error Message */}
          {errorMsg && (
            <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-2xl text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 flex-shrink-0 text-red-600" />
              <span>{errorMsg}</span>
            </div>
          )}

          {/* Submit Button */}
          <button
            disabled={isProcessing}
            onClick={handleConfirmPayment}
            className="w-full bg-gradient-to-r from-[#FF385C] to-[#E00B41] hover:opacity-95 text-white font-extrabold py-4 px-6 rounded-2xl shadow-xl transition-all active:scale-95 text-base flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {isProcessing ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>Đang xử lý giao dịch...</span>
              </>
            ) : (
              <span>Xác nhận & Hoàn tất đặt phòng</span>
            )}
          </button>
        </div>

        {/* Right Card: Snapshot Summary (5 cols) */}
        <div className="lg:col-span-5">
          <div className="bg-white border border-gray-200 rounded-3xl p-6 shadow-lg space-y-6 sticky top-28">
            <div className="flex gap-4 items-center pb-5 border-b border-gray-100">
              <img
                src={listing.cover_image}
                alt={listing.title}
                className="w-24 h-24 rounded-2xl object-cover shadow-sm flex-shrink-0"
              />
              <div className="space-y-1">
                <span className="text-[10px] font-bold uppercase tracking-wider text-gray-500">
                  {listing.property_type}
                </span>
                <h3 className="font-bold text-gray-900 text-sm line-clamp-2">
                  {listing.title}
                </h3>
                <p className="text-xs text-gray-500">{listing.city}, Việt Nam</p>
              </div>
            </div>

            <div className="space-y-3 text-xs text-gray-600">
              <h4 className="font-bold text-gray-900 text-sm">Chi tiết giá</h4>

              <div className="flex justify-between items-center">
                <span>
                  {listing.base_price.toLocaleString("vi-VN")} ₫ × {nights} đêm
                </span>
                <span className="font-bold text-gray-900">
                  {subtotal.toLocaleString("vi-VN")} ₫
                </span>
              </div>

              <div className="flex justify-between items-center">
                <span>Phí dịch vụ khách</span>
                <span className="font-bold text-gray-900">
                  {serviceFee.toLocaleString("vi-VN")} ₫
                </span>
              </div>

              <div className="flex justify-between items-center">
                <span>Thuế giá trị gia tăng VAT</span>
                <span className="font-bold text-gray-900">
                  {tax.toLocaleString("vi-VN")} ₫
                </span>
              </div>

              <div className="border-t border-gray-200 pt-3 flex justify-between items-center text-sm font-black text-gray-900">
                <span>Tổng tiền (VND)</span>
                <span className="text-[#FF385C] text-lg">
                  {total.toLocaleString("vi-VN")} ₫
                </span>
              </div>
            </div>

            <div className="bg-gray-50 p-4 rounded-2xl border border-gray-100 text-xs text-gray-500 space-y-1">
              <p className="font-semibold text-gray-800 flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-[#FF385C]" />
                Cam kết giá minh bạch
              </p>
              <p>
                Không có chi phí ẩn. Bạn được đảm bảo mức giá tốt nhất theo thỏa thuận với chủ
                nhà.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
