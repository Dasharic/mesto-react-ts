import { Card } from "../../ui/Card/Card";
import styles from "./CardGrid.module.css";

type CardItem = {
  id: number;
  title: string;
  image: string;
  isFavorite: boolean;
};

type Props = {
  cards: CardItem[];
  onFavoriteClick: (id:number) => void;
};

export function CardGrid({ cards, onFavoriteClick }: Props) {
  return (
    <section className={styles.grid}>
      {cards.map((card) => (
        <Card 
        key={card.id}
        id={card.id}
        title={card.title}
        image={card.image}
        isFavorite={card.isFavorite} 
        onFavoriteClick={onFavoriteClick} />
      ))}
    </section>
  );
}