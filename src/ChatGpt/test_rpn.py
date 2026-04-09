#!/usr/bin/env python3
"""test_rpn.py — Tests unitarios para rpn.py con cobertura completa."""

import math
import sys
import unittest
from io import StringIO
from unittest.mock import patch

import rpn
from rpn import RPNError, evaluate, fmt, main, MEM


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def ev(expr):
    """Shortcut para evaluate()."""
    return evaluate(expr)


def reset_mem():
    """Limpia las memorias entre tests."""
    for i in range(10):
        MEM[i] = 0.0


# ---------------------------------------------------------------------------
# 1. Números
# ---------------------------------------------------------------------------

class TestNumbers(unittest.TestCase):

    def test_entero_positivo(self):
        self.assertEqual(ev("7"), 7.0)

    def test_entero_negativo(self):
        self.assertEqual(ev("-4"), -4.0)

    def test_float_positivo(self):
        self.assertAlmostEqual(ev("2.5"), 2.5)

    def test_float_negativo(self):
        self.assertAlmostEqual(ev("-3.14"), -3.14)


# ---------------------------------------------------------------------------
# 2. Operadores básicos
# ---------------------------------------------------------------------------

class TestOperadoresBasicos(unittest.TestCase):

    def test_suma(self):
        self.assertEqual(ev("3 4 +"), 7.0)

    def test_resta(self):
        self.assertEqual(ev("10 3 -"), 7.0)

    def test_multiplicacion(self):
        self.assertEqual(ev("3 4 *"), 12.0)

    def test_division(self):
        self.assertAlmostEqual(ev("10 4 /"), 2.5)

    def test_division_float(self):
        self.assertAlmostEqual(ev("7.5 2.5 /"), 3.0)

    def test_expresion_compuesta_1(self):
        # 5 1 2 + 4 * + 3 - → 14
        self.assertEqual(ev("5 1 2 + 4 * + 3 -"), 14.0)

    def test_expresion_compuesta_2(self):
        # 2 3 4 * + → 14
        self.assertEqual(ev("2 3 4 * +"), 14.0)

    def test_negativos_en_operacion(self):
        self.assertEqual(ev("-3 -4 +"), -7.0)

    def test_division_por_cero(self):
        with self.assertRaises(RPNError) as ctx:
            ev("3 0 /")
        self.assertIn("cero", str(ctx.exception).lower())


# ---------------------------------------------------------------------------
# 3. Errores de pila
# ---------------------------------------------------------------------------

class TestErroresPila(unittest.TestCase):

    def test_pila_vacia_operador(self):
        with self.assertRaises(RPNError):
            ev("+")

    def test_pila_un_elemento_operador_binario(self):
        with self.assertRaises(RPNError):
            ev("3 +")

    def test_pila_vacia_al_final(self):
        with self.assertRaises(RPNError) as ctx:
            ev("clear 1 2")  # queda 2 elementos
        self.assertIn("exactamente 1", str(ctx.exception))

    def test_pila_sin_elementos_al_final(self):
        with self.assertRaises(RPNError):
            ev("1 drop")  # queda vacía

    def test_token_invalido(self):
        with self.assertRaises(RPNError) as ctx:
            ev("3 foo +")
        self.assertIn("inválido", str(ctx.exception))


# ---------------------------------------------------------------------------
# 4. Comandos de pila
# ---------------------------------------------------------------------------

class TestComandosPila(unittest.TestCase):

    def test_dup(self):
        self.assertEqual(ev("5 dup +"), 10.0)

    def test_swap(self):
        self.assertEqual(ev("3 7 swap -"), 4.0)   # 7 - 3 = 4

    def test_drop(self):
        self.assertEqual(ev("1 2 drop"), 1.0)

    def test_clear_luego_valor(self):
        self.assertEqual(ev("9 8 7 clear 42"), 42.0)

    def test_dup_pila_insuficiente(self):
        with self.assertRaises(RPNError):
            ev("dup")

    def test_swap_pila_insuficiente(self):
        with self.assertRaises(RPNError):
            ev("5 swap")

    def test_drop_pila_insuficiente(self):
        with self.assertRaises(RPNError):
            ev("drop")


# ---------------------------------------------------------------------------
# 5. Constantes
# ---------------------------------------------------------------------------

class TestConstantes(unittest.TestCase):

    def test_pi(self):
        self.assertAlmostEqual(ev("p"), math.pi)

    def test_e(self):
        self.assertAlmostEqual(ev("e"), math.e)

    def test_phi(self):
        phi = (1 + math.sqrt(5)) / 2
        self.assertAlmostEqual(ev("j"), phi)

    def test_constante_mayuscula(self):
        self.assertAlmostEqual(ev("P"), math.pi)


# ---------------------------------------------------------------------------
# 6. Funciones matemáticas
# ---------------------------------------------------------------------------

class TestFuncionesMatematicas(unittest.TestCase):

    def test_sqrt(self):
        self.assertAlmostEqual(ev("9 sqrt"), 3.0)

    def test_sqrt_negativo(self):
        with self.assertRaises(RPNError):
            ev("-1 sqrt")

    def test_log(self):
        self.assertAlmostEqual(ev("100 log"), 2.0)

    def test_log_no_positivo(self):
        with self.assertRaises(RPNError):
            ev("0 log")

    def test_log_negativo(self):
        with self.assertRaises(RPNError):
            ev("-5 log")

    def test_ln(self):
        self.assertAlmostEqual(ev("e ln"), 1.0)

    def test_ln_no_positivo(self):
        with self.assertRaises(RPNError):
            ev("0 ln")

    def test_ex(self):
        self.assertAlmostEqual(ev("1 ex"), math.e)

    def test_10x(self):
        self.assertAlmostEqual(ev("2 10x"), 100.0)

    def test_yx(self):
        self.assertAlmostEqual(ev("2 10 yx"), 1024.0)

    def test_1_sobre_x(self):
        self.assertAlmostEqual(ev("4 1/x"), 0.25)

    def test_1_sobre_0(self):
        with self.assertRaises(RPNError):
            ev("0 1/x")

    def test_chs(self):
        self.assertEqual(ev("5 chs"), -5.0)

    def test_chs_negativo(self):
        self.assertEqual(ev("-3 chs"), 3.0)


# ---------------------------------------------------------------------------
# 7. Trigonometría (grados)
# ---------------------------------------------------------------------------

class TestTrigonometria(unittest.TestCase):

    def test_sin_0(self):
        self.assertAlmostEqual(ev("0 sin"), 0.0)

    def test_sin_90(self):
        self.assertAlmostEqual(ev("90 sin"), 1.0)

    def test_cos_0(self):
        self.assertAlmostEqual(ev("0 cos"), 1.0)

    def test_cos_90(self):
        self.assertAlmostEqual(ev("90 cos"), 0.0, places=10)

    def test_tg_45(self):
        self.assertAlmostEqual(ev("45 tg"), 1.0)

    def test_asin(self):
        self.assertAlmostEqual(ev("1 asin"), 90.0)

    def test_acos(self):
        self.assertAlmostEqual(ev("1 acos"), 0.0)

    def test_atg(self):
        self.assertAlmostEqual(ev("1 atg"), 45.0)


# ---------------------------------------------------------------------------
# 8. Memorias STO / RCL
# ---------------------------------------------------------------------------

class TestMemoria(unittest.TestCase):

    def setUp(self):
        reset_mem()

    def test_sto_rcl_basico(self):
        # STO consume el valor de la pila; usamos dup para preservar uno
        self.assertAlmostEqual(ev("42 dup STO 3 1 +"), 43.0)
        self.assertAlmostEqual(ev("RCL 3"), 42.0)

    def test_sto_rcl_todas_memorias(self):
        for i in range(10):
            # dup guarda copia; STO la consume; queda el original, drop lo borra, 0 final
            ev(f"{i * 10} dup STO {i} drop 0")
        for i in range(10):
            self.assertAlmostEqual(ev(f"RCL {i}"), float(i * 10))

    def test_sto_memoria_invalida(self):
        with self.assertRaises(RPNError):
            ev("5 STO a")

    def test_rcl_memoria_invalida(self):
        with self.assertRaises(RPNError):
            ev("RCL z")

    def test_sto_pila_insuficiente(self):
        with self.assertRaises(RPNError):
            ev("STO 0")


# ---------------------------------------------------------------------------
# 9. fmt()
# ---------------------------------------------------------------------------

class TestFmt(unittest.TestCase):

    def test_entero_como_float(self):
        self.assertEqual(fmt(7.0), 7)
        self.assertIsInstance(fmt(7.0), int)

    def test_float_real(self):
        self.assertEqual(fmt(2.5), 2.5)
        self.assertIsInstance(fmt(2.5), float)

    def test_negativo_entero(self):
        self.assertEqual(fmt(-3.0), -3)


# ---------------------------------------------------------------------------
# 10. main() — integración con argv / stdin
# ---------------------------------------------------------------------------

class TestMain(unittest.TestCase):

    def test_main_argv(self):
        with patch.object(sys, 'argv', ['rpn.py', '3', '4', '+']):
            with patch('sys.stdout', new_callable=StringIO) as out:
                main()
        self.assertEqual(out.getvalue().strip(), '7')

    def test_main_stdin(self):
        with patch.object(sys, 'argv', ['rpn.py']):
            with patch('builtins.input', return_value='5 1 2 + 4 * + 3 -'):
                with patch('sys.stdout', new_callable=StringIO) as out:
                    main()
        self.assertEqual(out.getvalue().strip(), '14')

    def test_main_error_stderr(self):
        with patch.object(sys, 'argv', ['rpn.py', '3', '0', '/']):
            with patch('sys.stderr', new_callable=StringIO) as err:
                with self.assertRaises(SystemExit) as cm:
                    main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn('Error', err.getvalue())

    def test_main_float_resultado(self):
        with patch.object(sys, 'argv', ['rpn.py', '7.5', '2.5', '/']):
            with patch('sys.stdout', new_callable=StringIO) as out:
                main()
        self.assertEqual(out.getvalue().strip(), '3')


if __name__ == '__main__':
    unittest.main(verbosity=2)