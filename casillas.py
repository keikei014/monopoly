from random import randint

class Casilla:
    nombre = None
    id = None

    def __init__(self, nombre, id):
        self.nombre = nombre
        self.id = id
    
    def activarEfecto():
        pass

class Inicio(Casilla):
    def __init__(self, nombre, id):
        self.nombre = nombre
        self.id = id

class Calle(Casilla):

    def __init__(self, nombre, id, barrio, precio, alquiler):
        self.nombre = nombre
        self.id = id
        self.barrio = barrio
        self.precio = precio
        self.alquiler = alquiler
        self.propietario = None
        self.nCasas = 0

    def activarEfecto(self, partida, id):
        if( self.propietario == None ):
            print("Esta calle no tiene dueño. La compras por %i dolaritos? (Y/N)" % self.precio)
            accion = input()
            if( accion == 'Y'):
                partida.adquirirCalle(self.id, id)
            else:
                print("Has decidido no comprar la calle...")
        elif( self.propietario != id):
            print("Esta calle tiene dueño! Tienes que pagar renta.")
            cantidad = self.alquiler[self.nCasas]
            partida.pagarAlquiler(self.propietario, id, cantidad)

class Estacion(Casilla):
    precio = 400
    alquiler = [50, 100, 200, 400]
    propietario = None

    def activarEfecto(self, partida, id):
        if( self.propietario == None ):
            print("Esta estacion no tiene dueño. La compras por %i dolaritos? (Y/N)" % self.precio)
            accion = input()
            if( accion == 'Y'):
                partida.adquirirEstacion(self.id, id)
            else:
                print("Has decidido no comprar la estacion...")
        elif( self.propietario != id):
            print("Esta estacion tiene dueño. Tienes que pagar una renta.")
            nEstaciones = len(partida.jugadores[self.propietario].propiedades.estaciones)
            cantidad = self.alquiler[nEstaciones-1]
            partida.pagarAlquiler(self.propietario, id, cantidad)
        else:
            print("Estas en una propiedad que te pertenece...")


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

