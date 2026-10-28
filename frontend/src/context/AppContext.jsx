import React, { createContext, useContext, useState, useEffect } from "react";
import { api } from "../api/client";
import { INITIAL_LISTINGS, INITIAL_BOOKINGS, INITIAL_REVIEWS, INITIAL_MESSAGES, INITIAL_BLOCKS } from "../data/initialData";

const AppContext = createContext();

const parseUrlToState = () => {
  if (typeof window === "undefined") return { view: "home" };
  const path = window.location.pathname.toLowerCase().replace(/\/$/, "");

  if (path === "/login") return { view: "login" };
  if (path === "/register") return { view: "register" };
  if (path === "/search") return { view: "search-results" };

  const roomMatch = path.match(/^\/rooms?\/([0-9]+)/);
  if (roomMatch) {
    return { view: "room-detail", id: Number(roomMatch[1]) };
  }

  if (path === "/checkout") return { view: "checkout" };
  if (path === "/confirmation") return { view: "confirmation" };
  if (path === "/my-bookings" || path === "/trips") return { view: "my-bookings" };
  if (path === "/wishlist") return { view: "wishlist" };
  if (path === "/messages") return { view: "messages" };

  if (path === "/host" || path === "/host/dashboard") return { view: "host-dashboard" };
  if (path === "/host/listings") return { view: "host-listings" };
  if (path === "/host/new-listing") return { view: "host-new-listing" };
  if (path === "/host/calendar") return { view: "host-calendar" };
  if (path === "/host/reservations") return { view: "host-reservations" };

  return { view: "home" };
};

const getUrlForView = (view, id) => {
  switch (view) {
    case "login": return "/login";
    case "register": return "/register";
    case "search-results": return "/search";
    case "room-detail": return `/rooms/${id || 101}`;
    case "checkout": return "/checkout";
    case "confirmation": return "/confirmation";
    case "my-bookings": return "/my-bookings";
    case "wishlist": return "/wishlist";
    case "messages": return "/messages";
    case "host-dashboard": return "/host/dashboard";
    case "host-listings": return "/host/listings";
    case "host-new-listing": return "/host/new-listing";
    case "host-calendar": return "/host/calendar";
    case "host-reservations": return "/host/reservations";
    case "home":
    default: return "/";
  }
};

export function AppProvider({ children }) {
  const initialRoute = parseUrlToState();

  // Current user state (null if not logged in)
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("airbnb_user");
    return saved ? JSON.parse(saved) : null;
  });

  const [role, setRole] = useState(() => {
    if (initialRoute.view.startsWith("host-")) return "host";
    const savedUser = localStorage.getItem("airbnb_user");
    if (savedUser) {
      try {
        const u = JSON.parse(savedUser);
        return u.role || "customer";
      } catch (e) {}
    }
    return "customer";
  });

  const [listings, setListings] = useState(INITIAL_LISTINGS);
  const [bookings, setBookings] = useState(INITIAL_BOOKINGS);
  const [reviews, setReviews] = useState(INITIAL_REVIEWS);
  const [availabilityBlocks, setAvailabilityBlocks] = useState(INITIAL_BLOCKS);
  const [wishlist, setWishlist] = useState(() => {
    const saved = localStorage.getItem("airbnb_wishlist");
    return saved ? JSON.parse(saved) : [101, 102];
  });
  const [conversations, setConversations] = useState(INITIAL_MESSAGES);

  // Navigation views synchronized with browser URL
  const [currentView, setCurrentViewState] = useState(initialRoute.view);
  const [selectedListingId, setSelectedListingIdState] = useState(initialRoute.id || 101);
  const [pendingBookingData, setPendingBookingData] = useState(null);
  const [lastCreatedBooking, setLastCreatedBooking] = useState(null);

  // Active submitted search criteria for Search Results Page
  const [activeSearch, setActiveSearch] = useState(null); // { city, checkIn, checkOut, guests, nights }

  const setCurrentView = (view, optionalId) => {
    const targetId = optionalId !== undefined ? optionalId : selectedListingId;
    setCurrentViewState(view);
    if (optionalId !== undefined) {
      setSelectedListingIdState(optionalId);
    }

    if (view.startsWith("host-")) {
      setRole("host");
    } else if (["home", "search-results", "room-detail", "checkout", "confirmation", "my-bookings", "wishlist"].includes(view)) {
      setRole("customer");
    }

    const targetUrl = getUrlForView(view, targetId);
    if (typeof window !== "undefined" && window.location.pathname !== targetUrl) {
      window.history.pushState({ view, id: targetId }, "", targetUrl);
    }
  };

  const setSelectedListingId = (id) => {
    setSelectedListingIdState(id);
    if (currentView === "room-detail" && typeof window !== "undefined") {
      const targetUrl = `/rooms/${id}`;
      if (window.location.pathname !== targetUrl) {
        window.history.pushState({ view: "room-detail", id }, "", targetUrl);
      }
    }
  };

  // Sync with browser back/forward buttons (popstate)
  useEffect(() => {
    const handlePopState = () => {
      const { view, id } = parseUrlToState();
      setCurrentViewState(view);
      if (id) setSelectedListingIdState(id);
      if (view.startsWith("host-")) {
        setRole("host");
      } else if (["home", "search-results", "room-detail", "checkout", "confirmation", "my-bookings", "wishlist"].includes(view)) {
        setRole("customer");
      }
    };
    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, [selectedListingId]);

  // Global search params
  const [searchParams, setSearchParams] = useState({
    city: "",
    checkIn: "",
    checkOut: "",
    guests: 1,
    category: "all",
    priceRange: [0, 10000000],
    selectedAmenities: [],
    sortBy: "recommended",
  });

  // Sync data from SQLite Backend API
  const refreshDataFromBackend = async () => {
    try {
      const listingsRes = await api.getListings();
      if (listingsRes.data && listingsRes.data.length > 0) {
        setListings(listingsRes.data);
      }
    } catch (e) {
      console.log("Using local listings fallback:", e.message);
    }

    try {
      const bookingsRes = await api.getBookings();
      if (bookingsRes.data) {
        setBookings(bookingsRes.data);
      }
    } catch (e) {}

    try {
      const revsRes = await api.getReviews();
      if (revsRes.data) {
        setReviews(revsRes.data);
      }
    } catch (e) {}

    try {
      const blocksRes = await api.getBlocks();
      if (blocksRes.data) {
        setAvailabilityBlocks(blocksRes.data);
      }
    } catch (e) {}
  };

  useEffect(() => {
    refreshDataFromBackend();
  }, []);

  // Save wishlist
  useEffect(() => {
    localStorage.setItem("airbnb_wishlist", JSON.stringify(wishlist));
  }, [wishlist]);

  // Auth Handlers
  const handleLoginSuccess = (userData, token) => {
    setUser(userData);
    setRole(userData.role);
    localStorage.setItem("airbnb_user", JSON.stringify(userData));
    localStorage.setItem("airbnb_token", token);

    // Redirect to appropriate workspace
    if (userData.role === "host") {
      setCurrentView("host-dashboard");
    } else {
      setCurrentView("home");
    }
  };

  const handleLogout = () => {
    setUser(null);
    setRole("customer");
    localStorage.removeItem("airbnb_user");
    localStorage.removeItem("airbnb_token");
    setCurrentView("home");
  };

  const toggleWishlist = (listingId) => {
    setWishlist((prev) =>
      prev.includes(listingId)
        ? prev.filter((id) => id !== listingId)
        : [...prev, listingId]
    );
  };

  // Availability Check
  const checkAvailability = (listingId, checkInStr, checkOutStr) => {
    const reqStart = new Date(checkInStr);
    const reqEnd = new Date(checkOutStr);

    if (reqStart >= reqEnd) {
      return { available: false, error: "Ngày trả phòng phải sau ngày nhận phòng!" };
    }

    // Check confirmed bookings
    const conflictBooking = bookings.find((b) => {
      if (b.listing_id !== listingId || b.status !== "Confirmed") return false;
      const bStart = new Date(b.check_in);
      const bEnd = new Date(b.check_out);
      return reqStart < bEnd && reqEnd > bStart;
    });

    if (conflictBooking) {
      return {
        available: false,
        error: `Phòng đã có khách đặt từ ${conflictBooking.check_in} đến ${conflictBooking.check_out}!`,
      };
    }

    // Check host blocks
    const conflictBlock = availabilityBlocks.find((blk) => {
      if (blk.listing_id !== listingId) return false;
      const blkStart = new Date(blk.start_date);
      const blkEnd = new Date(blk.end_date);
      return reqStart < blkEnd && reqEnd > blkStart;
    });

    if (conflictBlock) {
      return {
        available: false,
        error: `Phòng bị chủ nhà tạm khóa từ ${conflictBlock.start_date} đến ${conflictBlock.end_date} (${conflictBlock.reason || "Bảo trì"}).`,
      };
    }

    return { available: true };
  };

  // Create Booking
  const createBooking = async ({ listing, checkIn, checkOut, guests, paymentMethod }) => {
    const avail = checkAvailability(listing.id, checkIn, checkOut);
    if (!avail.available) {
      return { success: false, error: avail.error };
    }

    try {
      const res = await api.createBooking({
        listing_id: listing.id,
        customer_id: user ? user.id : 2,
        check_in: checkIn,
        check_out: checkOut,
        guests,
        payment_method: paymentMethod,
      });

      const newBooking = res.booking;
      setBookings((prev) => [newBooking, ...prev]);
      setLastCreatedBooking(newBooking);
      return { success: true, booking: newBooking };
    } catch (err) {
      // Fallback local creation if offline
      const start = new Date(checkIn);
      const end = new Date(checkOut);
      const nights = Math.max(1, Math.round((end - start) / (1000 * 60 * 60 * 24)));
      const unitPrice = listing.base_price;
      const subtotal = nights * unitPrice;
      const serviceFee = Math.round(subtotal * 0.08);
      const tax = Math.round(subtotal * 0.08);
      const total = subtotal + serviceFee + tax;
      const bookingCode = `BK-2026-${Math.floor(100000 + Math.random() * 900000)}`;

      const newBooking = {
        id: Date.now(),
        booking_code: bookingCode,
        listing_id: listing.id,
        customer_id: user ? user.id : 2,
        check_in: checkIn,
        check_out: checkOut,
        nights,
        guests,
        unit_price: unitPrice,
        subtotal,
        service_fee: serviceFee,
        tax,
        total,
        currency: "VND",
        payment_method: paymentMethod,
        status: "Confirmed",
        created_at: new Date().toISOString(),
        listing_snapshot: {
          title: listing.title,
          city: listing.city,
          address: listing.address,
          cover_image: listing.cover_image,
          host_name: listing.host?.name || "Lê Minh Thảo",
        },
      };

      setBookings((prev) => [newBooking, ...prev]);
      setLastCreatedBooking(newBooking);
      return { success: true, booking: newBooking };
    }
  };

  // Cancel Booking
  const cancelBooking = async (bookingId, reason) => {
    try {
      await api.cancelBooking(bookingId, reason);
    } catch (e) {}

    setBookings((prev) =>
      prev.map((b) =>
        b.id === bookingId
          ? {
              ...b,
              status: "Cancelled",
              cancellation_reason: reason,
            }
          : b
      )
    );
  };

  // Add Review
  const addReview = async ({ listingId, bookingId, rating, comment }) => {
    const authorName = user ? user.full_name : "Khách lưu trú";
    const authorAvatar = user ? user.avatar_url : "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80";

    try {
      await api.createReview({
        listing_id: listingId,
        booking_id: bookingId,
        customer_id: user ? user.id : 2,
        author: authorName,
        avatar: authorAvatar,
        rating: Number(rating),
        comment,
      });
    } catch (e) {}

    const newRev = {
      id: Date.now(),
      listing_id: listingId,
      booking_id: bookingId,
      author: authorName,
      avatar: authorAvatar,
      rating: Number(rating),
      comment,
    };

    setReviews((prev) => [newRev, ...prev]);
    setBookings((prev) =>
      prev.map((b) => (b.id === bookingId ? { ...b, reviewed: true } : b))
    );
  };

  // Host Add Listing
  const addListing = async (listingData) => {
    try {
      const res = await api.createListing({
        host_id: user ? user.id : 1,
        ...listingData,
      });
      setListings((prev) => [res.data, ...prev]);
      return res.data;
    } catch (e) {
      const newListing = {
        id: Date.now(),
        host_id: user ? user.id : 1,
        rating: 5.0,
        reviews_count: 0,
        status: "Published",
        is_featured: false,
        host: {
          name: user ? user.full_name : "Chủ nhà",
          avatar: user ? user.avatar_url : "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=300&q=80",
          isSuperhost: true,
        },
        ...listingData,
      };
      setListings((prev) => [newListing, ...prev]);
      return newListing;
    }
  };

  // Toggle Listing Status
  const toggleListingStatus = async (listingId) => {
    try {
      await api.toggleListingStatus(listingId);
    } catch (e) {}

    setListings((prev) =>
      prev.map((l) =>
        l.id === listingId
          ? { ...l, status: l.status === "Published" ? "Hidden" : "Published" }
          : l
      )
    );
  };

  // Host Add Block Date
  const addAvailabilityBlock = async ({ listingId, startDate, endDate, reason }) => {
    const reqStart = new Date(startDate);
    const reqEnd = new Date(endDate);

    const conflict = bookings.find((b) => {
      if (b.listing_id !== listingId || b.status !== "Confirmed") return false;
      const bStart = new Date(b.check_in);
      const bEnd = new Date(b.check_out);
      return reqStart < bEnd && reqEnd > bStart;
    });

    if (conflict) {
      return {
        success: false,
        error: `Không thể chặn ngày vì đã có đơn ${conflict.booking_code} của khách (${conflict.check_in} -> ${conflict.check_out})!`,
      };
    }

    try {
      const res = await api.addBlock({
        listing_id: listingId,
        start_date: startDate,
        end_date: endDate,
        reason,
      });
      setAvailabilityBlocks((prev) => [...prev, res.data]);
      return { success: true, block: res.data };
    } catch (e) {
      const newBlock = {
        id: Date.now(),
        listing_id: listingId,
        start_date: startDate,
        end_date: endDate,
        reason: reason || "Chủ nhà tạm đóng",
      };
      setAvailabilityBlocks((prev) => [...prev, newBlock]);
      return { success: true, block: newBlock };
    }
  };

  // Host Remove Block Date
  const removeAvailabilityBlock = async (blockId) => {
    try {
      await api.removeBlock(blockId);
    } catch (e) {}
    setAvailabilityBlocks((prev) => prev.filter((b) => b.id !== blockId));
  };

  // Chat
  const sendMessage = (conversationId, text) => {
    if (!text.trim()) return;
    const nowTime = new Date().toLocaleTimeString("vi-VN", {
      hour: "2-digit",
      minute: "2-digit",
    }) + `, ${new Date().toLocaleDateString("vi-VN")}`;

    const newMsg = {
      sender: role === "host" ? "host" : "me",
      text,
      time: nowTime,
    };

    setConversations((prev) =>
      prev.map((conv) =>
        conv.conversation_id === conversationId
          ? { ...conv, messages: [...conv.messages, newMsg] }
          : conv
      )
    );
  };

  const startConversationWithHost = (listing) => {
    let conv = conversations.find((c) => c.listing_id === listing.id);
    if (!conv) {
      conv = {
        id: Date.now(),
        conversation_id: `conv-${listing.id}`,
        listing_id: listing.id,
        listing_title: listing.title,
        listing_image: listing.cover_image,
        host: {
          name: listing.host?.name || "Lê Minh Thảo",
          avatar: listing.host?.avatar || "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=300&q=80",
        },
        messages: [
          {
            sender: "host",
            text: `Xin chào! Tôi là chủ nhà của ${listing.title}. Bạn có câu hỏi nào về chỗ ở cứ nhắn cho mình nhé!`,
            time: "Vừa xong",
          },
        ],
      };
      setConversations((prev) => [conv, ...prev]);
    }
    setCurrentView("messages");
  };

  return (
    <AppContext.Provider
      value={{
        user,
        role,
        currentView,
        setCurrentView,
        handleLoginSuccess,
        handleLogout,
        listings,
        bookings,
        wishlist,
        toggleWishlist,
        reviews,
        conversations,
        availabilityBlocks,
        selectedListingId,
        setSelectedListingId,
        pendingBookingData,
        setPendingBookingData,
        lastCreatedBooking,
        setLastCreatedBooking,
        activeSearch,
        setActiveSearch,
        searchParams,
        setSearchParams,
        checkAvailability,
        createBooking,
        cancelBooking,
        addReview,
        addListing,
        toggleListingStatus,
        addAvailabilityBlock,
        removeAvailabilityBlock,
        sendMessage,
        startConversationWithHost,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export const useApp = () => useContext(AppContext);
