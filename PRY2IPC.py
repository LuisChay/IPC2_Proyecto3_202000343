from flask import Flask, jsonify, request

from flask_cors import CORS



app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def rutaInicial():
    return("<h1>Inicio de flask</h1>")



@app.route('/', methods=['POST'])
def rutaPost():
    objeto = {"Mensaje":"Prueba en flask"}
    return(jsonify(objeto))



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
