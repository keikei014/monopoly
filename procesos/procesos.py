from threading import Thread
from queue import Queue

class Jugador:
    nombre = None
    id = None 

    def __init__(self, nombre, id):
        self.nombre = nombre
        self.id = id

    def jugarTurno(cls,partida,queue):
        accion = input("Modificar casilla (1) o jugador (2)?\n")
       
        if( accion == '1' ):
            partida.tablero.append(4)
        elif( accion == '2' ):
            partida.jugadores.append(4)

        queue.put(partida)
            

class Partida:
    tablero = []
    jugadores = []

    def __init__(self):
        self.tablero = [0, 1, 2, 3]
        self.jugadores = [0, 1, 2, 3]

    def modCasilla(self):
        # mock method
        self.tablero.append(4)

    def modJugador(self):
        # mock method
        self.jugadores.append(4)


partida = Partida()
jugador = Jugador("J1", 0)
q = Queue()

t = Thread(target=jugador.jugarTurno, args=[partida,q])

t.start()
t.join()

partida_mod = q.get()
partida = partida_mod

print(partida.tablero)
print(partida.jugadores)
