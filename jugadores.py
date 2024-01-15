from random import randint
from time import sleep
from fuzzy import venta_calle_Fuzzy, poner_casas_Fuzzy

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

class Jugador:
    nombre = None
    id = None
    posicion = 0
    dinero = 1000
    nCalles = 0
    nEstaciones = 0
    nCasastotales = 0
    arruinado = False

    # contador de carcel, se pone a 1 si un jugador entra en la carcel
    carcel = 0

    def tirarDado(self, partida):
        dado1 = randint(1,5)
        dado2 = randint(1,5)

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
            elif( accion == '4' ):
                self.ponerCasa(partida)
       
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
    
    def ponerCasa(self, partida):
        print("¿Sobre qué calle quieres edificar? Pulsa '0' para volver.\n")
        partida.printCalles(self.id)
        accion = input()
        while( (int(accion) > len(self.propiedades.calles)) and (accion != '0') ):
            print("Numero de calle no valido...\nVuelve a introducir un numero o pulsa 'B' para volver:")
            accion = input()
        if(accion == '0'):
            print("Has decidido no construir.")
        else:
            print("Cada casa te cuesta %i dolaritos. ¿Cuántas quieres construir? (1-5)" % (partida.tablero[self.propiedades.calles[int(accion)-1]].precio/2))
            cantidad = int(input())
            partida.añadirCasa(self.id, self.propiedades.calles[int(accion)-1], cantidad)

class Jugador_Fuzzy(Jugador):
    
    def __init__(self, nombre, id):
        self.nombre = nombre
        self.id = id
        self.propiedades = Propiedades()
        self.nCalles = 0
        self.nEstaciones = 0
        self.nCasastotales = 0

    def jugarTurno(self,partida,queue):

        #self.nCalles = len(self.propiedades.calles) 
        #self.nEstaciones = len(self.propiedades.estaciones)
        print("El jugador %i se lo está pensando...\n" % (self.id+1))
        sleep(3.0)
        print("El jugador %i ha tirado el dado!\n" % (self.id+1))

        tirada, dobles = self.tirarDado(partida)
        if(self.carcel == 0):
            casilla = partida.moverJugador(self.id, tirada)
            if( dobles ):
                print("Has sacado dobles!")
            

            self.nCalles = len(self.propiedades.calles) 
            self.nEstaciones = len(self.propiedades.estaciones) 
            partida.tablero[casilla].activarEfecto_Fuzzy(partida, self.id)

        else:
            partida.manejarCarcel(self.id, tirada, dobles)

        # Evaluar posible venta de propiedades:
        venta = venta_calle_Fuzzy(self.dinero, self.nCalles, self.nEstaciones)
        if venta == 1:
            self.venta_fuzzy(partida)
        else:
            print("Fuzzy ha decidido no vender nada.")

        # Evaluar poner casas:
        casas = poner_casas_Fuzzy(self.dinero, self.nCalles, self.nEstaciones)
        if casas == 1:
            self.poner_casas(partida)
        else:
            print("Fuzzy ha decidido no poner casas.")

        queue.put(partida)


    def venta_fuzzy(self, partida):
        calles_p = self.propiedades.calles
        if (len(calles_p) > 0):
            precios_propiedades = list(range(len(self.propiedades.calles)))
            for i in range(0, len(precios_propiedades)):
                precios_propiedades[i] = partida.tablero[self.propiedades.calles[i]].precio
            maximo = max(precios_propiedades)
            calle_maximo = [i for i, valor in enumerate(precios_propiedades) if valor == maximo]
            print("Fuzzy ha decidido vender la calle {0} por {1} dolaritos.".format(partida.tablero[self.propiedades.calles[calle_maximo[0]]].nombre,(partida.tablero[self.propiedades.calles[calle_maximo[0]]].precio/2)))
            partida.venderCalle(self.propiedades.calles[calle_maximo[0]], self.id)
            
        else:
            print("Fuzzy no dispone de calle para vender")

    
    def poner_casas(self,partida):
        calles_p = self.propiedades.calles
        if (len(calles_p) > 0):
            precios_propiedades = list(range(len(self.propiedades.calles)))
            for i in range(0, len(precios_propiedades)):
                precios_propiedades[i] = partida.tablero[self.propiedades.calles[i]].precio
            maximo = max(precios_propiedades)
            calle_maximo = [i for i, valor in enumerate(precios_propiedades) if valor == maximo]
            if self.dinero > 2000:
                cantidad = 3
            elif self.dinero > 1500:
                cantidad = 2
            else:
                cantidad = 1
            print("Fuzzy ha decidido poner en {0} %i casas ".format(partida.tablero[self.propiedades.calles[calle_maximo[0]]].nombre, cantidad))
            partida.añadirCasa(self.id, self.propiedades.calles[int(calle_maximo)], cantidad)

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