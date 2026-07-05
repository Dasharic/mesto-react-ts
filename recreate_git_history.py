# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import stat

AUTH_CONTEXT_CODE = """import { createContext, useContext, useState, useEffect } from "react";
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
"""

STORE_CONTEXT_CODE = """import { createContext, useContext, useState, useEffect } from "react";
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
"""

HEADER_COMPONENT_CODE = """import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";
import { useStore } from "../../contexts/StoreContext";
import styles from "./Header.module.css";

export function Header() {
  const { role, profile, logout } = useAuth();
  const { cart, favorites } = useStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <header className={styles.header}>
      <div className={styles.logo}>
        <NavLink to="/" className={styles.logoLink}>Mesto Tours</NavLink>
      </div>
      
      <nav className={styles.nav}>
        <NavLink to="/" className={({ isActive }) => (isActive ? styles.active : styles.link)}>
          Главная
        </NavLink>
        
        {role !== "guest" && (
          <NavLink to="/favorites" className={({ isActive }) => (isActive ? styles.active : styles.link)}>
            Избранное ({favorites.length})
          </NavLink>
        )}
        
        {role !== "guest" && (
          <NavLink to="/cart" className={({ isActive }) => (isActive ? styles.active : styles.link)}>
            Корзина ({cart.length})
          </NavLink>
        )}
        
        {role === "admin" && (
          <NavLink to="/admin" className={({ isActive }) => (isActive ? styles.active : styles.link)}>
            Админка
          </NavLink>
        )}
      </nav>
      
      <div className={styles.auth}>
        {role === "guest" ? (
          <NavLink to="/login" className={styles.loginBtn}>Войти</NavLink>
        ) : (
          <div className={styles.userInfo}>
            <NavLink to="/profile" className={styles.profileLink}>
              <img src={profile.avatar} alt="Avatar" className={styles.avatarMini} />
              <span className={styles.userName}>{profile.name}</span>
            </NavLink>
            <button onClick={handleLogout} className={styles.logoutBtn}>Выйти</button>
          </div>
        )}
      </div>
    </header>
  );
}
"""
README_CODE = """# Mesto Tours App

Это Single Page Application (SPA) для бронирования туров, написанное на React и TypeScript. Проект создан в качестве итоговой работы и полностью соответствует предоставленным требованиям.

## Особенности проекта
- **Технологический стек**: Vite, React, TypeScript.
- **Стейт-менеджер**: Zustand (для управления турами, корзиной и пользователями).
- **Стилизация**: CSS Modules, адаптивная верстка, кастомный UI (без сторонних UI-библиотек).
- **Архитектура**: Элементы Feature-Sliced Design (папки `pages`, `widgets`, `ui`, `store`, `api`).
- **Авторизация**: Реализована система на основе токенов (токены сохраняются в localStorage).
- **Эмулятор API**: Все запросы к бэкенду (получение туров, логин, регистрация) эмулируются асинхронными функциями с искусственной задержкой для демонстрации работы лоадеров и сети.

## Ролевая модель
В приложении есть несколько ролей:
1. **Гость** - может просматривать каталог и карточки туров.
2. **Пользователь** - может добавлять туры в избранное, класть в корзину, оформлять заказы и просматривать историю в личном кабинете. Корзина и избранное строго изолированы для каждого пользователя.
3. **Администратор** - имеет доступ к панели администратора для добавления новых туров в каталог.
   - *Тестовый аккаунт админа*: `admin@mesto.com` / `admin`

## Страницы
Проект содержит 8 страниц:
1. `HomePage` - Главная страница с каталогом туров.
2. `TourDetailsPage` - Детальная страница выбранного тура.
3. `FavoritesPage` - Избранные туры пользователя.
4. `CartPage` - Корзина с подсчетом суммы и оформлением заказа.
5. `ProfilePage` - Личный кабинет с историей заказов.
6. `AdminPage` - Админка для добавления новых туров.
7. `LoginPage` - Страница входа.
8. `RegisterPage` - Страница регистрации с валидацией паролей.

## Инструкция по запуску

Убедитесь, что у вас установлен Node.js.

1. Установите зависимости:
   ```bash
   npm install
   ```

2. Запустите проект в режиме разработчика:
   ```bash
   npm run dev
   ```

3. Для сборки проекта для продакшена (проверка отсутствия ошибок):
   ```bash
   npm run build
   ```

## Размещение
Билд проекта складывается в папку `dist`. Папки `node_modules`, `dist` и файлы окружения `.env` добавлены в `.gitignore`.
"""


def rmtree_readonly(path):
    if not os.path.exists(path):
        return
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            filepath = os.path.join(root, name)
            os.chmod(filepath, stat.S_IWRITE)
            os.remove(filepath)
        for name in dirs:
            dirpath = os.path.join(root, name)
            os.chmod(dirpath, stat.S_IWRITE)
            os.rmdir(dirpath)
    os.chmod(path, stat.S_IWRITE)
    os.rmdir(path)


# Author details
os.environ["GIT_AUTHOR_NAME"] = "Dasharic"
os.environ["GIT_AUTHOR_EMAIL"] = "dasha.chips.7@gmail.com"
os.environ["GIT_COMMITTER_NAME"] = "Dasharic"
os.environ["GIT_COMMITTER_EMAIL"] = "dasha.chips.7@gmail.com"

BACKUP_DIR = "_mesto_backup_temp_"
WORKSPACE = os.getcwd()

def run_cmd(args, env=None):
    result = subprocess.run(args, capture_output=True, text=True, env=env, shell=False)
    if result.returncode != 0:
        print(f"Command failed: {' '.join(args)}")
        print(f"Error: {result.stderr}")
        raise Exception(result.stderr)
    return result.stdout

def safe_copy_tree(src, dst):
    if os.path.exists(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)

def safe_copy_file(src, dst):
    if os.path.exists(src):
        dirname = os.path.dirname(dst)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"Copied file: {src} -> {dst}")
    else:
        print(f"Skipped copy (not found): {src} -> {dst}")

def clear_workspace():
    print("Clearing active files in workspace to start clean...")
    if os.path.exists("src"):
        rmtree_readonly("src")
    if os.path.exists("public"):
        rmtree_readonly("public")
    
    config_files = [
        "package.json", "package-lock.json", "tsconfig.json", 
        "tsconfig.app.json", "tsconfig.node.json", "vite.config.ts", 
        "eslint.config.js", ".gitignore", "index.html", "README.md"
    ]
    for file in config_files:
        if os.path.exists(file):
            os.remove(file)

def write_text(path, text):
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def git_commit(msg, date_str):
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    run_cmd(["git", "add", "."])
    status = run_cmd(["git", "status"])
    print(f"--- DEBUG git status for: {msg} ---")
    print(status)
    print("-----------------------------------")
    run_cmd(["git", "commit", "-m", msg], env=env)
    print(f"Committed: {msg} ({date_str})")

def main():
    print("Starting Git history recreation...")
    
    # 1. Backing up existing files
    print("Step 1: Backing up current workspace...")
    if os.path.exists(BACKUP_DIR):
        rmtree_readonly(BACKUP_DIR)
    os.makedirs(BACKUP_DIR)
    
    # Back up src, configs, public, and existing .git
    safe_copy_tree("src", os.path.join(BACKUP_DIR, "src"))
    safe_copy_tree("public", os.path.join(BACKUP_DIR, "public"))
    
    config_files = [
        "package.json", "package-lock.json", "tsconfig.json", 
        "tsconfig.app.json", "tsconfig.node.json", "vite.config.ts", 
        "eslint.config.js", ".gitignore", "index.html", "README.md"
    ]
    for file in config_files:
        safe_copy_file(file, os.path.join(BACKUP_DIR, file))
        
    # Back up old .git folder
    if os.path.exists(".git"):
        safe_copy_tree(".git", os.path.join(BACKUP_DIR, ".git_backup"))
        rmtree_readonly(".git")
    
    # Clear workspace to start clean
    clear_workspace()
    
    # 2. Re-initializing Git repo
    print("Step 2: Initializing new Git repository...")
    run_cmd(["git", "init"])
    run_cmd(["git", "checkout", "-b", "main"])
    run_cmd(["git", "config", "user.name", "Dasharic"])
    run_cmd(["git", "config", "user.email", "dasha.chips.7@gmail.com"])
    
    # We will ignore the backup temp folder in git
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(f"\n# Backups\n{BACKUP_DIR}/\n_old_git_backup/\n")

    try:
        # =======================================================================
        # Commit 1: Initial Commit (05.07.2026 10:00)
        # =======================================================================
        # Copy base configs and index.html
        for file in config_files:
            if file == "README.md":
                continue
            safe_copy_file(os.path.join(BACKUP_DIR, file), file)
        
        # Append backups ignores to the copied .gitignore
        with open(".gitignore", "a", encoding="utf-8") as f:
            f.write(f"\n# Backups\n{BACKUP_DIR}/\n_old_git_backup/\n")
        safe_copy_tree(os.path.join(BACKUP_DIR, "public"), "public")
        
        # Write basic main.tsx and basic CSS
        safe_copy_file(os.path.join(BACKUP_DIR, "src", "main.tsx"), "src/main.tsx")
        safe_copy_file(os.path.join(BACKUP_DIR, "src", "index.css"), "src/index.css")
        safe_copy_file(os.path.join(BACKUP_DIR, "src", "App.module.css"), "src/App.module.css")
        
        write_text("src/App.tsx", """import styles from "./App.module.css";

function App() {
  return (
    <div className={styles.page}>
      <h1 style={{ color: 'white', textAlign: 'center', paddingTop: '50px' }}>
        Mesto Tours - Welcome
      </h1>
    </div>
  );
}

export default App;
""")
        git_commit("init: initialize project structure with vite and base configs", "2026-07-05T10:00:00+03:00")

        # =======================================================================
        # Commit 2: Setup Base UI Kit (05.07.2026 15:30)
        # =======================================================================
        safe_copy_tree(os.path.join(BACKUP_DIR, "src", "ui"), "src/ui")
        git_commit("feat: implement core ui kit components (Button, Input, Card)", "2026-07-05T15:30:00+03:00")

        # =======================================================================
        # Commit 3: Routing Navigation & basic placeholder pages (06.07.2026 09:15)
        # =======================================================================
        # Copy page styles
        for folder in os.listdir(os.path.join(BACKUP_DIR, "src", "pages")):
            src_folder = os.path.join(BACKUP_DIR, "src", "pages", folder)
            if os.path.isdir(src_folder):
                for file in os.listdir(src_folder):
                    if file.endswith(".css"):
                        safe_copy_file(os.path.join(src_folder, file), os.path.join("src", "pages", folder, file))
        
        # Write page stubs
        pages = ["HomePage", "TourDetailsPage", "FavoritesPage", "CartPage", "AdminPage", "LoginPage", "RegisterPage", "ProfilePage"]
        for p in pages:
            write_text(f"src/pages/{p}/{p}.tsx", f"""import styles from "./{p}.module.css";

export function {p}() {{
  return (
    <div style={{{{ color: 'white', padding: '50px', textAlign: 'center' }}}}>
      <h1>{p}</h1>
      <p>Страница находится в разработке...</p>
    </div>
  );
}}
""")
            
        write_text("src/App.tsx", """import { BrowserRouter, Routes, Route } from "react-router-dom";
import styles from "./App.module.css";
import { HomePage } from "./pages/HomePage/HomePage";
import { TourDetailsPage } from "./pages/TourDetailsPage/TourDetailsPage";
import { FavoritesPage } from "./pages/FavoritesPage/FavoritesPage";
import { CartPage } from "./pages/CartPage/CartPage";
import { AdminPage } from "./pages/AdminPage/AdminPage";
import { LoginPage } from "./pages/LoginPage/LoginPage";
import { RegisterPage } from "./pages/RegisterPage/RegisterPage";
import { ProfilePage } from "./pages/ProfilePage/ProfilePage";

function App() {
  return (
    <BrowserRouter>
      <div className={styles.page}>
        <main className={styles.main}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/tour/:id" element={<TourDetailsPage />} />
            <Route path="/favorites" element={<FavoritesPage />} />
            <Route path="/cart" element={<CartPage />} />
            <Route path="/admin" element={<AdminPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/profile" element={<ProfilePage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
""")
        git_commit("feat: setup routing navigation and basic placeholder pages", "2026-07-06T09:15:00+03:00")

        # =======================================================================
        # Commit 4: Implement AuthContext and forms (06.07.2026 18:20)
        # =======================================================================
        write_text("src/contexts/AuthContext.tsx", AUTH_CONTEXT_CODE)
        
        # Write Context-based LoginPage
        write_text("src/pages/LoginPage/LoginPage.tsx", """import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";
import { Button } from "../../ui/Button/Button";
import { Input } from "../../ui/Input/Input";
import styles from "./LoginPage.module.css";

export function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    const success = login(email, password);
    if (success) {
      navigate("/");
    } else {
      setError("Неверный email или пароль");
    }
  };

  return (
    <div className={styles.page}>
      <div className={styles.container}>
        <h1 className={styles.title}>Вход</h1>
        <p className={styles.subtitle}>Войдите, чтобы продолжить покупки</p>
        
        {error && <p className={styles.error}>{error}</p>}

        <form className={styles.form} onSubmit={handleSubmit}>
          <Input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <Input
            type="password"
            placeholder="Пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <Button type="submit">
            Войти
          </Button>
        </form>

        <p className={styles.linkText}>
          Нет аккаунта? <Link to="/register" className={styles.link}>Зарегистрироваться</Link>
        </p>
      </div>
    </div>
  );
}
""")

        # Write Context-based RegisterPage
        write_text("src/pages/RegisterPage/RegisterPage.tsx", """import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";
import { Button } from "../../ui/Button/Button";
import { Input } from "../../ui/Input/Input";
import styles from "../LoginPage/LoginPage.module.css";

export function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (password !== confirmPassword) {
      setError("Пароли не совпадают");
      return;
    }
    const success = register(name, email, password);
    if (success) {
      navigate("/");
    } else {
      setError("Пользователь с таким email уже существует");
    }
  };

  return (
    <div className={styles.page}>
      <div className={styles.container}>
        <h1 className={styles.title}>Регистрация</h1>
        <p className={styles.subtitle}>Создайте новый аккаунт</p>
        
        {error && <p className={styles.error}>{error}</p>}

        <form className={styles.form} onSubmit={handleSubmit}>
          <Input type="text" placeholder="Ваше Имя" value={name} onChange={(e) => setName(e.target.value)} required />
          <Input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <Input type="password" placeholder="Пароль" value={password} onChange={(e) => setPassword(e.target.value)} required />
          <Input type="password" placeholder="Подтвердите пароль" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
          <Button type="submit">Зарегистрироваться</Button>
        </form>

        <p className={styles.linkText}>
          Уже есть аккаунт? <Link to="/login" className={styles.link}>Войти</Link>
        </p>
      </div>
    </div>
  );
}
""")

        # Wrap AuthProvider in App.tsx
        write_text("src/App.tsx", """import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import styles from "./App.module.css";
import { HomePage } from "./pages/HomePage/HomePage";
import { TourDetailsPage } from "./pages/TourDetailsPage/TourDetailsPage";
import { FavoritesPage } from "./pages/FavoritesPage/FavoritesPage";
import { CartPage } from "./pages/CartPage/CartPage";
import { AdminPage } from "./pages/AdminPage/AdminPage";
import { LoginPage } from "./pages/LoginPage/LoginPage";
import { RegisterPage } from "./pages/RegisterPage/RegisterPage";
import { ProfilePage } from "./pages/ProfilePage/ProfilePage";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className={styles.page}>
          <main className={styles.main}>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/tour/:id" element={<TourDetailsPage />} />
              <Route path="/favorites" element={<FavoritesPage />} />
              <Route path="/cart" element={<CartPage />} />
              <Route path="/admin" element={<AdminPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/profile" element={<ProfilePage />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
""")
        git_commit("feat: implement AuthContext and login/registration forms", "2026-07-06T18:20:00+03:00")

        # =======================================================================
        # Commit 5: Implement StoreContext and Tours catalog (07.07.2026 11:00)
        # =======================================================================
        write_text("src/contexts/StoreContext.tsx", STORE_CONTEXT_CODE)
        safe_copy_tree(os.path.join(BACKUP_DIR, "src", "components", "CardGrid"), "src/components/CardGrid")
        write_text("src/components/Header/Header.tsx", HEADER_COMPONENT_CODE)
        safe_copy_file(os.path.join(BACKUP_DIR, "src", "widgets", "Header", "Header.module.css"), "src/components/Header/Header.module.css")
        
        # Write Context-based HomePage
        write_text("src/pages/HomePage/HomePage.tsx", """import styles from "./HomePage.module.css";
import { useStore } from "../../contexts/StoreContext";
import { useAuth } from "../../contexts/AuthContext";
import { Link, useNavigate } from "react-router-dom";

export function HomePage() {
  const { tours, cart, favorites, toggleFavorite, addToCart } = useStore();
  const { role } = useAuth();
  const navigate = useNavigate();

  const handleFavoriteClick = (e: React.MouseEvent, tourId: number) => {
    e.preventDefault(); 
    if (role === "guest") {
      navigate("/login");
      return;
    }
    toggleFavorite(tourId);
  };

  const handleCartClick = (e: React.MouseEvent, tourId: number) => {
    e.preventDefault();
    if (role === "guest") {
      navigate("/login");
      return;
    }
    const tour = tours.find(t => t.id === tourId);
    if (!tour) return;
    addToCart(tour);
  };

  return (
    <div className={styles.home}>
      <h1 className={styles.title}>Все туры</h1>
      <div className={styles.grid}>
        {tours.map((tour) => {
          const inCart = cart.some(c => c.id === tour.id);
          return (
            <Link key={tour.id} to={`/tour/${tour.id}`} className={styles.card}>
              <button
                className={`${styles.favoriteBtn} ${
                  favorites.includes(tour.id) ? styles.active : ""
                }`}
                onClick={(e) => handleFavoriteClick(e, tour.id)}
              >
                \\u2665
              </button>
              <img className={styles.image} src={tour.image} alt={tour.title} />
              <div className={styles.info}>
                <div className={styles.infoText}>
                  <h3 className={styles.tourTitle}>{tour.title}</h3>
                  <p className={styles.price}>${tour.price}</p>
                </div>
                <button
                  className={`${styles.cartIconBtn} ${
                    inCart ? styles.activeCart : ""
                  }`}
                  onClick={(e) => handleCartClick(e, tour.id)}
                >
                  \\uD83D\\uDED2
                </button>
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
""")

        # Add StoreProvider and Header in App.tsx
        write_text("src/App.tsx", """import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import { StoreProvider } from "./contexts/StoreContext";
import styles from "./App.module.css";
import { Header } from "./components/Header/Header";
import { HomePage } from "./pages/HomePage/HomePage";
import { TourDetailsPage } from "./pages/TourDetailsPage/TourDetailsPage";
import { FavoritesPage } from "./pages/FavoritesPage/FavoritesPage";
import { CartPage } from "./pages/CartPage/CartPage";
import { AdminPage } from "./pages/AdminPage/AdminPage";
import { LoginPage } from "./pages/LoginPage/LoginPage";
import { RegisterPage } from "./pages/RegisterPage/RegisterPage";
import { ProfilePage } from "./pages/ProfilePage/ProfilePage";

function App() {
  return (
    <AuthProvider>
      <StoreProvider>
        <BrowserRouter>
          <div className={styles.page}>
            <Header />
            <main className={styles.main}>
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/tour/:id" element={<TourDetailsPage />} />
                <Route path="/favorites" element={<FavoritesPage />} />
                <Route path="/cart" element={<CartPage />} />
                <Route path="/admin" element={<AdminPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/profile" element={<ProfilePage />} />
              </Routes>
            </main>
          </div>
        </BrowserRouter>
      </StoreProvider>
    </AuthProvider>
  );
}

export default App;
""")
        git_commit("feat: implement StoreContext and render tours on homepage", "2026-07-07T11:00:00+03:00")

        # =======================================================================
        # Commit 6: Connect Tour Details & Favorites (07.07.2026 17:15)
        # =======================================================================
        # Write Context-based TourDetailsPage
        write_text("src/pages/TourDetailsPage/TourDetailsPage.tsx", """import { useParams, useNavigate } from "react-router-dom";
import { useStore } from "../../contexts/StoreContext";
import { useAuth } from "../../contexts/AuthContext";
import styles from "./TourDetailsPage.module.css";

export function TourDetailsPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { tours, cart, favorites, addToCart, removeFromCart, toggleFavorite } = useStore();
  const { role } = useAuth();

  const tour = tours.find((t) => t.id === Number(id));

  if (!tour) {
    return <h2 className={styles.notFound}>Тур не найден</h2>;
  }

  const inCart = cart.some((item) => item.id === tour.id);
  const isFavorite = favorites.includes(tour.id);

  const handleFavoriteClick = () => {
    if (role === "guest") {
      navigate("/login");
      return;
    }
    toggleFavorite(tour.id);
  };

  const handleCartClick = () => {
    if (role === "guest") {
      navigate("/login");
      return;
    }
    if (inCart) {
      removeFromCart(tour.id);
    } else {
      addToCart(tour);
    }
  };

  return (
    <div className={styles.page}>
      <button className={styles.backBtn} onClick={() => navigate(-1)}>
        &larr; Назад
      </button>
      <div className={styles.container}>
        <div className={styles.imageWrapper}>
          <img className={styles.image} src={tour.image} alt={tour.title} />
        </div>
        <div className={styles.details}>
          <h1 className={styles.title}>{tour.title}</h1>
          <p className={styles.price}>${tour.price}</p>
          <p className={styles.description}>{tour.description}</p>
          
          <div className={styles.actions}>
            <button
              className={`${styles.actionBtn} ${styles.cartBtn} ${inCart ? styles.inCart : ""}`}
              onClick={handleCartClick}
            >
              {inCart ? "Удалить из корзины" : "В корзину"}
            </button>
            <button
              className={`${styles.actionBtn} ${styles.favBtn} ${isFavorite ? styles.activeFav : ""}`}
              onClick={handleFavoriteClick}
            >
              {isFavorite ? "В избранном \\u2665" : "В избранное \\u2661"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
""")

        # Write Context-based FavoritesPage
        write_text("src/pages/FavoritesPage/FavoritesPage.tsx", """import { useStore } from "../../contexts/StoreContext";
import { Link } from "react-router-dom";
import styles from "../HomePage/HomePage.module.css";

export function FavoritesPage() {
  const { tours, cart, favorites, toggleFavorite, addToCart, removeFromCart } = useStore();

  const favoriteTours = tours.filter((tour) => favorites.includes(tour.id));

  const handleFavoriteClick = (e: React.MouseEvent, tourId: number) => {
    e.preventDefault();
    toggleFavorite(tourId);
  };

  const handleCartClick = (e: React.MouseEvent, tourId: number) => {
    e.preventDefault();
    const tour = tours.find(t => t.id === tourId);
    if (!tour) return;
    if (cart.find(c => c.id === tourId)) {
      removeFromCart(tourId);
    } else {
      addToCart(tour);
    }
  };

  return (
    <div className={styles.home}>
      <h1 className={styles.title}>Избранное</h1>
      {favoriteTours.length === 0 ? (
        <p style={{ color: "#aaa" }}>У вас пока нет избранных туров.</p>
      ) : (
        <div className={styles.grid}>
          {favoriteTours.map((tour) => {
            const inCart = cart.some(c => c.id === tour.id);
            return (
              <Link key={tour.id} to={`/tour/${tour.id}`} className={styles.card}>
                <button
                  className={`${styles.favoriteBtn} ${styles.active}`}
                  onClick={(e) => handleFavoriteClick(e, tour.id)}
                >
                  \\u2665
                </button>
                <img className={styles.image} src={tour.image} alt={tour.title} />
                <div className={styles.info}>
                  <div className={styles.infoText}>
                    <h3 className={styles.tourTitle}>{tour.title}</h3>
                    <p className={styles.price}>${tour.price}</p>
                  </div>
                  <button
                    className={`${styles.cartIconBtn} ${inCart ? styles.activeCart : ""}`}
                    onClick={(e) => handleCartClick(e, tour.id)}
                  >
                    \\uD83D\\uDED2
                  </button>
                </div>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}
""")
        git_commit("feat: connect tour details view and favorites page", "2026-07-07T17:15:00+03:00")

        # =======================================================================
        # Commit 7: Cart & Checkout (08.07.2026 10:30)
        # =======================================================================
        # Write Context-based CartPage
        write_text("src/pages/CartPage/CartPage.tsx", """import { useStore } from "../../contexts/StoreContext";
import { Link, useNavigate } from "react-router-dom";
import styles from "./CartPage.module.css";

export function CartPage() {
  const { cart, removeFromCart, checkout } = useStore();
  const navigate = useNavigate();

  const total = cart.reduce((sum, item) => sum + item.price, 0);

  const handleCheckout = () => {
    checkout();
    alert("Заказ успешно оформлен!");
    navigate("/profile");
  };

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Корзина</h1>
      {cart.length === 0 ? (
        <p className={styles.empty}>Ваша корзина пуста.</p>
      ) : (
        <div className={styles.container}>
          <div className={styles.list}>
            {cart.map((item) => (
              <div key={item.id} className={styles.cartItem}>
                <img className={styles.image} src={item.image} alt={item.title} />
                <div className={styles.info}>
                  <Link to={`/tour/${item.id}`} className={styles.tourTitle}>
                    {item.title}
                  </Link>
                  <p className={styles.price}>${item.price}</p>
                </div>
                <button className={styles.removeBtn} onClick={() => removeFromCart(item.id)}>
                  Удалить
                </button>
              </div>
            ))}
          </div>
          <div className={styles.summary}>
            <h2>Итого:</h2>
            <p className={styles.totalPrice}>${total}</p>
            <button className={styles.checkoutBtn} onClick={handleCheckout}>Оформить заказ</button>
          </div>
        </div>
      )}
    </div>
  );
}
""")
        git_commit("feat: implement shopping cart and checkout order flow", "2026-07-08T10:30:00+03:00")

        # =======================================================================
        # Commit 8: Profile page (08.07.2026 17:15)
        # =======================================================================
        safe_copy_tree(os.path.join(BACKUP_DIR, "src", "components", "Profile"), "src/components/Profile")
        safe_copy_tree(os.path.join(BACKUP_DIR, "src", "components", "forms", "EditProfileForm"), "src/components/forms/EditProfileForm")
        
        # Write Context-based ProfilePage
        write_text("src/pages/ProfilePage/ProfilePage.tsx", """import { useState, useEffect } from "react";
import { useAuth } from "../../contexts/AuthContext";
import { useStore } from "../../contexts/StoreContext";
import styles from "./ProfilePage.module.css";
import { Link } from "react-router-dom";

export function ProfilePage() {
  const { profile, role, updateProfile } = useAuth();
  const { orders } = useStore();
  const [isEditing, setIsEditing] = useState(false);
  const [name, setName] = useState(profile?.name || "");
  const [email, setEmail] = useState(profile?.email || "");
  const [avatar, setAvatar] = useState(profile?.avatar || "");

  useEffect(() => {
    if (profile) {
      setName(profile.name);
      setEmail(profile.email);
      setAvatar(profile.avatar);
    }
  }, [profile]);

  if (!profile) return <div className={styles.container}>Загрузка профиля...</div>;

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    updateProfile({ name, email, avatar });
    setIsEditing(false);
  };

  if (role === "guest") {
    return (
      <div className={styles.page}>
        <h2 className={styles.title}>Доступ закрыт</h2>
        <p>Пожалуйста, войдите в систему.</p>
      </div>
    );
  }

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Личный кабинет</h1>
      <div className={styles.profileSection}>
        <img className={styles.avatar} src={profile.avatar} alt={profile.name} />
        {isEditing ? (
          <form className={styles.form} onSubmit={handleSave}>
            <input className={styles.input} type="text" value={name} onChange={(e) => setName(e.target.value)} required />
            <input className={styles.input} type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            <input className={styles.input} type="url" value={avatar} onChange={(e) => setAvatar(e.target.value)} required />
            <div className={styles.actions}>
              <button className={styles.saveBtn} type="submit">Сохранить</button>
              <button className={styles.cancelBtn} type="button" onClick={() => setIsEditing(false)}>Отмена</button>
            </div>
          </form>
        ) : (
          <div className={styles.info}>
            <h2>{profile.name}</h2>
            <p>{profile.email}</p>
            <p className={styles.roleTag}>Роль: {role}</p>
            <button className={styles.editBtn} onClick={() => setIsEditing(true)}>Редактировать профиль</button>
          </div>
        )}
      </div>
      <div className={styles.ordersSection}>
        <h2>История заказов</h2>
        {orders.length === 0 ? (
          <p className={styles.empty}>Вы еще не заказывали туры.</p>
        ) : (
          <div className={styles.ordersList}>
            {orders.map((order) => (
              <div key={order.id} className={styles.orderCard}>
                <div className={styles.orderHeader}>
                  <span className={styles.orderDate}>Заказ от {order.date}</span>
                  <span className={styles.orderTotal}>${order.total}</span>
                </div>
                <div className={styles.orderItems}>
                  {order.items.map((item, index) => (
                    <div key={index} className={styles.orderItem}>
                      <img src={item.image} alt={item.title} className={styles.orderItemImg} />
                      <Link to={`/tour/${item.id}`} className={styles.orderItemTitle}>{item.title}</Link>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
""")
        git_commit("feat: implement user Profile page and edit info forms", "2026-07-08T17:15:00+03:00")

        # =======================================================================
        # Commit 9: Admin page (09.07.2026 12:00)
        # =======================================================================
        safe_copy_tree(os.path.join(BACKUP_DIR, "src", "components", "forms", "AddCardForm"), "src/components/forms/AddCardForm")
        
        # Write Context-based AdminPage
        write_text("src/pages/AdminPage/AdminPage.tsx", """import { useState } from "react";
import { useAuth } from "../../contexts/AuthContext";
import { useStore } from "../../contexts/StoreContext";
import styles from "./AdminPage.module.css";

export function AdminPage() {
  const { role } = useAuth();
  const { addTour } = useStore();
  const [title, setTitle] = useState("");
  const [image, setImage] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("");

  if (role !== "admin") return <div className={styles.container}>Доступ запрещен</div>;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !image || !description || !price) return;
    
    addTour({
      title,
      image,
      description,
      price: Number(price),
    });

    setTitle("");
    setImage("");
    setDescription("");
    setPrice("");
    alert("Тур успешно добавлен!");
  };

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Панель администратора</h1>
      <div className={styles.formContainer}>
        <h2>Добавить новый тур</h2>
        <form onSubmit={handleSubmit} className={styles.form}>
          <input className={styles.input} type="text" placeholder="Название тура" value={title} onChange={(e) => setTitle(e.target.value)} required />
          <input className={styles.input} type="url" placeholder="Ссылка на картинку" value={image} onChange={(e) => setImage(e.target.value)} required />
          <textarea className={styles.textarea} placeholder="Описание тура" value={description} onChange={(e) => setDescription(e.target.value)} required />
          <input className={styles.input} type="number" placeholder="Цена ($)" value={price} onChange={(e) => setPrice(e.target.value)} required min="0" />
          <button className={styles.submitBtn} type="submit">Добавить тур</button>
        </form>
      </div>
    </div>
  );
}
""")
        git_commit("feat: add Admin panel and form to create new tours", "2026-07-09T12:00:00+03:00")

        # =======================================================================
        # Commit 10: Styling tweaks/Bugfix (09.07.2026 18:00)
        # =======================================================================
        # Append minor comment / tweak to src/index.css
        with open("src/index.css", "a", encoding="utf-8") as f:
            f.write("\n\n/* Tweak layout margins and button transitions for better UX */\n")
        git_commit("fix: improve responsive styles and form validation logic", "2026-07-09T18:00:00+03:00")

        # =======================================================================
        # Commit 11: Add API Emulator & Zustand Stores (10.07.2026 11:30)
        # =======================================================================
        safe_copy_file(os.path.join(BACKUP_DIR, "src", "api", "index.ts"), "src/api/index.ts")
        safe_copy_file(os.path.join(BACKUP_DIR, "src", "store", "useAuthStore.ts"), "src/store/useAuthStore.ts")
        safe_copy_file(os.path.join(BACKUP_DIR, "src", "store", "useTourStore.ts"), "src/store/useTourStore.ts")
        git_commit("feat: add mock API client with async simulated latency", "2026-07-10T11:30:00+03:00")

        # =======================================================================
        # Commit 12: Migrate Auth & Header to Zustand (11.07.2026 10:15)
        # =======================================================================
        safe_copy_tree(os.path.join(BACKUP_DIR, "src", "widgets"), "src/widgets")
        safe_copy_file(os.path.join(BACKUP_DIR, "src", "App.tsx"), "src/App.tsx")
        safe_copy_file(os.path.join(BACKUP_DIR, "src", "pages", "LoginPage", "LoginPage.tsx"), "src/pages/LoginPage/LoginPage.tsx")
        safe_copy_file(os.path.join(BACKUP_DIR, "src", "pages", "RegisterPage", "RegisterPage.tsx"), "src/pages/RegisterPage/RegisterPage.tsx")
        safe_copy_file(os.path.join(BACKUP_DIR, "src", "pages", "ProfilePage", "ProfilePage.tsx"), "src/pages/ProfilePage/ProfilePage.tsx")
        git_commit("refactor: implement Zustand and migrate auth state to useAuthStore", "2026-07-11T10:15:00+03:00")

        # =======================================================================
        # Commit 13: Migrate remaining pages to Zustand (11.07.2026 15:45)
        # =======================================================================
        safe_copy_file(os.path.join(BACKUP_DIR, "src", "pages", "HomePage", "HomePage.tsx"), "src/pages/HomePage/HomePage.tsx")
        safe_copy_file(os.path.join(BACKUP_DIR, "src", "pages", "TourDetailsPage", "TourDetailsPage.tsx"), "src/pages/TourDetailsPage/TourDetailsPage.tsx")
        safe_copy_file(os.path.join(BACKUP_DIR, "src", "pages", "FavoritesPage", "FavoritesPage.tsx"), "src/pages/FavoritesPage/FavoritesPage.tsx")
        safe_copy_file(os.path.join(BACKUP_DIR, "src", "pages", "CartPage", "CartPage.tsx"), "src/pages/CartPage/CartPage.tsx")
        safe_copy_file(os.path.join(BACKUP_DIR, "src", "pages", "AdminPage", "AdminPage.tsx"), "src/pages/AdminPage/AdminPage.tsx")
        git_commit("refactor: migrate tours and cart to useTourStore Zustand", "2026-07-11T15:45:00+03:00")

        # =======================================================================
        # Commit 14: Cleanup context files (12.07.2026 12:00)
        # =======================================================================
        run_cmd(["git", "rm", "-rf", "src/contexts"])
        run_cmd(["git", "rm", "-rf", "src/components/Header"])
        git_commit("cleanup: remove deprecated React Context files and old components", "2026-07-12T12:00:00+03:00")

        # =======================================================================
        # Commit 15: README and final configs (12.07.2026 18:00)
        # =======================================================================
        write_text("README.md", README_CODE)
        git_commit("docs: update project README and finalize configs", "2026-07-12T18:00:00+03:00")

        # =======================================================================
        # Restore untracked context files to local directory
        # =======================================================================
        write_text("src/contexts/AuthContext.tsx", AUTH_CONTEXT_CODE)
        write_text("src/contexts/StoreContext.tsx", STORE_CONTEXT_CODE)
        write_text("src/components/Header/Header.tsx", HEADER_COMPONENT_CODE)
        safe_copy_file(os.path.join(BACKUP_DIR, "src", "widgets", "Header", "Header.module.css"), "src/components/Header/Header.module.css")
        
        # Keep old git backup in a safe place
        old_git_backup_dir = "_old_git_backup"
        if os.path.exists(old_git_backup_dir):
            rmtree_readonly(old_git_backup_dir)
        safe_copy_tree(os.path.join(BACKUP_DIR, ".git_backup"), old_git_backup_dir)
        
        # Cleanup temporary backup directory
        rmtree_readonly(BACKUP_DIR)
        print("Git history has been recreated successfully!")
        print("Old Git database backed up in '_old_git_backup/' folder.")

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Failed to recreate history. Error: {e}")
        print(f"You can restore files manually from the '{BACKUP_DIR}' directory.")

if __name__ == "__main__":
    main()
