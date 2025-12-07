import lwjgl
import pathlib
import CheckSpecialStr
import sys
import threading
import time
import os
import get_disk_info
import requests
import webbrowser
try:
    from flask import Flask, render_template, session, request, redirect, url_for, send_file, jsonify
    import getPwd
    import json
    import psutil
    import flask_limiter
    import toml
    from flask_socketio import SocketIO, emit
except ImportError as e:
    print(e)
    import installdep
    if installdep.install():
        lwjgl.logging.log("INFO", "Dependencies installed, please restart the application.")
    sys.exit(0)

app = Flask(__name__)
app.secret_key = getPwd.generate_random_password(length=10)
app.static_folder='/assets'

PANEL_CONFIG = toml.load("config.toml")
PANEL_PORT = PANEL_CONFIG['PANEL_PORT']
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

trust_session = {} # 存储信任的session字典
trust_socket =[] # 存储信任的socketio sid列表

limiter = flask_limiter.Limiter(
    app=app,
    key_func=flask_limiter.util.get_remote_address,
    default_limits=["30 per minute"]
)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("LoginSession", "") not in trust_session:
            return redirect(url_for("login_pages"))
        return f(*args, **kwargs)
    return decorated_function



@app.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login_pages():
    if session.get("LoginSession", "") in trust_session:
            return redirect(url_for("index_pages"))
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        with open("user.json", "r") as f:
            users = json.load(f)
        if username in users and getPwd.string_to_sha256(password) == users[username]["pwd"]:
            session_key = getPwd.generate_random_password(length=20)
            session["LoginSession"] = session_key
            trust_session[session_key] = {} # 添加信任session
            return redirect(url_for("index_pages",session_id=session))
        else:
            return "Incorrect password"
    else:
        return render_template("login.html")


@app.route("/")
@login_required
def index_pages():
    return render_template("index.html")

@app.route("/GetAssets/<type>")
@limiter.limit("200 per minute")
def get_assets(type):
    if CheckSpecialStr.CheckSpecialStr(type):
        return "Invalid asset type", 400
    with open("assets.json", "r") as f:
        assets = json.load(f)
    if type not in assets:
        return "404"
    assets_path = pathlib.Path("assets") / assets[type]["path"]
    if os.path.exists(assets_path):
        return send_file(assets_path)
    else:
        return "404"

# SocketIO 连接事件
@socketio.on('connect')
def handle_connect(data):
    lwjgl.logging.log("INFO", 'Client connected')
@socketio.on('disconnect')
def handle_disconnect():
    lwjgl.logging.log("INFO", 'Client disconnected')
    if request.sid in trust_socket:
        trust_socket.remove(request.sid)
        lwjgl.logging.log("INFO",f"Del trust socketio sid: {request.sid}")

@socketio.on("add_session")
def handle_add_session(data):
    lwjgl.logging.log("INFO", f"Adding trusted socket for session: {data}")
    if data in trust_session:
        if request.sid not in trust_socket:
            trust_socket.append(request.sid)
            lwjgl.logging.log("INFO", f"Trusted socket added: {request.sid}")
            socketio.emit("add_session_success",{"status":"ok"},to=request.sid)

def send_usage():
    while True:
        try:
            cpu_usage = psutil.cpu_percent(interval=1) # 这里包含1s延迟
            memory_usage = psutil.virtual_memory().percent
            
            for trust_user in trust_socket:
                socketio.emit("usage_update", {
                    "cpu": cpu_usage,
                    "mem": memory_usage
                },to=trust_user)
        except Exception as e:
            lwjgl.logging.log("ERROR", f"Error in send_usage: {e}")
            time.sleep(1)

def send_disk_usage():
    while True:
        try:
            disk_data = get_disk_info.get_mounted_disks()
            for trust_user in trust_socket:
                socketio.emit("disk_usage_update",disk_data,to=trust_user)
        except Exception as e:
            lwjgl.logging.log("ERROR", f"Error in send_disk_usage: {e}")
            time.sleep(60)
        time.sleep(1)

def open_browser():
    # 这里是浏览器启动进程
    Server_is_running = False
    while not Server_is_running:
        try:
            if requests.get(f"http://127.0.0.1:{PANEL_PORT}").status_code == 200:
                Server_is_running = True
                webbrowser.open(f"http://127.0.0.1:{PANEL_PORT}")
                break
        except requests.exceptions.ConnectionError:
            lwjgl.logging.log("INFO", "Waiting for server to start...")
        except webbrowser.Error as e:
            lwjgl.logging.log("ERROR", f"Error opening browser: {e}")
        time.sleep(2)
if __name__ == "__main__":
    usage_update_thread = threading.Thread(target=send_usage, daemon=True)
    usage_update_thread.start()
    disk_usage_thread = threading.Thread(target=send_disk_usage, daemon=True)
    disk_usage_thread.start()
    open_browser_thread = threading.Thread(target=open_browser, daemon=True)
    open_browser_thread.start()
    lwjgl.logging.log("INFO", "Starting server...")
    socketio.run(app, host="0.0.0.0", port=PANEL_PORT, debug=True)