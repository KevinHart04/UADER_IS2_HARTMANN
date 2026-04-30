from abc import ABC, abstractmethod


class IPing(ABC):
    """
    Interfaz común para el patrón Proxy.
    Define el método execute().
    """

    @abstractmethod
    def execute(self, ip: str) -> None:
        """Ejecuta la acción de ping."""
        pass


class Ping(IPing):
    """
    Objeto real (RealSubject).
    Se encarga de ejecutar los pings verdaderos.
    """

    def execute(self, ip: str) -> None:
        """
        Realiza 10 intentos de ping solo si la IP comienza con '192.'.
        """
        if ip.startswith("192."):
            self.execute_free(ip)
        else:
            print("Acceso denegado: solo se permiten IP que comiencen con '192.'")

    def execute_free(self, ip: str) -> None:
        """
        Realiza 10 intentos de ping sin restricciones.
        """
        for intento in range(1, 11):
            print(f"Ping {intento} a {ip}")


class PingProxy(IPing):
    """
    Proxy que controla el acceso al objeto real Ping.
    """

    def __init__(self):
        """Inicializa la referencia al objeto real."""
        self._ping = Ping()

    def execute(self, ip: str) -> None:
        """
        Si la IP es '192.168.0.254', redirige a Google usando execute_free().
        En cualquier otro caso, delega al execute() real.
        """
        if ip == "192.168.0.254":
            print("Proxy detectó IP especial. Redirigiendo a www.google.com...")
            self._ping.execute_free("www.google.com")
        else:
            self._ping.execute(ip)


# -------------------------
# Ejemplo de uso
# -------------------------
proxy = PingProxy()

print("Caso 1:")
proxy.execute("192.168.1.10")

print("\nCaso 2:")
proxy.execute("8.8.8.8")

print("\nCaso 3:")
proxy.execute("192.168.0.254")