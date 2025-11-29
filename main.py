import lwjgl
import pathlib
import CheckSpecialStr
import sys
import threading
try:
    from flask import Flask, render_template, session, request, redirect, url_for, send_file, jsonify
    import getPwd
    import json
    import psutil
    import flask_limiter
except ImportError as e:
    print(e)
    import installdep
    if installdep.install():
        lwjgl.logging.log("INFO", "Dependencies installed, please restart the application.")
    sys.exit(0)

app = Flask(__name__)
app.secret_key = getPwd.generate_random_password(length=10)
app.static_folder='/assets'

trust_session = []

limiter = flask_limiter.Limiter(
    app=app,
    key_func=flask_limiter.util.get_remote_address,
    default_limits=["30 per minute"] # 全局默认限制
)


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("LoginSession", "") not in trust_session:
            return redirect(url_for("login_pages"))
        return f(*args, **kwargs)
    # 返回包装后的函数，以便在视图中使用 login_required 装饰器
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login_pages():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        with open("user.json", "r") as f:
            users = json.load(f)
        if username in users and getPwd.string_to_sha256(password) == users[username]["pwd"]:
            session_key = getPwd.generate_random_password(length=20)
            session["LoginSession"] = session_key
            trust_session.append(session_key) # 添加信任session
            return redirect(url_for("index_pages"))
        else:
            return "Incorrect password"
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
    return send_file(pathlib.Path("assets") / assets[type]["path"])

@app.route("/usage")
@login_required
@limiter.limit("90 per minute")
def send_usage():
        cpu_usage = psutil.cpu_percent(interval=1)
        return jsonify({
                        'cpu': cpu_usage,
                        "mem": psutil.virtual_memory().percent
                        })

if __name__ == "__main__":
    app.run()