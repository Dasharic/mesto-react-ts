import { NavLink, useNavigate } from "react-router-dom";
import { useAuthStore } from "../../store/useAuthStore";
import { useTourStore } from "../../store/useTourStore";
import styles from "./Header.module.css";

export function Header() {
  const { role, profile, logout } = useAuthStore();
  const { cart, favorites } = useTourStore();
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
              <img src={profile?.avatar || "https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png"} alt="Avatar" className={styles.avatarMini} />
              <span className={styles.userName}>{profile?.name}</span>
            </NavLink>
            <button onClick={handleLogout} className={styles.logoutBtn}>Выйти</button>
          </div>
        )}
      </div>
    </header>
  );
}