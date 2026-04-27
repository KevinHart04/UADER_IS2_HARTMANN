class Airplane:
    """
    Clase que representa el producto final: un avión.
    """

    def __init__(self):
        self.body = None
        self.turbines = None
        self.wings = None
        self.landing_gear = None

    def __str__(self):
        return (
            "Avión construido con:\n"
            f"- Cuerpo: {self.body}\n"
            f"- Turbinas: {self.turbines}\n"
            f"- Alas: {self.wings}\n"
            f"- Tren de aterrizaje: {self.landing_gear}"
        )


class AirplaneBuilder:
    """
    Builder base que define los pasos de construcción.
    """

    def __init__(self):
        self.airplane = Airplane()

    def build_body(self):
        pass

    def build_turbines(self):
        pass

    def build_wings(self):
        pass

    def build_landing_gear(self):
        pass

    def get_result(self):
        """
        Retorna el avión construido.
        """
        return self.airplane


class CommercialAirplaneBuilder(AirplaneBuilder):
    """
    Builder concreto para un avión comercial.
    """

    def build_body(self):
        self.airplane.body = "Fuselaje de pasajeros de gran capacidad"

    def build_turbines(self):
        self.airplane.turbines = "2 Turbinas Turbofan de alto empuje"

    def build_wings(self):
        self.airplane.wings = "2 Alas de gran envergadura con winglets"

    def build_landing_gear(self):
        self.airplane.landing_gear = "Tren de aterrizaje triciclo reforzado"


class Director:
    """
    Director que organiza el proceso de construcción.
    """

    def __init__(self, builder):
        self.builder = builder

    def construct_airplane(self):
        """
        Ejecuta los pasos en orden.
        """
        self.builder.build_body()
        self.builder.build_turbines()
        self.builder.build_wings()
        self.builder.build_landing_gear()


def main():
    """
    Función principal.
    """
    print("--- Construcción de Avión Comercial ---")

    builder = CommercialAirplaneBuilder()
    director = Director(builder)

    director.construct_airplane()

    airplane = builder.get_result()

    print()
    print(airplane)


if __name__ == "__main__":
    main()