from abc import ABC, abstractmethod


class TrenLaminador(ABC):
    """
    Implementador del patrón Bridge.
    Define el comportamiento común de cualquier tren laminador.
    """

    @abstractmethod
    def producir(self, espesor: float, ancho: float) -> None:
        """
        Produce una lámina con las dimensiones indicadas.
        """
        pass


class Tren5M(TrenLaminador):
    """
    Implementación concreta.
    Produce planchas de 5 metros de largo.
    """

    def producir(self, espesor: float, ancho: float) -> None:
        print(f"Produciendo lámina de {espesor}\" x {ancho}m x 5m")


class Tren10M(TrenLaminador):
    """
    Implementación concreta.
    Produce planchas de 10 metros de largo.
    """

    def producir(self, espesor: float, ancho: float) -> None:
        print(f"Produciendo lámina de {espesor}\" x {ancho}m x 10m")


class Lamina:
    """
    Abstracción del patrón Bridge.

    La lámina conoce sus dimensiones,
    pero delega la fabricación al tren laminador.
    """

    def __init__(self, espesor: float, ancho: float, tren: TrenLaminador):
        self.espesor = espesor
        self.ancho = ancho
        self.tren = tren

    def fabricar(self) -> None:
        """
        Solicita al tren laminador que fabrique la lámina.
        """
        self.tren.producir(self.espesor, self.ancho)


def main():
    """
    Punto de entrada principal del programa.
    Se prueban distintos trenes laminadores con la misma lámina.
    """

    print("=== SISTEMA DE PRODUCCIÓN DE LÁMINAS ===\n")

    # Caso 1:
    # Se usa el tren que fabrica planchas de 5 metros.
    print("Caso 1: Producción en tren laminador de 5 metros")
    tren_corto = Tren5M()
    lamina_corta = Lamina(0.5, 1.5, tren_corto)
    lamina_corta.fabricar()

    print()

    # Caso 2:
    # La misma lámina se fabrica en el tren de 10 metros.
    print("Caso 2: Producción en tren laminador de 10 metros")
    tren_largo = Tren10M()
    lamina_larga = Lamina(0.5, 1.5, tren_largo)
    lamina_larga.fabricar()

    print()

    # Caso 3:
    # Demostración del Bridge:
    # La abstracción Lamina no cambia,
    # solo se reemplaza la implementación del tren.
    print("Caso 3: Cambio dinámico de tren laminador")
    lamina_variable = Lamina(0.5, 1.5, tren_corto)
    lamina_variable.fabricar()

    print("Cambiando al tren de 10 metros...")
    lamina_variable.tren = tren_largo
    lamina_variable.fabricar()


if __name__ == "__main__":
    main()
