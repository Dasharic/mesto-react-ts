import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";
import { Button } from "../../ui/Button/Button";
import { Input } from "../../ui/Input/Input";
import styles from "../LoginPage/LoginPage.module.css";

export function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (password !== confirmPassword) {
      setError("Пароли не совпадают");
      return;
    }
    const success = register(name, email, password);
    if (success) {
      navigate("/");
    } else {
      setError("Пользователь с таким email уже существует");
    }
  };

  return (
    <div className={styles.page}>
      <div className={styles.container}>
        <h1 className={styles.title}>Регистрация</h1>
        <p className={styles.subtitle}>Создайте новый аккаунт</p>
        
        {error && <p className={styles.error}>{error}</p>}

        <form className={styles.form} onSubmit={handleSubmit}>
          <Input type="text" placeholder="Ваше Имя" value={name} onChange={(e) => setName(e.target.value)} required />
          <Input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <Input type="password" placeholder="Пароль" value={password} onChange={(e) => setPassword(e.target.value)} required />
          <Input type="password" placeholder="Подтвердите пароль" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
          <Button type="submit">Зарегистрироваться</Button>
        </form>

        <p className={styles.linkText}>
          Уже есть аккаунт? <Link to="/login" className={styles.link}>Войти</Link>
        </p>
      </div>
    </div>
  );
}
