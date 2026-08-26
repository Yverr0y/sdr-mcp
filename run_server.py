"""PyInstaller entry point."""
import os
import sys

import _strptime  # noqa: F401

sys.path.insert(0, "src")

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from sdr_mcp.server import mcp

app = mcp.http_app(path="/")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:10890", "http://127.0.0.1:10890",
        "http://localhost:10891", "http://127.0.0.1:10891",
        "http://localhost:10892", "http://127.0.0.1:10892",
        "http://tauri.localhost", "https://tauri.localhost", "tauri://localhost",
    ],
    allow_origin_regex=r"https?://(?:[a-zA-Z0-9-]+\.ts\.net|.*?\.tail-[a-f0-9]+\.ts\.net|tauri\.localhost|localhost|127\.0\.0\.1|192\.168\.\d{1,3}\.\d{1,3}|10\.\d{1,3}\.\d{1,3}\.\d{1,3}|100\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?$|^tauri://localhost$",
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)
# backend.rs sets PORT=<BACKEND_PORT>; bind that so the webview health check passes.
port = int(os.environ.get("PORT") or (sys.argv[1] if len(sys.argv) > 1 else 10891))
uvicorn.run(app, host="127.0.0.1", port=port)
