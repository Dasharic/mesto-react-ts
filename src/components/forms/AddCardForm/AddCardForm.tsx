import { useState } from "react";
import styles from "./AddCardForm.module.css";

type Props = {
  onAdd: (title: string, image: string) => void;
};

export function AddCardForm({ onAdd }: Props) {
  const [title, setTitle] = useState("");
  const [image, setImage] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    onAdd(title, image);
    setTitle("");
    setImage("");
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <h2 className={styles.title}>Новое место</h2>

      <input
        className={styles.input}
        placeholder="Название"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <input
        className={styles.input}
        placeholder="Ссылка на картинку"
        value={image}
        onChange={(e) => setImage(e.target.value)}
      />

      <button className={styles.button} type="submit">
        Создать
      </button>
    </form>
  );
}