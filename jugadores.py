from random import randint
from time import sleep

class Jugador:
    nombre = None
    id = None
    posicion = 0
    dinero = 2000

    # contador de carcel, se pone a 1 si un jugador entra en la carcel
    carcel = 0

    def tirarDado(self, partida):
        dado1 = randint(3,3)
        dado2 = randint(3,3)

        dobles = False
        
        if(dado1 != dado2):
            partida.turno_activo = False
            print("Te han salido un {} y un {}!\n".format(dado1,dado2))
        else:
            dobles = True
        
        return dado1+dado2, dobles

class Jugador_Humano(Jugador):

    def __init__(self, nombre, id):
        self.nombre = nombre
        self.id = id

    def jugarTurno(self,partida,queue):
        accion = None
        while(accion != '1'):
            print("Es tu turno! Qué quieres hacer?")
            print("   1. Tirar el dado\n   2. Consultar dinero\n")
            accion = input()
            if( accion == '2' ):
                print("Tienes %i dolaritos." % self.dinero)
       
        tirada, dobles = self.tirarDado(partida)
        if(self.carcel == 0):
            casilla = partida.moverJugador(self.id, tirada)
            if( dobles ):
                print("Has sacado dobles!\n")
            partida.tablero[casilla].activarEfecto(partida, self.id)
        else:
            partida.manejarCarcel(self.id, tirada, dobles)

        queue.put(partida)

class Jugador_IA(Jugador):

    def __init__(self, nombre, id):
        self.nombre = nombre
        self.id = id

    def jugarTurno(self,partida,queue):

        print("El jugador %i se lo está pensando...\n" % self.id)
        sleep(3.0)
        print("El jugador %i ha tirado el dado!\n" % self.id)

        tirada, dobles = self.tirarDado(partida)
        if(self.carcel == 0):
            casilla = partida.moverJugador(self.id, tirada)
            if( dobles ):
                print("Has sacado dobles!")
            partida.tablero[casilla].activarEfecto(partida, self.id)
        else:
            partida.manejarCarcel(self.id, tirada, dobles)

        queue.put(partida)