from threading import Thread
from queue import Queue
from random import randint
from casillas import Suerte, AlaCarcel, Carcel, Estacion
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

        if( self.jugadores[id].posicion > 7 ):
            # cuando llega al final del tablero, empieza una nueva vuelta
            self.jugadores[id].posicion -= 8
            # al pasar por la casilla de salida cobras
            self.actualizarDinero(id, 400)
            print("Has dado una vuelta al tablero. Recibes 400 dolaritos\n")

        print("La nueva posicion del jugador {} es {}\n".format(id+1,self.jugadores[id].posicion))
        return self.jugadores[id].posicion

    def actualizarDinero(self, id, cantidad):
        if( cantidad > 0 ):
            print("Jugador {}, ganas {} dolaritos.\n".format(id+1,cantidad))
        else:
            print("Jugador {}, pierdes {} dolaritos.\n".format(id+1,abs(cantidad)))

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
    
    def adquirirPropiedad(self, casillaId, jugadorId):
        self.jugadores[jugadorId].dinero -= self.tablero[casillaId].precio
        self.jugadores[jugadorId].propiedades.añadirEstacion(casillaId)
        self.tablero[casillaId].propietario = jugadorId
        print("Has adquirido la propiedad! Te quedan %i dolaritos." % self.jugadores[jugadorId].dinero)

    def pagarAlquiler(self, propietarioId, jugadorId, cantidad):
        self.actualizarDinero(propietarioId, cantidad)
        self.actualizarDinero(jugadorId,-cantidad)



# Crear jugadores
jugador1 = Jugador_Humano("J1", 0)
jugador2 = Jugador_IA("J2", 1)
jugadores = [jugador1, jugador2]

# Inicializar tablero
tablero = [Suerte("init", 0)]*8
tablero[0] = Suerte("Suerte0", 0)
tablero[4] = Suerte("Suerte4", 4)
tablero[6] = AlaCarcel("AlaCarcel", 6)
tablero[2] = Carcel("Carcel", 2)
tablero[1] = Estacion("E1", 1)
tablero[3] = Estacion("E2", 3)
tablero[5] = Estacion("E3", 5)
tablero[7] = Estacion("E4", 7)

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
