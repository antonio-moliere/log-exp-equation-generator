from flask import Flask, render_template, url_for
import sys
import os
import random

# --- IMPORTAR EL NUEVO GENERADOR ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules')))
try:
    # Importa la nueva función
    from log_exp_generator import generate_log_exp_exercise # Cambiado
    generator_imported = True
    generator_error_msg = None
except ImportError as e:
    print(f"ERROR: No se pudo importar el generador: {e}")
    generator_imported = False
    generator_error_msg = str(e)
    # Define una función dummy
    def generate_log_exp_exercise(*args, **kwargs): # Cambiado
        return {
            "problem_latex": r"\text{Error al importar generador}",
            "solution_latex": r"\text{Revisar consola Flask}",
            "problem_sympy": None,
            "solution_sympy": None
        }

# ------------------------------------

app = Flask(__name__)

@app.route('/')
def index():
    print("--- Accediendo a la ruta / ---")
    exercise_data = None
    if not generator_imported:
         exercise_data = generate_log_exp_exercise() # Llama a la dummy
         print(f"Error de importación: {generator_error_msg}")
    else:
        try:
            # --- PARÁMETROS (si los hubiera, 'difficulty' por ahora) ---
            print(f"Generando ejercicio log/exp...")
            # --- LLAMAR AL NUEVO GENERADOR ---
            exercise_data = generate_log_exp_exercise(difficulty=1) # Cambiado
            # ----------------------------------
            if exercise_data and exercise_data.get("problem_latex"):
                 print(f"Datos generados (problema): {exercise_data['problem_latex']}")
            else:
                 print("Generador devolvió datos inválidos.")
                 # Asegurar que exercise_data no sea None o inválido
                 exercise_data = generate_log_exp_exercise() # Llamar a dummy

        except Exception as e:
            import traceback
            print(f"¡ERROR al generar el ejercicio dentro de la ruta!: {e}")
            print(traceback.format_exc())
            exercise_data = {
                "problem_latex": r"\text{Excepción durante la generación}",
                "solution_latex": f"Error: {e}",
                 "problem_sympy": None,
                 "solution_sympy": None
            }

    # Asegurar que exercise_data sea un diccionario válido para la plantilla
    if not isinstance(exercise_data, dict) or 'problem_latex' not in exercise_data:
         print("¡ALERTA! exercise_data no es un diccionario válido o está incompleto.")
         exercise_data = {
             "problem_latex": r"\text{Error interno en generación}",
             "solution_latex": r"\text{Revisar consola Flask}",
             "problem_sympy": None,
             "solution_sympy": None
         }

    print(f"Renderizando index.html...")
    return render_template('index.html', exercise=exercise_data)

if __name__ == '__main__':
    if not generator_imported:
         print(f"\n!!! ADVERTENCIA: No se pudo importar el generador ({generator_error_msg}). La aplicación mostrará errores. !!!\n")
    app.run(debug=True) # Usar debug=True para desarrollo