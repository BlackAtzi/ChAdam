#!flask/bin/python
from app import app
import socket

host = socket.gethostbyname(socket.gethostname())
app.run(debug=True, host=host)
