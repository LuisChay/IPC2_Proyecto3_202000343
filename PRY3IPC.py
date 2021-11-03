from flask import Flask, jsonify, request
import xml.etree.ElementTree as ET
from dict2xml import dict2xml
import collections
from flask_cors import CORS
from Facturas import Facturas
from Aprobacion import Aprobacion
import re



facturasArr = []
aprobaciones = []
fecharesumen1 = []
fecharesumen2 = []

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

    facturasArr = []

    entrada = request.data.decode('utf-8')

    xmlentrada = ET.fromstring(entrada)


    for dte in xmlentrada.findall('DTE'):
        tiempo = dte.find('TIEMPO').text
        #regFecha = re.findall(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", tiempo)

        linea = 1
        columna = 1
        centinela = '#'
        buffer = ''
        estado = 0
        fecha = ""
        aux = ""

        tiempo += centinela
        i = 0
        while i < len(tiempo):
            c = tiempo[i]
            if estado == 0:
                if c.isalpha():
                    columna += 1
                    estado = 1
                elif c.isdigit():
                    buffer += c
                    columna += 1
                    estado = 2
                elif c == '#':
                    print('Se aceptó la cadena!')
                    break
                else:
                    buffer += c
                    buffer = ''
                    columna += 1
            elif estado == 1:
                if c.isalpha():
                    linea += 1
                    columna = 1
                elif c == ',':
                    linea += 1
                    columna = 1
                elif c == ' ':
                    linea += 1
                    columna = 1
                    estado = 0
                else:
                    columna += 1
            elif estado == 2:
                if c.isdigit():
                    buffer += c
                    linea += 1
                    columna = 1
                elif c == "/":
                    buffer += c
                    linea += 1
                    columna = 1
                elif c == ' ':
                    fecha += buffer
                    buffer = ''
                    estado = 3
                else:
                    pass
            elif estado == 3:
                buffer += c

            i += 1
        #aux = buffer
        #buffer = ''
        print(fecha)

        referencia = dte.find('REFERENCIA').text
        nitemi = dte.find('NIT_EMISOR').text
        nitrec = dte.find('NIT_RECEPTOR').text
        valor = dte.find('VALOR').text
        iva = dte.find('IVA').text
        total = dte.find('TOTAL').text

        nuevo = Facturas(fecha,referencia,nitemi,nitrec,valor,iva,total, False)

        facturasArr.append(nuevo)


    return jsonify({'Mensaje':'Se agregaron las facturas exitosamente',})

# METODO - OBTENER TODOS PPACIENTES
@app.route('/Facturas', methods=['GET'])
def getFacturas():
    global facturasArr

    global aprobaciones

    tiempo1 = ""
    contadorfecha = 1
    coni =  0

    listamalas = []

    for factura in facturasArr:

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
                factura.setEstadoMalo(True)
                factura.setListaerrores("error nit emisor")
        elif nit_emisor[-1] != str(final):
            factura.setEstadoMalo(True)
            factura.setListaerrores("error nit emisor")


    #IVA NitReceptor MALO
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
            factura.setListaerrores("error nit receptor")
            factura.setEstadoMalo(True)
    elif nit_receptor[-1] != str(final1):
        factura.setEstadoMalo(True)
        factura.setListaerrores("error nit receptor")



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

    for y in repetidos:
        for factura  in facturasArr:
            if factura.getReferencia() == y:
                factura.setListaerrores("referencia doble")
                factura.setEstadoMalo(True)





    for factura in facturasArr:

        #IIVA MALO
        operacion = ( float(factura.getValor() ) - ( float(factura.getValor()) * 0.88 ) )
        ivax = float(factura.getIva())
        aprox = round(ivax, 2)

        if aprox != operacion:
            factura.setEstadoMalo(True)
            factura.setListaerrores("iva malo")



        #total MALO
        operaciontotal = ( float(factura.getValor() ) + ( float(factura.getIva())) )
        totalx = float(factura.getTotal())
        aprox1 = round(totalx, 2)

        if aprox1 != operaciontotal:
            factura.setListaerrores("total malo")
            factura.setEstadoMalo(True)


    fechas = []
    for factura in facturasArr:
        if fechas.count(factura.getTiempo()) == 0:
            fechas.append(factura.getTiempo())


    for fecha in fechas:
        switch = False


        for aprobacion in aprobaciones:


            if aprobacion.fecha == fecha:
                switch = True
                listacodigoaprobacion = fecha.split("/")
                codigoaprobacion = listacodigoaprobacion[2] + listacodigoaprobacion[1] + listacodigoaprobacion[0]
                emisores = []
                receptores = []

                for factura in facturasArr:

                    if factura.getTiempo() == fecha:
                        if emisores.count(factura.getNitemisor()) == 0:
                            emisores.append(factura.getNitemisor())
                            aprobacion.contador_nitemisores += 1

                        if receptores.count(factura.getNitreceptor()) == 0:
                            receptores.append(factura.getNitreceptor())
                            aprobacion.contador_nitreceptores += 1

                        aprobacion.contador_facturasrecibidas += 1

                        if factura.getEstadoMalo() == False:

                            aprobacion.contador_factbuenas += 1
                            correlativo = str(aprobacion.contador_factbuenas)
                            cantidad = 8 - len(correlativo)
                            ceros = ""
                            for i in range(cantidad):
                                ceros += "0"
                            codigounico = codigoaprobacion + ceros + correlativo

                            facturaaprobada = [factura, codigounico]
                            aprobacion.listaaprobaciones.append(facturaaprobada)


                        else:
                            aprobacion.contador_facturasmalas += 1
                            for error in factura.getLista():
                                if error == "error nit emisor":
                                    aprobacion.contador_nitemimalo += 1
                                elif error == "error nit receptor":
                                    aprobacion.contador_nitrecmalo += 1
                                elif error == "referencia doble":
                                    aprobacion.contador_refdoble += 1
                                elif error == "iva malo":
                                    aprobacion.contador_ivamalo += 1
                                elif error == "total malo":
                                    aprobacion.contador_totalmalo += 1


                break
        if switch == False:
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
            listaaprobaciones = []
            emisores = []
            receptores = []

            listacodigoaprobacion = fecha.split("/")
            codigoaprobacion = listacodigoaprobacion[2] + listacodigoaprobacion[1] + listacodigoaprobacion[0]


            for factura in facturasArr:



                if factura.getTiempo() == fecha:
                    # NIT EMISORES CONTADOR

                    if emisores.count(factura.getNitemisor()) == 0:
                        emisores.append(factura.getNitemisor())

                    # NIT RECEPTOR CONTADOR

                    if receptores.count(factura.getNitreceptor()) == 0:
                        receptores.append(factura.getNitreceptor())

                    contador_facturasrecibidas += 1

                    if factura.getEstadoMalo() == False:

                        contador_factbuenas += 1
                        correlativo = str(contador_factbuenas)
                        cantidad = 8 - len(correlativo)
                        ceros = ""
                        for i in range(cantidad):
                            ceros += "0"
                        codigounico = codigoaprobacion + ceros + correlativo
                        print(codigounico)

                        facturaaprobada = [factura, codigounico]
                        listaaprobaciones.append(facturaaprobada)


                    else:
                        print(fecha, "mala")
                        contador_facturasmalas += 1
                        for error in factura.getLista():
                            if error == "error nit emisor":
                                contador_nitemimalo += 1
                            elif error == "error nit receptor":
                                contador_nitrecmalo += 1
                            elif error == "referencia doble":
                                contador_refdoble += 1
                            elif error == "iva malo":
                                contador_ivamalo += 1
                            elif error == "total malo":
                                contador_totalmalo += 1
            contador_nitemisores = len(emisores)
            contador_nitreceptores = len(receptores)
            aprobaciones.append(Aprobacion(fecha,listaaprobaciones,contador_facturasrecibidas,contador_nitemimalo,contador_nitrecmalo, contador_ivamalo, contador_totalmalo, contador_refdoble, contador_factbuenas,contador_nitemisores, contador_nitreceptores, contador_facturasmalas))


    xml = """
<LISTAAUTORIZACIONES>
"""
    for aprobacion in aprobaciones:
        xml += f"""
     <AUTORIZACION>
        <FECHA> {aprobacion.fecha} </FECHA>
        <FACTURAS_RECIBIDAS> {aprobacion.contador_facturasrecibidas} </FACTURAS_RECIBIDAS>
        <ERRORES>
            <NIT_EMISOR> {aprobacion.contador_nitemisores} </NIT_EMISOR>
            <NIT_RECEPTOR> {aprobacion.contador_nitreceptores} </NIT_RECEPTOR>
            <IVA> {aprobacion.contador_ivamalo} </IVA>
            <TOTAL> {aprobacion.contador_totalmalo} </TOTAL>
            <REFERENCIA_DUPLICADA> {aprobacion.contador_refdoble} </REFERENCIA_DUPLICADA>
        </ERRORES>
        <FACTURAS_CORRECTAS> {aprobacion.contador_factbuenas} </FACTURAS_CORRECTAS>
        <CANTIDAD_EMISORES> {aprobacion.contador_nitemisores} </CANTIDAD_EMISORES>
        <CANTIDAD_RECEPTORES> {aprobacion.contador_nitreceptores} </CANTIDAD_RECEPTORES>
        <LISTADO_AUTORIZACIONES>
        """
        for correcta in aprobacion.listaaprobaciones:
            xml += f'''
        <APROBACION>
            <NIT_EMISOR ref="{correcta[0].referencia}"> {correcta[0].nitemisor} </NIT_EMISOR>
            <CODIGO_APROBACION> {correcta[1]} </CODIGO_APROBACION>
        </APROBACION>
        '''
        xml += f"""
        <TOTAL_APROBACIONES> {len(listaaprobaciones)} </TOTAL_APROBACIONES>
        </LISTADO_AUTORIZACIONES>
</AUTORIZACION>
"""
        xml += """
</LISTAAUTORIZACIONES>
"""
    autorizaciones = open("autorizaciones.xml", "w")
    autorizaciones.write(xml)
    autorizaciones.close()

    objeto = {
            'XML': xml
        }

    xmlsalida = dict2xml(objeto)
    return xmlsalida



@app.route('/resumeniva', methods=['POST'])
def resumendeivaPost():
    global fecharesumen1

    fechapost = request.json['Fecha']
    fecharesumen1.append(fechapost)


    return jsonify({'Mensaje':'Se esta generando el resumen',})


@app.route('/resumeniva', methods=['GET'])
def resumendeivaGet():
    global facturasArr
    global fecharesumen1


    fechaanalisis1 = ""

    for fecha in fecharesumen1:
        fechapass = fecha

    for factura in facturasArr:
        if fechapass == factura.getTiempo():
            objeto = {
            'Total': factura.getTotal()

            }

            return(jsonify(objeto))

    salida = { "Mensaje": "No existe registros en esa fecha" }

    return(jsonify(salida))



@app.route('/resumenrango', methods=['POST'])
def resumenderangoPost():

    global fecharesumen2

    fechapost1 = request.json['Fecha']

    fecharesumen2.append(fechapost1)


    return jsonify({'Mensaje':'Se esta generando el resumen',})




@app.route('/resumenrango', methods=['GET'])
def resumenderangoGet():

    for fecha in fecharesumen2:
        fechapass1 = fecha
        for factura in facturasArr:

            if fechapass1 == str(factura.getTiempo()):
                objeto = {
                'Total': factura.getTotal(),
                'Valor': factura.getValor(),
                'Fecha': factura.getTiempo()
                }

                return(jsonify(objeto))

    salida = { "Mensaje": "No existe registros en esa fecha" }

    return(jsonify(salida))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
