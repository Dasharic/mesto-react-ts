import { useTourStore } from "../../store/useTourStore";
import { Link, useNavigate } from "react-router-dom";
import styles from "./CartPage.module.css";

export function CartPage() {
  const { cart, removeFromCart, checkout } = useTourStore();
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
                <button
                  className={styles.removeBtn}
                  onClick={() => removeFromCart(item.id)}
                >
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
