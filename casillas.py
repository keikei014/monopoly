from random import randint

class Casilla:
    nombre = None
    posicion = None

    def activarEfecto():
        pass

class Calle(Casilla):
    barrio = None
    precio = None
    alquiler = []
    propietario = None
    nCasas = 0

class Estacion(Casilla):
    precio = None
    alquiler = []
    propietario = None

    # def activarEfecto(self):
    #     if( self.propietario == None ):


class Suerte(Casilla):
    def activarEfecto(self, partida, id):
        cantidad = 100*randint(-10,10)
        if( cantidad > 0 ):
            print("Te ganas unas pelillas! Recibes %i dolaritos." % cantidad)
        else:
            print("Te sale a pagar! Pierdes %i dolaritos." % abs(cantidad))

        partida.actualizarDinero(id,cantidad)

class Carcel(Casilla):
    def activarEfecto(self, jugador):
        pass

