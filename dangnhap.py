import bcrypt
from connect_sql import DatabaseSQLServer  # Import class kết nối SQL Server

# Database setup
db = DatabaseSQLServer()  # Kết nối SQL Server

# HASH PASSWORD
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

# REGISTER
def register(username, email, password):
    if db.username_exists(username):
        print("Username already exists")
        return "❌ Username đã tồn tại!"
    if db.email_exists(email):
        print("Email already exists")
        return "❌ Email đã tồn tại!"

    hashed_password = hash_password(password)  # Hash mật khẩu
    if db.insert_user(username, email, hashed_password):
        print("User registered successfully")
        return "✅ Đăng ký thành công!"
    else:
        print("User registration failed")
        return "❌ Đăng ký thất bại!"

# LOGIN
def login(email, password):
    stored_hashed_password = db.get_user_password_by_email(email)
    if stored_hashed_password:
        if check_password(password, stored_hashed_password):
            return "✅ Đăng nhập thành công!"
        else:
            print("Password check failed")
            return "❌ Sai email hoặc password!"
    else:
        return "❌ Sai email hoặc password!"

# Example usage
if __name__ == "__main__": 
    while True:
        choice = input("Bạn muốn [1] Đăng ký hay [2] Đăng nhập? ")
        if choice == '1':
            username = input("Nhập username: ")
            email = input("Nhập email: ")
            password = input("Nhập password: ")
            print(register(username, email, password))
        elif choice == '2':
            email = input("Nhập email: ")
            password = input("Nhập password: ")
            print(login(email, password))
        else:
            print("❌ Lựa chọn không hợp lệ!")
