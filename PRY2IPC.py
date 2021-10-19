from flask import Flask, jsonify, request
import xml.etree.ElementTree as ET

from flask_cors import CORS
from Facturas import Facturas


facturasArr = []

app = Flask(__name__)
CORS(app)

#--------------iniciales------------------------
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

    global facturasArr



    xmlentrada = ET.parse(archivoinput)
    raizxml = xmlentrada.getroot()

    for dte in raizxml.find('DTE'):
        tiempo = dte.find('TIEMPO').text
        referencia = dte.find('REFERENCIA').text
        nitemi = dte.find('NIT_EMISOR').text
        nitrec = dte.find('NIT_RECEPTOR').text
        valor = dte.find('VALOR').text
        iva = dte.find('IVA').text
        total = dte.find('TOTAL').text
        nuevo = Facturas(tiempo,referencia,nitemi,nitrec,valor,iva,total)

    facturasArr.append(nuevo)


    return jsonify({'Mensaje':'Se agregaron las facturas exitosamente',})

# METODO - OBTENER TODOS PPACIENTES
@app.route('/Facturas', methods=['GET'])
def getFacturas():

    global facturasArr

    Datos = []

    for factura in facturasArr:

        objeto = {
            'Tiempo': factura.getTiempo(),
            'Referencia': factura.getReferencia(),
            'NitEmisor': factura.getNitemisor(),
            'NitReceptor': factura.getNitreceptor(),
            'Valor': factura.getValor(),
            'IVA': factura.getIva(),
            'Total': factura.getTotal(),
        }

        Datos.append(objeto)

    return(jsonify(Datos))


# METODO - OBTENER UN DATO PACIENTE ESPECIFICO
@app.route('/Pacientes/<string:nombrepac>', methods=['GET'])
def ObtenerPacientes(nombrepac):

    global PacientesArr

    for paciente in PacientesArr:

        if paciente.getUsuariopac() == nombrepac:
            objeto = {
            'Nombre': paciente.getNombrepac(),
            'Apellido': paciente.getApellidopac(),
            'Fecha': paciente.getFechapac(),
            'Sexo': paciente.getSexopac(),
            'Usuario': paciente.getUsuariopac(),
            'Contrasena': paciente.getContrapac(),
            'Telefono': paciente.getTelefonopac(),
            }

            return(jsonify(objeto))

    salida = { "Mensaje": "No existe el paciente con ese nombre"}

    return(jsonify(salida))

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
