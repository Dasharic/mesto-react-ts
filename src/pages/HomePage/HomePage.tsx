import styles from "./HomePage.module.css";
import { useTourStore } from "../../store/useTourStore";
import { useAuthStore } from "../../store/useAuthStore";
import { Link, useNavigate } from "react-router-dom";

export function HomePage() {
  const { tours, cart, favorites, toggleFavorite, addToCart, removeFromCart } = useTourStore();
  const { role } = useAuthStore();
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

    if (cart.find(c => c.id === tourId)) {
      removeFromCart(tourId);
    } else {
      addToCart(tour);
    }
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
              title="В избранное"
            >
              ♥
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
                title={inCart ? "Удалить из корзины" : "Добавить в корзину"}
              >
                🛒
              </button>
            </div>
          </Link>
        )})}
      </div>
    </div>
  );
}
