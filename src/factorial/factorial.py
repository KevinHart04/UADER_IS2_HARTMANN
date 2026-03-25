#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial.py                                                            *
#* calcula el factorial de un número                                       *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*
import sys
def factorial(num): 
    if num < 0: 
        print("Factorial de un número negativo no existe")
        return 0
    elif num == 0: 
        return 1
        
    else: 
        fact = 1
        while(num > 1): 
            fact *= num 
            num -= 1
        return fact 


# 1. Verificar argumento
if len(sys.argv) < 2:
    print("[x] Tenés que ingresar un número como argumento")
    sys.exit()

try:
    num = int(sys.argv[1])


    if num < 0:
        print("Factorial de un número negativo no existe")
        sys.exit()

    if not (4 <= num <= 8):
        print("Número fuera de rango, debe ser entre 4 y 8")
        sys.exit()
    factorial_result = factorial(num)
    print("Factorial de", num, "es", factorial_result)

except ValueError:
    print("Debe informar un número entero válido")

