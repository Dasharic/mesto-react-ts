import { createContext, useContext, useState, useEffect } from "react";
import type { ReactNode } from "react";

export type Role = "guest" | "user" | "admin";

export type UserProfile = {
  name: string;
  email: string;
  avatar: string;
};

export type User = {
  email: string;
  password: string; // Plaintext for learning
  role: Role;
  profile: UserProfile;
};

interface AuthContextType {
  role: Role;
  profile: UserProfile;
  currentUser: User | null;
  login: (email: string, password: string) => boolean;
  register: (name: string, email: string, password: string) => boolean;
  logout: () => void;
  updateProfile: (data: Partial<UserProfile>) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const defaultAdmin: User = {
  email: "admin@mesto.com",
  password: "admin",
  role: "admin",
  profile: {
    name: "Администратор",
    email: "admin@mesto.com",
    avatar: "https://images.unsplash.com/photo-1544723795-3cj3h9f28d82"
  }
};

export function AuthProvider({ children }: { children: ReactNode }) {
  const [users, setUsers] = useState<User[]>(() => {
    const saved = localStorage.getItem("auth_users");
    return saved ? JSON.parse(saved) : [defaultAdmin];
  });

  const [currentUser, setCurrentUser] = useState<User | null>(() => {
    const saved = localStorage.getItem("auth_current_user");
    return saved ? JSON.parse(saved) : null;
  });

  useEffect(() => {
    localStorage.setItem("auth_users", JSON.stringify(users));
  }, [users]);

  useEffect(() => {
    if (currentUser) {
      localStorage.setItem("auth_current_user", JSON.stringify(currentUser));
      // Update user in users array
      setUsers((prev) =>
        prev.map((u) => (u.email === currentUser.email ? currentUser : u))
      );
    } else {
      localStorage.removeItem("auth_current_user");
    }
  }, [currentUser]);

  const login = (email: string, password: string) => {
    const user = users.find((u) => u.email === email && u.password === password);
    if (user) {
      setCurrentUser(user);
      return true;
    }
    return false;
  };

  const register = (name: string, email: string, password: string) => {
    if (users.find((u) => u.email === email)) return false; // Email exists

    const newUser: User = {
      email,
      password,
      role: "user",
      profile: {
        name,
        email,
        avatar: "https://i.pravatar.cc/150?u=" + email,
      },
    };

    setUsers((prev) => [...prev, newUser]);
    setCurrentUser(newUser);
    return true;
  };

  const logout = () => setCurrentUser(null);

  const updateProfile = (data: Partial<UserProfile>) => {
    if (currentUser) {
      setCurrentUser({
        ...currentUser,
        profile: { ...currentUser.profile, ...data },
      });
    }
  };

  const role = currentUser?.role || "guest";
  const profile = currentUser?.profile || { name: "Гость", email: "", avatar: "" };

  return (
    <AuthContext.Provider
      value={{ role, profile, currentUser, login, register, logout, updateProfile }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
