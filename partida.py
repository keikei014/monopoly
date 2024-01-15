from random import randint

class Partida:
    tablero = []
    jugadores = []
    turno_activo = True
    nJugadores = 0
    jugadores_activos = []

    def __init__(self, tablero, jugadores):
        self.tablero = tablero
        self.jugadores = jugadores
        self.nJugadores = len(jugadores)
        for jugador in jugadores:
            self.jugadores_activos.append(jugador.id)

    def moverJugador(self, id, dado):
        self.jugadores[id].posicion += dado

        if( self.jugadores[id].posicion > (len(self.tablero)-1) ):
            # cuando llega al final del tablero, empieza una nueva vuelta
            self.jugadores[id].posicion -= len(self.tablero)
            # al pasar por la casilla de salida cobras
            self.actualizarDinero(id, 100)
            print("Has dado una vuelta al tablero. Recibes 400 dolaritos\n")

        print("La nueva posicion del jugador {} es {}\n".format(id+1,self.jugadores[id].posicion))
        return self.jugadores[id].posicion

    def actualizarDinero(self, id, cantidad):
        if( cantidad > 0 ):
            print("Jugador {}, ganas {} dolaritos.\n".format(id+1,cantidad))
        else:
            print("Jugador {}, pierdes {} dolaritos.\n".format(id+1,abs(cantidad)))

        self.jugadores[id].dinero += cantidad
        if(self.jugadores[id].dinero < 0):
            self.declararBancarrota(id)

    def encarcelarJugador(self, id):
        self.jugadores[id].posicion = 2
        self.jugadores[id].carcel = 1
        self.turno_activo = False

    def manejarCarcel(self, id, cantidad, dobles):
        if( dobles ):
            self.moverJugador(id, cantidad)
            self.jugadores[id].carcel = 0
            print("Has sacado dobles y sales de la cárcel!")
        else:
            self.jugadores[id].carcel += 1
            print("No has podido salir de la cárcel!")
            if(self.jugadores[id].carcel == 3):
                self.jugadores[id].carcel = 0
                print("Has cumplido tu condena. El siguiente turno tiras normalmente.")
    
    def adquirirEstacion(self, casillaId, jugadorId):
        self.actualizarDinero(jugadorId, -(self.tablero[casillaId].precio))
        self.jugadores[jugadorId].propiedades.añadirEstacion(casillaId)
        self.tablero[casillaId].propietario = jugadorId
        print("Has adquirido la propiedad! Te quedan %i dolaritos." % self.jugadores[jugadorId].dinero)

    def venderEstacion(self, casillaId, jugadorId):
        self.actualizarDinero(jugadorId,(self.tablero[casillaId].precio/2))
        self.jugadores[jugadorId].propiedades.eliminarEstacion(casillaId)
        self.tablero[casillaId].propietario = None

    def adquirirCalle(self, casillaId, jugadorId):
        self.actualizarDinero(jugadorId, -(self.tablero[casillaId].precio))
        self.jugadores[jugadorId].propiedades.añadirCalle(casillaId)
        self.tablero[casillaId].propietario = jugadorId
        print("Has adquirido la propiedad! Te quedan %i dolaritos." % self.jugadores[jugadorId].dinero)

    def venderCalle(self, casillaId, jugadorId):
        self.actualizarDinero(jugadorId,(self.tablero[casillaId].precio/2))
        self.jugadores[jugadorId].propiedades.eliminarCalle(casillaId)
        self.tablero[casillaId].propietario = None

    def pagarAlquiler(self, propietarioId, jugadorId, cantidad):
        self.actualizarDinero(propietarioId, cantidad)
        self.actualizarDinero(jugadorId,-cantidad)

    def printCalles(self, jugadorId):
        i = 1
        if( len(self.jugadores[jugadorId].propiedades.calles) == 0):
            print("No tienes ninguna calle!\n")
        else:
            for calle in self.jugadores[jugadorId].propiedades.calles:
                print("{n}. Nombre: {name}\n   Barrio: {hood}\n   Hipoteca: {price}\n\n".format(n=i,name=self.tablero[calle].nombre, hood=self.tablero[calle].barrio, price=(self.tablero[calle].precio/2)))
                i += 1
    
    def printEstaciones(self,jugadorId):
        i = 1
        if( len(self.jugadores[jugadorId].propiedades.estaciones) == 0):
            print("No tienes ninguna estacion!\n")
        else:
            for estacion in self.jugadores[jugadorId].propiedades.estaciones:
                print("{n}. Nombre: {name}\n   Estacion: {num}\n   Hipoteca: {price}\n\n".format(n=i,name=self.tablero[estacion].nombre, num=self.tablero[estacion].id, price=(self.tablero[estacion].precio/2)))
                i += 1

    def añadirCasa(self,jugadorId,casillaId,cantidad):
        if( self.tablero[casillaId].nCasas == 5):
            print("Esta casilla ya tiene un hotel. No puedes poner mas casas.")
        elif((self.tablero[casillaId].nCasas+cantidad) <= 5):
            self.tablero[casillaId].nCasas += cantidad
            self.actualizarDinero(jugadorId, -(cantidad*self.tablero[casillaId].precioCasa))
        else:
            print("No puedes poner tantas casas!\nPuedes poner %i en esta casilla\n" % (5-self.tablero[casillaId].nCasas))

    def declararBancarrota(self, jugadorId):
        self.jugadores[jugadorId].arruinado = True
        self.jugadores_activos.remove(jugadorId)
        print("Jugador %i, estas en la ruina! Ya no juegas mas." % (jugadorId+1))
        self.nJugadores -= 1
        self.turno_activo = False