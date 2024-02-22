from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional

import click


@click.command()
@click.option('--port', '-p', default=8080, show_default=True,
              help='The port that echomirror will listen to')
@click.option('--status-code', '-s', default=200, show_default=True,
              help='The HTTP status code we will return')
@click.option('--text', default=None, type=str,
              help='Respond to requests with this text using the text/plain content-type')
@click.option('--json', default=None, type=str,
              help='Respond to requests with this JSON using the application/json content-type')
@click.option('--expose/--localhost-only', default=False, show_default=True, is_flag=True,
              help='Whether to expose this port to the outside network (i.e., host on 0.0.0.0), or only allow localhost '
                   'connections.')
def main(port, status_code: int, text: Optional[str], json: Optional[str], expose: bool) -> None:
    class MyServer(BaseHTTPRequestHandler):
        method: str = None

        def handle_request(self):
            self.send_response(status_code)
            if text:
                self.send_header("Content-type", "text/plain")
            elif json:
                self.send_header("Content-type", "application/json")

            self.end_headers()
            self.wfile.write(bytes(text or json or '', "utf-8"))

        def do_GET(self):
            self.method = 'GET'
            self.handle_request()

        def do_POST(self):
            self.method = 'POST'
            self.handle_request()

        def do_PUT(self):
            self.method = 'PUT'
            self.handle_request()

        def do_DELETE(self):
            self.method = 'DELETE'
            self.handle_request()

        def do_HEAD(self):
            self.method = 'HEAD'
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def do_OPTIONS(self):
            self.method = 'OPTIONS'
            self.send_response(204)
            self.send_header('Allow', 'GET, POST, PUT, DELETE, OPTIONS')
            self.end_headers()

        def log_request(self, format, *args):
            click.echo("")
            click.secho(f"{self.method} {self.path}", fg='green')
            for header_name in self.headers:
                for header_value in self.headers.get_all(header_name):
                    click.echo(f"    {header_name}: {header_value}")
            content_len = self.headers.get('Content-Length');
            if content_len:
                click.echo(self.rfile.read(int(content_len)).decode('utf-8'))

    if text and json:
        click.echo("--text and --json cannot be used at the same time.", err=True)
        return

    host = 'locahost' if expose else '0.0.0.0'

    server = HTTPServer((host, port), MyServer)

    try:
        click.secho(f"Serving on http://{host}:{port}", fg='cyan')
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
