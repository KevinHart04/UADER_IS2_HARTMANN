import copy

class Prototype:
    """
    Clase que implementa el patrón Prototype para permitir la clonación de objetos.
    """

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def clone(self):
        """
        Crea y retorna una copia profunda de la instancia actual.
        """
        return copy.deepcopy(self)

    def __str__(self):
        return f"Objeto [Nombre: {self.name}, Data: {self.data}, ID: {id(self)}]"


def main():
    print("--- Demostración del Patrón Prototype ---")

    # 1. Crear el objeto original (Prototipo inicial)
    original = Prototype("Prototipo Alfa", [10, 20, 30])
    print(f"Original: {original}")

    # 2. Crear una copia a partir del original
    copia_1 = original.clone()
    copia_1.name = "Copia de Alfa"
    print(f"Copia 1:  {copia_1}")

    # 3. Verificar que la copia puede generar sus propias copias
    # (Validación de que la clase generada permite obtener copias de sí misma)
    copia_2 = copia_1.clone()
    copia_2.name = "Copia de la Copia"
    copia_2.data.append(99)  # Modificamos la data para verificar independencia

    print(f"Copia 2:  {copia_2}")

    print("\n--- Verificaciones Finales ---")
    print(f"¿Copia 1 es el mismo objeto que Original?: {copia_1 is original}")
    print(f"¿Copia 2 es el mismo objeto que Copia 1?:  {copia_2 is copia_1}")
    print(f"Data Original: {original.data}")
    print(f"Data Copia 2:  {copia_2.data}")


if __name__ == "__main__":
    main()
