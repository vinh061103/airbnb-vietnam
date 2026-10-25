import React, { useState } from "react";
import { useApp } from "./context/AppContext";
import Navbar from "./components/Navbar";
import HeroSearch from "./components/HeroSearch";
import CategoryBar from "./components/CategoryBar";
import ListingCard from "./components/ListingCard";
import FilterModal from "./components/FilterModal";
import SearchResults from "./components/SearchResults";
import RoomDetail from "./components/RoomDetail";
import BookingCheckout from "./components/BookingCheckout";
import BookingConfirmation from "./components/BookingConfirmation";
import MyBookings from "./components/MyBookings";
import Wishlist from "./components/Wishlist";
import Messages from "./components/Messages";
import LoginPage from "./components/LoginPage";
import RegisterPage from "./components/RegisterPage";
import HostDashboard from "./components/HostDashboard";
import HostListings from "./components/HostListings";
import HostNewListing from "./components/HostNewListing";
import HostCalendar from "./components/HostCalendar";
import HostReservations from "./components/HostReservations";
import Footer from "./components/Footer";
import { Frown } from "lucide-react";

export default function App() {
  const {
    role,
    currentView,
    setCurrentView,
    listings,
    searchParams,
    setSearchParams,
    bookings,
    availabilityBlocks,
  } = useApp();

  const [filterModalOpen, setFilterModalOpen] = useState(false);

  // Filter listings for Home page (Categories & Advanced filters)
  // Specific search criteria (destination, dates, guests) will navigate to the Search Results page
  const filteredListings = listings.filter((listing) => {
    // Only published listings for customer
    if (listing.status !== "Published") return false;

    // Filter by category
    if (
      searchParams.category &&
      searchParams.category !== "all" &&
      listing.category !== searchParams.category
    ) {
      return false;
    }

    // Filter by price range (if modal filter applied)
    if (
      listing.base_price < searchParams.priceRange[0] ||
      listing.base_price > searchParams.priceRange[1]
    ) {
      return false;
    }

    // Filter by selected amenities (if modal filter applied)
    if (searchParams.selectedAmenities?.length > 0) {
      const hasAllAmenities = searchParams.selectedAmenities.every((amId) =>
        listing.amenities?.includes(amId)
      );
      if (!hasAllAmenities) return false;
    }

    return true;
  });

  // Sort listings
  const sortedListings = [...filteredListings].sort((a, b) => {
    if (searchParams.sortBy === "price_asc") {
      return a.base_price - b.base_price;
    }
    if (searchParams.sortBy === "price_desc") {
      return b.base_price - a.base_price;
    }
    if (searchParams.sortBy === "rating") {
      return (b.rating || 0) - (a.rating || 0);
    }
    return 0; // recommended
  });

  return (
    <div className="min-h-screen flex flex-col bg-white">
      {/* Top Navigation */}
      <Navbar />

      {/* Main Container */}
      <main className="flex-1">
        {/* Auth Pages (S01, S02) */}
        {currentView === "login" && <LoginPage />}
        {currentView === "register" && <RegisterPage />}

        {/* CUSTOMER VIEWS */}
        {role === "customer" && currentView !== "login" && currentView !== "register" && (
          <>
            {currentView === "home" && (
              <div>
                <HeroSearch onOpenFilter={() => setFilterModalOpen(true)} />
                <CategoryBar onOpenFilter={() => setFilterModalOpen(true)} />

                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                  {sortedListings.length === 0 ? (
                    <div className="text-center py-16 space-y-4 bg-gray-50 rounded-3xl border border-gray-200 p-8 max-w-lg mx-auto">
                      <div className="w-16 h-16 bg-rose-50 text-[#FF385C] rounded-full flex items-center justify-center mx-auto">
                        <Frown className="w-8 h-8" />
                      </div>
                      <h3 className="text-lg font-bold text-gray-900">
                        Không tìm thấy chỗ ở nào phù hợp
                      </h3>
                      <p className="text-xs text-gray-500">
                        Thử thay đổi địa điểm, nới lỏng khoảng ngày nhận/trả phòng hoặc bỏ bớt các bộ lọc tiện nghi.
                      </p>
                      <button
                        onClick={() =>
                          setSearchParams({
                            city: "",
                            checkIn: "",
                            checkOut: "",
                            guests: 1,
                            category: "all",
                            priceRange: [0, 10000000],
                            selectedAmenities: [],
                            sortBy: "recommended",
                          })
                        }
                        className="bg-gray-900 text-white font-bold py-2.5 px-6 rounded-xl text-xs hover:bg-black transition-colors"
                      >
                        Đặt lại tất cả bộ lọc
                      </button>
                    </div>
                  ) : (
                    <>
                      <div className="flex items-center justify-between mb-6">
                        <p className="text-xs font-semibold text-gray-500">
                          Hiển thị{" "}
                          <strong className="text-gray-900">{sortedListings.length}</strong>{" "}
                          chỗ ở tuyệt vời tại Việt Nam (Dữ liệu từ SQLite Database)
                        </p>
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                        {sortedListings.map((listing) => (
                          <ListingCard key={listing.id} listing={listing} />
                        ))}
                      </div>
                    </>
                  )}
                </div>
              </div>
            )}

            {currentView === "search-results" && <SearchResults />}
            {currentView === "room-detail" && <RoomDetail />}
            {currentView === "checkout" && <BookingCheckout />}
            {currentView === "confirmation" && <BookingConfirmation />}
            {currentView === "my-bookings" && <MyBookings />}
            {currentView === "wishlist" && <Wishlist />}
            {currentView === "messages" && <Messages />}
          </>
        )}

        {/* HOST VIEWS */}
        {role === "host" && currentView !== "login" && currentView !== "register" && (
          <>
            {currentView === "host-dashboard" && <HostDashboard />}
            {currentView === "host-listings" && <HostListings />}
            {currentView === "host-new-listing" && <HostNewListing />}
            {currentView === "host-calendar" && <HostCalendar />}
            {currentView === "host-reservations" && <HostReservations />}
            {currentView === "messages" && <Messages />}
          </>
        )}
      </main>

      {/* Advanced Filter Modal */}
      <FilterModal
        isOpen={filterModalOpen}
        onClose={() => setFilterModalOpen(false)}
      />

      {/* Footer */}
      <Footer />
    </div>
  );
}
