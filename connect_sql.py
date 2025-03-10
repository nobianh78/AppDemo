import pyodbc

class DatabaseSQLServer:
    def __init__(self):
        self.server = 'python-project.database.windows.net'
        self.database = 'python_project'
        self.username = 'admin1'
        self.password = 'Sql123456'
        self.driver = '{ODBC Driver 17 for SQL Server}'
        self.conn = self.connect_db()
        self.create_table()

    def connect_db(self):
        """Kết nối đến SQL Server"""
        try:
            conn = pyodbc.connect(
                f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
            )
            print("✅ Kết nối SQL Server thành công!")
            return conn
        except Exception as e:
            print(f"❌ Lỗi kết nối: {e}")
            return None

    def create_table(self):
        """Tạo bảng users nếu chưa tồn tại"""
        query = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
        CREATE TABLE users (
            id INT PRIMARY KEY,
            username NVARCHAR(50) UNIQUE NOT NULL,
            email NVARCHAR(100) UNIQUE NOT NULL,
            password VARBINARY(MAX) NOT NULL
        )
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()

    def get_next_available_id(self):
        """Tìm ID nhỏ nhất còn trống"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COALESCE(MIN(t.id) + 1, 1) 
            FROM users AS t
            WHERE NOT EXISTS (SELECT 1 FROM users u WHERE u.id = t.id + 1)
        """)
        return cursor.fetchone()[0]

    def insert_user(self, username, email, hashed_password):
        """Thêm người dùng mới vào database"""
        try:
            next_id = self.get_next_available_id()
            print(f"Inserting user: {username}, email: {email},")
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO users (id, username, email, password) VALUES (?, ?, ?, ?)",
                (next_id, username, email, hashed_password)
            )
            self.conn.commit()
            print("User inserted successfully")
            return True
        except pyodbc.IntegrityError as e:
            print(f"IntegrityError: {e}")
            return False  # Trả về False nếu username hoặc email đã tồn tại
        except Exception as e:
            print(f"❌ Lỗi thêm user: {e}")
            return False

    def get_user_password(self, username):
        """Lấy password đã băm từ database"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return row[0] if row else None  # Trả về password dưới dạng bytes

    def get_user_password_by_email(self, email):
        """Lấy password đã băm từ database bằng email"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        return row[0] if row else None  # Trả về password dưới dạng bytes

    def email_exists(self, email):
        """Kiểm tra email có tồn tại trong database không"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,))
        return cursor.fetchone() is not None

    def username_exists(self, username):
        """Kiểm tra username có tồn tại trong database không"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        return cursor.fetchone() is not None

