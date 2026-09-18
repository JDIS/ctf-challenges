from flask import Flask, request, render_template_string, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "super_secret_session_key_ctf"

def init_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT);")
    cursor.execute("CREATE TABLE flags (flag TEXT);")
    cursor.execute("CREATE TABLE pirates (id INTEGER PRIMARY KEY, name TEXT, boat TEXT);")
    
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'sUp3r_s3cr3t_p4ssw0rd_987!')")
    cursor.execute("INSERT INTO users (username, password) VALUES ('guest', 'guest')")
    cursor.execute("INSERT INTO flags (flag) VALUES ('JDIS{s1mpl3_sql1_byp4ss_succ3ss}')")
    cursor.execute("INSERT INTO flags (flag) VALUES ('JDIS{un1onSql1nj3ction}')")
    
    cursor.execute("INSERT INTO pirates (name, boat) VALUES ('Barbe Rousse', 'Insubmersible ')")
    cursor.execute("INSERT INTO pirates (name, boat) VALUES ('Barbe Noire', 'Grand canot')")
    cursor.execute("INSERT INTO pirates (name, boat) VALUES ('Barbe Bleue', 'Le Codpère')")
    conn.commit()
    return conn

db = init_db()

BASE_STYLE = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Pirata+One&family=IM+Fell+English:ital@0;1&display=swap" rel="stylesheet">
<style>
    * { box-sizing: border-box; }
    body {
        font-family: 'IM Fell English', Georgia, serif;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        margin: 0;
        background-color: #0b0e14;
        background-image: 
            radial-gradient(circle at 50% 50%, rgba(20, 30, 48, 0.7) 0%, rgba(10, 14, 23, 0.95) 100%),
            repeating-linear-gradient(45deg, rgba(0, 0, 0, 0.15) 0px, rgba(0, 0, 0, 0.15) 2px, transparent 2px, transparent 6px);
        color: #2b1d0c;
        padding: 20px;
    }
    .card {
        background: #f4ecd8;
        background-image: radial-gradient(#dfcca6 10%, transparent 11%), radial-gradient(#e7d7b5 10%, transparent 11%);
        background-size: 24px 24px;
        background-position: 0 0, 12px 12px;
        padding: 2.5rem 2rem;
        border-radius: 6px;
        width: 440px;
        max-width: 95vw;
        border: 4px double #5a381b;
        box-shadow: 
            0 0 0 3px #2d1807,
            0 15px 35px rgba(0,0,0,0.7),
            inset 0 0 45px rgba(112, 66, 20, 0.25);
        position: relative;
    }
    .card::before {
        content: '☠';
        position: absolute;
        top: -24px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 28px;
        background: #2a1a0c;
        color: #d4af37;
        width: 46px;
        height: 46px;
        line-height: 44px;
        text-align: center;
        border-radius: 50%;
        border: 2px solid #8b5a2b;
        box-shadow: 0 4px 8px rgba(0,0,0,0.6);
    }
    h2 {
        font-family: 'Pirata One', cursive;
        font-size: 2.2rem;
        text-align: center;
        color: #3b220c;
        margin: 0.8rem 0 1.2rem;
        text-shadow: 1px 1px 0px rgba(255,255,255,0.4);
        letter-spacing: 1px;
    }
    label {
        display: block;
        font-weight: bold;
        font-size: 1.05rem;
        color: #49280d;
        margin-top: 8px;
    }
    input {
        width: 100%;
        padding: 10px 12px;
        margin: 6px 0 14px 0;
        background: #fff9ea;
        border: 2px solid #8b6845;
        border-radius: 4px;
        font-family: 'IM Fell English', Georgia, serif;
        font-size: 1rem;
        color: #2b1d0c;
        box-shadow: inset 1px 1px 4px rgba(0,0,0,0.15);
    }
    input:focus {
        outline: none;
        border-color: #d4af37;
        box-shadow: 0 0 6px rgba(212, 175, 55, 0.5), inset 1px 1px 4px rgba(0,0,0,0.15);
    }
    button {
        width: 100%;
        padding: 11px;
        margin-top: 6px;
        background: linear-gradient(180deg, #6c3b17 0%, #46250e 100%);
        color: #f7e7ce;
        border: 2px solid #2a1408;
        border-radius: 4px;
        font-family: 'Pirata One', cursive;
        font-size: 1.4rem;
        letter-spacing: 1px;
        cursor: pointer;
        text-shadow: 1px 1px 2px #000;
        box-shadow: 0 4px 6px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.2);
        transition: all 0.15s ease;
    }
    button:hover {
        background: linear-gradient(180deg, #81461b 0%, #582f12 100%);
        box-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    .nav {
        margin-bottom: 0.5rem;
        text-align: center;
        font-size: 1.05rem;
        border-bottom: 1px dashed #a78257;
        padding-bottom: 8px;
    }
    .nav a {
        margin: 0 8px;
        color: #7b2e00;
        text-decoration: none;
        font-weight: bold;
    }
    .nav a:hover {
        text-decoration: underline;
        color: #ab4407;
    }
    .msg {
        margin-top: 1.2rem;
        padding: 10px 14px;
        border-radius: 4px;
        font-size: 0.95rem;
        border: 1px solid transparent;
    }
    .success {
        background: #e2edd8;
        color: #27521c;
        border-color: #8da47f;
    }
    .fail {
        background: #f8dedb;
        color: #721c17;
        border-color: #bd7d76;
        margin-bottom: 1rem;
    }
    .results {
        margin-top: 1.2rem;
        list-style-type: none;
        padding: 0;
        border: 1px solid #c9af88;
        border-radius: 4px;
        background: rgba(255,255,255,0.3);
    }
    .results li {
        padding: 10px 12px;
        border-bottom: 1px dashed #d1b892;
    }
    .results li:last-child {
        border-bottom: none;
    }
    .result-title {
        font-weight: bold;
        font-size: 1.15rem;
        color: #3b220c;
    }
    .result-desc {
        font-size: 0.95rem;
        color: #654321;
        font-style: italic;
    }
    .query {
        margin-top: 1rem;
        padding: 6px;
        font-family: monospace;
        font-size: 0.8em;
        color: rgba(60, 40, 20, 0.45);
        word-break: break-all;
        background: rgba(0,0,0,0.03);
        border-radius: 3px;
    }
</style>
"""

LOGIN_TEMPLATE = BASE_STYLE + """
<div class="card">
    <div class="nav">
        <a href="/">Connexion</a>
        {% if session.get('user') == 'admin' %}
            | <a href="/search">Registre Secret</a>
            | <a href="/logout">Quitter le navire</a>
        {% elif session.get('user') %}
            | <a href="/logout">Quitter le navire</a>
        {% endif %}
    </div>
    <h2>Registre de la Flotte</h2>
    <form method="POST" action="/login">
        <label>Nom de pirate</label>
        <input type="text" name="username" required autocomplete="off">
        <label>Mot de passe secret</label>
        <input type="password" name="password">
        <button type="submit">Connexion</button>
    </form>
    {% if message %}
        <div class="msg {{ status }}">{{ message | safe }}</div>
    {% endif %}
</div>
"""

SEARCH_TEMPLATE = BASE_STYLE + """
<div class="card">
    <div class="nav">
        <a href="/">Repaire</a> | <a href="/logout"> Quitter le navire</a>
    </div>
    <h2>Registre des Corsaires ☠</h2>
    <form method="GET" action="/search">
        <input type="text" name="q" placeholder="Fouiller un pirate ou un navire..." value="{{ arg }}">
        <button type="submit">Recherche</button>
    </form>
    {% if results is not none %}
        <ul class="results">
            {% for item in results %}
                <li>
                    <div class="result-title">🏴‍☠️ {{ item[0] }}</div>
                    <div class="result-desc">Vaisseau de guerre : {{ item[1] }}</div>
                </li>
            {% else %}
                <li style="color: #7e6950; font-style: italic; text-align: center;">Aucun pirate repéré à l'horizon...</li>
            {% endfor %}
        </ul>
    {% endif %}
    {% if error %}
        <div class="msg fail">{{ error }}</div>
    {% endif %}
    {% if query %}
        <div class="query">{{ query }}</div>
    {% endif %}
</div>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(LOGIN_TEMPLATE)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

    cursor = db.cursor()
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        
        if user and user[1] == "admin":
            session["user"] = "admin"
            cursor.execute("SELECT flag FROM flags")
            flag = cursor.fetchone()[0]
            return render_template_string(
                LOGIN_TEMPLATE, 
                message=f"Bienvenue Capitaine admin! {flag} <br><br><a href='/search' style='color:#1b4d13;font-weight:bold;'>Consulter le registre secret &rarr;</a>", 
                status="success"
            )
        elif user:
            session["user"] = user[1]
            return render_template_string(
                LOGIN_TEMPLATE, 
                message=f"Bienvenue moussaillon {user[1]}! (Matelot ordinaire - Le registre est gardé sous clef par le Capitaine admin)", 
                status="success"
            )
        else:
            return render_template_string(
                LOGIN_TEMPLATE, 
                message="Mot de passe ou moussaillon introuvable !", 
                status="fail"
            )
    except sqlite3.OperationalError as e:
        return render_template_string(LOGIN_TEMPLATE, message=f"Database Error: {e}", status="fail")

@app.route("/search", methods=["GET"])
def search():
    if session.get("user") != "admin":
        return render_template_string(
            LOGIN_TEMPLATE, 
            message="403 Forbidden: Tu dois être Capitaine admin pour fouiller le registre secret.", 
            status="fail"
        ), 403

    search_query = request.args.get("q")
    if search_query is None:
        return render_template_string(SEARCH_TEMPLATE, results=None, query="")

    sql = f"SELECT name, boat FROM pirates WHERE name LIKE '%{search_query}%' OR boat LIKE '%{search_query}%'"
    
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return render_template_string(SEARCH_TEMPLATE, results=results, arg=search_query, error=None, query=sql)
    except sqlite3.OperationalError as e:
        return render_template_string(SEARCH_TEMPLATE, results=[], arg=search_query, error=f"Database Error: {e}", query=sql)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)