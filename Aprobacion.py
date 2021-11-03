class Aprobacion:
    def __init__(self,fecha,listaaprobaciones,contador_facturasrecibidas,contador_nitemimalo,contador_nitrecmalo, contador_ivamalo, contador_totalmalo, contador_refdoble, contador_factbuenas,contador_nitemisores, contador_nitreceptores, contador_facturasmalas):

        self.fecha = fecha
        self.listaaprobaciones = listaaprobaciones
        self.contador_facturasrecibidas = contador_facturasrecibidas
        self.contador_nitemimalo = contador_nitemimalo
        self.contador_nitrecmalo = contador_nitrecmalo
        self.contador_ivamalo = contador_ivamalo
        self.contador_totalmalo = contador_totalmalo
        self.contador_refdoble = contador_refdoble
        self.contador_factbuenas = contador_factbuenas
        self.contador_nitemisores = contador_nitemisores
        self.contador_nitreceptores = contador_nitreceptores
        self.contador_facturasmalas = contador_facturasmalas

        '''
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
        '''
