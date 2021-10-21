from flask import Flask, jsonify, request
import xml.etree.ElementTree as ET
from dict2xml import dict2xml

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
@app.route('/Facturas', methods=['POST'])
def cargafacturas():

    global facturasArr

    entrada = request.data.decode('utf-8')

    xmlentrada = ET.fromstring(entrada)

    for dte in xmlentrada.findall('DTE'):
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

    contador_facturasrecibidas = 0
    contador_nitemimalo = 0
    contador_nitrecmalo = 0
    contador_ivamalo = 0
    contador_totalmalo = 0
    contador_refdoble = 0
    contador_factbuenas = 0
    contador_nitemisores = 0
    contador_nitreceptores = 0

    #Datos = []
    print(facturasArr)
    for factura in facturasArr:
        print(factura)
        contador_facturasrecibidas += 1

        contador_nitemisores = int(len(factura.getNitemisor()))
        contador_nitreceptores = int(len(factura.getNitreceptor()))

        if len(factura.getReferencia()) == len(set(factura.getReferencia())):
            contador_refdoble += 1
        else:
            contador_refdoble == 0

        if len(factura.getNitemisor()) == len(set(factura.getNitemisor())):
            contador_nitemisores += 1
        else:
            contador_nitemisores += 1

        if len(factura.getNitreceptor()) == len(set(factura.getNitreceptor())):
            contador_nitreceptores += 1
        else:
            contador_nitreceptores += 1

        if (float(factura.getTotal()) - (float(factura.getTotal()) * 0.88)) == factura.getIva():
            contador_ivamalo += 1
        else:
            contador_ivamalo += 0

    objeto = {
            'Facturas recibidas': contador_facturasrecibidas,
            'Referencia doble':contador_refdoble,
            'NitEmisor': contador_nitemisores,
            'NitReceptor': contador_nitreceptores,
            'IVA malo' : contador_ivamalo
        }


    #Datos.append(objeto)
    xmlsalida = dict2xml(objeto)
    return(xmlsalida)


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
