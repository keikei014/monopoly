from random import randint 

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
