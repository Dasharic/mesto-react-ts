// Types
export type Role = "guest" | "user" | "admin";

export type UserProfile = {
  name: string;
  email: string;
  avatar?: string;
};

export type Tour = {
  id: number;
  title: string;
  image: string;
  description: string;
  price: number;
};

export type Order = {
  id: number;
  date: string;
  items: Tour[];
  total: number;
};

const BASE_URL = "http://localhost:8000/api";

function getToken() {
  const authStorage = localStorage.getItem("auth-storage");
  if (authStorage) {
    try {
      const parsed = JSON.parse(authStorage);
      return parsed.state?.token;
    } catch(e) {}
  }
  return null;
}

async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const headers = new Headers(options.headers || {});
  const token = getToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);
  headers.set("Content-Type", "application/json");
  
  const res = await fetch(`${BASE_URL}${url}`, { ...options, headers });
  if (!res.ok) {
    let msg = "API Error";
    try {
      const err = await res.json();
      msg = err.detail || msg;
    } catch(e) {}
    throw new Error(msg);
  }
  return res.json();
}

export const api = {
  // --- Catalog ---
  async fetchTours(): Promise<Tour[]> {
    return fetchWithAuth("/tours/");
  },
  async addTour(tour: Omit<Tour, "id">): Promise<Tour> {
    return fetchWithAuth("/tours/", { method: "POST", body: JSON.stringify(tour) });
  },
  async deleteTour(id: number): Promise<void> {
    await fetchWithAuth(`/tours/${id}`, { method: "DELETE" });
  },

  // --- Identity ---
  async login(email: string, password: string): Promise<{ token: string; profile: UserProfile; role: Role }> {
    return fetchWithAuth("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) });
  },
  async register(name: string, email: string, password: string): Promise<{ token: string; profile: UserProfile; role: Role }> {
    return fetchWithAuth("/auth/register", { method: "POST", body: JSON.stringify({ name, email, password }) });
  },
  async getMe(token: string): Promise<{ profile: UserProfile; role: Role }> {
    const res = await fetch(`${BASE_URL}/auth/me?token=${token}`);
    if (!res.ok) throw new Error("Invalid token");
    return res.json();
  },
  async updateProfile(token: string, data: Partial<UserProfile>): Promise<void> {
    await fetchWithAuth(`/auth/me?token=${token}`, { method: "PATCH", body: JSON.stringify(data) });
  },

  // --- Booking ---
  async getCart(): Promise<Tour[]> { return fetchWithAuth("/booking/cart"); },
  async addToCart(tourId: number): Promise<void> { await fetchWithAuth(`/booking/cart/${tourId}`, { method: "POST" }); },
  async removeFromCart(tourId: number): Promise<void> { await fetchWithAuth(`/booking/cart/${tourId}`, { method: "DELETE" }); },
  
  async getFavorites(): Promise<number[]> { return fetchWithAuth("/booking/favorites"); },
  async toggleFavorite(tourId: number): Promise<{ favorites: number[] }> { return fetchWithAuth(`/booking/favorites/${tourId}`, { method: "POST" }); },

  async getOrders(): Promise<Order[]> { return fetchWithAuth("/booking/orders"); },
  async checkout(): Promise<Order> { return fetchWithAuth("/booking/checkout", { method: "POST" }); }
};
