from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
from jinja2 import Environment, PackageLoader, select_autoescape
from models import Author, App, User, Currency, UserCurrency
from utils.currencies_api import get_currencies
import json
import traceback

HOST = "127.0.0.1"
PORT = 8000

env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

template_index = env.get_template("index.html")
template_users = env.get_template("users.html")
template_user = env.get_template("user.html")
template_currencies = env.get_template("currencies.html")

main_author = Author(name="Сукачева Мария", group="P4150")
app_info = App(name="CurrenciesListApp", version="1.0", author=main_author)

users = [User(1, "Alice"), User(2, "Bob")]
user_currencies = [] 

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            path = parsed.path
            qs = parse_qs(parsed.query)
            if path == "/":
                self.handle_index()
            elif path == "/author":
                self.handle_author()
            elif path == "/users":
                self.handle_users()
            elif path == "/user":
                self.handle_user(qs)
            elif path == "/currencies":
                self.handle_currencies(qs)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Not found")
        except Exception:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Server error\n")
            tb = traceback.format_exc()
            self.wfile.write(tb.encode("utf8"))

    def send_html(self, content: str):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def handle_index(self):
        html = template_index.render(app=app_info, author=main_author)
        self.send_html(html)

    def handle_author(self):
        html = template_index.render(app=app_info, author=main_author)
        self.send_html(html)

    def handle_users(self):
        html = template_users.render(users=users)
        self.send_html(html)

    def handle_user(self, qs):
        # expecting ?id=1
        uid = None
        if "id" in qs:
            try:
                uid = int(qs["id"][0])
            except Exception:
                uid = None
        user = next((u for u in users if u.id == uid), None)
        if not user:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"User not found")
            return
        # collect user's subscriptions
        subs = [uc.currency for uc in user_currencies if uc.user.id == user.id]
        html = template_user.render(user=user, subscriptions=subs)
        self.send_html(html)

    def handle_currencies(self, qs):
        # optional ?update=true
        update = ("update" in qs and qs["update"][0].lower() in ("1", "true", "yes"))
        # fetch currencies (on demand)
        currencies = get_currencies()
        # Optionally convert Currency objects to dicts for template
        html = template_currencies.render(currencies=currencies)
        self.send_html(html)


def run():
    server = HTTPServer((HOST, PORT), MyHandler)
    print(f"Server running http://{HOST}:{PORT}/")
    server.serve_forever()


if __name__ == "__main__":
    run()
