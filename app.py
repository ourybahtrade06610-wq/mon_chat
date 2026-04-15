from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, send
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

FILE = "messages.json"

# charger messages existants
if os.path.exists(FILE):
    with open(FILE, "r") as f:
        messages = json.load(f)
else:
    messages = []

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Chat Persistant</title>
</head>

<body style="background:#0f172a; color:white; font-family:Arial; text-align:center;">

<h1>💬 Chat Sauvegardé</h1>

<input id="name" placeholder="Ton nom"
style="padding:10px; width:120px;">

<div id="messages" style="width:60%; margin:auto; margin-top:20px;"></div>

<input id="msg" placeholder="Message..."
style="padding:10px; width:200px;">
<button onclick="sendMessage()">Envoyer</button>

<script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
<script>
var socket = io();

function sendMessage(){
    var name = document.getElementById("name").value;
    var msg = document.getElementById("msg").value;

    if(name && msg){
        socket.send(name + " : " + msg);
        document.getElementById("msg").value = "";
    }
}

socket.on("message", function(msg){
    var div = document.createElement("div");
    div.style = "background:#1e3a8a; margin:10px; padding:10px; border-radius:10px;";
    div.innerHTML = msg;
    document.getElementById("messages").appendChild(div);
});
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html)

@socketio.on('message')
def handleMessage(msg):
    messages.append(msg)

    # sauvegarde dans fichier
    with open(FILE, "w") as f:
        json.dump(messages, f)

    send(msg, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)