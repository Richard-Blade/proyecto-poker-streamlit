# poker_logic/evaluator.py

# AHORA IMPORTAMOS DE TREYS (la librería sucesora y mejorada)
from treys import Card as TreysCard
from treys import Evaluator

def _convert_to_treys_format(card):
    """
    Función "privada" de ayuda.
    Convierte nuestro objeto Card (de cards.py) al formato
    que la librería 'treys' entiende (que es idéntico al de 'deuces').
    """
    
    # Mapeo de nuestros palos unicode a las letras que 'treys' espera
    suit_map = {"♠": "s", "♥": "h", "♦": "d", "♣": "c"}
    
    # 'treys' espera "As", "Kh", "Td", etc.
    treys_card_string = card.rank + suit_map[card.suit]
    
    # Crea el objeto Card especial de la librería
    return TreysCard.new(treys_card_string)

def evaluate_hand(player_hand, board):
    """
    Evalúa una mano de poker.
    
    Recibe 2 cartas de jugador y 5 de la mesa (nuestros objetos Card)
    y devuelve la puntuación y el nombre de la mano.
    """
    # 1. Crear la instancia del evaluador
    evaluator = Evaluator()
    
    # 2. Convertir nuestras cartas al formato de 'treys'
    treys_board = [_convert_to_treys_format(c) for c in board]
    treys_hand = [_convert_to_treys_format(c) for c in player_hand]
    
    # 3. Evaluar la mano
    # ¡Importante! 'treys' (y 'deuces') usa un sistema donde un NÚMERO MÁS BAJO es MEJOR.
    score = evaluator.evaluate(treys_board, treys_hand)
    
    # 4. Obtener el nombre legible de la mano (ej. "Full House")
    # El método 'get_class' ahora es 'get_rank_class' en treys, pero usamos
    # directamente 'class_to_string' que funciona con la puntuación.
    hand_name = evaluator.class_to_string(evaluator.get_rank_class(score))

    # Devolvemos la puntuación (para comparar) y el nombre (para mostrar)
    return score, hand_name