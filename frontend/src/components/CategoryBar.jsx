import React from "react";
import { useApp } from "../context/AppContext";
import { CATEGORIES } from "../data/initialData";
import {
  Flame,
  Palmtree,
  Building2,
  Trees,
  Hotel,
  Waves,
  Heart,
  Home,
  SlidersHorizontal,
} from "lucide-react";

const ICON_MAP = {
  Flame,
  Palmtree,
  Building2,
  Trees,
  Hotel,
  Waves,
  Heart,
  Home,
};

export default function CategoryBar({ onOpenFilter }) {
  const { searchParams, setSearchParams } = useApp();

  return (
    <div className="border-b border-gray-200 bg-white py-3">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between gap-4">
        {/* Scrollable Categories */}
        <div className="flex items-center gap-8 overflow-x-auto no-scrollbar scroll-smooth py-1">
          {CATEGORIES.map((cat) => {
            const IconComponent = ICON_MAP[cat.icon] || Home;
            const isSelected = (searchParams.category || "all") === cat.id;

            return (
              <button
                key={cat.id}
                onClick={() =>
                  setSearchParams((prev) => ({ ...prev, category: cat.id }))
                }
                className={`flex flex-col items-center gap-1.5 pb-2 transition-all flex-shrink-0 group relative ${
                  isSelected
                    ? "text-gray-900 font-bold border-b-2 border-gray-900"
                    : "text-gray-500 hover:text-gray-900 border-b-2 border-transparent hover:border-gray-300 font-medium"
                }`}
              >
                <IconComponent
                  className={`w-6 h-6 transition-transform group-hover:scale-110 ${
                    isSelected ? "text-gray-900" : "text-gray-500 group-hover:text-gray-800"
                  }`}
                />
                <span className="text-xs sm:text-sm font-semibold whitespace-nowrap">{cat.label}</span>
              </button>
            );
          })}
        </div>

        {/* Filter Trigger Button */}
        <div className="hidden sm:block flex-shrink-0 pl-4">
          <button
            onClick={onOpenFilter}
            className="flex items-center gap-2 border border-gray-300 rounded-xl px-4 py-2.5 text-xs sm:text-sm font-bold text-gray-800 hover:border-gray-900 transition-colors shadow-sm"
          >
            <SlidersHorizontal className="w-4 h-4" />
            <span>Bộ lọc</span>
          </button>
        </div>
      </div>
    </div>
  );
}
