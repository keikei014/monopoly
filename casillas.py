from random import randint

class Casilla:
    nombre = None
    id = None

    def __init__(self, nombre, id):
        self.nombre = nombre
        self.id = id
    
    def activarEfecto():
        pass

class Calle(Casilla):
    barrio = None
    precio = None
    alquiler = []
    propietario = None
    nCasas = 0

class Estacion(Casilla):
    precio = 500
    alquiler = [250, 500, 750, 1000]
    propietario = None

    def activarEfecto(self, partida, id):
        if( self.propietario == None ):
            print("Esta estacion no tiene dueño. La compras por %i dolaritos? (Y/N)" % self.precio)
            accion = input()
            if( accion == 'Y'):
                partida.adquirirPropiedad(self.id, id)
            else:
                print("Has decidido no comprar la estacion...")
        else:
            print("Esta estacion tiene dueño. Tienes que pagar una renta.")
            nEstaciones = len(partida.jugadores[self.propietario].estaciones)
            cantidad = self.alquiler[nEstaciones-1]
            partida.pagarAlquiler(self.propietario, id, cantidad)


class Suerte(Casilla):
    def activarEfecto(self, partida, id):
        cantidad = 100*randint(-10,10)
        print("Has caido en una casilla de suerte!")

        partida.actualizarDinero(id,cantidad)

class AlaCarcel(Casilla):
    def activarEfecto(self, partida, id):
        partida.encarcelarJugador(id)
        print("A la carcel!")

class Carcel(Casilla):
    def activarEfecto(self, partida, id):
        print("Has caido en la cárcel, pero solo de visita")

