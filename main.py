from flask import Flask, render_template, session, request, redirect, url_for, send_file
import getPwd
import json
import CheckSpecialStr

app = Flask(__name__)
app.secret_key = getPwd.generate_random_password(length=10)
app.static_folder='/assets'
trust_session = []

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
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/")
@login_required
def index_pages():
    return render_template("index.html")

@app.route("/GetAssets/<type>")
@login_required
def get_assets(type):
    if CheckSpecialStr.CheckSpecialStr(type):
        return "Invalid asset type", 400
    with open("assets/assets.json", "r") as f:
        assets = json.load(f)
    return send_file(assets[type]["path"])
if __name__ == "__main__":
    app.run()