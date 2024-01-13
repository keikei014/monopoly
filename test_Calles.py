from partida import Partida
from threading import Thread
from queue import Queue
from casillas import Suerte, Calle
from jugadores import Jugador, Jugador_Humano, Jugador_IA    

# Crear jugadores
jugador1 = Jugador_Humano("J1", 0)
jugador2 = Jugador_IA("J2", 1)
jugadores = [jugador1, jugador2]

# Inicializar tablero
tablero = [Suerte("init", 0)]*8
tablero[1] = Calle("jeketiezo", 1, 0, 50, [10, 30, 50, 70, 100, 120])
tablero[2] = Calle("superboke", 2, 0, 50, [10, 30, 50, 70, 100, 120])
tablero[3] = Calle("cortijo", 3, 0, 80, [15, 35, 60, 80, 120, 150])
tablero[4] = Calle("Teatinos", 4, 2, 150, [40, 70, 100, 150, 210, 300])
tablero[5] = Calle("Trinidad", 5, 2, 150, [40, 70, 100, 150, 210, 300])
tablero[6] = Calle("Victoria", 6, 2, 200, [55, 90, 120, 180, 250, 360])
tablero[7] = Suerte("final", 7)

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
