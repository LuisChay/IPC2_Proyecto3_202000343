from flask import Flask, jsonify, request

from flask_cors import CORS
from Facturas import facturas


facturasArr = []

app = Flask(__name__)
CORS(app)

#--------------iniciales----------------
@app.route('/', methods=['GET'])
def rutaInicial():
    return("<h1>Inicio de flask</h1>")

@app.route('/', methods=['POST'])
def rutaPost():
    objeto = {"Mensaje":"Prueba en flask"}
    return(jsonify(objeto))










#--------------rutas especificas----------------

@app.route('/facturas', methods=['POST'])
def cargafacturas():
    return("<h1>Consulta de datos</h1>")



@app.route('/consultadatos', methods=['GET'])
def consultadedatos():
    return("<h1>Consulta de datos</h1>")

@app.route('/resumeniva', methods=['GET'])
def resumendeiva():
    return("<h1>Resumen de IVA</h1>")

@app.route('/resumenrango', methods=['GET'])
def resumenderango():
    return("<h1>Resumen de rango</h1>")

@app.route('/grafica', methods=['GET'])
def graficas():
    return("<h1>Grafica</h1>")

@app.route('/procesar', methods=['POST'])
def procesamiento():
    return("<h1>Procesar</h1>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
