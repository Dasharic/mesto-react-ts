import styles from "./Card.module.css";

type CardProps = {
  id: number;
  title: string;
  image: string;
  isFavorite: boolean;
  onFavoriteClick: (id:number)=>void;
};

export function Card({
  id,
  title,
  image,
  isFavorite,
  onFavoriteClick,
}: CardProps) {

  return (
    <div className={styles.card}>

      <button
        className={`${styles.favorite} ${
          isFavorite ? styles.active : ""
        }`}
        onClick={() => onFavoriteClick(id)}
      >
        ♥
      </button>

      <img
        className={styles.image}
        src={image}
        alt={title}
      />

      <h3 className={styles.title}>
        {title}
      </h3>

    </div>
  );
}