from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import sys

class CORSRequestHandler(SimpleHTTPRequestHandler):
    """
    This custom handler adds the necessary CORS headers and, critically,
    responds correctly to OPTIONS preflight requests.
    """
    def do_OPTIONS(self):
        # Send a success response for the preflight request
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Range")
        self.end_headers()

    def end_headers(self):
        # Add the CORS header to all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5500
    # Use the test function with our corrected handler
    test(CORSRequestHandler, HTTPServer, port=port)