import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuthStore } from "../../store/useAuthStore";
import { Button } from "../../ui/Button/Button";
import { Input } from "../../ui/Input/Input";
import styles from "../LoginPage/LoginPage.module.css";

export function RegisterPage() {
  const { register, error, clearError, isLoading } = useAuthStore();
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [localError, setLocalError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError("");
    clearError();

    if (!name || !email || !password || !confirmPassword) {
      setLocalError("Заполните все поля");
      return;
    }

    if (password.length < 6) {
      setLocalError("Пароль должен содержать минимум 6 символов");
      return;
    }

    if (password !== confirmPassword) {
      setLocalError("Пароли не совпадают");
      return;
    }
    
    const success = await register(name, email, password);
    if (success) navigate("/");
  };

  const displayError = localError || error;

  return (
    <div className={styles.page}>
      <div className={styles.container}>
        <h1 className={styles.title}>Регистрация</h1>
        <p className={styles.subtitle}>Создайте новый аккаунт</p>
        
        {displayError && <p className={styles.error}>{displayError}</p>}

        <form className={styles.form} onSubmit={handleSubmit}>
          <Input type="text" placeholder="Ваше Имя" value={name} onChange={(e) => setName(e.target.value)} required />
          <Input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <Input type="password" placeholder="Пароль" value={password} onChange={(e) => setPassword(e.target.value)} required />
          <Input type="password" placeholder="Подтвердите пароль" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
          <Button type="submit" disabled={isLoading}>{isLoading ? "Загрузка..." : "Зарегистрироваться"}</Button>
        </form>

        <p className={styles.linkText}>
          Уже есть аккаунт? <Link to="/login" className={styles.link}>Войти</Link>
        </p>
      </div>
    </div>
  );
}
