from flask import Flask, render_template
from src.flask.database import Database
from gevent.pywsgi import WSGIServer


app = Flask(__name__)
database = Database("db.sqlite")
database.connect()

@app.route("/")
def main():
    logs = database.execute_sql("""
        SELECT r.contents
        FROM record r
        ORDER BY r.id DESC
        LIMIT 500
    """)
    return render_template("main.html.jinja", logs=logs)

if __name__ == "__main__":
    server = WSGIServer(("0.0.0.0", 80), app)
    server.serve_forever()
