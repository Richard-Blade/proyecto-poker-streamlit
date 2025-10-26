import streamlit as st
from poker_logic.cards import Deck
from poker_logic.evaluator import evaluate_hand

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Entrenador de Crupier de Poker",
    page_icon="♠️",
    layout="wide"
)

st.title("Mi Entrenador de Poker ♠️")

# --- Funciones de Lógica del Quiz ---

def find_winner(player_hands, board):
    """
    Evalúa todas las manos y encuentra al ganador.
    Devuelve el índice del ganador y los detalles de su mano.
    """
    scores = []
    for hand in player_hands:
        # evaluate_hand nos da (score, hand_name)
        # Recordar: en 'deuces', un score más BAJO es mejor.
        score, name = evaluate_hand(hand, board)
        scores.append({'score': score, 'name': name})

    # Encontrar la puntuación más baja (la mejor mano)
    best_score = min(s['score'] for s in scores)
    
    # Encontrar el índice del jugador con esa puntuación
    # (Manejo simple, no considera empates por ahora)
    winner_index = [i for i, s in enumerate(scores) if s['score'] == best_score][0]
    
    return winner_index, scores[winner_index]['name']

# --- Estado de Sesión (Memoria de la App) ---
# Necesitamos guardar el estado del juego entre clics de botones

if 'hand_dealt' not in st.session_state:
    st.session_state.hand_dealt = False
    st.session_state.board = []
    st.session_state.player_hands = []
    st.session_state.winner_info = None
    st.session_state.quiz_answered = False

# --- Barra Lateral (Configuración) ---

with st.sidebar:
    st.header("Configuración")
    num_players = st.slider(
        "Número de Jugadores",
        min_value=2,
        max_value=9,
        value=3  # Valor inicial
    )
    
    mode = st.radio(
        "Modo de Juego",
        ("Aleatorio (Quiz)", "Manual (Próximamente)")
    )

# --- Lógica Principal de la App ---

if mode == "Aleatorio (Quiz)":
    
    # Botón para repartir una nueva mano
    if st.button("Repartir Siguiente Mano"):
        # 1. Crear y barajar la baraja
        deck = Deck()
        
        # 2. Guardar las cartas de la mesa (Flop, Turn, River)
        st.session_state.board = deck.deal(5)
        
        # 3. Repartir a cada jugador
        st.session_state.player_hands = []
        for _ in range(num_players):
            st.session_state.player_hands.append(deck.deal(2))
            
        # 4. Resetear el estado del quiz
        st.session_state.hand_dealt = True
        st.session_state.quiz_answered = False
        st.session_state.winner_info = None

    # Si ya se repartió una mano, la mostramos
    if st.session_state.hand_dealt:
        
        # Mostrar la mesa (usamos st.code para un formato monoespaciado)
        #board_str = " ".join([str(card) for card in st.session_state.board])
        #st.header(f"Mesa: {board_str}")
        #st.markdown("---")

        board_str = " ".join([card.to_colored_markdown() for card in st.session_state.board])
        # Usamos st.markdown con unsafe_allow_html=True para interpretar el color
        st.markdown(f"## Mesa: {board_str}", unsafe_allow_html=True)


        # Preparar columnas para el Quiz
        cols = st.columns(num_players)
        
        # Variable para almacenar la elección del usuario
        user_choice = -1

        for i, hand in enumerate(st.session_state.player_hands):
            player_name = f"Jugador {i + 1}"
            # hand_str = " ".join([str(card) for card in hand])
            hand_str = " ".join([card.to_colored_markdown() for card in hand])

            with cols[i]:
                st.subheader(player_name)
                # Mostramos las cartas del jugador, usando st.markdown con HTML
                st.markdown(hand_str, unsafe_allow_html=True)
            
            #with cols[i]:
            #    st.subheader(player_name)
            #    Mostramos las cartas del jugador
            #    st.code(hand_str, language=None)
                
                # Botón de Quiz (solo si aún no se ha respondido)
                if not st.session_state.quiz_answered:
                    if st.button(f"Gana {player_name}", key=f"player_{i}"):
                        user_choice = i

        # --- Lógica de Evaluación del Quiz ---
        
        # Si el usuario acaba de hacer clic en un botón (user_choice != -1)
        if user_choice != -1:
            st.session_state.quiz_answered = True
            
            # Encontrar al ganador real
            winner_index, winner_hand_name = find_winner(
                st.session_state.player_hands, 
                st.session_state.board
            )
            
            # Guardar la información del ganador
            st.session_state.winner_info = {
                "index": winner_index,
                "name": winner_hand_name,
                "user_correct": (user_choice == winner_index)
            }

        # Mostrar el resultado DESPUÉS de que se haya respondido
        if st.session_state.quiz_answered and st.session_state.winner_info:
            info = st.session_state.winner_info
            winner_name = f"Jugador {info['index'] + 1}"
            
            if info["user_correct"]:
                st.success(f"¡Correcto! ✅ {winner_name} gana con {info['name']}.")
            else:
                st.error(f"Incorrecto. ❌ El ganador era {winner_name} con {info['name']}.")

elif mode == "Manual (Próximamente)":
    st.info("El modo manual para ingresar cartas específicas está en construcción. 🏗️")