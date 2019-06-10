from flask import Flask, request, render_template

from session import SessionManager

app = Flask(__name__)

sm = SessionManager()


@app.route("/")
def index():
    session_id = sm.create_session()
    return render_template("index.html", session_id=session_id)


@app.route("/api/evaluate", methods=["POST"])
def evaluate():
    j = request.get_json()
    s_id = j["session_id"]
    new_input = j["input"]
    output = sm.eval(s_id, new_input)
    return output


if __name__ == "__main__":
    app.run(debug=True)
