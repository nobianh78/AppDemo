from database import Database  # Nếu file tên khác, sửa lại

db = Database()

# Thêm tài khoản admin
admin_email = "admin@example.com"
admin_password = "admin123"

if db.add_user(admin_email, admin_password, role="admin"):
    print("Admin account created successfully!")
else:
    print("Admin account already exists!")

db.close()
