import { createContext, useContext, useState, useEffect } from "react";
import type { ReactNode } from "react";
import { useAuth } from "./AuthContext";

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

const initialTours: Tour[] = [
  {
    id: 1,
    title: "Париж, Франция",
    image: "https://images.unsplash.com/photo-1502602898657-3e91760cbb34",
    description: "Незабываемые выходные в столице романтики. Включает экскурсию на Эйфелеву башню.",
    price: 1500,
  },
  {
    id: 2,
    title: "Токио, Япония",
    image: "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf",
    description: "Погружение в культуру Азии. Неоновые огни, храмы и суши мирового класса.",
    price: 2500,
  },
  {
    id: 3,
    title: "Нью-Йорк, США",
    image: "https://images.unsplash.com/photo-1522083165195-3424ed129620",
    description: "Город, который никогда не спит. Центральный парк, Таймс-сквер и Бродвей.",
    price: 2000,
  },
];

interface StoreContextType {
  tours: Tour[];
  cart: Tour[];
  favorites: number[];
  orders: Order[];
  addTour: (tour: Omit<Tour, "id">) => void;
  addToCart: (tour: Tour) => void;
  removeFromCart: (tourId: number) => void;
  toggleFavorite: (tourId: number) => void;
  checkout: () => void;
}

const StoreContext = createContext<StoreContextType | undefined>(undefined);

export function StoreProvider({ children }: { children: ReactNode }) {
  const { currentUser } = useAuth();
  const userKey = currentUser ? `_${currentUser.email}` : "";

  const [tours, setTours] = useState<Tour[]>(() => {
    const saved = localStorage.getItem("tours");
    return saved ? JSON.parse(saved) : initialTours;
  });

  const [cart, setCart] = useState<Tour[]>([]);
  const [favorites, setFavorites] = useState<number[]>([]);
  const [orders, setOrders] = useState<Order[]>([]);

  // Load user specific data when user changes
  useEffect(() => {
    if (currentUser) {
      const savedCart = localStorage.getItem(`cart${userKey}`);
      const savedFavs = localStorage.getItem(`favorites${userKey}`);
      const savedOrders = localStorage.getItem(`orders${userKey}`);
      setCart(savedCart ? JSON.parse(savedCart) : []);
      setFavorites(savedFavs ? JSON.parse(savedFavs) : []);
      setOrders(savedOrders ? JSON.parse(savedOrders) : []);
    } else {
      setCart([]);
      setFavorites([]);
      setOrders([]);
    }
  }, [currentUser, userKey]);

  useEffect(() => {
    localStorage.setItem("tours", JSON.stringify(tours));
  }, [tours]);

  // Save user specific data when it changes (only if logged in)
  useEffect(() => {
    if (currentUser) {
      localStorage.setItem(`cart${userKey}`, JSON.stringify(cart));
    }
  }, [cart, currentUser, userKey]);

  useEffect(() => {
    if (currentUser) {
      localStorage.setItem(`favorites${userKey}`, JSON.stringify(favorites));
    }
  }, [favorites, currentUser, userKey]);

  useEffect(() => {
    if (currentUser) {
      localStorage.setItem(`orders${userKey}`, JSON.stringify(orders));
    }
  }, [orders, currentUser, userKey]);

  const addTour = (tourData: Omit<Tour, "id">) => {
    const newTour = { ...tourData, id: Date.now() };
    setTours((prev) => [newTour, ...prev]);
  };

  const addToCart = (tour: Tour) => {
    if (!cart.find((item) => item.id === tour.id)) {
      setCart((prev) => [...prev, tour]);
    }
  };

  const removeFromCart = (tourId: number) => {
    setCart((prev) => prev.filter((item) => item.id !== tourId));
  };

  const toggleFavorite = (tourId: number) => {
    setFavorites((prev) =>
      prev.includes(tourId)
        ? prev.filter((id) => id !== tourId)
        : [...prev, tourId]
    );
  };

  const checkout = () => {
    if (cart.length === 0) return;
    
    const total = cart.reduce((sum, item) => sum + item.price, 0);
    const newOrder: Order = {
      id: Date.now(),
      date: new Date().toLocaleDateString(),
      items: [...cart],
      total,
    };
    
    setOrders((prev) => [newOrder, ...prev]);
    setCart([]); 
  };

  return (
    <StoreContext.Provider
      value={{
        tours,
        cart,
        favorites,
        orders,
        addTour,
        addToCart,
        removeFromCart,
        toggleFavorite,
        checkout,
      }}
    >
      {children}
    </StoreContext.Provider>
  );
}

export function useStore() {
  const context = useContext(StoreContext);
  if (!context) {
    throw new Error("useStore must be used within a StoreProvider");
  }
  return context;
}
