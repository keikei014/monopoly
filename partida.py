from threading import Thread
from queue import Queue
from random import randint
from casillas import Suerte
from jugadores import Jugador_Humano, Jugador_IA     

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
            self.jugadores[id].posicion -= 9

        print("La nueva posicion del jugador {} es {}\n".format(id+1,self.jugadores[id].posicion))   


# Crear jugadores
jugador1 = Jugador_Humano("J1", 0)
jugador2 = Jugador_IA("J2", 1)
jugadores = [jugador1, jugador2]

# Inicializar tablero
tablero = [Suerte()]*9

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
