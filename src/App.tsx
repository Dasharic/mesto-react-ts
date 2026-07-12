import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useEffect } from "react";
import { useAuthStore } from "./store/useAuthStore";
import { useTourStore } from "./store/useTourStore";
import styles from "./App.module.css";
import { Header } from "./widgets/Header/Header";
import { HomePage } from "./pages/HomePage/HomePage";
import { TourDetailsPage } from "./pages/TourDetailsPage/TourDetailsPage";
import { FavoritesPage } from "./pages/FavoritesPage/FavoritesPage";
import { CartPage } from "./pages/CartPage/CartPage";
import { AdminPage } from "./pages/AdminPage/AdminPage";
import { LoginPage } from "./pages/LoginPage/LoginPage";
import { RegisterPage } from "./pages/RegisterPage/RegisterPage";
import { ProfilePage } from "./pages/ProfilePage/ProfilePage";

function App() {
  const initAuth = useAuthStore((state) => state.initAuth);
  const token = useAuthStore((state) => state.token);
  const { fetchTours, loadUserData } = useTourStore();

  useEffect(() => {
    initAuth();
    fetchTours();
  }, [initAuth, fetchTours]);

  useEffect(() => {
    loadUserData();
  }, [token, loadUserData]);

  return (
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
  );
}

export default App;
