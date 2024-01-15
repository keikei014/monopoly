import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def comprar_calle_fuzzy(dinero_val, calles_val, estaciones_val):
    # Definir las variables de entrada
    dinero = ctrl.Antecedent(np.arange(0, 20000, 1), 'dinero')
    calles = ctrl.Antecedent(np.arange(0, 12, 1), 'calles')
    estaciones = ctrl.Antecedent(np.arange(0, 4, 1), 'estaciones')

    dinero['muy_poco'] = fuzz.trimf(dinero.universe, [0, 250, 500])
    dinero['poco'] = fuzz.trimf(dinero.universe, [250, 750, 1000])
    dinero['dinero_medio'] = fuzz.trimf(dinero.universe, [750, 1500, 2250])
    dinero['mucho_dinero'] = fuzz.trimf(dinero.universe, [1500, 2250, 2500])
    dinero['muchisimo_dinero'] = fuzz.trimf(dinero.universe, [2250, 20000, 20000])
    
    calles.automf(5, names=['muy_pocas','pocas','medio','muchas','muchisimas'])
    estaciones.automf(3, names =['pocas', 'medio', 'muchas'])

    # Definir las variables de salida
    comprar_calle = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'comprar_calle')

    # Definir las funciones de membresía para las salidas
    comprar_calle['no_comprar'] = fuzz.trimf(comprar_calle.universe, [0, 0, 0.35])
    comprar_calle['comprar'] = fuzz.trimf(comprar_calle.universe, [0, 0.65, 1])

    # Reglas difusas
    regla1 = ctrl.Rule(dinero['muy_poco'], comprar_calle['no_comprar'])
    regla2 = ctrl.Rule(dinero['muy_poco'] & (calles['muchas'] | estaciones['medio']), comprar_calle['no_comprar'])
    regla3 = ctrl.Rule(dinero['poco'] & (calles['muchisimas'] & estaciones['muchas']), comprar_calle['no_comprar'])
    regla4 = ctrl.Rule(dinero['poco'] & calles['muy_pocas'] & estaciones['pocas'], comprar_calle['comprar'])
    regla5 = ctrl.Rule(dinero['poco'] & calles['pocas'] & estaciones['pocas'], comprar_calle['comprar'])
    regla6 = ctrl.Rule(dinero['poco'] & calles['medio'] & estaciones['pocas'], comprar_calle['comprar'])
    regla7 = ctrl.Rule(dinero['poco'] & calles['medio'] & estaciones['medio'], comprar_calle['comprar'])
    regla8 = ctrl.Rule(dinero['poco'] & calles['muchas'] & estaciones['medio'], comprar_calle['no_comprar'])
    regla9 = ctrl.Rule(dinero['dinero_medio'], comprar_calle['comprar'])
    regla10 = ctrl.Rule(dinero['dinero_medio'] & calles['muy_pocas'] & estaciones['pocas'], comprar_calle['comprar'])
    regla11 = ctrl.Rule(dinero['dinero_medio'] & calles['pocas'] & estaciones['pocas'], comprar_calle['comprar'])
    regla12 = ctrl.Rule(dinero['dinero_medio'] & calles['medio'] & estaciones['pocas'], comprar_calle['comprar'])
    regla13 = ctrl.Rule(dinero['dinero_medio'] & calles['muchisimas'] & estaciones['muchas'], comprar_calle['comprar'])
    regla14 = ctrl.Rule(dinero['dinero_medio'] & calles['muchas'] & estaciones['muchas'], comprar_calle['comprar'])
    regla15 = ctrl.Rule(dinero['mucho_dinero'], comprar_calle['comprar'])
    regla16 = ctrl.Rule(dinero['mucho_dinero'] &  calles['muy_pocas'] & estaciones['pocas'], comprar_calle['comprar'])
    regla17 = ctrl.Rule(dinero['mucho_dinero'] &  calles['pocas'] & estaciones['pocas'], comprar_calle['comprar'])
    regla18 = ctrl.Rule(dinero['mucho_dinero'] &  calles['muchas'] & estaciones['muchas'], comprar_calle['comprar'])
    regla19 = ctrl.Rule(dinero['mucho_dinero'] &  calles['muchisimas'] & estaciones['muchas'], comprar_calle['comprar'])
    regla20 = ctrl.Rule(dinero['muchisimo_dinero'], comprar_calle['comprar'])

    # Sistema de control difuso
    sistema_comprar_calle = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5, regla6, regla7, regla8, regla9, regla10, regla11, regla12, regla13, regla14, regla15, regla16, regla17, regla18, regla19, regla20])

    # Simulador
    simulador_comprar_calle = ctrl.ControlSystemSimulation(sistema_comprar_calle)

    # Establecer los valores de entrada
    simulador_comprar_calle.input['dinero'] = dinero_val
    simulador_comprar_calle.input['calles'] = calles_val
    simulador_comprar_calle.input['estaciones'] = estaciones_val

    # Calcular la salida difusa
    simulador_comprar_calle.compute()

    salida_compra = simulador_comprar_calle.output['comprar_calle']

    if salida_compra > 0.35:
        salida_compra = 1
    else: 
        salida_compra = 0

    # Devolver el resultado
    return salida_compra


def comprar_estaciones_fuzzy(dinero_val, calles_val, estaciones_val):
    # Definir las variables de entrada
    dinero = ctrl.Antecedent(np.arange(0, 20000, 1), 'dinero')
    calles = ctrl.Antecedent(np.arange(0, 12, 1), 'calles')
    estaciones = ctrl.Antecedent(np.arange(0, 4, 1), 'estaciones')

    dinero['muy_poco'] = fuzz.trimf(dinero.universe, [0, 250, 500])
    dinero['poco'] = fuzz.trimf(dinero.universe, [250, 750, 1000])
    dinero['dinero_medio'] = fuzz.trimf(dinero.universe, [750, 1500, 2250])
    dinero['mucho_dinero'] = fuzz.trimf(dinero.universe, [1500, 2250, 2500])
    dinero['muchisimo_dinero'] = fuzz.trimf(dinero.universe, [2250, 20000, 20000])

    calles.automf(5, names=['muy_pocas','pocas','medio','muchas','muchisimas'])
    estaciones.automf(3, names =['pocas', 'medio', 'muchas'])

    # Definir las variables de salida
    comprar_estacion = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'comprar_estacion')

    # Definir las funciones de membresía para las salidas
    comprar_estacion['no_comprar'] = fuzz.trimf(comprar_estacion.universe, [0, 0, 0.35])
    comprar_estacion['comprar'] = fuzz.trimf(comprar_estacion.universe, [0, 0.65, 1])

    # Reglas difusas
    regla1 = ctrl.Rule(dinero['muy_poco'], comprar_estacion['no_comprar'])
    regla2 = ctrl.Rule(dinero['poco'] & calles['muy_pocas'] & estaciones['pocas'], comprar_estacion['comprar'])
    regla3 = ctrl.Rule(dinero['poco'] & (calles['muchas'] & estaciones['muchas']), comprar_estacion['no_comprar'])
    regla4 = ctrl.Rule(dinero['poco'] & (calles['medio'] & estaciones['medio']), comprar_estacion['no_comprar'])
    regla5 = ctrl.Rule(dinero['mucho_dinero'] & calles['muchisimas'] & estaciones['muchas'], comprar_estacion['comprar'])
    regla6 = ctrl.Rule(dinero['dinero_medio'] & calles['medio'] & estaciones['medio'], comprar_estacion['comprar'])
    regla7 = ctrl.Rule(dinero['dinero_medio'] & (calles['pocas'] | estaciones['medio']), comprar_estacion['comprar'])
    regla8 = ctrl.Rule(dinero['dinero_medio'] & (calles['muchas'] & estaciones['medio']), comprar_estacion['comprar'])
    regla9 = ctrl.Rule(dinero['mucho_dinero'] & (calles['muchisimas'] | estaciones['muchas']), comprar_estacion['comprar'])
    regla10 = ctrl.Rule(dinero['mucho_dinero'] & (calles['pocas'] | estaciones['pocas']), comprar_estacion['comprar'])
    regla11 = ctrl.Rule(dinero['muchisimo_dinero'], comprar_estacion['comprar'])


    # Sistema de control difuso
    sistema_comprar_estacion = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5, regla6, regla7, regla8, regla9, regla10, regla11])

    # Simulador
    simulador_comprar_estacion = ctrl.ControlSystemSimulation(sistema_comprar_estacion)

    # Establecer los valores de entrada
    simulador_comprar_estacion.input['dinero'] = dinero_val
    simulador_comprar_estacion.input['calles'] = calles_val
    simulador_comprar_estacion.input['estaciones'] = estaciones_val

    # Calcular la salida difusa
    simulador_comprar_estacion.compute()

    salida_estacion = simulador_comprar_estacion.output['comprar_estacion']

    if salida_estacion > 0.35:
        salida_estacion = 1
    else: 
        salida_estacion = 0

    # Devolver el resultado
    return salida_estacion


def venta_calle_Fuzzy(dinero_val, calles_val, estaciones_val):
    # Definir las variables de entrada
    dinero = ctrl.Antecedent(np.arange(0, 20000, 1), 'dinero')
    calles = ctrl.Antecedent(np.arange(0, 12, 1), 'calles')
    estaciones = ctrl.Antecedent(np.arange(0, 4, 1), 'estaciones')

    dinero['muy_poco'] = fuzz.trimf(dinero.universe, [0, 250, 500])
    dinero['poco'] = fuzz.trimf(dinero.universe, [250, 750, 1000])
    dinero['dinero_medio'] = fuzz.trimf(dinero.universe, [750, 1500, 2250])
    dinero['mucho_dinero'] = fuzz.trimf(dinero.universe, [1500, 2250, 2500])
    dinero['muchisimo_dinero'] = fuzz.trimf(dinero.universe, [2250, 20000, 20000])

    calles.automf(5, names=['muy_pocas','pocas','medio','muchas','muchisimas'])
    estaciones.automf(3, names =['pocas', 'medio', 'muchas'])

    # Definir las variables de salida
    venta_calle = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'venta_calle')

    # Definir las funciones de membresía para las salidas
    venta_calle['no_vender'] = fuzz.trimf(venta_calle.universe, [0, 0, 0.35])
    venta_calle['vender'] = fuzz.trimf(venta_calle.universe, [0, 0.65, 1])

    # Reglas:
    regla1 = ctrl.Rule(dinero['muy_poco'], venta_calle['vender'])
    regla2 = ctrl.Rule(dinero['poco'] & calles['muy_pocas'] & estaciones['pocas'], venta_calle['no_vender'])
    regla3 = ctrl.Rule(dinero['poco'] & (calles['pocas'] | estaciones['medio']), venta_calle['no_vender'])
    regla4 = ctrl.Rule(dinero['poco'] & (calles['muchas'] | estaciones['medio']), venta_calle['no_vender'])
    regla5 = ctrl.Rule(dinero['poco'] & (calles['muchisimas'] | estaciones['medio']), venta_calle['no_vender'])
    regla6 = ctrl.Rule(dinero['poco'] & (calles['medio'] | estaciones['muchas']), venta_calle['no_vender'])
    regla7 = ctrl.Rule(dinero['dinero_medio'], venta_calle['no_vender'])
    regla8 = ctrl.Rule(dinero['mucho_dinero'], venta_calle['no_vender'])
    regla9 = ctrl.Rule(dinero['muchisimo_dinero'], venta_calle['no_vender'])

    # Sistema de control difuso
    sistema_venta_calle = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5, regla6, regla7, regla8, regla9])

    # Simulador
    simulador_venta_calle = ctrl.ControlSystemSimulation(sistema_venta_calle)

    # Establecer los valores de entrada
    simulador_venta_calle.input['dinero'] = dinero_val
    simulador_venta_calle.input['calles'] = calles_val
    simulador_venta_calle.input['estaciones'] = estaciones_val

    # Calcular la salida difusa
    simulador_venta_calle.compute()

    salida_venta = simulador_venta_calle.output['venta_calle']

    if salida_venta > 0.5:
        salida_venta = 1
    else: 
        salida_venta = 0

    # Devolver el resultado
    return salida_venta



def poner_casas_Fuzzy(dinero_val, calles_val, estaciones_val):
    # Definir las variables de entrada
    dinero = ctrl.Antecedent(np.arange(0, 20000, 1), 'dinero')
    calles = ctrl.Antecedent(np.arange(0, 12, 1), 'calles')
    estaciones = ctrl.Antecedent(np.arange(0, 4, 1), 'estaciones')

    dinero['muy_poco'] = fuzz.trimf(dinero.universe, [0, 250, 500])
    dinero['poco'] = fuzz.trimf(dinero.universe, [250, 750, 1000])
    dinero['dinero_medio'] = fuzz.trimf(dinero.universe, [750, 1500, 2250])
    dinero['mucho_dinero'] = fuzz.trimf(dinero.universe, [1500, 2250, 2500])
    dinero['muchisimo_dinero'] = fuzz.trimf(dinero.universe, [2250, 20000, 20000])

    calles.automf(5, names=['muy_pocas','pocas','medio','muchas','muchisimas'])
    estaciones.automf(3, names =['pocas', 'medio', 'muchas'])

    # Definir las variables de salida
    poner_casas = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'poner_casas')

    # Definir las funciones de membresía para las salidas
    poner_casas['no_poner'] = fuzz.trimf(poner_casas.universe, [0, 0, 0.35])
    poner_casas['poner'] = fuzz.trimf(poner_casas.universe, [0, 0.65, 1])

    # Definición de reglas:
    regla1 = ctrl.Rule(dinero['muy_poco'], poner_casas['no_poner'])
    regla2 = ctrl.Rule(dinero['poco'] & calles['muy_pocas'] & estaciones['pocas'], poner_casas['no_poner'])
    regla3 = ctrl.Rule(dinero['poco'] & (calles['pocas'] | estaciones['medio']), poner_casas['no_poner'])
    regla4 = ctrl.Rule(dinero['poco'] & (calles['muchas'] | estaciones['medio']), poner_casas['no_poner'])
    regla5 = ctrl.Rule(dinero['poco'] & (calles['muchisimas'] | estaciones['medio']), poner_casas['no_poner'])
    regla6 = ctrl.Rule(dinero['poco'] & (calles['medio'] | estaciones['muchas']), poner_casas['no_poner'])
    regla7 = ctrl.Rule(dinero['dinero_medio'], poner_casas['no_poner'])
    regla8 = ctrl.Rule(dinero['mucho_dinero'], poner_casas['poner'])
    regla9 = ctrl.Rule(dinero['muchisimo_dinero'], poner_casas['poner'])

    # Sistema de control difuso
    sistema_poner_casas = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5, regla6, regla7, regla8, regla9])

    # Simulador
    simulador_poner_casas = ctrl.ControlSystemSimulation(sistema_poner_casas)

    # Establecer los valores de entrada
    simulador_poner_casas.input['dinero'] = dinero_val
    simulador_poner_casas.input['calles'] = calles_val
    simulador_poner_casas.input['estaciones'] = estaciones_val

    # Calcular la salida difusa
    simulador_poner_casas.compute()

    salida_poner_casas = simulador_poner_casas.output['poner_casas']

    if salida_poner_casas > 0.5:
        salida_poner_casas = 1
    else: 
        salida_poner_casas = 0

    # Devolver el resultado
    return salida_poner_casas