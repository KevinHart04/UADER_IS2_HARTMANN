#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial_OOP.py                                                        *
#* calcula el factorial de un número usando POO                            *
#*-------------------------------------------------------------------------*

import sys

class Factorial:
    def __init__(self):
        """Inicializa la clase Factorial"""
        pass
    
    def factorial(self, n):
        """
        Calcula el factorial de un número entero.
        
        Args:
            n (int): número entero
        
        Returns:
            int: factorial de n
        """
        if n < 0:
            raise ValueError("Factorial de un número negativo no existe")
        elif n == 0 or n == 1:
            return 1
        else:
            result = 1
            for i in range(2, n + 1):
                result *= i
            return result
    
    def run(self, start, end):
        """
        Calcula los factoriales en el rango [start, end].
        
        Args:
            start (int): inicio del rango
            end (int): fin del rango
        """
        if start <= 0 or end <= 0:
            raise ValueError("Debe informar números enteros positivos para el rango")
        
        if start > end:
            raise ValueError("El número inicial del rango no puede ser mayor que el número final")
        
        for i in range(start, end + 1):
            result = self.factorial(i)
            print(f"[-] Factorial de {i} = {result}")


# ---------------------- MAIN ----------------------

calculator = Factorial()

# Verificar argumento
if len(sys.argv) < 2:
    print("[x] Tenés que ingresar un número como argumento")
    sys.exit()

arg = sys.argv[1]

# Caso inválido "-"
if arg == "-":
    print("[x] Tenés que ingresar un número después del guión")
    sys.exit(1)

# Caso "-hasta" (ej: -10)
if arg.startswith("-"):
    try:
        num = int(arg[1:])
    except ValueError:
        print("Debe informar un número entero válido")
        sys.exit(1)

    if num <= 0:
        print("Debe informar un número entero positivo después del guión")
        sys.exit(1)

    try:
        calculator.run(1, num)
    except ValueError as e:
        print(f"[x] Error: {e}")
        sys.exit(1)

# Caso "desde-" (ej: 10-)
elif arg.endswith("-"):
    try:
        num = int(arg[:-1])
    except ValueError:
        print("Debe informar un número entero válido")
        sys.exit(1)

    if num <= 0:
        print("Debe informar un número entero positivo antes del guión")
        sys.exit(1)

    try:
        calculator.run(num, 60)
    except ValueError as e:
        print(f"[x] Error: {e}")
        sys.exit(1)

# Caso número normal
else:
    try:
        num = int(arg)
        result = calculator.factorial(num)
        print(f"[-] Factorial de {num} = {result}")
    except ValueError as e:
        print(f"[x] Error: {e}")
        sys.exit(1)