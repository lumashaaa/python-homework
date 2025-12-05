from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, PackageLoader, select_autoescape

from models import Author, App, User, UserCurrency
from controllers.currency_controller import CurrencyController

HOST = "127.0.0.1"
PORT = 8000

author = Author("Сукачева Мария", "P4150")
app_info = App("Currencies Manager", "2.0", author)

users = [
    User(1, "Alice"),
    User(2, "Bob"),
    User(3, "Charlie")
]
user_currencies: list[UserCurrency] = []

env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)
template_index = env.get_template("index.html")

currency_ctrl = CurrencyController()

# === Обработчик запросов ===
class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path in ("/", "/index"):
            self.send_html(template_index.render(app=app_info, author=author))

        elif path == "/users":
            html = env.get_template("users.html").render(users=users)
            self.send_html(html)

        elif path == "/user":
            uid = qs.get("id", [None])[0]
            if not uid or not uid.isdigit():
                self.send_error(400, "Нужен параметр ?id=число")
                return
            user = next((u for u in users if u.id == int(uid)), None)
            if not user:
                self.send_error(404, "Пользователь не найден")
                return
            subs = [uc.currency for uc in user_currencies if uc.user.id == user.id]
            html = env.get_template("user.html").render(user=user, subscriptions=subs)
            self.send_html(html)

        elif path == "/currencies":
            message = None
            if qs.get("refresh"):
                try:
                    currency_ctrl.refresh_from_cbr()
                    message = "Курсы успешно обновлены из ЦБ!"
                except Exception as e:
                    message = f"Ошибка обновления: {e}"

            currencies = currency_ctrl.list()
            html = env.get_template("currencies.html").render(
                currencies=currencies,
                message=message
            )
            self.send_html(html)

        elif path.startswith("/delete/"):
            code = path.split("/")[-1]
            currency_ctrl.delete(code)
            self.send_response(303)
            self.send_header("Location", "/currencies")
            self.end_headers()
            return

        else:
            self.send_error(404, "Страница не найдена")

    # метод для отправки HTML
    def send_html(self, content: str):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

# === Запуск сервера ===
if __name__ == "__main__":
    print("Сервер запущен!")
    print("Открой в браузере → http://localhost:8000")
    print("Остановить → Ctrl + C")
    server = HTTPServer((HOST, PORT), MyHandler)
    server.serve_forever()
