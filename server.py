import http.server
import socketserver
import json
import os

PORT = 8080
DB_FILE = "consultations.json"

class SPACEHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/submit-consultation":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode('utf-8'))

                records = []
                if os.path.exists(DB_FILE):
                    with open(DB_FILE, "r") as f:
                        try:
                            records = json.load(f)
                        except json.JSONDecodeError:
                            records = []

                records.append(data)

                with open(DB_FILE, "w") as f:
                    json.dump(records, f, indent=4)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                response = {"status": "success", "message": "Consultation protocol successfully logged."}
                self.wfile.write(json.dumps(response).encode('utf-8'))

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                error_response = {"status": "error", "message": str(e)}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        else:
            super().do_POST()

print(f"[S.P.A.C.E.] Operational Node active on port {PORT}...")
with socketserver.TCPServer(("", PORT), SPACEHandler) as httpd:
    httpd.serve_forever()
