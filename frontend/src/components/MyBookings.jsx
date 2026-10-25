import React, { useState } from "react";
import { useApp } from "../context/AppContext";
import {
  Luggage,
  Calendar,
  MapPin,
  Star,
  MessageSquare,
  AlertTriangle,
  XCircle,
  CheckCircle,
  Clock,
  Sparkles,
  ArrowRight,
} from "lucide-react";

export default function MyBookings() {
  const {
    bookings,
    cancelBooking,
    addReview,
    setCurrentView,
    setSelectedListingId,
    startConversationWithHost,
    listings,
  } = useApp();

  const [activeTab, setActiveTab] = useState("all"); // 'all' | 'confirmed' | 'completed' | 'cancelled'

  // Review modal state
  const [reviewModalBooking, setReviewModalBooking] = useState(null);
  const [ratingInput, setRatingInput] = useState(5);
  const [commentInput, setCommentInput] = useState("");

  // Cancel modal state
  const [cancelModalBooking, setCancelModalBooking] = useState(null);
  const [cancelReason, setCancelReason] = useState("Thay đổi kế hoạch cá nhân");

  const filteredBookings = bookings.filter((b) => {
    if (activeTab === "confirmed") return b.status === "Confirmed";
    if (activeTab === "completed") return b.status === "Completed";
    if (activeTab === "cancelled") return b.status === "Cancelled";
    return true;
  });

  const handleSubmitReview = (e) => {
    e.preventDefault();
    if (!commentInput.trim()) return;

    addReview({
      listingId: reviewModalBooking.listing_id,
      bookingId: reviewModalBooking.id,
      rating: ratingInput,
      comment: commentInput,
    });

    setReviewModalBooking(null);
    setCommentInput("");
    setRatingInput(5);
    alert("Cảm ơn bạn! Đánh giá đã được đăng thành công.");
  };

  const handleConfirmCancel = () => {
    if (!cancelModalBooking) return;
    cancelBooking(cancelModalBooking.id, cancelReason);
    setCancelModalBooking(null);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-gray-900 flex items-center gap-2">
            <Luggage className="w-8 h-8 text-[#FF385C]" />
            Chuyến đi của tôi
          </h1>
          <p className="text-xs sm:text-sm text-gray-500 mt-1">
            Quản lý các đặt phòng, theo dõi trạng thái và đánh giá kỳ nghỉ (C07 & C08)
          </p>
        </div>

        {/* Tab Filters */}
        <div className="flex items-center gap-1 bg-gray-100 p-1.5 rounded-2xl text-xs font-semibold">
          {[
            { id: "all", label: "Tất cả" },
            { id: "confirmed", label: "Sắp tới" },
            { id: "completed", label: "Đã ở" },
            { id: "cancelled", label: "Đã hủy" },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-3.5 py-2 rounded-xl transition-all ${
                activeTab === tab.id
                  ? "bg-white text-gray-900 shadow-sm"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {filteredBookings.length === 0 ? (
        <div className="bg-white border border-gray-200 rounded-3xl p-12 text-center space-y-4">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto text-gray-400">
            <Luggage className="w-8 h-8" />
          </div>
          <h3 className="font-bold text-gray-900 text-lg">
            Không có đơn đặt phòng nào trong mục này
          </h3>
          <p className="text-xs text-gray-500 max-w-sm mx-auto">
            Hãy bắt đầu lên kế hoạch cho kỳ nghỉ tuyệt vời tiếp theo của bạn ngay hôm nay!
          </p>
          <button
            onClick={() => setCurrentView("home")}
            className="bg-gradient-to-r from-[#FF385C] to-[#E00B41] text-white font-bold py-3 px-6 rounded-2xl text-xs shadow-md transition-all"
          >
            Tìm phòng ngay
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredBookings.map((b) => {
            const currentListing = listings.find((l) => l.id === b.listing_id);

            return (
              <div
                key={b.id}
                className="bg-white border border-gray-200 rounded-3xl p-5 sm:p-6 shadow-sm hover:shadow-md transition-all flex flex-col md:flex-row gap-6 items-start md:items-center justify-between"
              >
                {/* Left info */}
                <div className="flex gap-4 items-center">
                  <img
                    src={b.listing_snapshot.cover_image}
                    alt={b.listing_snapshot.title}
                    className="w-24 h-24 sm:w-28 sm:h-28 rounded-2xl object-cover shadow-sm flex-shrink-0 cursor-pointer"
                    onClick={() => {
                      setSelectedListingId(b.listing_id);
                      setCurrentView("room-detail");
                    }}
                  />
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-bold bg-gray-100 text-gray-700 px-2 py-0.5 rounded-md">
                        {b.booking_code}
                      </span>

                      {/* Status Badges */}
                      {b.status === "Confirmed" && (
                        <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
                          <CheckCircle className="w-3 h-3" /> Đã xác nhận giữ chỗ
                        </span>
                      )}
                      {b.status === "Completed" && (
                        <span className="inline-flex items-center gap-1 text-[11px] font-bold text-blue-700 bg-blue-50 px-2.5 py-0.5 rounded-full border border-blue-200">
                          <Clock className="w-3 h-3" /> Đã hoàn thành
                        </span>
                      )}
                      {b.status === "Cancelled" && (
                        <span className="inline-flex items-center gap-1 text-[11px] font-bold text-red-700 bg-red-50 px-2.5 py-0.5 rounded-full border border-red-200">
                          <XCircle className="w-3 h-3" /> Đã hủy phòng
                        </span>
                      )}
                    </div>

                    <h3
                      onClick={() => {
                        setSelectedListingId(b.listing_id);
                        setCurrentView("room-detail");
                      }}
                      className="font-bold text-gray-900 text-sm sm:text-base line-clamp-1 hover:text-[#FF385C] cursor-pointer"
                    >
                      {b.listing_snapshot.title}
                    </h3>

                    <p className="text-xs text-gray-500 flex items-center gap-1">
                      <MapPin className="w-3.5 h-3.5 text-gray-400" />
                      {b.listing_snapshot.city}, Việt Nam
                    </p>

                    <div className="flex items-center gap-3 text-xs text-gray-600 pt-1 font-medium">
                      <span>{b.check_in} → {b.check_out} ({b.nights} đêm)</span>
                      <span>•</span>
                      <span>{b.guests} khách</span>
                    </div>

                    <p className="text-xs text-gray-900 pt-1">
                      Tổng tiền:{" "}
                      <strong className="text-[#FF385C] text-sm">
                        {b.total.toLocaleString("vi-VN")} ₫
                      </strong>
                    </p>
                  </div>
                </div>

                {/* Right Actions */}
                <div className="flex flex-wrap md:flex-col gap-2 w-full md:w-44 flex-shrink-0">
                  {/* Cancel button (UC-04) */}
                  {b.status === "Confirmed" && (
                    <button
                      onClick={() => setCancelModalBooking(b)}
                      className="w-full py-2.5 px-3 rounded-xl border border-red-200 text-red-600 hover:bg-red-50 text-xs font-bold transition-colors"
                    >
                      Hủy đặt phòng
                    </button>
                  )}

                  {/* Review button (UC-08 / BR-09) */}
                  {b.status === "Completed" && (
                    <button
                      disabled={b.reviewed}
                      onClick={() => setReviewModalBooking(b)}
                      className={`w-full py-2.5 px-3 rounded-xl text-xs font-bold transition-colors flex items-center justify-center gap-1.5 ${
                        b.reviewed
                          ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                          : "bg-amber-50 text-amber-800 border border-amber-300 hover:bg-amber-100"
                      }`}
                    >
                      <Star className="w-3.5 h-3.5 fill-current" />
                      <span>{b.reviewed ? "Đã gửi đánh giá" : "Viết đánh giá"}</span>
                    </button>
                  )}

                  {/* Contact Host */}
                  {currentListing && (
                    <button
                      onClick={() => startConversationWithHost(currentListing)}
                      className="w-full py-2 px-3 rounded-xl border border-gray-200 text-gray-700 hover:bg-gray-50 text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors"
                    >
                      <MessageSquare className="w-3.5 h-3.5 text-gray-500" />
                      <span>Nhắn tin chủ nhà</span>
                    </button>
                  )}

                  {/* Rebook */}
                  <button
                    onClick={() => {
                      setSelectedListingId(b.listing_id);
                      setCurrentView("room-detail");
                    }}
                    className="w-full py-2 px-3 rounded-xl bg-gray-900 hover:bg-black text-white text-xs font-bold transition-colors"
                  >
                    Xem lại phòng
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Review Modal (UC-08) */}
      {reviewModalBooking && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 animate-in fade-in">
          <div className="bg-white rounded-3xl w-full max-w-lg p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-gray-100">
              <h3 className="font-bold text-gray-900 text-base flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-amber-500" />
                Đánh giá chỗ ở sau chuyến đi
              </h3>
              <button
                onClick={() => setReviewModalBooking(null)}
                className="text-gray-400 hover:text-gray-700 font-bold text-sm"
              >
                ✕
              </button>
            </div>

            <p className="text-xs text-gray-600">
              Bạn đánh giá thế nào về kỳ nghỉ tại{" "}
              <strong>{reviewModalBooking.listing_snapshot.title}</strong>?
            </p>

            <form onSubmit={handleSubmitReview} className="space-y-4">
              {/* Star Picker */}
              <div className="flex items-center justify-center gap-2 py-2">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setRatingInput(star)}
                    className="p-1 hover:scale-125 transition-transform"
                  >
                    <Star
                      className={`w-8 h-8 ${
                        star <= ratingInput
                          ? "fill-amber-400 text-amber-400"
                          : "text-gray-300"
                      }`}
                    />
                  </button>
                ))}
              </div>

              {/* Text comment */}
              <div>
                <label className="text-xs font-bold text-gray-700 block mb-1">
                  Nhận xét chi tiết của bạn
                </label>
                <textarea
                  rows="4"
                  value={commentInput}
                  onChange={(e) => setCommentInput(e.target.value)}
                  placeholder="Hãy chia sẻ trải nghiệm về phòng, độ sạch sẽ, sự nhiệt tình của chủ nhà..."
                  className="w-full border border-gray-300 rounded-2xl p-3 text-xs outline-none focus:border-gray-900"
                  required
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setReviewModalBooking(null)}
                  className="px-4 py-2 text-xs font-bold text-gray-600 hover:bg-gray-100 rounded-xl"
                >
                  Đóng
                </button>
                <button
                  type="submit"
                  className="px-6 py-2.5 bg-gray-900 hover:bg-black text-white text-xs font-bold rounded-xl shadow-md"
                >
                  Gửi đánh giá
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Cancel Confirmation Modal (UC-04) */}
      {cancelModalBooking && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 animate-in fade-in">
          <div className="bg-white rounded-3xl w-full max-w-md p-6 shadow-2xl space-y-4">
            <div className="w-12 h-12 bg-red-100 text-red-600 rounded-full flex items-center justify-center mx-auto">
              <AlertTriangle className="w-6 h-6" />
            </div>

            <div className="text-center space-y-1">
              <h3 className="font-bold text-gray-900 text-base">
                Xác nhận hủy đặt phòng?
              </h3>
              <p className="text-xs text-gray-500">
                Đơn {cancelModalBooking.booking_code} sẽ được chuyển sang trạng thái Hủy.
                Lịch trống cho khoảng ngày {cancelModalBooking.check_in} →{" "}
                {cancelModalBooking.check_out} sẽ được tự động giải phóng!
              </p>
            </div>

            <div className="text-xs space-y-1">
              <label className="font-bold text-gray-700 block">Lý do hủy phòng:</label>
              <select
                value={cancelReason}
                onChange={(e) => setCancelReason(e.target.value)}
                className="w-full border border-gray-300 rounded-xl p-2.5 bg-white font-medium outline-none"
              >
                <option value="Thay đổi kế hoạch cá nhân">Thay đổi kế hoạch cá nhân</option>
                <option value="Tìm thấy chỗ ở khác phù hợp hơn">
                  Tìm thấy chỗ ở khác phù hợp hơn
                </option>
                <option value="Lý do sức khỏe / thời tiết">
                  Lý do sức khỏe / thời tiết
                </option>
              </select>
            </div>

            <div className="flex items-center gap-3 pt-3">
              <button
                type="button"
                onClick={() => setCancelModalBooking(null)}
                className="flex-1 py-2.5 border border-gray-300 rounded-xl text-xs font-bold text-gray-700 hover:bg-gray-50"
              >
                Giữ lại đơn
              </button>
              <button
                type="button"
                onClick={handleConfirmCancel}
                className="flex-1 py-2.5 bg-red-600 hover:bg-red-700 text-white rounded-xl text-xs font-bold shadow-md"
              >
                Xác nhận hủy
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
