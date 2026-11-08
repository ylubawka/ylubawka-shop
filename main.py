"""
Локальный просмотр сайта Улыбашка.

Запуск:  python main.py
Откроется http://localhost:8000  (остановить: Ctrl+C)
На хостинг этот файл заливать не нужно.
"""

import http.server
import socketserver
import webbrowser
import os

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            path = os.path.join(DIRECTORY, "404.html")
            if os.path.exists(path):
                with open(path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b"<h1>404</h1>")
            return
        super().send_error(code, message, explain)


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"Сайт запущен: {url}")
        try:
            webbrowser.open(url)
        except Exception:
            pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nСервер остановлен.")
