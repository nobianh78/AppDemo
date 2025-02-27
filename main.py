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
import sqlite3
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.label import MDLabel

# Load các file KV
Builder.load_file("myapp.kv")
Builder.load_file("login.kv")
Builder.load_file("signup.kv")
Builder.load_file("home.kv")
Builder.load_file("profile.kv")
Builder.load_file("welcome.kv")

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
    def check_internet(self):
        """Kiểm tra kết nối Internet trước khi cho phép đăng nhập"""
        url = "http://www.google.com"  # URL kiểm tra mạng

        def success_callback(req, result):
            # Nếu có mạng, chuyển sang màn hình khác
            self.manager.transition.direction = "left"
            self.manager.current = "home"

        def error_callback(req, error):
            # Nếu không có mạng, hiển thị thông báo lỗi
            self.show_no_internet_dialog()

        # Kiểm tra kết nối (timeout 3 giây)
        UrlRequest(url, on_success=success_callback, on_error=error_callback, timeout=3)

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
    def login(self):
        email = self.ids.email.text
        password = self.ids.password.text

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE email=? AND password=?", (email, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            role = result[0]
            if role == "admin":
                self.manager.current = "admin"
            else:
                self.manager.current = "home"
        else:
            self.show_popup("Error", "Invalid email or password!")

    def forgot_password(self):
        self.show_popup("Notice", "Please contact admin to reset your password!")

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
    popup = None

    def register(self):
        username = self.ids.full_name.text  # Sử dụng username thay vì full_name cho khớp với thiết kế
        email = self.ids.email.text
        password = self.ids.password.text

        if not email or not password or not username:
            self.show_popup("Error", "Please fill in all fields!")
            return

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                email TEXT UNIQUE,
                password TEXT,
                role TEXT DEFAULT 'user'
            )
        """)
        try:
            cursor.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, 'user')", (username, email, password))
            conn.commit()
            self.show_popup("Success", "Registration successful!")
            self.manager.current = "login"
        except sqlite3.IntegrityError:
            self.show_popup("Error", "Email already in use!")
        finally:
            conn.close()

    def goto_login(self):
        self.manager.current = "login"

    def show_popup(self, title, message):
        if not self.popup:
            close_button = MDFlatButton(text="Close", on_release=self.close_popup)
            self.popup = MDDialog(title=title, text=message, buttons=[close_button])
        self.popup.open()

    def close_popup(self, *args):
        if self.popup:
            self.popup.dismiss(force=True)
            self.popup = None

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
        return sm

   # def on_start(self):
    #    self.blink_image(3)  # Ảnh 1 nhấp nháy 3 lần, ảnh 2 vẫn giữ nguyên
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