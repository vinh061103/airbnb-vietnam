import React, { useState } from "react";
import { useApp } from "../context/AppContext";
import { AMENITIES_LIST } from "../data/initialData";
import { X, Check } from "lucide-react";

export default function FilterModal({ isOpen, onClose }) {
  const { searchParams, setSearchParams } = useApp();

  const [minPrice, setMinPrice] = useState(searchParams.priceRange[0] || 0);
  const [maxPrice, setMaxPrice] = useState(searchParams.priceRange[1] || 10000000);
  const [selectedAmenities, setSelectedAmenities] = useState(
    searchParams.selectedAmenities || []
  );
  const [sortBy, setSortBy] = useState(searchParams.sortBy || "recommended");

  if (!isOpen) return null;

  const toggleAmenity = (id) => {
    setSelectedAmenities((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  const handleApply = () => {
    setSearchParams((prev) => ({
      ...prev,
      priceRange: [Number(minPrice), Number(maxPrice)],
      selectedAmenities,
      sortBy,
    }));
    onClose();
  };

  const handleReset = () => {
    setMinPrice(0);
    setMaxPrice(10000000);
    setSelectedAmenities([]);
    setSortBy("recommended");
    setSearchParams((prev) => ({
      ...prev,
      priceRange: [0, 10000000],
      selectedAmenities: [],
      sortBy: "recommended",
    }));
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 animate-in fade-in">
      <div className="bg-white rounded-3xl w-full max-w-xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 rounded-full text-gray-500 hover:text-gray-900"
          >
            <X className="w-5 h-5" />
          </button>
          <h3 className="font-bold text-gray-900 text-base">Bộ lọc tìm kiếm</h3>
          <div className="w-5" />
        </div>

        {/* Body */}
        <div className="p-6 overflow-y-auto space-y-6 text-sm divide-y divide-gray-100">
          {/* Sắp xếp */}
          <div className="space-y-3">
            <h4 className="font-bold text-gray-900 text-base">Sắp xếp theo</h4>
            <div className="grid grid-cols-2 gap-2">
              {[
                { id: "recommended", label: "Phù hợp nhất" },
                { id: "price_asc", label: "Giá tăng dần (Thấp → Cao)" },
                { id: "price_desc", label: "Giá giảm dần (Cao → Thấp)" },
                { id: "rating", label: "Đánh giá cao nhất" },
              ].map((opt) => (
                <button
                  key={opt.id}
                  onClick={() => setSortBy(opt.id)}
                  className={`py-2.5 px-3 rounded-xl border text-left font-semibold text-xs transition-colors flex items-center justify-between ${
                    sortBy === opt.id
                      ? "border-gray-900 bg-gray-900 text-white"
                      : "border-gray-200 text-gray-700 hover:border-gray-400"
                  }`}
                >
                  <span>{opt.label}</span>
                  {sortBy === opt.id && <Check className="w-3.5 h-3.5" />}
                </button>
              ))}
            </div>
          </div>

          {/* Khoảng giá */}
          <div className="pt-6 space-y-3">
            <h4 className="font-bold text-gray-900 text-base">Khoảng giá mỗi đêm</h4>
            <div className="flex items-center gap-4">
              <div className="flex-1 border border-gray-300 rounded-2xl p-3 focus-within:border-gray-900">
                <label className="text-[11px] font-bold text-gray-500 block uppercase">
                  Tối thiểu (VND)
                </label>
                <input
                  type="number"
                  step="100000"
                  value={minPrice}
                  onChange={(e) => setMinPrice(e.target.value)}
                  className="w-full font-bold text-gray-900 bg-transparent outline-none mt-1"
                />
              </div>
              <span className="text-gray-400 font-bold">-</span>
              <div className="flex-1 border border-gray-300 rounded-2xl p-3 focus-within:border-gray-900">
                <label className="text-[11px] font-bold text-gray-500 block uppercase">
                  Tối đa (VND)
                </label>
                <input
                  type="number"
                  step="100000"
                  value={maxPrice}
                  onChange={(e) => setMaxPrice(e.target.value)}
                  className="w-full font-bold text-gray-900 bg-transparent outline-none mt-1"
                />
              </div>
            </div>
          </div>

          {/* Tiện nghi */}
          <div className="pt-6 space-y-3">
            <h4 className="font-bold text-gray-900 text-base">Tiện nghi chỗ ở</h4>
            <div className="grid grid-cols-2 gap-2.5">
              {AMENITIES_LIST.map((am) => {
                const checked = selectedAmenities.includes(am.id);
                return (
                  <button
                    key={am.id}
                    onClick={() => toggleAmenity(am.id)}
                    className={`p-3 rounded-xl border text-left font-medium text-xs transition-colors flex items-center justify-between ${
                      checked
                        ? "border-[#FF385C] bg-rose-50 text-[#FF385C]"
                        : "border-gray-200 text-gray-700 hover:border-gray-300"
                    }`}
                  >
                    <span>{am.name}</span>
                    {checked && <Check className="w-3.5 h-3.5 stroke-[3]" />}
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-gray-200 flex items-center justify-between bg-gray-50">
          <button
            onClick={handleReset}
            className="text-xs font-bold text-gray-700 hover:underline"
          >
            Xóa tất cả
          </button>
          <button
            onClick={handleApply}
            className="bg-gray-900 hover:bg-black text-white font-bold py-3 px-6 rounded-xl text-xs shadow-md transition-colors"
          >
            Xem kết quả
          </button>
        </div>
      </div>
    </div>
  );
}
