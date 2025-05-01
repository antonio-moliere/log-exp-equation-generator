*(La apariencia real dependerá del CSS)*

## Requisitos

*   Python 3.7+
*   Un gestor de paquetes como `pip` (usualmente viene con Python) o `conda`.
*   Un entorno virtual (recomendado: `venv` o `conda`).

## Configuración e Instalación Local

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git # Reemplaza con tu URL de GitHub
    cd tu-repositorio # Navega al directorio clonado
    ```

2.  **Crear y activar un entorno virtual:**
    *   Usando `venv` (recomendado si no usas Conda):
        ```bash
        python -m venv venv
        # Activar:
        #   Linux/macOS: source venv/bin/activate
        #   Windows:     .\venv\Scripts\activate
        ```
    *   Usando `conda`:
        ```bash
        conda create --name logexp_env python=3.9 # O la versión de Python que prefieras
        conda activate logexp_env
        ```

3.  **Instalar dependencias:** Dentro del entorno activado, ejecuta:
    ```bash
    pip install -r requirements.txt
    ```
    *(Asegúrate de que `requirements.txt` contenga al menos `Flask` y `sympy`)*.

## Ejecución Local

1.  Asegúrate de que tu entorno virtual esté activado.
2.  Ejecuta la aplicación Flask desde el directorio raíz del proyecto:
    ```bash
    python app.py
    ```
3.  Abre tu navegador web y ve a la dirección que indique Flask (normalmente `http://127.0.0.1:5000`).

## Despliegue en Vivo (Ejemplo con Render)

Esta aplicación se puede desplegar en plataformas como Render (que ofrece un plan gratuito).

1.  **Prepara el repositorio:**
    *   Asegúrate de que `requirements.txt` incluya `Flask`, `sympy` y `gunicorn`.
    *   Crea un archivo `Procfile` (sin extensión) en la raíz con el contenido: `web: gunicorn app:app`.
    *   Asegúrate de que `app.run()` en `app.py` no tenga `debug=True` para producción.
    *   Haz commit y push de estos archivos a GitHub.
2.  **En Render:**
    *   Crea una cuenta y un "New Web Service".
    *   Conecta tu repositorio de GitHub.
    *   Configura el servicio:
        *   **Name:** Elige un nombre (ej. `logexp-solver`).
        *   **Runtime:** Python 3.
        *   **Build Command:** `pip install -r requirements.txt`
        *   **Start Command:** `gunicorn app:app` (debería detectarlo del `Procfile`).
        *   **Plan:** Selecciona "Free".
    *   Crea el servicio y espera a que se despliegue.
    *   Accede a la URL proporcionada por Render (ej. `https://logexp-solver.onrender.com`).

## Estructura del Proyecto
/tu-repositorio
|-- /templates # Plantillas HTML (Jinja2)
| |-- base.html
| |-- index.html
|-- /static # Archivos estáticos (CSS, JS)
| |-- /css
| |-- style.css
|-- /modules # Módulos Python personalizados
| |-- init.py
| |-- log_exp_generator.py # Lógica del generador de ecuaciones
|-- app.py # Aplicación principal Flask
|-- requirements.txt # Dependencias Python (Flask, sympy, gunicorn)
|-- Procfile # Instrucciones para el servidor (Render, Heroku, etc.)
|-- README.md # Este archivo
|-- .gitignore # Archivos ignorados por Git


## Posibles Mejoras

*   Añadir niveles de dificultad más granulares.
*   Incluir más tipos de ecuaciones (cambio de base, sistemas, etc.).
*   Permitir al usuario introducir su respuesta y validarla.
*   Mostrar pasos intermedios de la solución (requiere lógica de resolución más compleja).
*   Mejorar la interfaz de usuario.
*   Añadir más variables simbólicas.

