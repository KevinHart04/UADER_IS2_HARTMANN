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


arg = sys.argv[1]


# Comprobación de que el argumento no es solo un guión
if arg == "-":
    print("[x] Tenés que ingresar un número después del guión")
    sys.exit(1)


#lógica para leer -hasta
if arg.startswith("-"):
    try:
        num = int(arg[1:])
        if num <= 0:
            print("Debe informar un número entero positivo después del guión")
            sys.exit(1)
        
        inicio = 1
        fin = num
        
        for i in range(inicio, fin + 1):
            factorial_result = factorial(i)
            print(f"[-] Factorial de {i} = {factorial_result}")
        
        sys.exit()
        
    except ValueError:
        print("Debe informar un número entero válido")
        sys.exit(1)



# Lógica para leer rango "desde-hasta"

elif arg.count("-") == 1 and not arg.startswith("-") and not arg.endswith("-"):
    try:
        inicio_str, fin_str = arg.split("-")
        inicio = int(inicio_str)
        fin = int(fin_str)

        if inicio <= 0 or fin <= 0:
            print("Debe informar números enteros positivos en el rango")
            sys.exit(1)
        if inicio > fin:
            print("El número inicial debe ser menor o igual al final")
            sys.exit(1)
        for i in range(inicio, fin + 1):
            factorial_result = factorial(i)
            print(f"[-] Factorial de {i} = {factorial_result}")

        sys.exit()

    except ValueError:
        print("Debe informar un número entero válido para el rango")
        sys.exit(1)


# Lógica para leer -desde

elif arg.endswith("-"):
    try:
        num = int(arg[:-1])
        if num <= 0:
            print("Debe informar un número entero positivo antes del guión")
            sys.exit(1)
            
        inicio = num
        fin = 60
        
        for i in range(inicio, fin + 1):
            factorial_result = factorial(i)
            print(f"[-] Factorial de {i} = {factorial_result}")
            
        sys.exit()
        
    except ValueError:
        print("Debe informar un número entero válido")
        sys.exit(1)

# Caso donde se ingresa un número sin guiones
else:
    try:
        num = int(arg)
        factorial_result = factorial(num)
        print(f"[-] Factorial de {num} = {factorial_result}")
    except ValueError:
        print("Debe informar un número entero válido")
        sys.exit(1)



