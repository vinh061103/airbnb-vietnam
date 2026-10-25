const API_BASE = window.location.origin.includes(':5173')
  ? "http://127.0.0.1:5000/api/v1"
  : "/api/v1";

export async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem("airbnb_token");
  const headers = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || "Có lỗi xảy ra khi kết nối máy chủ");
  }

  return data;
}

export const api = {
  // Auth
  login: (email, password) =>
    apiRequest("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  register: (userData) =>
    apiRequest("/auth/register", {
      method: "POST",
      body: JSON.stringify(userData),
    }),

  getMe: () => apiRequest("/auth/me"),

  // Listings
  getListings: () => apiRequest("/listings"),
  createListing: (data) =>
    apiRequest("/listings", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  toggleListingStatus: (id) =>
    apiRequest(`/listings/${id}/status`, { method: "PATCH" }),

  // Bookings
  getBookings: (params = {}) => {
    const q = new URLSearchParams(params).toString();
    return apiRequest(`/bookings${q ? `?${q}` : ""}`);
  },
  createBooking: (data) =>
    apiRequest("/bookings", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  cancelBooking: (id, reason) =>
    apiRequest(`/bookings/${id}/cancel`, {
      method: "POST",
      body: JSON.stringify({ reason }),
    }),

  // Reviews
  getReviews: (listingId) =>
    apiRequest(`/reviews${listingId ? `?listing_id=${listingId}` : ""}`),
  createReview: (data) =>
    apiRequest("/reviews", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  // Availability blocks
  getBlocks: (listingId) =>
    apiRequest(`/availability/blocks${listingId ? `?listing_id=${listingId}` : ""}`),
  addBlock: (data) =>
    apiRequest("/availability/block", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  removeBlock: (id) =>
    apiRequest(`/availability/block/${id}`, { method: "DELETE" }),
};
