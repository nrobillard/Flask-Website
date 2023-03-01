from flask import Flask
from Money_Manager import create

app = create()

if __name__ == '__main__':
    app.run(debug=True)

