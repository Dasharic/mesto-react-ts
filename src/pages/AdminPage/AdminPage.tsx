import { useState } from "react";
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
