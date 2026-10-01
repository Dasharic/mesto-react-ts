import { create } from "zustand";
import { api } from "../api";
import type { Tour, Order } from "../api";

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
  
  // User specific actions
  loadUserData: () => Promise<void>;
  addToCart: (tour: Tour) => Promise<void>;
  removeFromCart: (tourId: number) => Promise<void>;
  toggleFavorite: (tourId: number) => Promise<void>;
  checkout: () => Promise<void>;
}

export const useTourStore = create<TourState>((set) => ({
  tours: [],
  cart: [],
  favorites: [],
  orders: [],
  isLoading: false,

  fetchTours: async () => {
    set({ isLoading: true });
    try {
      const tours = await api.fetchTours();
      set({ tours });
    } catch(e) { console.error(e) }
    set({ isLoading: false });
  },

  addTour: async (tourData) => {
    const newTour = await api.addTour(tourData);
    set((state) => ({ tours: [newTour, ...state.tours] }));
  },

  deleteTour: async (id) => {
    await api.deleteTour(id);
    set((state) => ({ tours: state.tours.filter((t) => t.id !== id) }));
  },

  loadUserData: async () => {
    try {
      const [cart, favorites, orders] = await Promise.all([
        api.getCart(),
        api.getFavorites(),
        api.getOrders()
      ]);
      set({ cart, favorites, orders });
    } catch (e) {
      set({ cart: [], favorites: [], orders: [] });
    }
  },

  addToCart: async (tour) => {
    await api.addToCart(tour.id);
    set((state) => ({ cart: [...state.cart, tour] }));
  },

  removeFromCart: async (tourId) => {
    await api.removeFromCart(tourId);
    set((state) => ({ cart: state.cart.filter(c => c.id !== tourId) }));
  },

  toggleFavorite: async (tourId) => {
    const { favorites } = await api.toggleFavorite(tourId);
    set({ favorites });
  },

  checkout: async () => {
    const newOrder = await api.checkout();
    set((state) => ({ orders: [newOrder, ...state.orders], cart: [] }));
  },
}));
