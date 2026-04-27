class FastFood:
    """
    Clase que representa un pedido de comida rápida
    y sus distintos métodos de entrega.
    """

    def __init__(self, nombre="Hamburguesa"):
        self.nombre = nombre

    def entregar_en_mostrador(self):
        """Entrega el pedido en mostrador."""
        print(f"Pedido: {self.nombre} | Método: Entregado en mostrador.")

    def retirar_por_cliente(self):
        """El cliente retira el pedido."""
        print(f"Pedido: {self.nombre} | Método: Retirado por el cliente.")

    def enviar_por_delivery(self):
        """Se envía el pedido por delivery."""
        print(f"Pedido: {self.nombre} | Método: Enviado por delivery.")


class DeliveryFactory:
    """
    Factory encargada de devolver el método
    de entrega solicitado.
    """

    @staticmethod
    def obtener_entrega(tipo, pedido):
        """
        Retorna el método de entrega según el tipo indicado.

        Args:
            tipo (str): Tipo de entrega.
            pedido (FastFood): Pedido sobre el cual actuar.

        Returns:
            function | None
        """
        metodos = {
            "mostrador": pedido.entregar_en_mostrador,
            "retiro": pedido.retirar_por_cliente,
            "delivery": pedido.enviar_por_delivery
        }

        return metodos.get(tipo.lower())


def main():
    """Función principal."""
    print("--- Demostración con Patrón Factory ---")

    mi_pedido = FastFood("Combo Whopper")

    opciones = ["mostrador", "retiro", "delivery"]

    for opcion in opciones:
        metodo = DeliveryFactory.obtener_entrega(opcion, mi_pedido)

        if metodo:
            metodo()
        else:
            print(f"No existe el método de entrega: {opcion}")


if __name__ == "__main__":
    main()
