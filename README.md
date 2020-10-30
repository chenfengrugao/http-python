
# http-python

## description

This is a simple http server based on http.server.

- support static resouces, such as html, css, js, ico, jpg, png, etc.
- support python backend program language
- support GET/POST
- support json

## start http server

Start http server: `python3 startserver.py`, the default port is `8006`.

## Demo page

The default page is `index.html`, and visit it by `http://127.0.0.1:8006/index.html` or `http://your-ip:8006/index.html`.

In this demo page, we use jquery `$.get()` to load string from python and json data from sqlite3 database.

## Note

Only test on RHEL6.8, Centos8.2
