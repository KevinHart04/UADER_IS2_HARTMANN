class Invoice:
    """
    Clase base que representa una factura.
    """

    def __init__(self, amount):
        self.amount = amount
        self.condition = ""

    def __str__(self):
        return (
            f"Factura | Condición: {self.condition} "
            f"| Importe Total: ${self.amount:.2f}"
        )


class ResponsibleInvoice(Invoice):
    """
    Factura para cliente IVA Responsable Inscripto.
    """

    def __init__(self, amount):
        super().__init__(amount)
        self.condition = "IVA Responsable Inscripto"


class NonRegisteredInvoice(Invoice):
    """
    Factura para cliente IVA No Inscripto.
    """

    def __init__(self, amount):
        super().__init__(amount)
        self.condition = "IVA No Inscripto"


class ExemptInvoice(Invoice):
    """
    Factura para cliente IVA Exento.
    """

    def __init__(self, amount):
        super().__init__(amount)
        self.condition = "IVA Exento"


class InvoiceFactory:
    """
    Factory encargada de crear facturas
    según la condición impositiva.
    """

    @staticmethod
    def create_invoice(condition_type, amount):
        """
        Crea una factura según el tipo indicado.

        Args:
            condition_type (str): Tipo de condición.
            amount (float): Importe total.

        Returns:
            Invoice
        """
        types = {
            "responsable": ResponsibleInvoice,
            "no_inscripto": NonRegisteredInvoice,
            "exento": ExemptInvoice
        }

        invoice_class = types.get(condition_type.lower())

        if invoice_class:
            return invoice_class(amount)

        raise ValueError(
            f"Condición impositiva '{condition_type}' no reconocida."
        )


def main():
    """
    Función principal.
    """
    print("--- Generador de Facturas ---")

    try:
        total = float(input("Ingrese el importe total: $"))

        print("\nSeleccione la condición impositiva:")
        print("1. IVA Responsable")
        print("2. IVA No Inscripto")
        print("3. IVA Exento")

        option = input("Opción: ")

        mapping = {
            "1": "responsable",
            "2": "no_inscripto",
            "3": "exento"
        }

        condition = mapping.get(option)

        if not condition:
            print("Opción inválida.")
            return

        invoice = InvoiceFactory.create_invoice(condition, total)

        print("\nFactura generada:")
        print(invoice)

    except ValueError:
        print("Debe ingresar un importe válido.")


if __name__ == "__main__":
    main()