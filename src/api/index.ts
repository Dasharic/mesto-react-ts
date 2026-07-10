// Types
export type Role = "guest" | "user" | "admin";

export type UserProfile = {
  name: string;
  email: string;
  avatar: string;
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

const MOCK_TOURS: Tour[] = [
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

// Helper to simulate network delay
const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export const api = {
  // --- Tours API ---
  async fetchTours(): Promise<Tour[]> {
    await delay(500);
    const saved = localStorage.getItem("tours");
    if (saved) return JSON.parse(saved);
    localStorage.setItem("tours", JSON.stringify(MOCK_TOURS));
    return MOCK_TOURS;
  },

  async addTour(tour: Omit<Tour, "id">): Promise<Tour> {
    await delay(300);
    const newTour = { ...tour, id: Date.now() };
    const saved = localStorage.getItem("tours");
    const tours: Tour[] = saved ? JSON.parse(saved) : MOCK_TOURS;
    tours.unshift(newTour);
    localStorage.setItem("tours", JSON.stringify(tours));
    return newTour;
  },

  // --- Auth API ---
  async login(email: string, password: string): Promise<{ token: string; profile: UserProfile; role: Role }> {
    await delay(600);
    const saved = localStorage.getItem("auth_users");
    const users = saved ? JSON.parse(saved) : [];
    
    // Check default admin
    if (email === "admin@mesto.com" && password === "admin") {
      return {
        token: "admin_token_123",
        role: "admin",
        profile: { name: "Администратор", email, avatar: "https://images.unsplash.com/photo-1544723795-3cj3h9f28d82" }
      };
    }

    const user = users.find((u: any) => u.email === email && u.password === password);
    if (!user) throw new Error("Неверный email или пароль");

    return { token: `token_${user.email}`, role: user.role, profile: user.profile };
  },

  async register(name: string, email: string, password: string): Promise<{ token: string; profile: UserProfile; role: Role }> {
    await delay(600);
    const saved = localStorage.getItem("auth_users");
    const users = saved ? JSON.parse(saved) : [];
    
    if (users.find((u: any) => u.email === email)) {
      throw new Error("Пользователь с таким email уже существует");
    }

    const newUser = {
      email,
      password,
      role: "user",
      profile: { name, email, avatar: "https://i.pravatar.cc/150?u=" + email },
    };
    users.push(newUser);
    localStorage.setItem("auth_users", JSON.stringify(users));

    return { token: `token_${email}`, role: "user", profile: newUser.profile };
  },

  async getMe(token: string): Promise<{ profile: UserProfile; role: Role }> {
    await delay(300);
    if (token === "admin_token_123") {
      return { role: "admin", profile: { name: "Администратор", email: "admin@mesto.com", avatar: "https://images.unsplash.com/photo-1544723795-3cj3h9f28d82" } };
    }
    
    const email = token.replace("token_", "");
    const saved = localStorage.getItem("auth_users");
    const users = saved ? JSON.parse(saved) : [];
    const user = users.find((u: any) => u.email === email);
    
    if (!user) throw new Error("Неверный токен");
    return { role: user.role, profile: user.profile };
  }
};
