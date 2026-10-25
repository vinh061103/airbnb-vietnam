import React, { useState } from "react";
import { useApp } from "../context/AppContext";
import { Star, Heart, ChevronLeft, ChevronRight, MapPin } from "lucide-react";

export default function ListingCard({ listing }) {
  const { wishlist, toggleWishlist, setSelectedListingId, setCurrentView } =
    useApp();

  const isLiked = wishlist.includes(listing.id);
  const [currentImgIndex, setCurrentImgIndex] = useState(0);

  const images = listing.images?.length ? listing.images : [listing.cover_image];

  const handleNextImg = (e) => {
    e.stopPropagation();
    setCurrentImgIndex((prev) => (prev + 1) % images.length);
  };

  const handlePrevImg = (e) => {
    e.stopPropagation();
    setCurrentImgIndex((prev) => (prev - 1 + images.length) % images.length);
  };

  const handleCardClick = () => {
    setSelectedListingId(listing.id);
    setCurrentView("room-detail");
  };

  return (
    <div
      onClick={handleCardClick}
      className="group cursor-pointer flex flex-col transition-transform duration-200"
    >
      {/* Image Gallery Container */}
      <div className="relative aspect-square w-full overflow-hidden rounded-2xl bg-gray-200">
        <img
          src={images[currentImgIndex]}
          alt={listing.title}
          className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
        />

        {/* Wishlist Heart Button (FR-12) */}
        <button
          onClick={(e) => {
            e.stopPropagation();
            toggleWishlist(listing.id);
          }}
          className="absolute top-3 right-3 p-2 rounded-full hover:scale-115 active:scale-95 transition-transform"
          title={isLiked ? "Bỏ lưu yêu thích" : "Lưu vào yêu thích"}
        >
          <Heart
            className={`w-6 h-6 stroke-white stroke-[2] drop-shadow-md ${
              isLiked ? "fill-[#FF385C] stroke-[#FF385C]" : "fill-black/30"
            }`}
          />
        </button>

        {/* Carousel Arrows on Hover */}
        {images.length > 1 && (
          <>
            <button
              onClick={handlePrevImg}
              className="absolute left-2 top-1/2 -translate-y-1/2 w-7 h-7 rounded-full bg-white/90 shadow hover:bg-white flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
            >
              <ChevronLeft className="w-4 h-4 text-gray-800" />
            </button>
            <button
              onClick={handleNextImg}
              className="absolute right-2 top-1/2 -translate-y-1/2 w-7 h-7 rounded-full bg-white/90 shadow hover:bg-white flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
            >
              <ChevronRight className="w-4 h-4 text-gray-800" />
            </button>

            {/* Dots */}
            <div className="absolute bottom-2.5 left-1/2 -translate-x-1/2 flex items-center gap-1.5">
              {images.map((_, idx) => (
                <span
                  key={idx}
                  className={`h-1.5 rounded-full transition-all ${
                    idx === currentImgIndex
                      ? "w-3 bg-white"
                      : "w-1.5 bg-white/60"
                  }`}
                />
              ))}
            </div>
          </>
        )}

        {/* Featured Badge */}
        {listing.is_featured && (
          <div className="absolute top-3 left-3 bg-white/95 backdrop-blur-sm px-3 py-1 rounded-full shadow-sm">
            <span className="text-xs font-black uppercase tracking-wider text-gray-900">
              Được yêu thích
            </span>
          </div>
        )}
      </div>

      {/* Info */}
      <div className="mt-3 flex flex-col gap-1">
        <div className="flex items-center justify-between">
          <p className="font-extrabold text-gray-900 text-base flex items-center gap-1.5">
            <MapPin className="w-4 h-4 text-[#FF385C]" />
            {listing.city}, Việt Nam
          </p>
          <div className="flex items-center gap-1 text-sm font-bold text-gray-900">
            <Star className="w-4 h-4 fill-current text-gray-900" />
            <span>{listing.rating ? listing.rating.toFixed(2) : "Mới"}</span>
            {listing.reviews_count > 0 && (
              <span className="text-gray-500 font-normal text-xs">({listing.reviews_count})</span>
            )}
          </div>
        </div>

        <p className="text-gray-500 text-xs sm:text-sm truncate font-medium">
          {listing.property_type} • Sức chứa {listing.capacity} khách
        </p>

        <p className="text-gray-700 text-sm line-clamp-1 font-medium">
          {listing.title}
        </p>

        <div className="mt-1 flex items-baseline gap-1">
          <span className="font-black text-gray-900 text-lg">
            {listing.base_price.toLocaleString("vi-VN")} ₫
          </span>
          <span className="text-xs text-gray-500 font-medium">/ đêm</span>
        </div>
      </div>
    </div>
  );
}
