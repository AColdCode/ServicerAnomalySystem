import sqlite3
import hashlib


class AuthManager:
    def __init__(self, db_path="db/database.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """)

        # 默认管理员
        cursor.execute("SELECT * FROM users WHERE username=?", ("admin",))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                ("admin", self.hash_password("123456"), "admin")
            )

        conn.commit()
        conn.close()

    def hash_password(self, password):
        return hashlib.md5(password.encode()).hexdigest()

    def login(self, username, password):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        hashed = self.hash_password(password)

        cursor.execute(
            "SELECT role FROM users WHERE username=? AND password=?",
            (username, hashed)
        )

        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]  # admin / user
        return None

    def register(self, username, password, role="user"):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 1. 查询当前用户数量
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]

        # 2. 如果只有默认管理员（1个用户），则新用户变管理员
        if count == 1:
            role = "admin"

        # 3. 加密密码
        hashed = self.hash_password(password)

        try:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, hashed, role)
            )
            conn.commit()
            return role
        except sqlite3.IntegrityError:
            # 用户名重复
            return
        finally:
            conn.close()
