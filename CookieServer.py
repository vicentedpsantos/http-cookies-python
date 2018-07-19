#!/usr/bin/env python3
#
# An HTTP server that remembers your name (in a cookie)
#
# In this exercise, you'll create and read a cookie to remember the name
# that the user submits in a form.  There are two things for you to do here:
#
# 1. Set the relevant fields of the cookie:  its value, domain, and max-age.
#
# 2. Read the cookie value into a variable.

from http.server import HTTPServer, BaseHTTPRequestHandler
from http import cookies
from urllib.parse import parse_qs
from html import escape as html_escape
from http.cookies import SimpleCookie, CookieError

form = '''<!DOCTYPE html>
<title>I Remember You</title>
<p>
{}
<p>
<form method="POST">
<label>What's your name again?
<input type="text" name="yourname">
</label>
<br>
<button type="submit">Tell me!</button>
</form>
'''


class NameHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-length', 0))

        data = self.rfile.read(length).decode()
        yourname = parse_qs(data)["yourname"][0]

        c = cookies.SimpleCookie()
        c['yourname'] = yourname
        c['yourname']['domain'] = 'localhost'
        c['yourname']['max-age'] = 60

        self.send_response(303)  # redirect via GET
        self.send_header('Location', '/')
        self.send_header('Set-Cookie', c['yourname'].OutputString())
        self.end_headers()

    def do_GET(self):
        message = "I don't know you yet!"

        if 'cookie' in self.headers:
            try:
                c = cookies.SimpleCookie(self.headers['cookie'])
                name = c['yourname'].value
                message = "Hey there, " + html_escape(name)
            except (KeyError, cookies.CookieError) as e:
                message = "I'm not sure who you are!"
                print(e)

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        mesg = form.format(message)
        self.wfile.write(mesg.encode())


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, NameHandler)
    httpd.serve_forever()
