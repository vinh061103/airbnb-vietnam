import React, { useState } from "react";
import { useApp } from "../context/AppContext";
import { AMENITIES_LIST } from "../data/initialData";
import {
  Star,
  Heart,
  Share2,
  MapPin,
  ShieldCheck,
  Award,
  Users,
  Bed,
  Bath,
  Home,
  MessageSquare,
  AlertCircle,
  CheckCircle2,
  Calendar,
  ChevronDown,
  ArrowLeft,
  Wifi,
  AirVent,
  UtensilsCrossed,
  Tv,
  Waves,
  Car,
  Flame,
  Shirt,
  Sun,
} from "lucide-react";

const AMENITY_ICONS = {
  wifi: Wifi,
  ac: AirVent,
  kitchen: UtensilsCrossed,
  tv: Tv,
  pool: Waves,
  parking: Car,
  bbq: Flame,
  washer: Shirt,
  bathtub: Bath,
  balcony: Sun,
};

export default function RoomDetail() {
  const {
    user,
    listings,
    selectedListingId,
    setCurrentView,
    activeSearch,
    wishlist,
    toggleWishlist,
    reviews,
    checkAvailability,
    setPendingBookingData,
    startConversationWithHost,
  } = useApp();

  const listing = listings.find((l) => l.id === selectedListingId) || listings[0];

  // Form Booking state
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  const next3Days = new Date();
  next3Days.setDate(next3Days.getDate() + 4);

  const [checkIn, setCheckIn] = useState(() => {
    if (activeSearch?.checkIn) return activeSearch.checkIn;
    return tomorrow.toISOString().split("T")[0];
  });
  const [checkOut, setCheckOut] = useState(() => {
    if (activeSearch?.checkOut) return activeSearch.checkOut;
    return next3Days.toISOString().split("T")[0];
  });
  const [guests, setGuests] = useState(() => {
    if (activeSearch?.guests) return activeSearch.guests;
    return 2;
  });
  const [errorMsg, setErrorMsg] = useState("");

  if (!listing) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center">
        <p className="text-gray-500 mb-4">Không tìm thấy thông tin phòng này.</p>
        <button
          onClick={() => setCurrentView("home")}
          className="px-6 py-2 bg-gray-900 text-white rounded-xl text-sm font-semibold"
        >
          Quay lại trang chủ
        </button>
      </div>
    );
  }

  const isLiked = wishlist.includes(listing.id);
  const listingReviews = reviews.filter((r) => r.listing_id === listing.id);

  // Calculate pricing breakdown (BR-04)
  const startDate = new Date(checkIn);
  const endDate = new Date(checkOut);
  const nights = Math.max(1, Math.round((endDate - startDate) / (1000 * 60 * 60 * 24)));
  const subtotal = nights * listing.base_price;
  const serviceFee = Math.round(subtotal * 0.08);
  const tax = Math.round(subtotal * 0.08);
  const total = subtotal + serviceFee + tax;

  const handleBookNow = () => {
    setErrorMsg("");

    if (!user) {
      alert("Vui lòng đăng nhập tài khoản khách hàng để tiến hành đặt phòng!");
      setCurrentView("login");
      return;
    }

    if (startDate >= endDate) {
      setErrorMsg("Ngày trả phòng phải sau ngày nhận phòng ít nhất 1 đêm!");
      return;
    }

    if (guests > listing.capacity) {
      setErrorMsg(`Chỗ ở này chỉ nhận tối đa ${listing.capacity} khách!`);
      return;
    }

    // BR-02 check
    const avail = checkAvailability(listing.id, checkIn, checkOut);
    if (!avail.available) {
      setErrorMsg(avail.error);
      return;
    }

    // Save pending booking & go to checkout
    setPendingBookingData({
      listing,
      checkIn,
      checkOut,
      guests,
      nights,
      unitPrice: listing.base_price,
      subtotal,
      serviceFee,
      tax,
      total,
    });

    setCurrentView("checkout");
  };

  const images = listing.images || [listing.cover_image];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      {/* Back button */}
      <button
        onClick={() => setCurrentView(activeSearch ? "search-results" : "home")}
        className="mb-4 inline-flex items-center gap-2 text-sm font-bold text-gray-700 hover:text-gray-900 bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded-xl transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />{" "}
        {activeSearch ? "Quay lại kết quả tìm kiếm" : "Quay lại danh sách phòng"}
      </button>

      {/* Title & Actions */}
      <div className="mb-4">
        <h1 className="text-2xl sm:text-3xl font-extrabold text-gray-900 leading-tight">
          {listing.title}
        </h1>

        <div className="mt-2 flex flex-wrap items-center justify-between gap-3 text-sm">
          <div className="flex items-center gap-3 flex-wrap">
            <div className="flex items-center gap-1 font-bold text-gray-900">
              <Star className="w-4 h-4 fill-current text-gray-900" />
              <span>{listing.rating ? listing.rating.toFixed(2) : "Mới"}</span>
              <span className="text-gray-500 font-normal">
                ({listingReviews.length} đánh giá)
              </span>
            </div>
            <span>•</span>
            <span className="font-semibold text-gray-700 flex items-center gap-1">
              <Award className="w-4 h-4 text-[#FF385C]" />
              Superhost
            </span>
            <span>•</span>
            <span className="text-gray-600 underline font-medium flex items-center gap-1">
              <MapPin className="w-4 h-4 text-gray-500" />
              {listing.address}
            </span>
          </div>

          <div className="flex items-center gap-4">
            <button
              onClick={() => alert("Đã sao chép liên kết phòng vào clipboard!")}
              className="flex items-center gap-1.5 text-xs font-semibold text-gray-700 hover:bg-gray-100 px-3 py-2 rounded-xl transition-colors"
            >
              <Share2 className="w-4 h-4" />
              Chia sẻ
            </button>
            <button
              onClick={() => toggleWishlist(listing.id)}
              className="flex items-center gap-1.5 text-xs font-semibold text-gray-700 hover:bg-gray-100 px-3 py-2 rounded-xl transition-colors"
            >
              <Heart
                className={`w-4 h-4 ${
                  isLiked ? "fill-[#FF385C] text-[#FF385C]" : "text-gray-700"
                }`}
              />
              {isLiked ? "Đã lưu" : "Lưu"}
            </button>
          </div>
        </div>
      </div>

      {/* Airbnb 5-Image Gallery Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-2 rounded-3xl overflow-hidden aspect-[16/9] max-h-[500px] mb-8 shadow-sm">
        <div className="md:col-span-2 h-full">
          <img
            src={images[0]}
            alt={listing.title}
            className="w-full h-full object-cover hover:scale-105 transition-transform duration-300 cursor-pointer"
          />
        </div>
        <div className="hidden md:grid grid-cols-2 col-span-2 gap-2 h-full">
          {images.slice(1, 5).map((img, i) => (
            <div key={i} className="h-full overflow-hidden">
              <img
                src={img}
                alt={`${listing.title} ${i + 1}`}
                className="w-full h-full object-cover hover:scale-105 transition-transform duration-300 cursor-pointer"
              />
            </div>
          ))}
        </div>
      </div>

      {/* Main Content & Sticky Booking Card */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
        {/* Left Col (2 cols) */}
        <div className="lg:col-span-2 space-y-8 divide-y divide-gray-200">
          {/* Host header info */}
          <div className="flex items-center justify-between pb-6">
            <div>
              <h2 className="text-xl font-bold text-gray-900">
                Toàn bộ {listing.property_type.toLowerCase()} • Chủ nhà{" "}
                {listing.host?.name}
              </h2>
              <p className="text-sm text-gray-600 mt-1">
                {listing.capacity} khách • {listing.bedrooms || 2} phòng ngủ •{" "}
                {listing.beds || 3} giường • {listing.baths || 2} phòng tắm
              </p>
            </div>
            <img
              src={listing.host?.avatar}
              alt={listing.host?.name}
              className="w-14 h-14 rounded-full object-cover border-2 border-gray-200 shadow-sm"
            />
          </div>

          {/* Highlights */}
          <div className="py-6 space-y-4 text-sm">
            <div className="flex items-start gap-4">
              <Award className="w-6 h-6 text-[#FF385C] flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-bold text-gray-900">Chủ nhà siêu cấp (Superhost)</p>
                <p className="text-gray-500 text-xs mt-0.5">
                  Chủ nhà giàu kinh nghiệm, được đánh giá cao và cam kết mang lại kỳ nghỉ tuyệt vời.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <ShieldCheck className="w-6 h-6 text-[#FF385C] flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-bold text-gray-900">Bảo vệ đặt phòng Airbnb Cover</p>
                <p className="text-gray-500 text-xs mt-0.5">
                  Đảm bảo đặt phòng chính xác, hỗ trợ chuyển chỗ ở hoặc hoàn tiền nếu có sự cố.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <Calendar className="w-6 h-6 text-[#FF385C] flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-bold text-gray-900">Hủy miễn phí trong vòng 48 giờ</p>
                <p className="text-gray-500 text-xs mt-0.5">
                  Linh hoạt thay đổi kế hoạch chuyến đi không mất phí.
                </p>
              </div>
            </div>
          </div>

          {/* Description */}
          <div className="py-6 space-y-3">
            <h3 className="text-lg font-bold text-gray-900">Mô tả chỗ ở</h3>
            <p className="text-gray-700 leading-relaxed text-sm whitespace-pre-line">
              {listing.description}
            </p>
          </div>

          {/* Amenities */}
          <div className="py-6 space-y-4">
            <h3 className="text-lg font-bold text-gray-900">Nơi này có những gì cho bạn</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              {listing.amenities?.map((amenityId) => {
                const item = AMENITIES_LIST.find((a) => a.id === amenityId);
                const IconComp = AMENITY_ICONS[amenityId] || Home;
                return (
                  <div
                    key={amenityId}
                    className="flex items-center gap-3 text-sm text-gray-800"
                  >
                    <IconComp className="w-5 h-5 text-gray-600" />
                    <span>{item ? item.name : amenityId}</span>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Reviews section (FR-14) */}
          <div className="py-6 space-y-6">
            <div className="flex items-center gap-2">
              <Star className="w-5 h-5 fill-current text-gray-900" />
              <h3 className="text-xl font-extrabold text-gray-900">
                {listing.rating ? listing.rating.toFixed(2) : "5.0"} • {listingReviews.length} đánh giá
              </h3>
            </div>

            {listingReviews.length === 0 ? (
              <p className="text-sm text-gray-500">Chưa có đánh giá nào cho phòng này.</p>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                {listingReviews.map((rev) => (
                  <div key={rev.id} className="space-y-2 bg-gray-50 p-4 rounded-2xl">
                    <div className="flex items-center gap-3">
                      <img
                        src={rev.avatar}
                        alt={rev.author}
                        className="w-10 h-10 rounded-full object-cover"
                      />
                      <div>
                        <p className="font-bold text-gray-900 text-sm">{rev.author}</p>
                        <p className="text-xs text-gray-500">{rev.date}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-1 text-amber-500">
                      {[...Array(rev.rating)].map((_, i) => (
                        <Star key={i} className="w-3.5 h-3.5 fill-current" />
                      ))}
                    </div>
                    <p className="text-gray-700 text-xs leading-relaxed">
                      "{rev.comment}"
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Contact Host button */}
          <div className="py-6 flex items-center justify-between bg-rose-50/50 p-6 rounded-3xl border border-rose-100">
            <div>
              <h4 className="font-bold text-gray-900 text-base">
                Bạn có câu hỏi cho chủ nhà?
              </h4>
              <p className="text-xs text-gray-600 mt-1">
                Nhắn tin trực tiếp với {listing.host?.name} để hỏi thêm về giờ giấc check-in, tiện nghi hoặc các lưu ý.
              </p>
            </div>
            <button
              onClick={() => startConversationWithHost(listing)}
              className="flex items-center gap-2 bg-white border border-gray-300 hover:border-gray-900 text-gray-900 font-bold px-5 py-3 rounded-2xl text-xs shadow-sm transition-all"
            >
              <MessageSquare className="w-4 h-4 text-[#FF385C]" />
              Nhắn tin cho Chủ nhà
            </button>
          </div>
        </div>

        {/* Right Col: Sticky Booking Box (BR-03, BR-04) */}
        <div className="lg:col-span-1">
          <div className="sticky top-28 bg-white border border-gray-200 rounded-3xl p-6 shadow-xl space-y-5">
            {/* Price header */}
            <div className="flex items-baseline justify-between pb-4 border-b border-gray-100">
              <div>
                <span className="text-2xl font-black text-gray-900">
                  {listing.base_price.toLocaleString("vi-VN")} ₫
                </span>
                <span className="text-gray-500 text-xs font-medium"> / đêm</span>
              </div>
              <div className="flex items-center gap-1 text-xs font-bold text-gray-900">
                <Star className="w-3.5 h-3.5 fill-current" />
                <span>{listing.rating ? listing.rating.toFixed(2) : "Mới"}</span>
              </div>
            </div>

            {/* Error Message */}
            {errorMsg && (
              <div className="bg-red-50 border border-red-200 text-red-700 p-3 rounded-2xl text-xs flex items-start gap-2">
                <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5 text-red-600" />
                <span>{errorMsg}</span>
              </div>
            )}

            {/* Date Picker Form */}
            <div className="border border-gray-300 rounded-2xl overflow-hidden divide-y divide-gray-300">
              <div className="grid grid-cols-2 divide-x divide-gray-300">
                <div className="p-2.5">
                  <label className="text-[10px] font-bold text-gray-600 uppercase block">
                    Nhận phòng
                  </label>
                  <input
                    type="date"
                    value={checkIn}
                    onChange={(e) => {
                      setCheckIn(e.target.value);
                      setErrorMsg("");
                    }}
                    className="w-full text-xs font-bold text-gray-900 bg-transparent outline-none cursor-pointer mt-0.5"
                  />
                </div>
                <div className="p-2.5">
                  <label className="text-[10px] font-bold text-gray-600 uppercase block">
                    Trả phòng
                  </label>
                  <input
                    type="date"
                    value={checkOut}
                    min={checkIn}
                    onChange={(e) => {
                      setCheckOut(e.target.value);
                      setErrorMsg("");
                    }}
                    className="w-full text-xs font-bold text-gray-900 bg-transparent outline-none cursor-pointer mt-0.5"
                  />
                </div>
              </div>

              {/* Guests */}
              <div className="p-2.5">
                <label className="text-[10px] font-bold text-gray-600 uppercase block">
                  Khách (Tối đa {listing.capacity} người)
                </label>
                <div className="flex items-center justify-between mt-1">
                  <span className="text-xs font-bold text-gray-900">
                    {guests} người lớn & trẻ em
                  </span>
                  <div className="flex items-center gap-2">
                    <button
                      disabled={guests <= 1}
                      onClick={() => setGuests((g) => Math.max(1, g - 1))}
                      className="w-6 h-6 rounded-full border border-gray-300 flex items-center justify-center text-xs font-bold text-gray-700 disabled:opacity-30"
                    >
                      -
                    </button>
                    <button
                      disabled={guests >= listing.capacity}
                      onClick={() => setGuests((g) => Math.min(listing.capacity, g + 1))}
                      className="w-6 h-6 rounded-full border border-gray-300 flex items-center justify-center text-xs font-bold text-gray-700 disabled:opacity-30"
                    >
                      +
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* Instant Reserve Button */}
            <button
              onClick={handleBookNow}
              className="w-full bg-gradient-to-r from-[#FF385C] to-[#E00B41] hover:opacity-95 text-white font-extrabold py-3.5 px-4 rounded-2xl shadow-lg transition-all active:scale-95 text-sm uppercase tracking-wide"
            >
              Đặt phòng ngay
            </button>

            <p className="text-center text-xs text-gray-500 font-medium">
              Bạn vẫn chưa bị trừ tiền ở bước này
            </p>

            {/* Price breakdown calculation (BR-04) */}
            <div className="space-y-2.5 pt-2 text-xs text-gray-600 divide-y divide-gray-100">
              <div className="flex justify-between items-center pt-2">
                <span className="underline">
                  {listing.base_price.toLocaleString("vi-VN")} ₫ × {nights} đêm
                </span>
                <span className="font-semibold text-gray-900">
                  {subtotal.toLocaleString("vi-VN")} ₫
                </span>
              </div>

              <div className="flex justify-between items-center pt-2">
                <span className="underline">Phí dịch vụ Airbnb (8%)</span>
                <span className="font-semibold text-gray-900">
                  {serviceFee.toLocaleString("vi-VN")} ₫
                </span>
              </div>

              <div className="flex justify-between items-center pt-2">
                <span className="underline">Thuế giá trị gia tăng VAT (8%)</span>
                <span className="font-semibold text-gray-900">
                  {tax.toLocaleString("vi-VN")} ₫
                </span>
              </div>

              <div className="flex justify-between items-center pt-3 text-sm font-black text-gray-900">
                <span>Tổng tiền thanh toán</span>
                <span className="text-[#FF385C] text-base">
                  {total.toLocaleString("vi-VN")} ₫
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
