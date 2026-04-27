class Invoice:
    """
    Producto abstracto: Factura.
    """

    def generate(self):
        raise NotImplementedError("Debe implementarse en la subclase.")


class Currency:
    """
    Producto abstracto: Moneda.
    """

    def symbol(self):
        raise NotImplementedError("Debe implementarse en la subclase.")


class TaxCalculator:
    """
    Producto abstracto: Calculador de impuestos.
    """

    def calculate(self, amount):
        raise NotImplementedError("Debe implementarse en la subclase.")


# ===============================
# Productos concretos Argentina
# ===============================

class ArgentinaInvoice(Invoice):
    """
    Factura para Argentina.
    """

    def generate(self):
        return "Factura electrónica AFIP generada."


class PesoCurrency(Currency):
    """
    Moneda Peso Argentino.
    """

    def symbol(self):
        return "$"


class ArgentinaTaxCalculator(TaxCalculator):
    """
    IVA Argentina.
    """

    def calculate(self, amount):
        return amount * 0.21


# ===============================
# Productos concretos USA
# ===============================

class USAInvoice(Invoice):
    """
    Factura para Estados Unidos.
    """

    def generate(self):
        return "Invoice generado bajo normativa USA."


class DollarCurrency(Currency):
    """
    Moneda Dólar.
    """

    def symbol(self):
        return "USD"


class USATaxCalculator(TaxCalculator):
    """
    Tax USA.
    """

    def calculate(self, amount):
        return amount * 0.07


# ===============================
# Abstract Factory
# ===============================

class EcommerceFactory:
    """
    Fábrica abstracta.
    """

    def create_invoice(self):
        raise NotImplementedError

    def create_currency(self):
        raise NotImplementedError

    def create_tax_calculator(self):
        raise NotImplementedError


# ===============================
# Fábricas concretas
# ===============================

class ArgentinaFactory(EcommerceFactory):
    """
    Fábrica para Argentina.
    """

    def create_invoice(self):
        return ArgentinaInvoice()

    def create_currency(self):
        return PesoCurrency()

    def create_tax_calculator(self):
        return ArgentinaTaxCalculator()


class USAFactory(EcommerceFactory):
    """
    Fábrica para USA.
    """

    def create_invoice(self):
        return USAInvoice()

    def create_currency(self):
        return DollarCurrency()

    def create_tax_calculator(self):
        return USATaxCalculator()


# ===============================
# Cliente
# ===============================

class EcommerceSystem:
    """
    Sistema que usa una fábrica abstracta.
    """

    def __init__(self, factory):
        self.invoice = factory.create_invoice()
        self.currency = factory.create_currency()
        self.tax = factory.create_tax_calculator()

    def checkout(self, amount):
        taxes = self.tax.calculate(amount)
        total = amount + taxes

        print(self.invoice.generate())
        print(f"Subtotal: {self.currency.symbol()} {amount:.2f}")
        print(f"Impuestos: {self.currency.symbol()} {taxes:.2f}")
        print(f"Total: {self.currency.symbol()} {total:.2f}")


# ===============================
# Main
# ===============================

def main():
    """
    Función principal.
    """

    print("Seleccione país:")
    print("1. Argentina")
    print("2. USA")

    option = input("Opción: ")

    if option == "1":
        factory = ArgentinaFactory()
    elif option == "2":
        factory = USAFactory()
    else:
        print("Opción inválida.")
        return

    amount = float(input("Ingrese monto de compra: "))

    system = EcommerceSystem(factory)

    print("\n--- Checkout ---")
    system.checkout(amount)


if __name__ == "__main__":
    main()