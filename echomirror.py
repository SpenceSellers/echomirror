from http.server import BaseHTTPRequestHandler, HTTPServer

import click




@click.command()
@click.option('--port', '-p', default=8080, help='The port that echomirror will listen to', show_default=True)
@click.option('--status-code', '-s', default=200, help='The HTTP status code we will return', show_default=True)
@click.option('--text', default=None, type=str, help='Respond to requests with this text using the text/plain content-type')
@click.option('--json', default=None, type=str, help='Respond to requests with this JSON using the application/json content-type')
def main(port, status_code, text, json):
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
            pass

    if text and json:
        click.echo("--text and --json cannot be used at the same time.", err=True)
        return

    server = HTTPServer(("localhost", port), MyServer)

    try:
        print(f"Serving on http://localhost:{port}")
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()