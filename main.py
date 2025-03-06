from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.togglebutton import ToggleButton
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
import mysql.connector
import sqlite3
import re
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.label import MDLabel
# Load các file KV
Builder.load_file("myapp.kv")
Builder.load_file("login.kv")
Builder.load_file("signup.kv")
Builder.load_file("home.kv")
Builder.load_file("profile.kv")
Builder.load_file("welcome.kv")
import sqlite3

import sqlite3

class Database:
    def __init__(self):
        """Kết nối đến database SQLite"""
        self.conn = sqlite3.connect("users.db")  # Kết nối hoặc tạo database nếu chưa có
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Tạo bảng users nếu chưa tồn tại"""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                email TEXT UNIQUE NOT NULL,
                                password TEXT NOT NULL
                              )''')
        self.conn.commit()

    def insert_user(self, email, password):
        """Thêm người dùng mới vào database"""
        try:
            self.cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Trả về False nếu email đã tồn tại

    def check_user(self, email, password):
        """Kiểm tra email & mật khẩu có đúng không"""
        self.cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        return self.cursor.fetchone() is not None  # Trả về True nếu tìm thấy user

    def close(self):
        """Đóng kết nối database"""
        self.conn.close()

def create_database():
    #tao mot database va bang uses de luu tru
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                      )''')
    conn.commit()
    conn.close()

create_database()
class MainScreen(Screen):
    pass


class WelcomeScreen(Screen):
    def toggle_language(self):
        if not all(k in self.ids for k in
                   ["welcome_text", "subtitle_text", "language_button", "login_button", "signup_button"]):
            print("Lỗi: ID không tồn tại!")
            return

        if self.ids.welcome_text.text == "Chào Mừng ! ":
            self.ids.welcome_text.text = "Welcome!"
            self.ids.subtitle_text.text = "Start your journey with us"
            self.ids.language_button.text = "Tiếng Việt"
            self.ids.login_button.text = "Login"
            self.ids.signup_button.text = "Sign Up"
        else:
            self.ids.welcome_text.text = "Chào Mừng ! "
            self.ids.subtitle_text.text = "Hãy bắt đầu hành trình cùng chúng tôi"
            self.ids.language_button.text = "English"
            self.ids.login_button.text = "Đăng Nhập"
            self.ids.signup_button.text = "Đăng Ký"

        # Cập nhật lại bố cục sau khi thay đổi văn bản
        self.ids.welcome_text.texture_update()
        self.ids.subtitle_text.texture_update()
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.dialog import MDDialog

class LoginScreen(Screen):
    dialog = None
    popup = None

    def login(self):
        email = self.ids.email.text.strip()
        password = self.ids.password.text.strip()

        # Sử dụng class Database để kiểm tra thông tin đăng nhập
        db = Database()  # Kết nối tới Database
        cursor = db.cursor

        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        db.close()  # Đóng kết nối Database

        # Kiểm tra kết quả trả về
        if not user:
            self.show_popup("Lỗi", "Sai email hoặc mật khẩu!")  # Hiển thị lỗi
            return  # Không chuyển màn hình nếu thông tin sai

        # Nếu thông tin đúng, chuyển tới màn hình Home
        self.manager.current = "home"

    def show_popup(self, title, message):
        if not self.dialog:
            self.dialog = MDDialog(
                title=title, text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        else:
            self.dialog.text = message  # Cập nhật nội dung nếu dialog đã tồn tại

        self.dialog.open()
    def check_internet(self):
        """Kiểm tra kết nối Internet trước khi cho phép đăng nhập"""
        url = "http://www.google.com"  # URL kiểm tra mạng



        def error_callback(req, error):
            # Nếu không có mạng, hiển thị thông báo lỗi
            self.show_no_internet_dialog()
            self.manager.current = "login"
        # Kiểm tra kết nối (timeout 3 giây)
        UrlRequest(url, on_error=error_callback, timeout=3)

    def show_no_internet_dialog(self):
        """Hiển thị dialog khi không có kết nối mạng"""
        if not self.dialog:
            self.dialog = MDDialog(
                title="Lỗi kết nối",
                text="Không có kết nối Internet. Vui lòng kiểm tra lại WiFi hoặc dữ liệu di động!",

                buttons=[
                    MDRaisedButton(text="OK", on_release=lambda x: self.dialog.dismiss())
                ]

            )
        self.dialog.open()

    def goto_signup(self):
        self.manager.current = "signup"

    def show_popup(self, title, message):
        if not self.popup:
            close_button = MDFlatButton(text="Close", on_release=self.close_popup)
            self.popup = MDDialog(title=title, text=message, buttons=[close_button])
        self.popup.open()

    def close_popup(self, *args):
        if self.popup:
            self.popup.dismiss(force=True)
            self.popup = None


class SignUpScreen(Screen):
    class SignUpScreen(Screen):
        def on_pre_enter(self, *args):
            """Cập nhật giao diện khi vào màn hình"""
            self.update_language()

        def update_language(self):
            """Cập nhật ngôn ngữ dựa trên trạng thái của ứng dụng"""
            app = MDApp.get_running_app()
            if app.language == "Tiếng Việt":
                self.ids.welcome_label.text = "XIN CHÀO!"
                self.ids.create_label.text = "Tạo tài khoản mới"
                self.ids.email.hint_text = "Email"
                self.ids.password.hint_text = "Mật khẩu"
                self.ids.re_password.hint_text = "Nhập lại mật khẩu"
                self.ids.login_button.text = "ĐĂNG NHẬP"
            else:
                self.ids.welcome_label.text = "HELLO!"
                self.ids.create_label.text = "Create a new account"
                self.ids.email.hint_text = "Email"
                self.ids.password.hint_text = "Password"
                self.ids.re_password.hint_text = "Re - Password"
                self.ids.login_button.text = "LOGIN"

    def register_user(self):
        email = self.ids.email.text.strip()
        password = self.ids.password.text.strip()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.ids.error_label.text = "Email không hợp lệ!"
            return
        if len(password) < 8:
            self.ids.error_label.text = "Mật khẩu phải có ít nhất 8 ký tự!"
            return
        if not email or not password:
            self.show_popup("Error", "Please enter all fields!")
            return
        self.ids.error_label.text = ""
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
            self.show_popup("Success", "Account created successfully!")
            self.manager.current = "login"  # Chuyển sang màn hình đăng nhập
        except sqlite3.IntegrityError:
            self.show_popup("Error", "Email already exists!")
        finally:
            conn.close()

    def show_popup(self, title, message):
        dialog = MDDialog(title=title, text=message,
                          buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())])
        dialog.open()
class HomeScreen(Screen):
    def add_team_card(self, team_name):
        """Thêm một thẻ đội nhóm vào màn hình với hiệu ứng fade-in."""
        card = MDCard(
            size_hint=(None, None),
            size=("90%", "120dp"),
            elevation=8,
            padding=10,
            radius=[15],
            pos_hint={"center_x": 0.5},
            opacity=0  # Bắt đầu với opacity 0 để tạo hiệu ứng fade-in
        )

        layout = MDBoxLayout(orientation="vertical", spacing=10, padding=10)
        label = MDLabel(text=team_name, theme_text_color="Primary", font_style="H5")
        button = MDRaisedButton(text="View Details", pos_hint={"center_x": 0.5})

        layout.add_widget(label)
        layout.add_widget(button)
        card.add_widget(layout)

        self.ids.teams_container.add_widget(card)

        # Hiệu ứng fade-in khi thêm thẻ
        anim = Animation(opacity=1, duration=0.5)
        anim.start(card)

class ProfileScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class MainApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SignUpScreen(name="signup"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(ProfileScreen(name="profile"))
        sm.add_widget(SettingsScreen(name="settings"))
        self.theme_cls.primary_palette = "Purple"  # Chọn bảng màu tím
        self.theme_cls.primary_hue = "300"  # Chọn sắc độ tím nhẹ
        return sm
    def change_tab_color(self, tab):
        """Hàm đổi màu khi bấm vào tab"""
        tab.theme_text_color = "Custom"  # Cho phép thay đổi màu chữ
        tab.text_color = (0.7, 0.5, 1, 1)  # Màu tím pastel
        tab.icon_color = (0.7, 0.5, 1, 1)  # ✅ Đổi cả màu ico
    def on_start(self):
        self.blink_image(3)  # Ảnh 1 nhấp nháy 3 lần, ảnh 2 vẫn giữ nguyên
   # def on_start(self):
    #    self.root.current = "welcome"

    def fade_in_image(self):
        """Hiệu ứng xuất hiện mượt mà trước khi nhấp nháy"""
        main_screen = self.root.get_screen("main")
        image = main_screen.ids.fade_image

        # Ảnh xuất hiện từ từ trong 2 giây
        anim = Animation(opacity=1, duration=2, t="out_quad")
        anim.bind(on_complete=lambda *_: self.blink_image(3))  # Sau đó mới nhấp nháy
        anim.start(image)

    def blink_image(self, times):
        """Hiệu ứng nhấp nháy chậm hơn cho ảnh 1"""
        main_screen = self.root.get_screen("main")
        image = main_screen.ids.fade_image

        if times > 0:
            anim = Animation(opacity=1, duration=1) + Animation(opacity=0.3, duration=1)  # Mỗi lần nhấp nháy mất 2s
            anim.bind(on_complete=lambda *_: self.blink_image(times - 1))
            anim.start(image)
        else:
            self.fade_out_images()  # Sau khi nhấp nháy xong, cả hai ảnh cùng mờ dần đi

    def fade_out_images(self):
        main_screen = self.root.get_screen("main")
        image1 = main_screen.ids.fade_image
        image2 = main_screen.ids.fade_image1

        anim = Animation(opacity=0, duration=1.5)  # Cả 2 ảnh mờ dần cùng lúc
        anim.bind(on_complete=lambda *_: setattr(self.root, "current", "welcome"))
        anim.start(image1)  # Corrected: 'start' instead of 'starat'
        anim.start(image2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = "English"  # Mặc định tiếng Anh
class MyApp(MDApp):
    def build(self):
        return Builder.load_file("home.kv")  # Load file .kv


if __name__ == "__main__":
    MainApp().run()