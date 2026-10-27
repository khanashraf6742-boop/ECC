#!/usr/bin/env python3
"""Serve the standalone course with byte-range support for video seeking.

Usage: python3 serve_course.py [port]
Only the Batch 01 directory is served. The script uses Python's standard
library and listens on 0.0.0.0 for Arena's preview proxy.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent


class CourseHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.remaining = None
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes')
        super().end_headers()

    def send_head(self):
        self.remaining = None
        if urlsplit(self.path).path == '/':
            self.send_response(302)
            self.send_header('Location', '/Batch-01-Guide.html')
            self.send_header('Content-Length', '0')
            self.end_headers()
            return None
        range_header = self.headers.get('Range')
        path = self.translate_path(self.path)
        if not range_header or not os.path.isfile(path):
            return super().send_head()
        match = re.fullmatch(r'bytes=(\d*)-(\d*)', range_header.strip())
        size = os.path.getsize(path)
        if not match or size == 0 or not (match.group(1) or match.group(2)):
            self.send_response(416)
            self.send_header('Content-Range', f'bytes */{size}')
            self.send_header('Content-Length', '0')
            self.end_headers()
            return None
        first, last = match.groups()
        if first:
            start = int(first)
            end = min(int(last), size - 1) if last else size - 1
        else:
            suffix = int(last)
            start, end = max(size - suffix, 0), size - 1
        if start >= size or end < start:
            self.send_response(416)
            self.send_header('Content-Range', f'bytes */{size}')
            self.send_header('Content-Length', '0')
            self.end_headers()
            return None
        try:
            opened = open(path, 'rb')
        except OSError:
            self.send_error(404, 'File not found')
            return None
        opened.seek(start)
        self.remaining = end - start + 1
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(self.remaining))
        self.send_header('Last-Modified', self.date_time_string(os.path.getmtime(path)))
        self.end_headers()
        return opened

    def copyfile(self, source, outputfile):
        if self.remaining is None:
            return super().copyfile(source, outputfile)
        while self.remaining > 0:
            chunk = source.read(min(64 * 1024, self.remaining))
            if not chunk:
                break
            outputfile.write(chunk)
            self.remaining -= len(chunk)


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 4173
    print(f'Serving TA Batch 1 on port {port}', flush=True)
    ThreadingHTTPServer(('0.0.0.0', port), CourseHandler).serve_forever()
