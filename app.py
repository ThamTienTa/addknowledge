from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "changeme-use-env-var")

OWNER_PASSWORD = os.environ.get("OWNER_PASSWORD", "unfail123")

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"pending": [], "approved": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def owner_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_owner"):
            return redirect(url_for("login", next=request.path))
        return f(*args, **kwargs)
    return decorated

@app.route("/", methods=["GET", "POST"])
def index():
    data = load_data()
    if request.method == "POST":
        text = request.form.get("training_text", "").strip()
        name = request.form.get("submitter_name", "").strip()
        if text:
            submission = {
                "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
                "text": text,
                "name": name if name else "An danh",
                "submitted_at": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            data["pending"].append(submission)
            save_data(data)
        return redirect(url_for("index"))
    return render_template("index.html",
                           pending=data["pending"],
                           approved=data["approved"],
                           is_owner=session.get("is_owner", False))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form.get("password") == OWNER_PASSWORD:
            session["is_owner"] = True
            next_url = request.args.get("next") or url_for("index")
            return redirect(next_url)
        error = "Sai mat khau!"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/approve/<submission_id>")
@owner_required
def approve(submission_id):
    data = load_data()
    for i, item in enumerate(data["pending"]):
        if item["id"] == submission_id:
            approved_item = data["pending"].pop(i)
            approved_item["approved_at"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            data["approved"].append(approved_item)
            break
    save_data(data)
    return redirect(url_for("index"))

@app.route("/delete/<submission_id>")
@owner_required
def delete(submission_id):
    data = load_data()
    data["pending"] = [item for item in data["pending"] if item["id"] != submission_id]
    save_data(data)
    return redirect(url_for("index"))

@app.route("/delete_approved/<submission_id>")
@owner_required
def delete_approved(submission_id):
    data = load_data()
    data["approved"] = [item for item in data["approved"] if item["id"] != submission_id]
    save_data(data)
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
