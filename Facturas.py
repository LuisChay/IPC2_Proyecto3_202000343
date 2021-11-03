class Facturas:

    def __init__(self,tiempo,referencia,nitemisor,nitreceptor,valor, iva, total, estadoMalo):
        self.tiempo = tiempo
        self.referencia = referencia
        self.nitemisor = nitemisor
        self.nitreceptor = nitreceptor
        self.valor = valor
        self.iva = iva
        self.total = total
        self.estadoMalo  = estadoMalo
        self.listaerrores = []



    def getTiempo(self):
        return self.tiempo

    def getLista(self):
        return self.listaerrores

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

    # METODOS SET
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

    def setListaerrores(self, cadena):
        self.listaerrores.append(cadena)
