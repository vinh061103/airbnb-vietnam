import React, { useState } from "react";
import { useApp } from "../context/AppContext";
import { normalizeVietnamese } from "../utils/vietnamese";
import {
  ArrowLeft,
  MapPin,
  Calendar,
  Users,
  Star,
  Heart,
  SlidersHorizontal,
  ChevronLeft,
  ChevronRight,
  Frown,
  Edit3,
  Check,
  Search,
  Sparkles,
} from "lucide-react";

export default function SearchResults() {
  const {
    activeSearch,
    setActiveSearch,
    setCurrentView,
    setSelectedListingId,
    listings,
    bookings,
    availabilityBlocks,
    wishlist,
    toggleWishlist,
  } = useApp();

  const effectiveSearch = activeSearch || {
    city: "Đà Lạt",
    checkIn: "2026-11-15",
    checkOut: "2026-11-18",
    guests: 2,
    nights: 3,
  };

  const [sortBy, setSortBy] = useState("recommended");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [isEditing, setIsEditing] = useState(false);

  // Edit form state
  const [editCity, setEditCity] = useState(effectiveSearch.city || "");
  const [editCheckIn, setEditCheckIn] = useState(effectiveSearch.checkIn || "");
  const [editCheckOut, setEditCheckOut] = useState(effectiveSearch.checkOut || "");
  const [editGuests, setEditGuests] = useState(effectiveSearch.guests || 1);
  const [editError, setEditError] = useState("");

  // Handle re-search
  const handleUpdateSearch = () => {
    setEditError("");
    if (!editCity.trim()) {
      setEditError("Vui lòng nhập hoặc chọn Địa điểm!");
      return;
    }
    if (!editCheckIn) {
      setEditError("Vui lòng chọn Ngày nhận phòng!");
      return;
    }
    if (!editCheckOut) {
      setEditError("Vui lòng chọn Ngày trả phòng!");
      return;
    }

    const start = new Date(editCheckIn);
    const end = new Date(editCheckOut);
    if (end <= start) {
      setEditError("Ngày trả phòng phải sau ngày nhận phòng ít nhất 1 đêm!");
      return;
    }

    const nights = Math.max(1, Math.round((end - start) / (1000 * 60 * 60 * 24)));

    setActiveSearch({
      city: editCity.trim(),
      checkIn: editCheckIn,
      checkOut: editCheckOut,
      guests: Number(editGuests) || 1,
      nights,
    });
    setIsEditing(false);
  };

  // Filter listings based on effectiveSearch criteria
  const matchingListings = listings.filter((listing) => {
    if (listing.status !== "Published") return false;

    // 1. Destination match (accent-insensitive)
    if (effectiveSearch.city) {
      const normCity = normalizeVietnamese(listing.city);
      const normQuery = normalizeVietnamese(effectiveSearch.city);
      if (!normCity.includes(normQuery) && !normQuery.includes(normCity)) {
        return false;
      }
    }

    // 2. Capacity match
    if (listing.capacity < effectiveSearch.guests) {
      return false;
    }

    // 3. Availability match (no overlap with bookings or blocks)
    if (effectiveSearch.checkIn && effectiveSearch.checkOut) {
      const reqStart = new Date(effectiveSearch.checkIn);
      const reqEnd = new Date(effectiveSearch.checkOut);

      // Bookings conflict
      const hasBookingConflict = bookings.some((b) => {
        if (b.listing_id !== listing.id || b.status !== "Confirmed") return false;
        const bStart = new Date(b.check_in);
        const bEnd = new Date(b.check_out);
        return reqStart < bEnd && reqEnd > bStart;
      });
      if (hasBookingConflict) return false;

      // Host calendar blocks conflict
      const hasBlockConflict = availabilityBlocks.some((blk) => {
        if (blk.listing_id !== listing.id) return false;
        const blkStart = new Date(blk.start_date);
        const blkEnd = new Date(blk.end_date);
        return reqStart < blkEnd && reqEnd > blkStart;
      });
      if (hasBlockConflict) return false;
    }

    // 4. Category filter
    if (selectedCategory !== "all" && listing.category !== selectedCategory) {
      return false;
    }

    return true;
  });

  // Sort listings
  const sortedListings = [...matchingListings].sort((a, b) => {
    if (sortBy === "price_asc") return a.base_price - b.base_price;
    if (sortBy === "price_desc") return b.base_price - a.base_price;
    if (sortBy === "rating") return (b.rating || 0) - (a.rating || 0);
    return 0;
  });

  const categoriesList = [
    { id: "all", label: "Tất cả loại phòng" },
    { id: "villa", label: "Biệt thự cao cấp" },
    { id: "homestay", label: "Homestay ấm cúng" },
    { id: "beach", label: "Gần biển" },
    { id: "nature", label: "Núi rừng & Thiên nhiên" },
    { id: "city", label: "Trung tâm thành phố" },
    { id: "pool", label: "Hồ bơi vô cực" },
  ];

  return (
    <div className="bg-gray-50 min-h-screen py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Navigation Breadcrumb & Back button */}
        <div className="flex items-center justify-between mb-6">
          <button
            onClick={() => setCurrentView("home")}
            className="inline-flex items-center gap-2 text-sm font-bold text-gray-700 hover:text-black bg-white px-4 py-2 rounded-xl border border-gray-200 shadow-sm transition-all hover:bg-gray-100"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>← Quay lại Trang chủ</span>
          </button>

          <span className="text-xs font-semibold text-gray-500 hidden sm:inline-block">
            Trang chủ &gt; Kết quả tìm kiếm &gt; {effectiveSearch.city}
          </span>
        </div>

        {/* Search Recap Hero Card */}
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-sm mb-8">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 pb-6 border-b border-gray-100">
            <div>
              <div className="flex items-center gap-2 text-[#FF385C] font-extrabold text-xs uppercase tracking-wider mb-2">
                <Sparkles className="w-4 h-4" />
                <span>Trang kết quả tìm kiếm đã xác thực</span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-black text-gray-900 tracking-tight">
                Chỗ ở tại {effectiveSearch.city}
              </h1>
              <p className="text-sm text-gray-500 mt-1">
                Tìm thấy{" "}
                <strong className="text-gray-900 font-bold">
                  {sortedListings.length} chỗ ở còn phòng trống
                </strong>{" "}
                phù hợp với tiêu chí của bạn
              </p>
            </div>

            {/* Quick action buttons */}
            <div className="flex items-center gap-3">
              <button
                onClick={() => setIsEditing(!isEditing)}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full border border-gray-300 font-bold text-sm text-gray-800 hover:border-gray-900 transition-colors shadow-sm bg-white"
              >
                <Edit3 className="w-4 h-4 text-[#FF385C]" />
                <span>{isEditing ? "Đóng chỉnh sửa" : "Chỉnh sửa tìm kiếm"}</span>
              </button>
            </div>
          </div>

          {/* Search Specs Badges */}
          <div className="flex items-center gap-3 flex-wrap mt-4">
            <div className="inline-flex items-center gap-2 bg-rose-50 border border-rose-200 px-4 py-2 rounded-2xl text-sm font-bold text-[#FF385C]">
              <MapPin className="w-4 h-4" />
              <span>Điểm đến: {effectiveSearch.city}</span>
            </div>

            <div className="inline-flex items-center gap-2 bg-blue-50 border border-blue-200 px-4 py-2 rounded-2xl text-sm font-bold text-blue-700">
              <Calendar className="w-4 h-4" />
              <span>
                {effectiveSearch.checkIn} → {effectiveSearch.checkOut} ({effectiveSearch.nights} đêm)
              </span>
            </div>

            <div className="inline-flex items-center gap-2 bg-emerald-50 border border-emerald-200 px-4 py-2 rounded-2xl text-sm font-bold text-emerald-700">
              <Users className="w-4 h-4" />
              <span>{effectiveSearch.guests} khách</span>
            </div>
          </div>

          {/* Inline Edit Search Form (Collapsible) */}
          {isEditing && (
            <div className="mt-6 pt-6 border-t border-gray-100 bg-gray-50 rounded-2xl p-5 animate-in fade-in">
              <h3 className="text-sm font-extrabold text-gray-900 mb-3">
                Thay đổi ngày hoặc thông tin tìm kiếm:
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                <div>
                  <label className="block text-xs font-bold text-gray-600 mb-1">
                    Địa điểm
                  </label>
                  <input
                    type="text"
                    value={editCity}
                    onChange={(e) => setEditCity(e.target.value)}
                    className="w-full bg-white border border-gray-300 rounded-xl px-3 py-2 text-sm font-semibold outline-none focus:border-[#FF385C]"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-gray-600 mb-1">
                    Ngày nhận phòng
                  </label>
                  <input
                    type="date"
                    value={editCheckIn}
                    onChange={(e) => setEditCheckIn(e.target.value)}
                    className="w-full bg-white border border-gray-300 rounded-xl px-3 py-2 text-sm font-semibold outline-none focus:border-[#FF385C]"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-gray-600 mb-1">
                    Ngày trả phòng
                  </label>
                  <input
                    type="date"
                    value={editCheckOut}
                    min={editCheckIn || undefined}
                    onChange={(e) => setEditCheckOut(e.target.value)}
                    className="w-full bg-white border border-gray-300 rounded-xl px-3 py-2 text-sm font-semibold outline-none focus:border-[#FF385C]"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-gray-600 mb-1">
                    Số lượng khách
                  </label>
                  <div className="flex items-center gap-2">
                    <input
                      type="number"
                      min={1}
                      max={20}
                      value={editGuests}
                      onChange={(e) => setEditGuests(e.target.value)}
                      className="w-24 bg-white border border-gray-300 rounded-xl px-3 py-2 text-sm font-semibold outline-none focus:border-[#FF385C]"
                    />
                    <button
                      onClick={handleUpdateSearch}
                      className="flex-1 bg-gray-900 hover:bg-black text-white font-bold py-2 px-4 rounded-xl text-xs transition-colors"
                    >
                      Cập nhật
                    </button>
                  </div>
                </div>
              </div>

              {editError && (
                <p className="text-xs text-rose-600 font-bold mt-2">
                  ⚠️ {editError}
                </p>
              )}
            </div>
          )}
        </div>

        {/* Filter bar & Sort dropdown */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          {/* Category Chips */}
          <div className="flex items-center gap-2 overflow-x-auto no-scrollbar py-1">
            {categoriesList.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setSelectedCategory(cat.id)}
                className={`px-4 py-2 rounded-full text-xs font-bold whitespace-nowrap transition-all ${
                  selectedCategory === cat.id
                    ? "bg-gray-900 text-white shadow-sm"
                    : "bg-white text-gray-700 hover:bg-gray-100 border border-gray-200"
                }`}
              >
                {cat.label}
              </button>
            ))}
          </div>

          {/* Sort Selector */}
          <div className="flex items-center gap-2 flex-shrink-0 self-end sm:self-auto">
            <span className="text-xs font-semibold text-gray-500">Sắp xếp theo:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="bg-white border border-gray-200 rounded-xl px-3 py-1.5 text-xs font-bold text-gray-800 outline-none shadow-sm cursor-pointer"
            >
              <option value="recommended">Được đề xuất</option>
              <option value="price_asc">Giá: Thấp đến Cao</option>
              <option value="price_desc">Giá: Cao đến Thấp</option>
              <option value="rating">Đánh giá cao nhất</option>
            </select>
          </div>
        </div>

        {/* LISTINGS RESULT GRID */}
        {sortedListings.length === 0 ? (
          <div className="bg-white rounded-3xl border border-gray-200 p-12 text-center max-w-xl mx-auto shadow-sm my-8">
            <div className="w-16 h-16 bg-rose-50 text-[#FF385C] rounded-full flex items-center justify-center mx-auto mb-4">
              <Frown className="w-8 h-8" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">
              Không tìm thấy chỗ ở nào còn trống tại {effectiveSearch.city}
            </h3>
            <p className="text-sm text-gray-500 mb-6 leading-relaxed">
              Các chỗ ở tại đây có thể đã kín lịch trong khoảng ngày{" "}
              <strong>
                {effectiveSearch.checkIn} → {effectiveSearch.checkOut}
              </strong>{" "}
              hoặc không đủ sức chứa cho <strong>{effectiveSearch.guests} khách</strong>.
            </p>

            <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4 text-left text-xs text-amber-800 space-y-1.5 mb-6">
              <p className="font-bold">Gợi ý tìm kiếm:</p>
              <p>• Thử chọn khoảng ngày nhận/trả phòng khác linh hoạt hơn.</p>
              <p>• Thử giảm số lượng khách nếu bạn có thể đặt 2 phòng riêng biệt.</p>
              <p>• Khám phá các địa điểm du lịch gần đó như Đà Lạt, Hội An, Vũng Tàu...</p>
            </div>

            <div className="flex items-center justify-center gap-3">
              <button
                onClick={() => setIsEditing(true)}
                className="bg-gray-900 hover:bg-black text-white font-bold py-2.5 px-6 rounded-xl text-xs transition-colors"
              >
                Đổi ngày tìm kiếm
              </button>
              <button
                onClick={() => setCurrentView("home")}
                className="bg-white hover:bg-gray-100 text-gray-800 font-bold py-2.5 px-6 rounded-xl text-xs border border-gray-300 transition-colors"
              >
                Quay về trang chủ
              </button>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {sortedListings.map((listing) => {
              const isLiked = wishlist.includes(listing.id);
              const nights = effectiveSearch.nights || 1;
              const totalPrice = nights * listing.base_price;

              return (
                <div
                  key={listing.id}
                  className="bg-white rounded-2xl overflow-hidden border border-gray-200 shadow-sm hover:shadow-xl transition-all flex flex-col group cursor-pointer"
                  onClick={() => {
                    setSelectedListingId(listing.id);
                    setCurrentView("room-detail", listing.id);
                  }}
                >
                  {/* Photo area */}
                  <div className="relative aspect-[4/3] bg-gray-100 overflow-hidden">
                    <img
                      src={listing.images?.[0] || "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800"}
                      alt={listing.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />

                    {/* Guest favorite badge */}
                    {listing.rating >= 4.9 && (
                      <div className="absolute top-3 left-3 bg-white/95 backdrop-blur-sm text-gray-900 text-xs font-black px-2.5 py-1 rounded-full shadow-sm tracking-wide">
                        ĐƯỢC YÊU THÍCH
                      </div>
                    )}

                    {/* Wishlist button */}
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        toggleWishlist(listing.id);
                      }}
                      className="absolute top-3 right-3 p-2 rounded-full hover:scale-110 active:scale-95 transition-transform text-white drop-shadow-md"
                    >
                      <Heart
                        className={`w-5 h-5 ${
                          isLiked ? "fill-[#FF385C] text-[#FF385C]" : "fill-black/30 text-white"
                        }`}
                      />
                    </button>

                    {/* Available badge */}
                    <div className="absolute bottom-3 left-3 bg-emerald-600/90 text-white text-[11px] font-bold px-2 py-0.5 rounded-md backdrop-blur-sm shadow">
                      ✓ Còn phòng trống
                    </div>
                  </div>

                  {/* Body Content */}
                  <div className="p-4 flex-1 flex flex-col justify-between">
                    <div>
                      {/* Location & Rating */}
                      <div className="flex items-center justify-between text-xs font-bold text-gray-600 mb-1">
                        <span className="truncate flex items-center gap-1 text-gray-700">
                          <MapPin className="w-3.5 h-3.5 text-[#FF385C]" />
                          {listing.city}, Việt Nam
                        </span>
                        <div className="flex items-center gap-1 text-gray-900 font-extrabold flex-shrink-0">
                          <Star className="w-3.5 h-3.5 fill-black text-black" />
                          <span>{listing.rating || 4.9}</span>
                          <span className="text-gray-400 font-normal">
                            ({listing.review_count || 12})
                          </span>
                        </div>
                      </div>

                      {/* Title */}
                      <h3 className="font-bold text-gray-900 text-sm line-clamp-2 leading-snug group-hover:text-[#FF385C] transition-colors mb-1.5">
                        {listing.title}
                      </h3>

                      {/* Room specs */}
                      <p className="text-xs text-gray-500 mb-3">
                        {listing.room_type} • Sức chứa {listing.capacity} khách • {listing.bedrooms} PN
                      </p>
                    </div>

                    {/* Pricing */}
                    <div className="pt-3 border-t border-gray-100">
                      <div className="flex items-baseline justify-between">
                        <div>
                          <span className="text-base font-extrabold text-gray-900">
                            {listing.base_price?.toLocaleString("vi-VN")}₫
                          </span>
                          <span className="text-xs text-gray-500 font-normal"> / đêm</span>
                        </div>
                        <span className="text-xs font-bold text-rose-600 bg-rose-50 px-2 py-0.5 rounded">
                          Tổng: {totalPrice.toLocaleString("vi-VN")}₫ ({nights} đêm)
                        </span>
                      </div>

                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedListingId(listing.id);
                          setCurrentView("room-detail", listing.id);
                        }}
                        className="mt-3 w-full bg-gradient-to-r from-[#FF385C] to-[#E00B41] hover:brightness-105 active:scale-95 text-white font-bold py-2 rounded-xl text-xs transition-all shadow-sm"
                      >
                        Xem phòng & Đặt ngay
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
