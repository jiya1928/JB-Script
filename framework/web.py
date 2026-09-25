import json
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler


class Response:

    def json(self, data, status=200, headers=None):
        return {
            "__jb_response__": True,
            "body": json.dumps(data),
            "status": status,
            "content_type": "application/json; charset=utf-8",
            "headers": headers or {}
        }

    def text(self, data, status=200, headers=None):
        return {
            "__jb_response__": True,
            "body": str(data),
            "status": status,
            "content_type": "text/plain; charset=utf-8",
            "headers": headers or {}
        }


class App:

    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.routes = []
        self.response = Response()

        from .db import db
        self.db = db()

    def get(self, path, handler):
        self.routes.append(("GET", path, handler))

    def post(self, path, handler):
        self.routes.append(("POST", path, handler))

    def put(self, path, handler):
        self.routes.append(("PUT", path, handler))

    def delete(self, path, handler):
        self.routes.append(("DELETE", path, handler))

    def find_route(self, method, path):
        for route_method, route_path, handler in self.routes:

            if route_method != method:
                continue

            route_parts = [
                part for part in route_path.split("/")
                if part
            ]

            path_parts = [
                part for part in path.split("/")
                if part
            ]

            if len(route_parts) != len(path_parts):
                continue

            params = {}
            matched = True

            for route_part, path_part in zip(
                route_parts,
                path_parts
            ):

                if route_part.startswith(":"):
                    param_name = route_part[1:]
                    params[param_name] = path_part

                elif route_part != path_part:
                    matched = False
                    break

            if matched:
                return handler, params

        return None, {}

    def run(self, port=8080):

        app = self

        class Handler(BaseHTTPRequestHandler):

            def handle_request(self, method):

                path = self.path.split("?", 1)[0]

                print(f"[JB DEBUG] {method}: {path}")

                content_type = self.headers.get(
                    "Content-Type",
                    ""
                )

                content_length = self.headers.get(
                    "Content-Length",
                    "0"
                )

                try:
                    content_length = int(content_length)
                except ValueError:
                    content_length = 0

                body = ""

                if content_length > 0:
                    raw_body = self.rfile.read(content_length)

                    print(
                        f"[JB DEBUG] Raw bytes: {raw_body}"
                    )

                    body = raw_body.decode(
                        "utf-8",
                        errors="replace"
                    )

                    print(
                        f"[JB DEBUG] Body: {body!r}"
                    )

                request_data = {
                    "method": method,
                    "path": path,
                    "body": body,
                    "headers": dict(self.headers),
                    "params": {},
                    "json": {}
                }

                if "application/json" in content_type:
                    try:
                        request_data["json"] = json.loads(body)

                        print(
                            f"[JB DEBUG] JSON: "
                            f"{request_data['json']}"
                        )

                    except Exception as error:
                        print(
                            f"[JB DEBUG] JSON error: {error}"
                        )

                        self.send_response(400)
                        self.send_header(
                            "Content-Type",
                            "application/json; charset=utf-8"
                        )
                        self.end_headers()

                        self.wfile.write(
                            json.dumps({
                                "error": "Invalid JSON"
                            }).encode("utf-8")
                        )

                        return

                handler, params = app.find_route(
                    method,
                    path
                )

                if handler is None:
                    self.send_response(404)
                    self.send_header(
                        "Content-Type",
                        "application/json; charset=utf-8"
                    )
                    self.end_headers()

                    self.wfile.write(
                        json.dumps({
                            "error": "Route not found"
                        }).encode("utf-8")
                    )

                    return

                request_data["params"] = params

                try:
                    from framework.request import Request

                    request = Request(
                        request_data,
                        app.response
                    )

                    print(
                        "[JB DEBUG] Calling JB handler"
                    )

                    result = app.interpreter.call_function(
                        handler,
                        [request]
                    )

                    print(
                        f"[JB DEBUG] Result: {result}"
                    )

                    status = 200
                    response_headers = {}
                    response_content_type = (
                        "text/plain; charset=utf-8"
                    )

                    if (
                        isinstance(result, dict)
                        and result.get("__jb_response__")
                    ):
                        response_body = result.get(
                            "body",
                            ""
                        )

                        status = result.get(
                            "status",
                            200
                        )

                        response_headers = result.get(
                            "headers",
                            {}
                        )

                        response_content_type = result.get(
                            "content_type",
                            "text/plain; charset=utf-8"
                        )

                    elif isinstance(result, (dict, list)):
                        response_body = json.dumps(result)
                        response_content_type = (
                            "application/json; charset=utf-8"
                        )

                    else:
                        response_body = str(result)

                    response_bytes = response_body.encode(
                        "utf-8"
                    )

                    self.send_response(status)

                    self.send_header(
                        "Content-Type",
                        response_content_type
                    )

                    self.send_header(
                        "Content-Length",
                        str(len(response_bytes))
                    )

                    for key, value in response_headers.items():
                        self.send_header(
                            str(key),
                            str(value)
                        )

                    self.end_headers()

                    self.wfile.write(response_bytes)

                except Exception as error:

                    print(
                        f"[JB ERROR] {error}"
                    )

                    self.send_response(500)

                    self.send_header(
                        "Content-Type",
                        "application/json; charset=utf-8"
                    )

                    self.end_headers()

                    self.wfile.write(
                        json.dumps({
                            "error": str(error)
                        }).encode("utf-8")
                    )

            def do_GET(self):
                self.handle_request("GET")

            def do_POST(self):
                self.handle_request("POST")

            def do_PUT(self):
                self.handle_request("PUT")

            def do_DELETE(self):
                self.handle_request("DELETE")

        server = ThreadingHTTPServer(
            ("localhost", port),
            Handler
        )

        print(
            f"JB server running at "
            f"http://localhost:{port}"
        )

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nJB server stopped.")
        finally:
            server.server_close()


def web(interpreter):
    return App(interpreter)