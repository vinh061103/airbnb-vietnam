import React from "react";
import { useApp } from "../context/AppContext";
import ListingCard from "./ListingCard";
import { Heart, Compass } from "lucide-react";

export default function Wishlist() {
  const { wishlist, listings, setCurrentView } = useApp();

  const favoriteListings = listings.filter((l) => wishlist.includes(l.id));

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-2xl sm:text-3xl font-black text-gray-900 flex items-center gap-2">
          <Heart className="w-8 h-8 text-[#FF385C] fill-[#FF385C]" />
          Danh sách yêu thích của bạn
        </h1>
        <p className="text-xs sm:text-sm text-gray-500 mt-1">
          Lưu giữ những căn phòng và biệt thự tuyệt vời bạn dự định ghé thăm (C09)
        </p>
      </div>

      {favoriteListings.length === 0 ? (
        <div className="bg-white border border-gray-200 rounded-3xl p-12 text-center space-y-4 max-w-xl mx-auto mt-8">
          <div className="w-16 h-16 bg-rose-50 text-[#FF385C] rounded-full flex items-center justify-center mx-auto">
            <Heart className="w-8 h-8" />
          </div>
          <h3 className="font-bold text-gray-900 text-lg">
            Bạn chưa lưu chỗ ở nào
          </h3>
          <p className="text-xs text-gray-500">
            Khi tìm kiếm phòng, hãy bấm vào biểu tượng hình trái tim để lưu lại những nơi bạn yêu thích nhất!
          </p>
          <button
            onClick={() => setCurrentView("home")}
            className="bg-gray-900 hover:bg-black text-white font-bold py-3 px-6 rounded-2xl text-xs shadow-md transition-all inline-flex items-center gap-2"
          >
            <Compass className="w-4 h-4" />
            Khám phá phòng ngay
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {favoriteListings.map((listing) => (
            <ListingCard key={listing.id} listing={listing} />
          ))}
        </div>
      )}
    </div>
  );
}
