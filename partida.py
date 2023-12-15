from threading import Thread
from queue import Queue
from random import randint
from casillas import Suerte, AlaCarcel
from jugadores import Jugador, Jugador_Humano, Jugador_IA     

class Partida:
    tablero = []
    jugadores = []
    turno_activo = True

    def __init__(self, tablero, jugadores):
        self.tablero = tablero
        self.jugadores = jugadores

    def moverJugador(self, id, dado):
        self.jugadores[id].posicion += dado

        if( self.jugadores[id].posicion > 8 ):
            # cuando llega al final del tablero, empieza una nueva vuelta
            self.jugadores[id].posicion -= 9
            # al pasar por la casilla de salida cobras
            self.actualizarDinero(id, 400)
            print("Has dado una vuelta al tablero. Recibes 400 dolaritos\n")

        print("La nueva posicion del jugador {} es {}\n".format(id+1,self.jugadores[id].posicion))
        return self.jugadores[id].posicion

    def actualizarDinero(self, id, cantidad):
        if( cantidad > 0 ):
            print("Ganas %i dolaritos.\n" % cantidad)
        else:
            print("Pierdes %i dolaritos.\n" % cantidad)

        self.jugadores[id].dinero += cantidad

    def encarcelarJugador(self, id):
        self.jugadores[id].posicion = 2
        self.jugadores[id].carcel = 1
        self.turno_activo = False

    def manejarCarcel(self, id, cantidad, dobles):
        if( dobles ):
            self.moverJugador(id, cantidad)
            print("Has sacado dobles y sales de la cárcel!")
        else:
            self.jugadores[id].carcel += 1
            print("No has podido salir de la cárcel!")
            if(self.jugadores[id].carcel == 3):
                self.jugadores[id].carcel = 0
                print("Has cumplido tu condena. El siguiente turno tiras normalmente.")


# Crear jugadores
jugador1 = Jugador_Humano("J1", 0)
jugador2 = Jugador_IA("J2", 1)
jugadores = [jugador1, jugador2]

# Inicializar tablero
tablero = [Suerte()]*9
tablero[6] = AlaCarcel()

# Crear la partida
partida = Partida(tablero, jugadores)

q = Queue()

while(True):

    while(partida.turno_activo):
        turno_j1 = Thread(target=jugador1.jugarTurno, args=[partida,q])
        turno_j1.start()
        turno_j1.join()
    
        partida_mod = q.get()
        partida = partida_mod
    
    partida.turno_activo = True

    

    while(partida.turno_activo):
        turno_j2 = Thread(target=jugador2.jugarTurno, args=[partida,q])
        turno_j2.start()
        turno_j2.join()

        partida_mod = q.get()
        partida = partida_mod

    partida.turno_activo = True
