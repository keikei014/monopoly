from partida import Partida
from threading import Thread
from queue import Queue
from casillas import Suerte, AlaCarcel, Carcel, Estacion, Inicio, Calle
from jugadores import Jugador_IA, Jugador_IAlisto, Jugador_Fuzzy
from pandas import DataFrame

# Crear jugadores



jugador1 = Jugador_IA("Jugador1", 0)
jugador2 = Jugador_IAlisto("Jugador2", 1)
jugador3= Jugador_Fuzzy("Jugador3", 2)
jugadores = [jugador1, jugador2, jugador3]
    

# Inicializar tablero
tablero = [Suerte("init", 0)]*24
tablero[0] = Inicio("Inicio", 0)
tablero[1] = Calle("jeketiezo", 1, 0, 50, [10, 30, 50, 70, 100, 120])
tablero[2] = Suerte("Suerte1",2)
tablero[3] = Estacion("Ozarberto", 3)
tablero[4] = Calle("superboke", 4, 0, 50, [10, 30, 50, 70, 100, 120])
tablero[5] = Calle("cortijo", 5, 0, 80, [15, 35, 60, 80, 120, 150])
tablero[6] = Carcel("AlaCarcel", 6)
tablero[7] = Calle("AveMaria", 7, 1, 100, [20, 40, 70, 95, 150, 200])
tablero[8] = Suerte("Suerte2", 8)
tablero[9] = Estacion("Pellisex", 9)
tablero[10] = Calle("Ranal", 10, 1, 100, [20, 40, 70, 95, 150, 200])
tablero[11] = Calle("La Muela", 11, 1, 120, [25, 50, 85, 110, 170, 240])
tablero[12] = Suerte("SuerteParking", 12)
tablero[13] = Calle("Teatinos", 13, 2, 150, [40, 70, 100, 150, 210, 300])
tablero[14] = Calle("Trinidad", 14, 2, 150, [40, 70, 100, 150, 210, 300])
tablero[15] = Estacion("VictorSanchezdelAmo", 15)
tablero[16] = Suerte("Suerte3", 16)
tablero[17] = Calle("Victoria", 17, 2, 200, [55, 90, 120, 180, 250, 360])
tablero[18] = AlaCarcel("Enchironao", 18)
tablero[19] = Calle("Sekiro", 19, 3, 250, [70, 105, 150, 220, 280, 400])
tablero[20] = Calle("Blodbor", 20, 3, 250, [70, 105, 150, 220, 280, 400])
tablero[21] = Estacion("Pellegrini", 21)
tablero[22] = Suerte("Suerte4", 22)
tablero[23] = Calle("EldenRin", 23, 3, 300, [80, 105, 150, 20, 350, 500])

# Crear la partida
partida = Partida(tablero, jugadores)
dinero_j1 = [0]
dinero_j2 = [0]
dinero_j3 = [0]

est_j1 = [0]
est_j2 = [0]
est_j3 = [0]

calles_j1 = [0]
calles_j2 = [0]
calles_j3 = [0]

casas_j1 = [0]
casas_j2 = [0]
casas_j3 = [0]

q = Queue()

while(partida.nJugadores > 1):

    for jugador in partida.jugadores:
        if(jugador.arruinado == False):
            while(partida.turno_activo):
                turno = Thread(target=jugador.jugarTurno, args=[partida,q])
                turno.start()
                turno.join()
            
                partida_mod = q.get()
                partida = partida_mod
            
            partida.turno_activo = True
        
        if( partida.nJugadores == 1 ):
            break
    
    dinero_j1.append(partida.jugadores[0].dinero)
    dinero_j2.append(partida.jugadores[1].dinero)
    dinero_j3.append(partida.jugadores[2].dinero)

    est_j1.append(len(partida.jugadores[0].propiedades.estaciones))
    est_j2.append(len(partida.jugadores[1].propiedades.estaciones))
    est_j3.append(len(partida.jugadores[2].propiedades.estaciones))

    calles_j1.append(len(partida.jugadores[0].propiedades.calles))
    calles_j2.append(len(partida.jugadores[1].propiedades.calles))
    calles_j3.append(len(partida.jugadores[2].propiedades.calles))

    casas = 0
    for calle in partida.jugadores[0].propiedades.calles:
        casas += calle.nCasas
    casas_j1.append(casas)
    casas = 0
    for calle in partida.jugadores[1].propiedades.calles:
        casas += calle.nCasas
    casas_j2.append(casas)
    casas = 0
    for calle in partida.jugadores[2].propiedades.calles:
        casas += calle.nCasas
    casas_j3.append(casas)
    
    
df = DataFrame({'Jugador 1': dinero_j1, 'Jugador 2': dinero_j2, 'Jugador 3': dinero_j3})
df.to_excel('resultados.xlsx',sheet_name='dinero',index=False)
df = DataFrame({'Jugador 1': est_j1, 'Jugador 2': est_j2, 'Jugador 3': est_j3})
df.to_excel('resultados.xlsx',sheet_name='estaciones',index=False)
df = DataFrame({'Jugador 1': calles_j1, 'Jugador 2': calles_j2, 'Jugador 3': calles_j3})
df.to_excel('resultados.xlsx',sheet_name='calles',index=False)
df = DataFrame({'Jugador 1': casas_j1, 'Jugador 2': casas_j2, 'Jugador 3': casas_j3})
df.to_excel('resultados.xlsx',sheet_name='calles',index=False)

print("Se acabó! El ganador es el jugador %i!\n" % (partida.jugadores_activos[0]+1))