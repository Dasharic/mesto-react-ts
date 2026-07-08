import { useState, useEffect } from "react";
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
