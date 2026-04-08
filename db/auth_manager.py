import datetime
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
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            parent_admin TEXT
        )
        """)

        # 默认管理员
        cursor.execute("SELECT * FROM users WHERE username=?", ("admin",))
        if not cursor.fetchone():
            cursor.execute(
                """INSERT INTO users 
                (username, password, role, created_at, is_active, parent_admin) 
                VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    "admin",
                    self.hash_password("123456"),
                    "admin",
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    1,
                    ""
                )
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
            """
            SELECT role FROM users 
            WHERE username=? 
              AND password=? 
              AND is_active=1
            """,
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

        # 管理员数量控制
        cursor.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
        admin_count = cursor.fetchone()[0]

        parent_admin = ""
        if admin_count < 2:
            role = "admin"
            parent_admin = "admin"

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hashed = self.hash_password(password)

        try:
            cursor.execute(
                """INSERT INTO users 
                (username, password, role, created_at, is_active, parent_admin) 
                VALUES (?, ?, ?, ?, ?, ?)""",
                (username, hashed, role, now, 1, parent_admin)
            )
            conn.commit()
            return role
        except sqlite3.IntegrityError:
            # 主键冲突（用户名已存在）
            return None
        finally:
            conn.close()

    def set_user_active(self, username, active):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE users SET is_active=? WHERE username=?",
                (active, username)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_all_users(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT username, role, created_at, is_active, parent_admin
            FROM users
            WHERE username != 'admin'
        """)

        rows = cursor.fetchall()
        conn.close()

        # 转换为字典列表（QML可识别）
        users = []
        for row in rows:
            users.append({
                "username": row[0],
                "role": row[1],
                "created_at": row[2],
                "is_active": row[3],
                "parent_admin": row[4]
            })

        return users

    def get_sub_admins(self, username):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT username FROM users WHERE parent_admin=?",
            (username,)
        )

        children = [row[0] for row in cursor.fetchall()]
        conn.close()

        result = []

        for child in children:
            result.append(child)
            result.extend(self.get_sub_admins(child))  # 🔥 递归

        return result

    def downgrade_admin(self, operator, target):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 检查权限
        cursor.execute(
            "SELECT parent_admin FROM users WHERE username=?",
            (target,)
        )
        row = cursor.fetchone()

        if not row or row[0] != operator:
            conn.close()
            return False

        # 获取所有子管理员
        sub_admins = self.get_sub_admins(target)

        # 包含自己
        sub_admins.append(target)

        # 批量降级
        try:
            for user in sub_admins:
                cursor.execute("""
                    UPDATE users
                    SET role='user',
                        parent_admin=NULL
                    WHERE username=?
                """, (user,))

            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def upgrade_to_admin(self, operator, target):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE users
                SET role='admin',
                    parent_admin=?
                WHERE username=?
            """, (operator, target))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def change_user_role(self, username, role, operator):
        if role == "admin":
            return self.upgrade_to_admin(operator, username)
        else:
            return self.downgrade_admin(operator, username)

    def change_user_active(self, username, active, operator):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 检查权限
        cursor.execute(
            "SELECT role, parent_admin FROM users WHERE username=?",
            (username,)
        )
        row = cursor.fetchone()

        if row[0] == "admin" and row[1] != operator:
            conn.close()
            return False
        return self.set_user_active(username, active)

    def delete_user(self, username, operator):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT role, parent_admin FROM users WHERE username=?",
                (username,)
            )
            row = cursor.fetchone()
            if row[0] == "admin" and row[1] != operator:
                conn.close()
                return False

            try:
                self.downgrade_admin(operator, username)    # 将该管理员的设置的管理员降级
                cursor.execute("DELETE FROM users WHERE username=?", (username,))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
