from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
import sys
import os
import re

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    daemon_threads = True
    allow_reuse_address = True

class RangeRequestHandler(SimpleHTTPRequestHandler):
    """
    This custom handler adds CORS headers and proper HTTP Range header support
    for partial content requests, which is essential for zarr chunk access.
    """
    def _init_(self, *args, **kwargs):
        # Serve files from the current working directory
        super()._init_(*args, directory='.', **kwargs)

    def do_OPTIONS(self):
        # Send a success response for the preflight request
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Range")
        self.end_headers()

    def do_GET(self):
        """Handle GET requests with Range header support"""
        path = self.translate_path(self.path)

        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(404, "File not found")
            return

        try:
            fs = os.fstat(f.fileno())
            file_len = fs.st_size

            # Check for Range header
            range_header = self.headers.get('Range')

            if range_header:
                # Parse the Range header (format: "bytes=start-end")
                match = re.match(r'bytes=(\d+)-(\d*)', range_header)
                if match:
                    start = int(match.group(1))
                    end = match.group(2)
                    end = int(end) if end else file_len - 1

                    # Validate range
                    if start >= file_len or start > end:
                        self.send_error(416, "Requested Range Not Satisfiable")
                        f.close()
                        return

                    # Clamp end to file length
                    end = min(end, file_len - 1)
                    content_len = end - start + 1

                    # Send partial content response
                    self.send_response(206, "Partial Content")
                    self.send_header("Content-Type", self.guess_type(path))
                    self.send_header("Content-Length", str(content_len))
                    self.send_header("Content-Range", f"bytes {start}-{end}/{file_len}")
                    self.send_header("Accept-Ranges", "bytes")
                    self.end_headers()

                    # Send the requested byte range
                    f.seek(start)
                    self.wfile.write(f.read(content_len))
                else:
                    # Invalid range format, return full content
                    self.send_full_content(f, file_len, path)
            else:
                # No Range header, return full content
                self.send_full_content(f, file_len, path)

        finally:
            f.close()

    def send_full_content(self, f, file_len, path):
        """Send the full file content"""
        self.send_response(200)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Length", str(file_len))
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()
        self.wfile.write(f.read())

    def end_headers(self):
        # Add the CORS header to all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5500
    server_address = ('', port)
    httpd = ThreadedHTTPServer(server_address, RangeRequestHandler)

    # Increase the listen backlog for better concurrent connection handling
    httpd.socket.listen(128)

    print(f"Starting multi-threaded zarr server with Range support on port {port}")
    print(f"Server supports concurrent connections and HTTP Range requests (backlog: 128)")
    httpd.serve_forever()
