# modules/log_exp_generator.py

import random
import sympy
# Importaciones esenciales de SymPy
from sympy import symbols, Eq, solve, log, exp, Pow, Integer, Rational, N, pretty, latex, E, Add, Mul, simplify
from sympy.solvers.solveset import solveset, S
from sympy.simplify.simplify import nsimplify
# Eliminamos la importación deprecada de as_int

# --- Símbolo ---
x = symbols('x')

# --- Funciones Auxiliares ---

def _generate_linear_or_const(var=x, min_coef=-5, max_coef=5, allow_const=True, force_non_zero=False):
    """
    Genera una expresión lineal ax+b o una constante b.
    force_non_zero asegura que la expresión resultante no sea el número 0.
    """
    a = Integer(random.randint(min_coef, max_coef))
    if not allow_const and a == 0:
        a = Integer(random.choice([i for i in range(min_coef, max_coef + 1) if i != 0] or [1]))

    b = Integer(random.randint(min_coef, max_coef))

    if a != 0:
        expr = a * var + b
    else:
        expr = b

    if force_non_zero and expr == 0:
        b = Integer(random.choice([i for i in range(min_coef, max_coef + 1) if i != 0] or [1]))
        if a != 0:
            expr = a * var + b
        else:
            expr = b

    return expr

def _check_log_domain(equation, solutions):
    """
    Verifica si las soluciones son válidas para el dominio de los logaritmos en la ecuación.
    Devuelve una lista de soluciones válidas.
    """
    valid_solutions = []
    log_terms_in_eq = list(equation.atoms(log))

    if not log_terms_in_eq:
        return solutions

    for sol in solutions:
        is_valid_solution = True
        try:
            sol_val_num = N(sol, chop=True)
            if not sol_val_num.is_real:
                is_valid_solution = False
                continue
        except (TypeError, ValueError, AttributeError, sympy.SympifyError) as e:
            print(f"Advertencia: No se pudo evaluar numéricamente la solución {sol}: {e}. Descartando.")
            is_valid_solution = False
            continue

        for log_term in log_terms_in_eq:
            arg = log_term.args[0]
            arg_expr_with_sol = arg.subs(x, sol)

            try:
                arg_val_num = N(arg_expr_with_sol, chop=True)
                if not arg_val_num.is_real or arg_val_num <= 0:
                    is_valid_solution = False
                    break
            except (TypeError, ValueError, AttributeError, sympy.SympifyError):
                try:
                    simplified_arg = simplify(arg_expr_with_sol)
                    if not (simplified_arg.is_positive == True):
                        is_valid_solution = False
                        break
                except Exception as e_simp:
                    print(f"Error simplificando argumento {arg_expr_with_sol} para verificar dominio: {e_simp}. Descartando sol {sol}.")
                    is_valid_solution = False
                    break
            # Si ya se marcó como inválida, salir del bucle interno
            if not is_valid_solution:
                 break

        if is_valid_solution:
            valid_solutions.append(sol)

    return valid_solutions


# --- Función Principal ---

def generate_log_exp_exercise(difficulty=1):
    """
    Genera un ejercicio de ecuación logarítmica o exponencial.
    Devuelve un diccionario con LaTeX para problema y solución (sin delimitadores $).
    """
    eq_type_pool = ['exp_basic', 'log_basic', 'exp_same_base', 'log_prop_sum', 'log_prop_diff', 'exp_needs_log']
    eq_type = random.choice(eq_type_pool)

    equation = None
    solutions = []
    valid_solutions = []
    problem_latex = ""
    solution_latex = ""
    base_for_latex = None

    attempts = 0
    max_attempts = 25

    while not valid_solutions and attempts < max_attempts:
        attempts += 1
        base_for_latex = None
        equation = None
        solutions = []
        valid_solutions = []

        try:
            # --- Generación basada en el tipo de ecuación ---

            if eq_type == 'exp_basic': # b^f(x) = c
                base = Integer(random.choice([2, 3, 4, 5, 10, E]))
                base_for_latex = base
                fx = _generate_linear_or_const(allow_const=False, force_non_zero=True)
                sol_val = Integer(random.randint(-2, 3))
                rhs_val = base**fx.subs(x, sol_val)
                if not isinstance(rhs_val, (Integer, Rational, Pow)) or abs(N(rhs_val)) > 10000:
                    continue

                lhs = Pow(base, fx, evaluate=False)
                rhs = rhs_val
                equation = Eq(lhs, rhs)
                solutions = solve(equation, x)

            elif eq_type == 'log_basic': # log_b(f(x)) = c
                base = Integer(random.choice([2, 3, 5, 10, E]))
                base_for_latex = base
                fx = _generate_linear_or_const(allow_const=False, force_non_zero=True)
                sol_val = Integer(random.randint(-2, 3))
                arg_val = fx.subs(x, sol_val)
                if arg_val <= 0: continue

                try:
                     rhs_val = log(arg_val, base)
                     # --- CORRECCIÓN AQUÍ ---
                     # Simplificar RHS si es posible y NO contiene símbolos
                     if not rhs_val.has(x): # Usar .has(x)
                          rhs_val = nsimplify(rhs_val, rational=True)
                     # -----------------------
                except ValueError:
                     continue

                if not (rhs_val.is_Integer or rhs_val.is_Rational or isinstance(rhs_val, log) or rhs_val.has(E)):
                     continue

                lhs = log(fx, base)
                rhs = rhs_val
                equation = Eq(lhs, rhs)
                solutions = solve(equation, x)

            elif eq_type == 'exp_same_base': # b^f(x) = b^g(x)
                base = Integer(random.choice([2, 3, 5, 7, 10]))
                base_for_latex = base
                fx = _generate_linear_or_const(allow_const=False, force_non_zero=True)
                gx = _generate_linear_or_const(allow_const=True, force_non_zero=False)
                if simplify(fx - gx) == 0: continue

                equation_simple = Eq(fx, gx)
                solutions = solve(equation_simple, x)
                if not solutions: continue

                equation = Eq(Pow(base, fx, evaluate=False), Pow(base, gx, evaluate=False))

            elif eq_type == 'log_prop_sum': # log f(x) + log g(x) = log c ó c'
                base = Integer(random.choice([2, 3, 5, 10, E]))
                base_for_latex = base
                fx = _generate_linear_or_const(min_coef=-2, max_coef=3, allow_const=True, force_non_zero=True)
                gx = _generate_linear_or_const(min_coef=-2, max_coef=3, allow_const=True, force_non_zero=True)
                if fx.is_Number and fx <= 0: fx = abs(fx) + 1
                if gx.is_Number and gx <= 0: gx = abs(gx) + 1
                if simplify(fx * gx) == 0: continue

                sol_val = Integer(random.randint(1, 5))
                fx_val = fx.subs(x, sol_val)
                gx_val = gx.subs(x, sol_val)
                if fx_val <= 0 or gx_val <= 0: continue

                rhs_prod = fx_val * gx_val
                if random.choice([True, False]):
                    rhs = log(rhs_prod, base)
                else:
                    rhs_numeric = log(rhs_prod, base)
                    # --- CORRECCIÓN AQUÍ ---
                    if not rhs_numeric.has(x): # Usar .has(x)
                         rhs_numeric = nsimplify(rhs_numeric, rational=True)
                    # -----------------------
                    if not (rhs_numeric.is_Integer or rhs_numeric.is_Rational):
                        rhs = log(rhs_prod, base)
                    else:
                        rhs = rhs_numeric

                log_fx = log(fx, base)
                log_gx = log(gx, base)
                equation = Eq(log_fx + log_gx, rhs)

                internal_eq = Eq(fx * gx, rhs_prod)
                solutions = solve(internal_eq, x)

            elif eq_type == 'log_prop_diff': # log f(x) - log g(x) = log c ó c'
                 base = Integer(random.choice([2, 3, 5, 10, E]))
                 base_for_latex = base
                 fx = _generate_linear_or_const(min_coef=1, max_coef=5, force_non_zero=True)
                 gx = _generate_linear_or_const(min_coef=1, max_coef=3, force_non_zero=True)
                 if fx.is_Number and fx <= 0: fx = abs(fx) + 1
                 if gx.is_Number and gx <= 0: gx = abs(gx) + 1
                 if simplify(fx - gx) == 0: continue

                 sol_val = Integer(random.randint(1, 5))
                 fx_val = fx.subs(x, sol_val)
                 gx_val = gx.subs(x, sol_val)
                 if fx_val <= 0 or gx_val <= 0: continue
                 # Evitar división por cero simbólica si gx fuera constante 0 (aunque forzamos non_zero)
                 if gx == 0: continue

                 try:
                     rhs_ratio = Rational(fx_val, gx_val) # Usar Rational para división exacta
                 except ZeroDivisionError:
                     continue # Si gx_val fue cero
                     
                 if rhs_ratio <= 0: continue

                 if random.choice([True, False]):
                     rhs = log(rhs_ratio, base)
                 else:
                     rhs_numeric = log(rhs_ratio, base)
                     # --- CORRECCIÓN AQUÍ ---
                     if not rhs_numeric.has(x): # Usar .has(x)
                         rhs_numeric = nsimplify(rhs_numeric, rational=True)
                     # -----------------------
                     if not (rhs_numeric.is_Integer or rhs_numeric.is_Rational):
                         rhs = log(rhs_ratio, base)
                     else:
                         rhs = rhs_numeric

                 log_fx = log(fx, base)
                 log_gx = log(gx, base)
                 equation = Eq(log_fx - log_gx, rhs)

                 internal_eq = Eq(fx, rhs_ratio * gx)
                 solutions = solve(internal_eq, x)

            elif eq_type == 'exp_needs_log': # b^f(x) = c (c no potencia simple)
                base = Integer(random.choice([2, 3, 5, E]))
                base_for_latex = base
                fx = _generate_linear_or_const(allow_const=False, force_non_zero=True)
                rhs_val = Integer(random.randint(2, 50))
                try:
                    log_check = log(rhs_val, base)
                    # Check if integer or rational with denominator 1
                    is_simple_power = log_check.is_Integer or (log_check.is_Rational and log_check.q == 1)
                    if is_simple_power:
                        rhs_val += 1
                        if rhs_val <= 1 : rhs_val = Integer(random.randint(2, 5)) # Asegurar > 1
                        log_check = log(rhs_val, base)
                        is_simple_power = log_check.is_Integer or (log_check.is_Rational and log_check.q == 1)
                        if is_simple_power: continue # Reintentar si sigue siendo simple
                except (ValueError, TypeError): # log de <= 0 o error
                     continue

                lhs = Pow(base, fx, evaluate=False)
                rhs = rhs_val
                equation = Eq(lhs, rhs)
                solutions = solve(equation, x)

            else: # Fallback
                base, base_for_latex = 2, 2
                fx = x + 1
                rhs = 8
                equation = Eq(Pow(base, fx, evaluate=False), rhs)
                solutions = solve(equation, x)

            # --- Verificación Post-Generación ---
            if equation is None or solutions is None: continue

            if isinstance(solutions, sympy.sets.Set):
                 if solutions.is_FiniteSet: solutions = list(solutions)
                 else: solutions = []
            if not isinstance(solutions, list):
                if isinstance(solutions, (sympy.Expr, sympy.Number)): solutions = [solutions]
                else: solutions = []
            if not solutions: continue

            valid_solutions = _check_log_domain(equation, solutions)

            if not valid_solutions: continue

        except TypeError as te:
             print(f"TypeError durante generación: {te}. Reintentando...")
             continue
        except Exception as e:
            import traceback
            print(f"ERROR generando/resolviendo ecuación tipo '{eq_type}': {e}")
            continue

    # --- Fin del bucle while ---

    if not valid_solutions:
        print(f"ERROR: No se pudo generar un ejercicio válido tras {max_attempts} intentos.")
        return {
            "problem_latex": r"\text{Error en generación}",
            "solution_latex": r"\text{No se pudo generar}",
            "problem_sympy": None,
            "solution_sympy": None
        }

    # --- Formatear Salida ---
    try:
        use_ln = base_for_latex == E
        problem_latex = latex(equation, mode='plain', ln_notation=use_ln, mul_symbol='dot') # Usar dot para mul?

        formatted_solutions = []
        for sol in valid_solutions:
             try:
                 simplified_sol = nsimplify(sol, tolerance=1e-10, rational=True)
                 formatted_solutions.append(latex(simplified_sol, mode='plain', ln_notation=use_ln))
             except Exception:
                 formatted_solutions.append(latex(sol, mode='plain', ln_notation=use_ln))

        if not formatted_solutions:
             solution_latex = r"\text{No hay solución válida}"
        elif len(formatted_solutions) == 1:
             solution_latex = f"x = {formatted_solutions[0]}"
        else:
             solution_latex = "x = " + " \\text{ ó } x = ".join(formatted_solutions)

    except Exception as e:
        print(f"Error formateando LaTeX final: {e}")
        problem_latex = latex(equation) # Fallback LaTeX
        solution_latex = r"\text{Error de formato}"

    return {
        "problem_latex": problem_latex,
        "solution_latex": solution_latex,
        "problem_sympy": equation,
        "solution_sympy": valid_solutions
    }

# --- Bloque de Prueba ---
if __name__ == "__main__":
    print("Generando ejercicios de ecuaciones logarítmicas y exponenciales:")
    generated_count = 0
    attempt_count = 20
    for i in range(attempt_count):
        print(f"\n--- Intento {i+1} ---")
        try:
            exercise = generate_log_exp_exercise()
            if exercise["problem_sympy"] is not None:
                 generated_count += 1
                 print(f"Ecuación Sympy: {pretty(exercise['problem_sympy'])}")
                 print(f"Problema LaTeX: {exercise['problem_latex']}")
                 print(f"Soluciones Sympy (válidas): {exercise['solution_sympy']}")
                 print(f"Solución LaTeX: {exercise['solution_latex']}")
            else:
                 print("Fallo en la generación en este intento.")

        except Exception as e:
            import traceback
            print("\n!!! ERROR DURANTE LA GENERACIÓN DEL EJERCICIO DE PRUEBA !!!")
            print(traceback.format_exc())
    print(f"\nGenerados exitosamente: {generated_count} de {attempt_count} intentos.")