from random import randint
from time import sleep

class Jugador:
    nombre = None
    id = None
    posicion = 0
    dinero = 2000

    def tirarDado(partida):
        dado1 = randint(1,2)
        dado2 = randint(1,2)
        
        if(dado1 != dado2):
            partida.turno_activo = False
            print("Te han salido un {} y un {}!\n".format(dado1,dado2))
        else:
            print("Doble %i! Has sacado dobles y tiras otra vez al final de tu turno.\n" % dado1)
        
        return dado1+dado2

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
       
        tirada = Jugador.tirarDado(partida)
        
        partida.moverJugador(self.id, tirada)

        queue.put(partida)

class Jugador_IA(Jugador):

    def __init__(self, nombre, id):
        self.nombre = nombre
        self.id = id

    def jugarTurno(self,partida,queue):

        print("El jugador %i se lo está pensando...\n" % self.id)
        sleep(3.0)
        print("El jugador %i ha tirado el dado!\n" % self.id)

        tirada = Jugador.tirarDado(partida)
        partida.moverJugador(self.id, tirada)

        queue.put(partida)