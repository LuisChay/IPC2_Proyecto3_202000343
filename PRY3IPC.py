from flask import Flask, jsonify, request
import xml.etree.ElementTree as ET
from dict2xml import dict2xml
import collections
from flask_cors import CORS
from Facturas import Facturas
import re



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
        nuevo = Facturas(tiempo,referencia,nitemi,nitrec,valor,iva,total, False)

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
    contador_facturasmalas = 0
    tiempo1 = ""
    contadorfecha = 1
    coni =  0

    fechasREvacia = []
    fechasREllena = []

    for factura in facturasArr:

        fechasREvacia.append(bytes(factura.getTiempo()))

        print(fechasREvacia)
        #patron = r'([0-9]{2}\/[0-9]{2}\/[0-9]{4})'
        #regFecha = re.search(patron, fechasREvacia)

        regFecha = re.findall(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", fechasREvacia)
        fechasREllena.append(regFecha)
        print(fechasREllena)





        if factura.getTiempo() == tiempo1:
            contadorfecha += 1
            coni += 1
            tiempo1 = factura.getTiempo()
            print("contador ")
            print(contadorfecha)
            print(tiempo1)
        else:
            coni += 1
            contadorfecha = 1
            tiempo1 = factura.getTiempo()



        contador_facturasrecibidas += 1
        #IVA EMISOR MALO
        auxMulti = []
        nit_emisor = factura.getNitemisor()
        nit_emisor = nit_emisor.replace(' ', '')
        posicion = len(nit_emisor)

        for x in range(len(nit_emisor) - 1):
            auxMulti.append(posicion * int(nit_emisor[x]))
            posicion = posicion - 1

        sumas = 0
        for y in auxMulti:
            sumas += y

        modulo11 = sumas % 11

        resta = 11 - modulo11

        final = resta % 11

        if final == 10:
            if nit_emisor[-1].lower() != "k":
                contador_nitemimalo += 1
                factura.setEstadoMalo(True)
        elif nit_emisor[-1] != str(final):
            contador_nitemimalo += 1
            factura.setEstadoMalo(True)


    #IVA NitReceptor MALO
    contador_facturasrecibidas += 1
    auxMulti1 = []
    nit_receptor = factura.getNitreceptor()
    nit_receptor = nit_receptor.replace(' ', '')
    posicion1 = len(nit_receptor)

    for x in range(len(nit_receptor) - 1):
        auxMulti1.append(posicion1 * int(nit_receptor[x]))
        posicion1 = posicion1 - 1

    sumas1 = 0
    for y in auxMulti1:
        sumas1 += y

    modulo111 = sumas1 % 11

    resta1 = 11 - modulo111

    final1 = resta1 % 11

    if final1 == 10:
        if nit_receptor[-1].lower() != "k":
            contador_nitrecmalo += 1
            factura.setEstadoMalo(True)
    elif nit_receptor[-1] != str(final1):
        contador_nitrecmalo += 1
        factura.setEstadoMalo(True)

    # referencias DOBLES
    referencias = []
    for factura in facturasArr:
        referencias.append(factura.getReferencia())

    repetidos = []

    for ref in referencias:
        if referencias.count(ref) >= 2:
            c = 0
            for rep in repetidos:
                if rep == ref:
                    c += 1
            if c == 0:
                repetidos.append(ref)

    contador_refdoble += len(repetidos)

    for y in repetidos:
        for factura  in facturasArr:
            if factura.getReferencia() == y:
                factura.setEstadoMalo(True)

    # NIT EMISORES CONTADOR

    emisores = []
    for factura in facturasArr:
        if emisores.count(factura.getNitemisor()) == 0:
            emisores.append(factura.getNitemisor())

    contador_nitemisores += len(emisores)

    # NIT RECEPTOR CONTADOR

    receptores = []
    for factura in facturasArr:
        if receptores.count(factura.getNitreceptor()) == 0:
            receptores.append(factura.getNitreceptor())

    contador_nitreceptores += len(receptores)

    for factura in facturasArr:

        #IIVA MALO
        operacion = ( float(factura.getValor() ) - ( float(factura.getValor()) * 0.88 ) )
        ivax = float(factura.getIva())
        aprox = round(ivax, 2)

        if aprox != operacion:
            factura.setEstadoMalo(True)
            contador_ivamalo += 1
            contador_facturasmalas += 1


        #total MALO
        operaciontotal = ( float(factura.getValor() ) + ( float(factura.getIva())) )
        totalx = float(factura.getTotal())
        aprox1 = round(totalx, 2)

        if aprox1 != operaciontotal:
            factura.setEstadoMalo(True)
            contador_totalmalo += 1
            contador_facturasmalas += 1


    for factura in facturasArr:
        if factura.getEstadoMalo() == False:
            contador_factbuenas += 1

    contador_facturasrecibidasformat = "{}".format(contador_facturasrecibidas)
    contador_nitemimaloformat = "{}".format(contador_nitemimalo)
    contador_nitrecmaloformat = "{}".format(contador_nitrecmalo)
    contador_ivamaloformat = "{}".format(contador_ivamalo)
    contador_totalmaloformat = "{}".format(contador_totalmalo)
    contador_refdobleformat = "{}".format(contador_refdoble)
    contador_factbuenasformat = "{}".format(contador_factbuenas)
    contador_nitemisoresformat = "{}".format(contador_nitemisores)
    contador_nitreceptoresformat = "{}".format(contador_nitreceptores)
    contador_facturasmalasformat = "{}".format(contador_facturasmalas)
        #contador_factbuenas = contador_facturasrecibidas - contador_facturasmalas




    xml = """
<LISTAAUTORIZACIONES>
     <AUTORIZACION>
        <FECHA> 01/09/2021 </FECHA>
        <FACTURAS_RECIBIDAS> {contador_facturasrecibidasformat} </FACTURAS_RECIBIDAS>
        <ERRORES>
            <NIT_EMISOR> {contador_nitemimaloformat} </NIT_EMISOR>
            <NIT_RECEPTOR> {contador_nitrecmaloformat} </NIT_RECEPTOR>
            <IVA> {contador_ivamaloformat} </IVA>
            <TOTAL> {contador_totalmaloformat} </TOTAL>
            <REFERENCIA_DUPLICADA> {contador_refdobleformat} </REFERENCIA_DUPLICADA>
        </ERRORES>
        <FACTURAS_CORRECTAS> {contador_factbuenasformat} </FACTURAS_CORRECTAS>
        <CANTIDAD_EMISORES> {contador_nitemisoresformat} </CANTIDAD_EMISORES>
        <CANTIDAD_RECEPTORES> {contador_nitreceptoresformat} </CANTIDAD_RECEPTORES>
        <LISTADO_AUTORIZACIONES>
        <APROBACION>
            <NIT_EMISOR ref=”A1990”> 7378106 </NIT_EMISOR>
            <CODIGO_APROBACION> 2021090100000001 </CODIGO_APROBACION>
        </APROBACION>
        <TOTAL_APROBACIONES> {contador_factbuenasformat} </TOTAL_APROBACIONES>
<AUTORIZACION>
</LISTADO_AUTORIZACIONES>
                """.format(**locals())

    objeto = {
            'Facturas recibidas': contador_facturasrecibidas,
            'Referencia doble':contador_refdoble,
            'NitEmisor': contador_nitemisores,
            'NitReceptor': contador_nitreceptores,
            'IVA malo' : contador_ivamalo,
            'Total malo' : contador_totalmalo,
            'Emisor malo' : contador_nitemimalo,
            'Facturas Buenas' : contador_factbuenas
        }


    #Datos.append(objeto)
    xmlsalida = dict2xml(objeto)
    return (xml)



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
