class Aprobacion:
    def __init__(self,tiempo,referencia,nitemisor,nitreceptor,valor, iva, total, estadoMalo):
        self.contador_facturasrecibidas = 0
        self.contador_nitemimalo = 0
        self.contador_nitrecmalo = 0
        self.contador_ivamalo = 0
        self.contador_totalmalo = 0
        self.contador_refdoble = 0
        self.contador_factbuenas = 0
        self.contador_nitemisores = 0
        self.contador_nitreceptores = 0
        self.contador_facturasmalas = 0

        self.fecha = fecha
        self.correcta = correcta
        self.listaaprobaciones = listaaprobaciones

        self.nitreceptor = nitreceptor
        self.valor = valor
        self.iva = iva
        self.total = total
        self.estadoMalo  = estadoMalo

    def getTiempo(self):
        return self.tiempo

    def getReferencia(self):
        return self.referencia

    def getNitemisor(self):
        return self.nitemisor

    def getNitreceptor(self):
        return self.nitreceptor

    def getValor(self):
        return self.valor

    def getIva(self):
        return self.iva

    def getTotal(self):
        return self.total

    def getEstadoMalo(self):
        return self.estadoMalo


    def setTiempo(self, tiempo):
        self.tiempo = tiempo

    def setReferencia(self, referencia):
        self.referencia = referencia

    def setReferencia(self, nitemisor):
        self.nitemisor = nitemisor

    def setNitreceptor(self, nitreceptor):
        self.nitreceptor = nitreceptor

    def setValor(self, valor):
        self.valor = valor

    def setIva(self, iva):
        self.iva = iva

    def setTotal(self, total):
        self.total = total

    def setTotal(self, total):
        self.total = total

    def setEstadoMalo(self, estadoMalo):
        self.estadoMalo = estadoMalo
