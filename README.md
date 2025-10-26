## Estructura de archivos ##

```
proyecto_poker_streamlit/
│
├── .gitignore
├── README.md
├── requirements.txt
├── app.py
│
└── poker_logic/
    ├── __init__.py
    ├── cards.py
    ├── evaluator.py
    └── table.py
```
## Explicación de cada archivo ##
```proyecto_poker_streamlit/``` : Es la carpeta raíz de tu proyecto. Esto es lo que subirás a GitHub.

`.gitignore` : Un archivo crucial para Git. Le dice qué archivos y carpetas ignorar (como entornos virtuales, archivos de caché de Python, etc.).

`README.md` : El "manual" de tu proyecto. Aquí explicas qué hace, cómo instalarlo (`pip install -r requirements.txt`) y cómo ejecutarlo (`streamlit run app.py`).

`requirements.txt` : Una lista de las librerías de Python que necesita tu proyecto. Como mínimo, aquí irá streamlit.

`app.py` : ¡Este es tu programa principal! 💻 Aquí es donde escribirás el código de Streamlit. Importará las funciones de la carpeta poker_logic para mostrar la mesa, las cartas, los botones y el resultado.

```poker_logic/``` : Este es un "paquete" de Python (gracias al `__init__.py`) que contendrá toda la lógica del juego, separada de la interfaz.

`__init__.py` : Un archivo (usualmente vacío) que le dice a Python que esta carpeta debe tratarse como un módulo.

`cards.py` : Aquí definirás tus clases básicas:`Card` (con un palo y un rango, ej. "Corazones", "As" ) y `Deck` (una baraja de 52 cartas con métodos para barajar y repartir).

`table.py` : Podría manejar el estado del juego: cuántos jugadores hay, qué cartas tienen, las cartas de la mesa (Flop, Turn, River) y el bote.

`evaluator.py` : Para tu Fase 1, este es el archivo más importante. 🧠 Contendrá la lógica para determinar la "fuerza" de una mano (ej.`evaluar_mano_de_7_cartas`). Recibirá las 2 cartas del jugador y las 5 de la mesa y devolverá qué jugada tiene (Par, Doble Par, Trío, Escalera, Color, Full House, Poker, Escalera de Color, Escalera Real).