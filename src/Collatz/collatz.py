import matplotlib.pyplot as plt


def collatz(n):
    """Función que genera la secuencia de Collatz para un número dado.
    """
    
    pasos = 0
    
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        pasos += 1
    
    return pasos

valores_n = []
iteraciones = []

for i in range(1, 100000):     # tardó pero se pudo
    
    pasos = collatz(i)
    
    valores_n.append(i)
    iteraciones.append(pasos)



def graficar(valores_n, iteraciones):
    """Función que grafica la cantidad de iteraciones necesarias para llegar a 1
    en la secuencia de Collatz para un rango de números.
    """
    
    plt.scatter(iteraciones, valores_n, s=1)
    plt.xlabel('iteraciones')
    plt.ylabel('numero inicial (n)')
    plt.title('Iteraciones para llegar a 1 en la secuencia de Collatz')

    plt.show()
    

def main():
    print(f"Valores de n: {valores_n}")
    print(f"Iteraciones: {iteraciones}")
    graficar(valores_n, iteraciones)



if __name__ == "__main__":
    main()