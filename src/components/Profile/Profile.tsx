import styles from "./Profile.module.css";

type Props = {
  name: string;
  about: string;
  onEditClick: () => void;
  onAddClick: () => void;
};

export function Profile({
  name,
  about,
  onEditClick,
  onAddClick,
}: Props) {
  return (
    <section className={styles.profile}>
      <div className={styles.profileInfo}>
        <div className={styles.avatar}></div>

        <div className={styles.info}>
          <div className={styles.nameRow}>
            <h2 className={styles.name}>{name}</h2>

            <button
              className={`${styles.baseButton} ${styles.editButton}`}
              onClick={onEditClick}
            >
              ✏️
            </button>
          </div>

          <p className={styles.about}>{about}</p>
        </div>
      </div>

      <div className={styles.profileActions}>
        <button className={`${styles.baseButton} ${styles.favoriteButton}`}>
          Избранное
        </button>

        <button
          className={`${styles.baseButton} ${styles.addButton}`}
          onClick={onAddClick}
        >
          +
        </button>
      </div>
    </section>
  );
}