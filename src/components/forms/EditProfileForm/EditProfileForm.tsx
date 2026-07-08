import { useState } from "react";
import styles from "./EditProfileForm.module.css";

type Props = {
  name: string;
  about: string;
  onSave: (name: string, about: string) => void;
};

export function EditProfileForm({
  name,
  about,
  onSave,
}: Props) {
  const [newName, setNewName] = useState(name);
  const [newAbout, setNewAbout] = useState(about);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    onSave(newName, newAbout);
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <h2 className={styles.title}>
        Редактировать профиль
      </h2>

      <input
        className={styles.input}
        placeholder="Имя"
        value={newName}
        onChange={(e) => setNewName(e.target.value)}
      />

      <input
        className={styles.input}
        placeholder="О себе"
        value={newAbout}
        onChange={(e) => setNewAbout(e.target.value)}
      />

      <button className={styles.button} type="submit">
        Сохранить
      </button>
    </form>
  );
}