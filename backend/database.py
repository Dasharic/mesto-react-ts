import sqlite3
import json

DB_PATH = "mesto.db"

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    # Users
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT,
            role TEXT,
            profile_name TEXT,
            profile_avatar TEXT
        )
    ''')
    # Tours
    c.execute('''
        CREATE TABLE IF NOT EXISTS tours (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            image TEXT,
            description TEXT,
            price INTEGER
        )
    ''')
    # Cart
    c.execute('''
        CREATE TABLE IF NOT EXISTS cart_items (
            email TEXT,
            tour_id INTEGER,
            PRIMARY KEY(email, tour_id)
        )
    ''')
    # Favorites
    c.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            email TEXT,
            tour_id INTEGER,
            PRIMARY KEY(email, tour_id)
        )
    ''')
    # Orders
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            date TEXT,
            total INTEGER,
            items_json TEXT
        )
    ''')
    
    # Seed data
    if c.execute('SELECT COUNT(*) FROM users').fetchone()[0] == 0:
        c.execute('INSERT INTO users (email, password, role, profile_name, profile_avatar) VALUES (?, ?, ?, ?, ?)',
                  ('admin@mesto.com', 'admin', 'admin', 'Admin User', 'https://images.unsplash.com/photo-1544723795-3cj3h9f28d82'))
        
    if c.execute('SELECT COUNT(*) FROM tours').fetchone()[0] == 0:
        tours = [
            ("Бали, Индонезия", "https://images.unsplash.com/photo-1502602898657-3e91760cbb34", "Тропический рай с вулканами и храмами.", 1500),
            ("Рим, Италия", "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf", "Античная архитектура и вкусная еда.", 2500),
            ("Нью-Йорк, США", "https://images.unsplash.com/photo-1522083165195-3424ed129620", "Мегаполис, который никогда не спит.", 2000)
        ]
        c.executemany('INSERT INTO tours (title, image, description, price) VALUES (?, ?, ?, ?)', tours)

    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()
