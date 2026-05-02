from abc import ABC, abstractmethod


class Componente(ABC):
    """
    Componente base del patrón Composite.

    Define la interfaz común para piezas simples
    y conjuntos compuestos.
    """

    def __init__(self, nombre: str):
        self.nombre = nombre

    @abstractmethod
    def mostrar(self, nivel: int = 0) -> None:
        """
        Muestra la estructura jerárquica.
        """
        pass


class Pieza(Componente):
    """
    Hoja del patrón Composite.

    Representa una pieza individual sin hijos.
    """

    def mostrar(self, nivel: int = 0) -> None:
        sangria = "   " * nivel
        print(f"{sangria}- Pieza: {self.nombre}")


class Conjunto(Componente):
    """
    Composite del patrón.

    Puede contener piezas o más subconjuntos.
    """

    def __init__(self, nombre: str):
        super().__init__(nombre)
        self.componentes = []

    def agregar(self, componente: Componente) -> None:
        """
        Agrega un componente hijo.
        """
        self.componentes.append(componente)

    def mostrar(self, nivel: int = 0) -> None:
        """
        Muestra el conjunto y luego sus hijos.
        """
        sangria = "   " * nivel
        print(f"{sangria}+ Conjunto: {self.nombre}")

        for componente in self.componentes:
            componente.mostrar(nivel + 1)


def main():
    """
    Construcción del ensamblado principal.
    """

    print("=== ENSAMBLADO INICIAL ===\n")

    # Producto principal
    producto = Conjunto("Producto Principal")

    # Crear 3 subconjuntos con 4 piezas cada uno
    for i in range(1, 4):
        subconjunto = Conjunto(f"Subconjunto {i}")

        for j in range(1, 5):
            pieza = Pieza(f"Pieza {i}.{j}")
            subconjunto.agregar(pieza)

        producto.agregar(subconjunto)

    # Mostrar estructura inicial
    producto.mostrar()

    print("\n=== AGREGANDO SUBCONJUNTO OPCIONAL ===\n")

    # Subconjunto opcional
    opcional = Conjunto("Subconjunto Opcional")

    for j in range(1, 5):
        opcional.agregar(Pieza(f"Pieza Opcional {j}"))

    producto.agregar(opcional)

    # Mostrar nueva estructura
    producto.mostrar()


if __name__ == "__main__":
    main()
