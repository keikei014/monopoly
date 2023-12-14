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
    def activarEfecto(jugador):
        cantidad = 100*randint(-10,10)
        jugador.dinero += cantidad
