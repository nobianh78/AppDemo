
import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()

        # Tạo lại bảng users với cột role
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user'  -- Thêm cột role
            )
        ''')
        self.conn.commit()

    def add_user(self, email, password, role="user"):
        """Thêm tài khoản mới vào database"""
        try:
            self.cursor.execute("INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
                                (email, password, role))
            self.conn.commit()
            return True  # Đăng ký thành công
        except sqlite3.IntegrityError:
            return False  # Email đã tồn tại

    def close(self):
        """Đóng kết nối database"""
        self.conn.close()

# Chạy file này một lần để tạo lại database
if __name__ == "__main__":
    db = Database()
    print("Database created successfully!")
    db.close()
