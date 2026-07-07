import { useStore } from "../../contexts/StoreContext";
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
                  \u2665
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
                    \uD83D\uDED2
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
