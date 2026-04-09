#!/usr/bin/env python3
"""
rpn_v3.py — Calculadora RPN (Reverse Polish Notation).

Uso:
    python rpn_v3.py "3 4 +"              -> 7
    python rpn_v3.py "5 1 2 + 4 * + 3 -" -> 14
    python rpn_v3.py                       -> modo interactivo (RPN>)

Tokens soportados:
    Numeros   : enteros y reales, incluyendo negativos  (3, -2.5, 0.7)
    Operadores: +  -  *  /
    Pila      : dup  swap  drop  clear
    Constantes: p (pi=3.14159), e (euler=2.71828), j (phi=1.61803)
    Funciones : sqrt  log  ln  ex  10x  yx  1/x  chs
    Trig      : sin  cos  tg  asin  acos  atg  (angulos en grados)
    Memoria   : STO <n>  RCL <n>  con n en rango 0-9

Invariante de evaluacion:
    Al finalizar la expresion debe quedar exactamente UN valor en la pila.
    Si quedan 0 o mas de 1, se lanza RPNError con la cantidad actual.

Manejo de errores:
    Todos los errores semanticos lanzan RPNError con mensaje descriptivo.
    Los errores se imprimen en stderr y el programa termina con exit code 1.
"""

import math
import operator
import sys

# ── Excepcion propia ──────────────────────────────────────────────────────────
# RPNError se usa para todos los errores semanticos de la calculadora.
# Separarla de ValueError/TypeError permite capturarla limpiamente en main().


class RPNError(Exception):
    """Error semantico del evaluador RPN.

    Se lanza para: token desconocido, pila insuficiente, division por cero,
    dominio invalido en funciones matematicas, indice de memoria fuera de rango,
    o cantidad incorrecta de elementos al finalizar la expresion.
    """


# ── Constantes simbolicas ─────────────────────────────────────────────────────
# Los tokens p, e, j (case-insensitive) se reemplazan por su valor numerico.
# j representa el numero aureo phi = (1 + sqrt(5)) / 2 aproximadamente 1.61803.

CONSTS = {
    "p": math.pi,
    "e": math.e,
    "j": (1 + math.sqrt(5)) / 2,
}

# ── Memoria de usuario (registros 0-9) ────────────────────────────────────────
# Diez registros de punto flotante accesibles via STO <n> y RCL <n>.
# Se inicializan en 0.0 y persisten durante toda la sesion del proceso.
# Ejemplo: "42 STO 3" guarda 42 en registro 3; "RCL 3" lo recupera.

MEM = [0.0] * 10

# ── Tabla de operadores binarios basicos ──────────────────────────────────────
# Usar un diccionario de funciones elimina la cadena de if/elif y reduce
# la complejidad ciclomatica de McCabe. La division se maneja por separado
# para poder verificar el divisor antes de operar y lanzar error util.

_BASIC_OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
}

# ── Nota de diseño: dict vs if/elif ────────────────────────────────────────
# Ambas tablas (_BASIC_OPS y _TRIG) usan el patron 'dispatch por diccionario'.
# Este patron reemplaza cadenas de if/elif por una sola busqueda O(1) en dict,
# lo que reduce la complejidad ciclomatica de McCabe y facilita agregar nuevos
# operadores sin modificar el cuerpo principal de evaluate().

# ── Tabla de funciones trigonometricas ───────────────────────────────────────
# Todas las funciones operan en GRADOS, no en radianes.
# Las funciones directas (sin, cos, tg) convierten grados->radianes internamente.
# Las funciones inversas (asin, acos, atg) convierten el resultado a grados.
# Usar un dict evita seis ramas elif y reduce CC en 5 puntos respecto a V1.

_TRIG = {
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tg": lambda x: math.tan(math.radians(x)),
    "asin": lambda x: math.degrees(math.asin(x)),
    "acos": lambda x: math.degrees(math.acos(x)),
    "atg": lambda x: math.degrees(math.atan(x)),
}


# ── Helpers de pila ───────────────────────────────────────────────────────────


def pop1(stack):
    """Extrae y retorna el valor en el tope de la pila.

    Lanza RPNError si la pila esta vacia, con mensaje descriptivo.
    """
    if not stack:
        raise RPNError("Pila insuficiente (se necesita 1 valor)")
    return stack.pop()


def pop2(stack):
    """Extrae dos valores del tope: retorna (a, b) donde b estaba en el tope.

    En 'a b op', a es el primer operando y b es el segundo (tope de pila).
    Lanza RPNError si hay menos de 2 elementos disponibles.
    """
    if len(stack) < 2:
        raise RPNError("Pila insuficiente (se necesitan 2 valores)")
    # b = tope (ultimo empujado), a = penultimo
    b, a = stack.pop(), stack.pop()
    return a, b


# ── Conversion de token a numero ──────────────────────────────────────────────


def to_num(token):
    """Intenta convertir token a int o float; retorna None si no es numerico.

    Prueba int primero para mantener representacion entera cuando sea posible.
    Acepta: enteros ('3', '-4'), decimales ('2.5'), notacion cientifica ('1e3').
    """
    try:
        return int(token)
    except ValueError:
        pass
    try:
        return float(token)
    except ValueError:
        return None


# ── Funciones matematicas unarias y binarias ──────────────────────────────────


def _apply_math(tl, stack):
    """Ejecuta una funcion matematica unaria o binaria sobre la pila.

    Cubre: sqrt, log (base 10), ln (base e), ex (e^x), 10x (10^x),
           yx (a^b con b en tope), 1/x (reciproco), chs (cambio de signo).
    Retorna True si reconocio el token; False en caso contrario.
    Lanza RPNError ante argumentos fuera del dominio de la funcion.
    """
    # pylint: disable=too-many-branches
    if tl == "sqrt":
        # La raiz cuadrada de negativos no esta definida en los reales
        x = pop1(stack)
        if x < 0:
            raise RPNError("sqrt: argumento negativo")
        stack.append(math.sqrt(x))
    elif tl == "log":
        # Logaritmo decimal (base 10); indefinido para x <= 0
        x = pop1(stack)
        if x <= 0:
            raise RPNError("log: argumento debe ser positivo")
        stack.append(math.log10(x))
    elif tl == "ln":
        # Logaritmo natural (base e); indefinido para x <= 0
        x = pop1(stack)
        if x <= 0:
            raise RPNError("ln: argumento debe ser positivo")
        stack.append(math.log(x))
    elif tl == "ex":
        # Exponencial: e elevado a x
        stack.append(math.exp(pop1(stack)))
    elif tl == "10x":
        # Potencia de 10: 10 elevado a x
        stack.append(10 ** pop1(stack))
    elif tl == "yx":
        # Potenciacion generica: a elevado a b, con b en el tope
        a, b = pop2(stack)
        stack.append(a**b)
    elif tl == "1/x":
        # Reciproco; indefinido para x = 0
        x = pop1(stack)
        if x == 0:
            raise RPNError("1/x: division por cero")
        stack.append(1.0 / x)
    elif tl == "chs":
        # Change Sign: invierte el signo del tope (equivale a multiplicar por -1)
        stack.append(-pop1(stack))
    else:
        # Token no corresponde a ninguna funcion de esta tabla
        return False
    return True


# ── Operacion de memoria ──────────────────────────────────────────────────────


def _apply_memory(tl, pos, tokens, stack):
    """Ejecuta STO o RCL sobre el registro de memoria indicado.

    Lee el token en la posicion pos+1 como indice de registro (0-9).
    STO extrae el tope de la pila y lo escribe en MEM[n].
    RCL copia MEM[n] al tope de la pila (sin modificar la memoria).
    Marca el token de indice como None para que evaluate() lo saltee.
    Retorna True si el token era 'sto' o 'rcl'; False en caso contrario.
    """
    if tl not in ("sto", "rcl"):
        return False
    # Verificar que existe un token siguiente para el indice
    if pos + 1 >= len(tokens):
        raise RPNError(f"{tl.upper()} requiere un indice de memoria (0-9)")
    idx = tokens[pos + 1]
    if not (idx is not None and idx.isdigit() and 0 <= int(idx) <= 9):
        raise RPNError(f"Indice de memoria invalido: '{idx}' (debe ser 0-9)")
    n = int(idx)
    if tl == "sto":
        MEM[n] = pop1(stack)
    else:
        stack.append(MEM[n])
    # Consumir el token de indice marcandolo como None (sentinel)
    tokens[pos + 1] = None
    return True


# ── Evaluador principal ───────────────────────────────────────────────────────


def evaluate(expression):
    """Evalua una expresion RPN y retorna el resultado como float.

    Algoritmo de pila clasico: recorre los tokens de izquierda a derecha;
    los numeros y constantes se empujan a la pila; los operadores extraen
    operandos, calculan y empujan el resultado. Al finalizar debe quedar
    exactamente un valor en la pila.

    Args:
        expression (str): tokens separados por espacios.

    Returns:
        float: resultado de la expresion.

    Raises:
        RPNError: ante token invalido, pila insuficiente, division por cero,
                  dominio invalido, o cantidad incorrecta de resultados finales.
    """
    # pylint: disable=too-many-branches
    stack = []
    tokens = expression.split()

    for pos, token in enumerate(tokens):
        # Saltear tokens de indice ya consumidos por STO/RCL
        if token is None:
            continue

        tl = token.lower()

        # 1) Constante simbolica: p=pi, e=euler, j=phi (case-insensitive)
        if tl in CONSTS:
            stack.append(CONSTS[tl])
            continue

        # 2) Literal numerico: int, float, negativos, notacion cientifica
        n = to_num(token)
        if n is not None:
            stack.append(float(n))
            continue

        # 3) Operadores binarios basicos via dict (+ - *)
        if token in _BASIC_OPS:
            a, b = pop2(stack)
            stack.append(_BASIC_OPS[token](a, b))
            continue

        # 4) Division separada para control explicito de division por cero
        if token == "/":
            a, b = pop2(stack)
            if b == 0:
                raise RPNError("Division por cero")
            stack.append(a / b)
            continue

        # 5) Comandos de manipulacion de pila
        if tl == "dup":
            # Duplica el tope: [... x] -> [... x x]
            x = pop1(stack)
            stack += [x, x]
        elif tl == "swap":
            # Intercambia los dos elementos del tope: [... a b] -> [... b a]
            a, b = pop2(stack)
            stack += [b, a]
        elif tl == "drop":
            # Descarta el tope de la pila sin usar su valor
            pop1(stack)
        elif tl == "clear":
            # Vacia la pila por completo; util para reiniciar el calculo
            stack.clear()

        # 6) Funciones matematicas (sqrt, log, ln, ex, 10x, yx, 1/x, chs)
        elif _apply_math(tl, stack):
            pass

        # 7) Funciones trigonometricas via dict de lambdas (en grados)
        elif tl in _TRIG:
            stack.append(_TRIG[tl](pop1(stack)))

        # 8) Comandos de memoria: STO <n> guarda, RCL <n> recupera
        elif _apply_memory(tl, pos, tokens, stack):
            pass

        else:
            raise RPNError(f"Token invalido: '{token}'")

    # Nota: enumerate() provee 'pos' para que STO/RCL puedan leer el siguiente
    # token como indice de memoria sin necesidad de un iterador externo manual.
    # Los tokens consumidos se marcan None y se saltean al inicio del loop.

    # Verificacion final: la expresion bien formada deja exactamente 1 resultado
    if len(stack) != 1:
        raise RPNError(
            f"La pila debe tener exactamente 1 valor al final " f"(tiene {len(stack)})"
        )
    return stack[0]


# ── Formateo de salida ────────────────────────────────────────────────────────


def fmt(n):
    """Formatea el resultado: entero si el float es entero, float en caso contrario.

    Ejemplos: fmt(7.0) -> 7  |  fmt(2.5) -> 2.5  |  fmt(-3.0) -> -3
    Evita mostrar '7.0' cuando el resultado matematico es exactamente entero.
    """
    return int(n) if isinstance(n, float) and n.is_integer() else n


# ── Punto de entrada ──────────────────────────────────────────────────────────


def main():
    """Lee la expresion RPN desde argv o stdin interactivo y la evalua.

    Si se proveen argumentos en la linea de comandos, se concatenan y evaluan.
    Sin argumentos, entra en modo interactivo mostrando el prompt 'RPN>'.
    Los errores semanticos se reportan en stderr y terminan con exit code 1.
    """
    if len(sys.argv) > 1:
        expr = " ".join(sys.argv[1:])
    else:
        expr = input("RPN> ").strip()
    try:
        print(fmt(evaluate(expr)))
    except RPNError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
