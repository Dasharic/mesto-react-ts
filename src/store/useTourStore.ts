import { create } from "zustand";
import { api } from "../api";
import type { Tour, Order } from "../api";
import { useAuthStore } from "./useAuthStore";

interface TourState {
  tours: Tour[];
  cart: Tour[];
  favorites: number[];
  orders: Order[];
  isLoading: boolean;
  
  // Actions
  fetchTours: () => Promise<void>;
  addTour: (tour: Omit<Tour, "id">) => Promise<void>;
  deleteTour: (id: number) => Promise<void>;
  
  // User specific actions (we keep them in localStorage tied to token for simplicity)
  loadUserData: () => void;
  addToCart: (tour: Tour) => void;
  removeFromCart: (tourId: number) => void;
  toggleFavorite: (tourId: number) => void;
  checkout: () => void;
}

export const useTourStore = create<TourState>((set) => ({
  tours: [],
  cart: [],
  favorites: [],
  orders: [],
  isLoading: false,

  fetchTours: async () => {
    set({ isLoading: true });
    const tours = await api.fetchTours();
    set({ tours, isLoading: false });
  },

  addTour: async (tourData) => {
    const newTour = await api.addTour(tourData);
    set((state) => ({ tours: [newTour, ...state.tours] }));
  },

  deleteTour: async (id) => {
    await api.deleteTour(id);
    set((state) => ({ tours: state.tours.filter((t) => t.id !== id) }));
  },

  loadUserData: () => {
    const token = useAuthStore.getState().token;
    if (!token) {
      set({ cart: [], favorites: [], orders: [] });
      return;
    }
    const suffix = `_${token}`;
    const cart = JSON.parse(localStorage.getItem(`cart${suffix}`) || "[]");
    const favs = JSON.parse(localStorage.getItem(`favorites${suffix}`) || "[]");
    const orders = JSON.parse(localStorage.getItem(`orders${suffix}`) || "[]");
    set({ cart, favorites: favs, orders });
  },

  addToCart: (tour) => {
    set((state) => {
      if (state.cart.find(c => c.id === tour.id)) return state;
      const newCart = [...state.cart, tour];
      const token = useAuthStore.getState().token;
      if (token) localStorage.setItem(`cart_${token}`, JSON.stringify(newCart));
      return { cart: newCart };
    });
  },

  removeFromCart: (tourId) => {
    set((state) => {
      const newCart = state.cart.filter(c => c.id !== tourId);
      const token = useAuthStore.getState().token;
      if (token) localStorage.setItem(`cart_${token}`, JSON.stringify(newCart));
      return { cart: newCart };
    });
  },

  toggleFavorite: (tourId) => {
    set((state) => {
      const newFavs = state.favorites.includes(tourId)
        ? state.favorites.filter(id => id !== tourId)
        : [...state.favorites, tourId];
      const token = useAuthStore.getState().token;
      if (token) localStorage.setItem(`favorites_${token}`, JSON.stringify(newFavs));
      return { favorites: newFavs };
    });
  },

  checkout: () => {
    set((state) => {
      if (state.cart.length === 0) return state;
      const total = state.cart.reduce((sum, item) => sum + item.price, 0);
      const newOrder: Order = {
        id: Date.now(),
        date: new Date().toLocaleDateString(),
        items: [...state.cart],
        total,
      };
      const newOrders = [newOrder, ...state.orders];
      const token = useAuthStore.getState().token;
      if (token) {
        localStorage.setItem(`orders_${token}`, JSON.stringify(newOrders));
        localStorage.setItem(`cart_${token}`, "[]");
      }
      return { orders: newOrders, cart: [] };
    });
  },
}));
