from functools import partial

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
from urllib3.util import url
import requests

# Load các file KV
Builder.load_file("myapp.kv")
Builder.load_file("login.kv")
Builder.load_file("signup.kv")
Builder.load_file("home.kv")
Builder.load_file("profile.kv")
Builder.load_file("welcome.kv")
import sqlite3

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
from database import Database

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

        if not user:
            self.show_popup("Lỗi", "Sai email hoặc mật khẩu!")  # Hiển thị lỗi
            return  # Không chuyển màn hình nếu thông tin sai

        # Kiểm tra kết quả trả về
        if not self.check_internet():  # Gọi hàm kiểm tra Internet và thông báo lỗi nếu không có mạng
            self.show_popup("Lỗi", "Không có kết nối mạng! Vui lòng kiểm tra lại.")
            return
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
        """Kiểm tra kết nối Internet bằng cách gửi yêu cầu ping tới một trang web đáng tin cậy."""
        try:
            requests.get("https://www.google.com", timeout=5)  # Test kết nối với Google
            return True  # Có mạng
        except requests.exceptions.RequestException:
            return False  # Không có mạng


class MyApp(MDApp):
        def build(self):
            return Builder.load_file("home.kv")  # Load file .kv

        def change_tab_color(self, tab):
            """Hàm đổi màu khi bấm vào tab"""
            tab.theme_text_color = "Custom"  # Cho phép thay đổi màu chữ
            tab.text_color = (0.7, 0.5, 1, 1)  # Màu tím pastel
            tab.icon_color = (0.7, 0.5, 1, 1)  # ✅ Đổi cả màu icon

        def check_internet(self):
            """Check if the device is connected to the internet."""
            try:
                # Test accessing a reliable site
                response = requests.get('https://www.google.com', timeout=5)
                if response.status_code == 200:
                    return True  # Internet is available
            except requests.exceptions.ConnectionError:
                pass
            except requests.exceptions.Timeout:
                pass
            # No internet connection
            self.show_no_internet_dialog()
            return False

        def show_no_internet_dialog(self):
            """Display a dialog if there is no internet connection."""
            if not hasattr(self, 'dialog'):
                print("Creating no internet connection dialog...")
                self.dialog = self.create_dialog(
                    title="No Internet Connection",
                    message="Please check your network and try again.",
                    buttons=["OK"]
                )
            self.dialog.open()

        def create_dialog(self, title, message, buttons):
            # Placeholder for dialog creation logic
            print(f"Dialog: {title}\n{message}\nButtons: {buttons}")
            return self  # Return a mock dialog object for demonstration purposes

        def open(self):
            # Mock success method for dialog
            print("Internet connection error dialog displayed.")

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
        def build(self):
            return Builder.load_file("home.kv")  # Load file .kv

        def change_tab_color(self, tab):
            """Hàm đổi màu khi bấm vào tab"""
            tab.theme_text_color = "Custom"  # Cho phép thay đổi màu chữ
            tab.text_color = (0.7, 0.5, 1, 1)  # Màu tím pastel
            tab.icon_color = (0.7, 0.5, 1, 1)  # ✅ Đổi cả màu icon

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
        return sm

    def on_start(self):
        self.blink_image(3)  # Ảnh 1 nhấp nháy 3 lần, ảnh 2 vẫn giữ nguyên
    def on_start(self):
        self.root.current = "welcome"

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
        anim.start(image1)
        anim.start(image2)

if __name__ == "__main__":
    MainApp().run()