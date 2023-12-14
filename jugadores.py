from random import randint
from time import sleep

class Jugador_Humano:
    nombre = None
    id = None
    posicion = 0

    def __init__(self, nombre, id):
        self.nombre = nombre
        self.id = id

    def jugarTurno(self,partida,queue):
        accion = input("Pulsa Enter para tirar el dado...\n")
       
        dado = randint(1,6)
        print("Te ha salido un %i!\n" % dado)
        partida.moverJugador(self.id, dado)

        queue.put(partida)

class Jugador_IA:
    nombre = None
    id = None
    posicion = 0

    def __init__(self, nombre, id):
        self.nombre = nombre
        self.id = id

    def jugarTurno(self,partida,queue):

        print("El jugador %i se lo está pensando...\n" % self.id)
        sleep(3.0)
        print("El jugador %i ha tirado el dado!\n" % self.id)

        dado = randint(1,6)
        print("Le ha salido un %i!\n" % dado)
        partida.moverJugador(self.id, dado)

        queue.put(partida)