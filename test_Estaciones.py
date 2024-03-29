from partida import Partida
from threading import Thread
from queue import Queue
from casillas import Suerte, AlaCarcel, Carcel, Estacion
from jugadores import Jugador, Jugador_Humano, Jugador_IA    

# Crear jugadores
jugador1 = Jugador_Humano("J1", 0)
jugador2 = Jugador_IA("J2", 1)
jugadores = [jugador1, jugador2]

# Inicializar tablero
tablero = [Suerte("init", 0)]*8
tablero[1] = Estacion("E1", 1)
tablero[2] = Estacion("E2", 2)
tablero[3] = Estacion("E3", 3)
tablero[4] = Estacion("E4", 4)
tablero[5] = Estacion("E5", 5)
tablero[6] = Estacion("E6", 6)
tablero[7] = Estacion("E7", 7)

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
