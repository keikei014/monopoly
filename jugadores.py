from random import randint
from time import sleep
from fuzzy import venta_calle_Fuzzy, poner_casas_Fuzzy
from casillas import Calle, Estacion, Suerte, Carcel, AlaCarcel

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
        # sleep(3.0)
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

    def jugarTurno(self, partida, queue):
        print(f"El jugador {self.id + 1} se lo está pensando...\n")
        # sleep(1.0)
        print(f"El jugador {self.id + 1} ha tirado el dado!\n")

        tirada, dobles = self.tirarDado(partida)
        if self.carcel == 0:
            casilla = partida.moverJugador(self.id, tirada)
            if dobles:
                print("Has sacado dobles!\n")
                
        else:
            partida.manejarCarcel(self.id, tirada, dobles)
               
        self.evaluarCasilla(partida, casilla)
            
        queue.put(partida)
        

    def evaluarCasilla(self, partida, casilla):
       casilla_actual = partida.tablero[casilla]
       
       self.venderProp(partida) #analizamos si necesitamos vender antes de hacer cualquier otra acción.
    
       self.ponerCasa(partida) #analizamos si podemos poner casa antes de hacer cualquier otra acción.
       
       if isinstance(casilla_actual, Calle):
                self.comprarCalle(partida, casilla_actual)
                
       elif isinstance(casilla_actual, Estacion):
                self.comprarEstacion(partida, casilla_actual)
                        
       elif isinstance(casilla_actual, Suerte):
           casilla_actual.activarEfecto(partida, self.id)   
            
       elif isinstance(casilla_actual, AlaCarcel):
            casilla_actual.activarEfecto(partida, self.id)
            
       elif isinstance(casilla_actual, Carcel):
            casilla_actual.activarEfecto(partida, self.id)


    def comprarCalle(self, partida, casilla):
        if self.dinero >= casilla.precio:
            print(f"El jugador {self.id + 1} decide comprar {casilla.nombre}.")
            partida.tablero[casilla.id].activarEfectoIA(partida, self.id)

        else:
            print(f"El jugador {self.id + 1} no tiene suficiente dinero para comprar {casilla.nombre}.")
            
    def comprarEstacion(self, partida, casilla):
        if self.dinero >= casilla.precio:
            print(f"El jugador {self.id + 1} decide comprar la estación {casilla.nombre}.")
            partida.tablero[casilla.id].activarEfectoIA(partida, self.id)
        else:
            print(f"El jugador {self.id + 1} no tiene suficiente dinero para comprar la estación {casilla.nombre}.")            
                    
    def venderProp(self, partida):
        # Define el umbral mínimo de dinero antes de considerar vender propiedades
        umbral_vender = 300  

        # Verifica si el dinero del jugador está por debajo del umbral
        if self.dinero < umbral_vender:
            # Intenta vender una estación primero
            if self.propiedades.estaciones:
                estacion_a_vender = self.propiedades.estaciones[0]  # Vende la primera estación
                print(f"El jugador IA {self.id + 1} vende la estación {partida.tablero[estacion_a_vender].nombre} por {partida.tablero[estacion_a_vender].precio / 2} dolaritos.")
                partida.venderEstacion(estacion_a_vender, self.id)
            # Si no hay estaciones, intenta vender una calle
            elif self.propiedades.calles:
                calle_a_vender = self.propiedades.calles[0]  # Vende la primera calle
                print(f"El jugador IA {self.id + 1} vende la calle {partida.tablero[calle_a_vender].nombre} por {partida.tablero[calle_a_vender].precio / 2} dolaritos.")
                partida.venderCalle(calle_a_vender, self.id)

    def ponerCasa(self, partida):
        # Decidir en qué calle construir basado en reglas específicas
        for id_calle in self.propiedades.calles:
            calle = partida.tablero[id_calle]
            costo_casa = calle.precioCasa

            # Verificar si tiene suficiente dinero para construir una casa
            if self.dinero >= costo_casa:
                # Decidir cuántas casas construir
                cantidad_casas = 1  # Por simplicidad, construye solo una casa

                # Actualizar el dinero y construir la casa
                self.dinero -= costo_casa * cantidad_casas
                partida.añadirCasa(self.id, id_calle, cantidad_casas)

                print(f"El jugador IA {self.id + 1} ha construido {cantidad_casas} casa(s) en {calle.nombre} gastando {costo_casa * cantidad_casas} dolaritos.")
                break  # Romper el bucle después de construir

class Jugador_IAlisto(Jugador):
      
    
    def __init__(self, nombre, id):
        self.nombre = nombre
        self.id = id
        self.propiedades = Propiedades()

    def jugarTurno(self, partida, queue):
        print(f"El jugador {self.id + 2} se lo está pensando...\n")
        # sleep(1.0)
        print(f"El jugador {self.id + 2} ha tirado el dado!\n")

        tirada, dobles = self.tirarDado(partida)
        if self.carcel == 0:
            casilla = partida.moverJugador(self.id, tirada)
            if dobles:
                print("Has sacado dobles!\n")
                
        else:
            partida.manejarCarcel(self.id, tirada, dobles)
               
        self.evaluarCasilla(partida, casilla)
            
        queue.put(partida)
        

    def evaluarCasilla(self, partida, casilla):
       casilla_actual = partida.tablero[casilla]
       
       self.venderProp(partida) #analizamos si necesitamos vender antes de hacer cualquier otra acción.
    
       self.ponerCasa(partida) #analizamos si podemos poner casa antes de hacer cualquier otra acción.
       
       if isinstance(casilla_actual, Calle):
                self.comprarCalle(partida, casilla_actual)
                
       elif isinstance(casilla_actual, Estacion):
                self.comprarEstacion(partida, casilla_actual)
                        
       elif isinstance(casilla_actual, Suerte):
           casilla_actual.activarEfecto(partida, self.id)   
            
       elif isinstance(casilla_actual, AlaCarcel):
            casilla_actual.activarEfecto(partida, self.id)
            
       elif isinstance(casilla_actual, Carcel):
            casilla_actual.activarEfecto(partida, self.id)



 ##################    COMPRA CALLES      ################################################# 
    def comprarCalle(self, partida, casilla):
         margen_seguridad = 500  # Mantener una reserva de dinero después de la compra

         if self.dinero >= casilla.precio + margen_seguridad:
            if self.bloquearOponente(partida, casilla) or self.esCompraEstrategica(partida, casilla):
                print(f"El jugador {self.id + 2} decide comprar {casilla.nombre}.")
                partida.tablero[casilla.id].activarEfectoIA(partida, self.id)
            else:
                print(f"El jugador {self.id + 2} decide no comprar {casilla.nombre} a pesar de tener suficientes fondos.")
         else:
            print(f"El jugador {self.id + 2} no tiene suficiente dinero para comprar {casilla.nombre}.")

          
    def bloquearOponente(self, partida, casilla):
        calles_del_mismo_barrio = [c for c in partida.tablero if isinstance(c, Calle) and c.barrio == casilla.barrio]

        for calle in calles_del_mismo_barrio:
            if calle.propietario and calle.propietario != self.id:
                propiedades_oponente = sum(1 for c in calles_del_mismo_barrio if c.propietario == calle.propietario)
                if propiedades_oponente == len(calles_del_mismo_barrio) - 1:
                    return True  # Comprar para bloquear a un oponente
        return False
         
    def esCompraEstrategica(self, partida, casilla):
        
        calles_del_mismo_barrio = [c for c in partida.tablero if isinstance(c, Calle) and c.barrio == casilla.barrio]
        calles_compradas = sum(1 for c in calles_del_mismo_barrio if c.propietario == self.id)

        if calles_compradas == len(calles_del_mismo_barrio) - 1:
            return True

        retorno_inversion = sum(casilla.alquiler) / casilla.precio
        if retorno_inversion > 0.10:  # umbral_retorno es un valor que decides tú
            return True
        
        total_barrios = set(c.barrio for c in partida.tablero if isinstance(c, Calle))
        propiedades_por_barrio = {barrio: 0 for barrio in total_barrios}

        for propiedad in self.propiedades.calles:
            barrio_actual = partida.tablero[propiedad].barrio
            propiedades_por_barrio[barrio_actual] += 1

        barrio_casilla_actual = casilla.barrio

        if propiedades_por_barrio[barrio_casilla_actual] < min(propiedades_por_barrio.values()):
            return True

        return False       
     
 ##################    COMPRA ESTACIONES     ################################################# 
    def comprarEstacion(self, partida, casilla):
        margen_seguridad = 500  # Mantener una reserva de dinero después de la compra

        if self.dinero >= casilla.precio + margen_seguridad and self.esCompraEstrategicaEstacion(partida, casilla):
            print(f"El jugador {self.id + 2} decide comprar la estación {casilla.nombre}.")
            partida.tablero[casilla.id].activarEfectoIA(partida, self.id)
        else:
            print(f"El jugador {self.id + 2} no tiene suficiente dinero para comprar la estación {casilla.nombre}.")

    def esCompraEstrategicaEstacion(self, partida, casilla):
        estaciones_poseidas = sum(1 for c in self.propiedades.estaciones)
        estaciones_oponentes = sum(1 for c in partida.tablero if isinstance(c, Estacion) and c.propietario and c.propietario != self.id)

        # Estrategia basada en el número de estaciones poseídas
        if estaciones_poseidas >= 0:
            return True

        # Estrategia para prevenir que los oponentes completen su conjunto de estaciones
        if estaciones_oponentes >= 1:
            return True           
        
          
   ##################    VENTA      #################################################  
    def venderProp(self, partida):
        # Define el umbral mínimo de dinero antes de considerar vender propiedades
        umbral_vender = 300  

        # Verifica si el dinero del jugador está por debajo del umbral
        if self.dinero < umbral_vender:
            propiedad_a_vender = self.elegirPropiedadOptimaParaVender(partida)

            if propiedad_a_vender:
                tipo_propiedad = type(partida.tablero[propiedad_a_vender]).__name__
                print(f"El jugador IA {self.id + 2} vende la {tipo_propiedad} {partida.tablero[propiedad_a_vender].nombre} por {partida.tablero[propiedad_a_vender].precio / 2} dolaritos.")
                
                if tipo_propiedad == 'Estacion':
                    partida.venderEstacion(propiedad_a_vender, self.id)
                elif tipo_propiedad == 'Calle':
                    partida.venderCalle(propiedad_a_vender, self.id)


    def elegirPropiedadOptimaParaVender(self, partida):
        propiedades_por_barrio = {}
        for id_calle in self.propiedades.calles:
            barrio = partida.tablero[id_calle].barrio
            if barrio in propiedades_por_barrio:
                propiedades_por_barrio[barrio].append(id_calle)
            else:
                propiedades_por_barrio[barrio] = [id_calle]

     
        for barrio, propiedades in propiedades_por_barrio.items():
            if len(propiedades) == 1:
                return propiedades[0]  
      
        propiedad_min_ingreso = min(self.propiedades.calles, key=lambda id: sum(partida.tablero[id].alquiler), default=None)

        return propiedad_min_ingreso

 ##################    PONER CASAS      ################################################# 
    def ponerCasa(self, partida):
        propiedades_optimas = self.elegirMejoresPropiedadesParaConstruir(partida)

        for id_calle in propiedades_optimas:
            calle = partida.tablero[id_calle]
            costo_casa = calle.precioCasa

           
            if self.dinero >= costo_casa:
                cantidad_casas = self.calcularCantidadCasas(calle, partida)

                self.dinero -= costo_casa * cantidad_casas
                partida.añadirCasa(self.id, id_calle, cantidad_casas)

                print(f"El jugador IA {self.id + 2} ha construido {cantidad_casas} casa(s) en {calle.nombre} gastando {costo_casa * cantidad_casas} dolaritos.")
                break  

    def elegirMejoresPropiedadesParaConstruir(self, partida):
        
        propiedades_optimas = []
        for id_calle in self.propiedades.calles:
            calle = partida.tablero[id_calle]
            if self.esConjuntoCompleto(calle.barrio, partida):
                propiedades_optimas.append(id_calle)
        return propiedades_optimas

    def esConjuntoCompleto(self, barrio, partida):
        calles_del_barrio = [c.id for c in partida.tablero if isinstance(c, Calle) and c.barrio == barrio]
        return all(partida.tablero[id_calle].propietario == self.id for id_calle in calles_del_barrio)

    def calcularCantidadCasas(self, calle, partida):
        return 1 if self.dinero >= calle.precioCasa * 2 else 0