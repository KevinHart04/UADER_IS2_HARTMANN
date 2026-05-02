from abc import ABC, abstractmethod


class NumeroBase(ABC):
    """
    Componente base del patrón Decorator.

    Define la interfaz común para el número base
    y para los decoradores.
    """

    @abstractmethod
    def mostrar(self) -> float:
        """
        Retorna el valor actual del número.
        """
        pass


class Numero(NumeroBase):
    """
    Componente concreto.

    Representa un número simple sin modificaciones.
    """

    def __init__(self, valor: float):
        self.valor = valor

    def mostrar(self) -> float:
        return self.valor


class DecoradorNumero(NumeroBase):
    """
    Decorador base.

    Mantiene una referencia al objeto decorado.
    """

    def __init__(self, numero: NumeroBase):
        self.numero = numero


class SumarDos(DecoradorNumero):
    """
    Decorador concreto.

    Suma 2 al valor recibido.
    """

    def mostrar(self) -> float:
        return self.numero.mostrar() + 2


class MultiplicarPorDos(DecoradorNumero):
    """
    Decorador concreto.

    Multiplica por 2 el valor recibido.
    """

    def mostrar(self) -> float:
        return self.numero.mostrar() * 2


class DividirPorTres(DecoradorNumero):
    """
    Decorador concreto.

    Divide por 3 el valor recibido.
    """

    def mostrar(self) -> float:
        return self.numero.mostrar() / 3


def main():
    """
    Prueba del patrón Decorator aplicando
    operaciones encadenadas sobre un número.
    """

    print("=== PATRÓN DECORATOR CON NÚMEROS ===\n")

    # Número original
    numero = Numero(9)

    print("Caso 1: Número sin decoradores")
    print("Resultado:", numero.mostrar())

    print("\nCaso 2: Sumarle 2")
    n1 = SumarDos(numero)
    print("Resultado:", n1.mostrar())

    print("\nCaso 3: Multiplicarlo por 2")
    n2 = MultiplicarPorDos(numero)
    print("Resultado:", n2.mostrar())

    print("\nCaso 4: Dividirlo por 3")
    n3 = DividirPorTres(numero)
    print("Resultado:", n3.mostrar())

    print("\nCaso 5: Decoración anidada")
    print("((9 + 2) * 2) / 3")

    anidado = DividirPorTres(
        MultiplicarPorDos(
            SumarDos(numero)
        )
    )

    print("Resultado:", anidado.mostrar())

    print("\nCaso 6: Otro orden de decoración")
    print("(9 / 3) + 2")

    otro = SumarDos(
        DividirPorTres(numero)
    )

    print("Resultado:", otro.mostrar())


if __name__ == "__main__":
    main()
