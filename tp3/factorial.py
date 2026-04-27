class Factorial():
    """Clase para calcular el factorial de un número utilizando el patrón Singleton."""
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia
    
    def calcular_factorial(self, n):
        """Calcula el factorial de un número dado."""
        if n < 0:
            raise ValueError("El factorial no está definido para números negativos.")
        elif n == 0 or n == 1:
            return 1
        else:
            resultado = 1
            for i in range(2, n + 1):
                resultado *= i
            return resultado

def main():
    factorial_calculator1 = Factorial()
    factorial_calculator2 = Factorial()
    print(f"¿Son la misma instancia? {factorial_calculator1 is factorial_calculator2}")
    numero = int(input("Ingrese un número para calcular su factorial: "))
    resultado = factorial_calculator1.calcular_factorial(numero)
    print(f"El factorial de {numero} es: {resultado}")

if __name__ == "__main__":
    main()