from random import randint
from time import sleep

class Propiedades:
    def __init__(self):
        self.calles = []
        self.estaciones = []
        self.servicios = []

    def añadirCalle(self, id):
        self.calles.append(id)

    def añadirEstacion(self, id):
        self.estaciones.append(id)

    def añadirServicio(self, id):
        self.servicios.append(id)
    
    def eliminarCalle(self, id):
        self.calles.remove(id)

    def eliminarEstacion(self, id):
        self.estaciones.remove(id)

    def eliminarServicio(self, id):
        self.servicios.remove(id)

    # def printCalles(self):
    #     i = 1
    #     if( len(self.calles) == 0):
    #         print("No tienes ninguna calle!\n")
    #     else:
    #         for calle in self.calles:
    #             print("{n}. Nombre: {name}\n   Barrio: {hood}\n   Hipoteca: {price}\n\n".format(n=i,name=calle.nombre, hood=calle.barrio, price=(calle.precio/2)))
    #             i += 1

    # def printEstaciones(self):
    #     i = 1
    #     if( len(self.calles) == 0):
    #         print("No tienes ninguna estacion!\n")
    #     else:
    #         for estacion in self.estaciones:
    #             print("{}. Nombre: {}\n   Estacion nº: {}\n\n".format(i,estacion.nombre, (estacion.id+1), (estacion.precio/2)))
    #             i += 1

class Jugador:
    nombre = None
    id = None
    posicion = 0
    dinero = 2000

    # contador de carcel, se pone a 1 si un jugador entra en la carcel
    carcel = 0

    def tirarDado(self, partida):
        dado1 = randint(1,3)
        dado2 = randint(1,3)

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
        self.propiedades = Propiedades()

    def jugarTurno(self,partida,queue):
        accion = None
        while(accion != '1'):
            print("Es tu turno! Qué quieres hacer?")
            print("   1. Tirar el dado\n   2. Consultar dinero\n   3. Hipotecar propiedad\n   4. Poner casas\n")
            accion = input()
            if( accion == '2' ):
                print("Tienes %i dolaritos." % self.dinero)
            elif( accion == '3' ):
                self.venderProp(partida)
       
        tirada, dobles = self.tirarDado(partida)
        if(self.carcel == 0):
            casilla = partida.moverJugador(self.id, tirada)
            if( dobles ):
                print("Has sacado dobles!\n")
            partida.tablero[casilla].activarEfecto(partida, self.id)
        else:
            partida.manejarCarcel(self.id, tirada, dobles)

        queue.put(partida)
    
    def venderProp(self, partida):
        print("¿Qué quieres vender?\n   1. Calle\n   2. Estacion\n")
        accion = input()
        if(accion == '1'):
            partida.printCalles(self.id)
            print("¿Qué calle quieres vender? Pulsa '0' para volver.\n")
            accion = input()
            while( (int(accion) > len(self.propiedades.calles)) and (accion != '0') ):
                print("Numero de calle no valido...\nVuelve a introducir un numero o pulsa 'B' para volver:")
                accion = input()

            if(accion == '0'):
                print("Has decidido no vender nada.")
            else:
                print("Has vendido la calle {0} por {1} dolaritos.".format(partida.tablero[self.propiedades.calles[int(accion)-1]].nombre,(partida.tablero[self.propiedades.calles[int(accion)-1]].precio/2)))
                partida.venderCalle(self.propiedades.calles[int(accion)-1], self.id)
                
        else:
            partida.printEstaciones(self.id)
            print("¿Qué estacion quieres vender? Pulsa '0' para volver.\n")
            accion = input()
            while( (int(accion) > len(self.propiedades.estaciones)) and (accion != '0') ):
                print("Numero de estacion no valido...\nVuelve a introducir un numero o pulsa 'B' para volver:")
                accion = input()

            if(accion == '0'):
                print("Has decidido no vender nada.")
            else:
                print("Has vendido la estacion {0} por {1} dolaritos.".format(partida.tablero[self.propiedades.estaciones[int(accion)-1]].nombre,(partida.tablero[self.propiedades.estaciones[int(accion)-1]].precio/2)))
                partida.venderEstacion(self.propiedades.estaciones[int(accion)-1], self.id)      


class Jugador_IA(Jugador):
    
    def __init__(self, nombre, id):
        self.nombre = nombre
        self.id = id
        self.propiedades = Propiedades()

    def jugarTurno(self,partida,queue):

        print("El jugador %i se lo está pensando...\n" % (self.id+1))
        sleep(3.0)
        print("El jugador %i ha tirado el dado!\n" % (self.id+1))

        tirada, dobles = self.tirarDado(partida)
        if(self.carcel == 0):
            casilla = partida.moverJugador(self.id, tirada)
            if( dobles ):
                print("Has sacado dobles!")
            partida.tablero[casilla].activarEfecto(partida, self.id)
        else:
            partida.manejarCarcel(self.id, tirada, dobles)

        queue.put(partida)