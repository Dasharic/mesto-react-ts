import { useParams, useNavigate } from "react-router-dom";
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
              {isFavorite ? "В избранном \u2665" : "В избранное \u2661"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
