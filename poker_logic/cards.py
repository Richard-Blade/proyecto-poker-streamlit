# poker_logic/cards.py

import random

# Definimos los palos y rangos (usamos unicode para los palos)
SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"] # T para 10

class Card:
    """
    Representa una sola carta de poker con formato de color.
    """
    def __init__(self, rank, suit):
        # ... (Tu código de validación existente) ...
        if rank not in RANKS:
            raise ValueError(f"Rango inválido: {rank}")
        if suit not in SUITS:
            raise ValueError(f"Palo inválido: {suit}")
            
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        """
        Devuelve la representación de texto plano (usado para la lógica de importación).
        """
        return f"{self.rank}{self.suit}"

    def to_colored_markdown(self):
        """
        NUEVA FUNCIÓN: Devuelve la carta como una cadena Markdown con estilo HTML
        para que Streamlit la muestre con color.
        """
        # Los palos Rojos son Corazones y Diamantes
        if self.suit == "♥" or self.suit == "♦":
            color = "red"
        else:
            # Los palos Negros son Picas y Tréboles
            color = "black" 
        
        # Usamos un span de HTML dentro de la sintaxis Markdown
        # para aplicar el color al texto completo de la carta.
        return f'<span style="color:{color}; font-size: 1.2em;">{self.rank}{self.suit}</span>'


class Deck:
    """
    Representa una baraja de 52 cartas.
    """
    def __init__(self):
        # Creamos una lista fresca de 52 cartas
        self.cards = [Card(r, s) for s in SUITS for r in RANKS]
        self.shuffle()

    def shuffle(self):
        """Baraja las cartas en su sitio."""
        random.shuffle(self.cards)

    def deal(self, num_cards=1):
        """
        Reparte un número de cartas de la parte superior (final de la lista).
        Retorna una lista de cartas o una sola carta.
        """
        if len(self.cards) < num_cards:
            # En un juego real, aquí se re-barajaría o se terminaría el juego.
            # Para simulación, lanzamos un error.
            raise ValueError("No hay suficientes cartas en la baraja para repartir.")
            
        if num_cards == 1:
            return self.cards.pop()
        
        dealt_cards = []
        for _ in range(num_cards):
            dealt_cards.append(self.cards.pop())
        return dealt_cards

    def __len__(self):
        """Permite usar len(deck) para saber cuántas cartas quedan."""
        return len(self.cards)