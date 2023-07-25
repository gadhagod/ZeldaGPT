from datetime import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO, send
from constants import embeddingCollection, questionCollection
from search import ask
from os import getenv

app = Flask(__name__)
app.config['SECRET_KEY'] = getenv("SECRET_KEY") or 'secret!'
socketio = SocketIO(app, async_handlers=True, cors_allowed_origins="*")

@app.route("/")
def main():
    return render_template("index.jinja")

@app.route("/about")
def about():
    return render_template(
        "about.jinja", 
        last_update=embeddingCollection.created_at
    )

@socketio.on("message")
def handle_message(question):
    send(ask(question))
    if questionCollection:
        questionCollection.add_doc({"question": question})


if __name__ == '__main__':
    socketio.run(app, debug=True)
