from flask import Flask, render_template
from flask_socketio import SocketIO, send
from search import ask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/")
def main():
    return render_template("index.jinja")

@socketio.on("message")
def handle_message(question):
    print('received question: ' + question)
    send(ask(question))


if __name__ == '__main__':
    socketio.run(app, debug=True)
