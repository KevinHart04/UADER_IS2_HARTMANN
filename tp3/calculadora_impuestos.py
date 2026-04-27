class CalculadoraImpuestos:
    """Clase para calcular impuestos utilizando el patrón Singleton."""
    _instancia = None

    def __new__(cls, *args, **kwargs):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def calcular_precio_final(self, precio_base):
        """Calcula el precio final sumando IVA (21%), IIBB (5%) y Tasas Municipales (1.2%)."""
        iva = precio_base * 0.21
        iibb = precio_base * 0.05
        tasas_municipales = precio_base * 0.012
        
        precio_final = precio_base + iva + iibb + tasas_municipales
        return precio_final

def main():
    calculadora1 = CalculadoraImpuestos()
    calculadora2 = CalculadoraImpuestos()
    
    print(f"¿Son la misma instancia? {calculadora1 is calculadora2}")
    
    try:
        precio = float(input("Ingrese el precio base para calcular impuestos: "))
        resultado = calculadora1.calcular_precio_final(precio)
        print(f"Precio Base: ${precio:.2f}")
        print(f"Precio Final (con IVA, IIBB y Tasas): ${resultado:.2f}")
    except ValueError:
        print("Por favor, ingrese un valor numérico válido.")

if __name__ == "__main__":
    main()
