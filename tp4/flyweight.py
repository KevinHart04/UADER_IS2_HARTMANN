class SensorABSFlyweight:
    """
    Flyweight concreto.

    Estado compartido (intrínseco):
    modelo, fabricante y voltaje nominal.

    Miles de autos pueden usar el mismo
    tipo de sensor ABS.
    """

    def __init__(
        self,
        modelo: str,
        fabricante: str,
        voltaje: int
    ):
        self.modelo = modelo
        self.fabricante = fabricante
        self.voltaje = voltaje

    def diagnosticar(
        self,
        vehiculo: str,
        rueda: str,
        kilometraje: int
    ) -> None:
        """
        Estado extrínseco:
        auto específico, rueda instalada y km.
        """
        print(
            f"Sensor {self.modelo} | "
            f"{self.fabricante} | "
            f"{self.voltaje}V | "
            f"Vehículo: {vehiculo} | "
            f"Rueda: {rueda} | "
            f"KM: {kilometraje}"
        )


class FabricaSensoresABS:
    """
    Flyweight Factory.

    Reutiliza sensores iguales.
    """

    def __init__(self):
        self._pool = {}

    def obtener(
        self,
        modelo: str,
        fabricante: str,
        voltaje: int
    ) -> SensorABSFlyweight:

        clave = (
            modelo,
            fabricante,
            voltaje
        )

        if clave not in self._pool:
            print(f"[CREADO] Sensor {modelo}")
            self._pool[clave] = SensorABSFlyweight(
                modelo,
                fabricante,
                voltaje
            )
        else:
            print(f"[REUTILIZADO] Sensor {modelo}")

        return self._pool[clave]

    def total_objetos(self) -> int:
        return len(self._pool)


class PlantaAutomotriz:
    """
    Contexto.

    Cada vehículo tiene sensores instalados,
    pero muchos comparten el mismo modelo.
    """

    def __init__(self, fabrica: FabricaSensoresABS):
        self.fabrica = fabrica
        self.instalaciones = []

    def instalar_sensor(
        self,
        modelo: str,
        fabricante: str,
        voltaje: int,
        vehiculo: str,
        rueda: str,
        kilometraje: int
    ) -> None:

        sensor = self.fabrica.obtener(
            modelo,
            fabricante,
            voltaje
        )

        self.instalaciones.append(
            (
                sensor,
                vehiculo,
                rueda,
                kilometraje
            )
        )

    def auditoria(self) -> None:
        """
        Recorre todas las instalaciones.
        """
        for item in self.instalaciones:
            sensor, vehiculo, rueda, km = item

            sensor.diagnosticar(
                vehiculo,
                rueda,
                km
            )


def main():
    """
    Ejemplo Flyweight aplicado a automotriz.

    Una fábrica arma autos y reutiliza
    configuraciones idénticas de sensores ABS.
    """

    print("=== PLANTA AUTOMOTRIZ ===\n")

    fabrica = FabricaSensoresABS()
    planta = PlantaAutomotriz(fabrica)

    # Auto 1
    planta.instalar_sensor(
        "ABS-X1", "BosalTech", 12,
        "Sedan A01", "Delantera Izq.", 0
    )

    planta.instalar_sensor(
        "ABS-X1", "BosalTech", 12,
        "Sedan A01", "Delantera Der.", 0
    )

    # Auto 2
    planta.instalar_sensor(
        "ABS-X1", "BosalTech", 12,
        "SUV B07", "Trasera Izq.", 0
    )

    planta.instalar_sensor(
        "ABS-X1", "BosalTech", 12,
        "SUV B07", "Trasera Der.", 0
    )

    # Otro modelo
    planta.instalar_sensor(
        "ABS-Z9", "NipponDrive", 24,
        "Camión C22", "Delantera Izq.", 0
    )

    print("\n=== AUDITORÍA ===\n")
    planta.auditoria()

    print("\n=== RESUMEN ===")
    print(
        f"Sensores instalados físicamente: "
        f"{len(planta.instalaciones)}"
    )

    print(
        f"Objetos reales creados: "
        f"{fabrica.total_objetos()}"
    )

    print(
        "Muchos sensores comparten "
        "instancias idénticas."
    )


if __name__ == "__main__":
    main()
