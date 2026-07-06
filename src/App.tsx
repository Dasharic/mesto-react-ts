import { BrowserRouter, Routes, Route } from "react-router-dom";
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
