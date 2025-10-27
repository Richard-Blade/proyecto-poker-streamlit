import streamlit as st
from poker_logic.cards import Deck
from poker_logic.evaluator import evaluate_hand

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Entrenador de Crupier de Poker",
    page_icon="♠", # Ícono corregido para mejor visualización en el navegador
    layout="wide"
)

st.title("Mi Entrenador de Poker ♠")

# --- Funciones de Lógica del Quiz ---

def find_winner(player_hands, board):
    """
    Evalúa todas las manos y encuentra a TODOS los jugadores con la mejor puntuación.
    Devuelve una lista de índices de ganadores y el nombre de la mano ganadora.
    """
    scores = []
    for hand in player_hands:
        score, name = evaluate_hand(hand, board)
        scores.append({'score': score, 'name': name})

    # Encontrar la MEJOR puntuación (la más baja)
    best_score = min(s['score'] for s in scores)
    
    # Encontrar todos los jugadores que tienen esa MEJOR puntuación (los ganadores)
    winner_indices = [i for i, s in enumerate(scores) if s['score'] == best_score]
    
    # Obtener el nombre de la mano ganadora
    winner_hand_name = [s['name'] for s in scores if s['score'] == best_score][0]
    
    # Devolvemos la lista de índices de ganadores y todas las puntuaciones
    return winner_indices, winner_hand_name, scores


# --- Estado de Sesión (Memoria de la App) ---

if 'hand_dealt' not in st.session_state:
    st.session_state.hand_dealt = False
    st.session_state.board = []
    st.session_state.player_hands = []
    st.session_state.winner_info = None
    st.session_state.quiz_answered = False
    st.session_state.user_selections = {} 
    
    # Variables para el seguimiento de rendimiento
    st.session_state.total_hands = 0
    st.session_state.correct_predictions = 0
    # NUEVO: Contador de racha positiva
    st.session_state.consecutive_correct = 0

# --- Barra Lateral (Configuración y Estadísticas) ---

with st.sidebar:
    st.header("Configuración")
    num_players = st.slider(
        "Número de Jugadores",
        min_value=2,
        max_value=9,
        value=5 
    )
    
    mode = st.radio(
        "Modo de Juego",
        ("Aleatorio (Quiz)", "Manual (Próximamente)")
    )
    
    st.markdown("---")
    st.header("Estadísticas de Rendimiento")
    
    # Métrica de Racha Positiva
    st.metric(label="Racha Positiva", value=f"{st.session_state.consecutive_correct} Manos")

    st.markdown("---")
    
    # Mostramos las métricas de evaluación AHORA EN FILAS
    if st.session_state.total_hands > 0:
        accuracy = (st.session_state.correct_predictions / st.session_state.total_hands) * 100
        
        # Muestra en Filas (usando un formato más limpio sin st.columns)
        st.metric(label="Manos Jugadas", value=st.session_state.total_hands)
        st.metric(label="Respuestas Correctas", value=st.session_state.correct_predictions)
        st.metric(label="Precisión", value=f"{accuracy:.1f}%")
        
        # Si la precisión es baja, podemos dar un mensaje de motivación
        if accuracy < 70:
            st.warning("¡Sigue practicando! Tu objetivo es alcanzar una precisión superior al 90%.")
        elif accuracy >= 90:
            st.success("¡Excelente precisión! Estás listo para repartir.")
            
    else:
        st.info("Juega tu primera mano para ver las estadísticas de tu precisión.")

# --- Lógica Principal de la App ---

if mode == "Aleatorio (Quiz)":
    
    # Botón para repartir una nueva mano
    if st.button("Repartir Siguiente Mano"):
        deck = Deck()
        st.session_state.board = deck.deal(5)
        
        st.session_state.player_hands = []
        for _ in range(num_players):
            st.session_state.player_hands.append(deck.deal(2))
            
        # Resetear el estado
        st.session_state.hand_dealt = True
        st.session_state.quiz_answered = False
        st.session_state.winner_info = None
        st.session_state.user_selections = {} 
        st.rerun() 

    # Si ya se repartió una mano, la mostramos
    if st.session_state.hand_dealt:      
        board_str = " ".join([card.to_colored_markdown() for card in st.session_state.board])
        st.markdown(f"### Mesa: {board_str}", unsafe_allow_html=True) 
        st.markdown("---")

        cols = st.columns(num_players)
        
        # Mostrar manos y checkboxes
        for i, hand in enumerate(st.session_state.player_hands):
            player_name = f"Jugador {i + 1}"
            hand_str = " ".join([card.to_colored_markdown() for card in hand])
            
            with cols[i]:
                st.subheader(player_name)
                st.markdown(hand_str, unsafe_allow_html=True)
                
                is_selected = st.session_state.user_selections.get(i, False)
                
                if not st.session_state.quiz_answered:
                    st.session_state.user_selections[i] = st.checkbox(
                        f"Ganador", 
                        key=f"winner_checkbox_{i}",
                        value=is_selected 
                    )

        # --- Botón Evaluar y Lógica ---
        
        if not st.session_state.quiz_answered:
            col_eval = st.columns(num_players) 
            
            with col_eval[0]:
                if st.button("Evaluar Ganadores", key="evaluate_button"):
                    
                    winner_indices, winner_hand_name, all_scores = find_winner(
                        st.session_state.player_hands, 
                        st.session_state.board
                    )
                    
                    user_selections_indices = [
                        i for i, is_checked in st.session_state.user_selections.items() if is_checked
                    ]

                    is_correct = sorted(user_selections_indices) == sorted(winner_indices)

                    # --- Lógica de Racha y Contadores ---
                    st.session_state.total_hands += 1 

                    if is_correct:
                        st.session_state.correct_predictions += 1
                        st.session_state.consecutive_correct += 1 # Acierto: Incrementa racha
                    else:
                        st.session_state.consecutive_correct = 0 # Error: Resetea racha

                    # --- Activación de Globos (Cada 10 aciertos en racha) ---
                    if st.session_state.consecutive_correct > 0 and st.session_state.consecutive_correct % 10 == 0:
                        st.balloons()
                        
                    st.session_state.quiz_answered = True
                    st.session_state.winner_info = {
                        "winner_indices": winner_indices,
                        "winner_hand_name": winner_hand_name,
                        "user_correct": is_correct,
                        "all_scores": all_scores 
                    }
                    st.rerun()

        # --- Mostrar el Resultado y Feedback ---
        if st.session_state.quiz_answered and st.session_state.winner_info:
            info = st.session_state.winner_info
            
            # NOTA: La lógica de incremento/reset de contadores se movió arriba,
            # ANTES del st.rerun, por lo que aquí solo mostramos el resultado.

            winner_names = [f"Jugador {i + 1}" for i in info['winner_indices']]
            
            if len(winner_names) > 1:
                 winner_str = f"{', '.join(winner_names[:-1])} y {winner_names[-1]}"
            else:
                 winner_str = winner_names[0]

            if info["user_correct"]:
                st.success(f"¡Correcto! ✅ {winner_str} gana(n) con {info['winner_hand_name']}.")
            else:
                st.error(f"Incorrecto. ❌ El(Los) ganador(es) era(n) {winner_str} con {info['winner_hand_name']}.")
                
            # Agregamos feedback para mostrar la jugada de cada jugador (con la elección del usuario)
            st.subheader("Detalle de Manos (Para Entrenamiento):")
            for i, score_data in enumerate(info['all_scores']):
                is_winner = i in info['winner_indices']
                is_selected = st.session_state.user_selections.get(i, False)

                prefix = ""
                selection_status = ""
                
                # 1. Icono para el Ganador Real
                if is_winner:
                    prefix += "🥇 "

                # 2. Indicador de la Selección del Usuario
                if is_selected:
                    if is_winner:
                        selection_status = ' <span style="color:green; font-weight:bold;">(Selección Correcta)</span>'
                    else:
                        selection_status = ' <span style="color:red; font-weight:bold;">(Tu Selección)</span>'
                elif is_winner:
                    # El usuario no seleccionó al ganador (Error de omisión)
                    selection_status = ' <span style="color:red; font-weight:bold;">(Ganador Omitido)</span>'

                st.markdown(
                    f"**{prefix}Jugador {i + 1}:** **{score_data['name']}**{selection_status}",
                    unsafe_allow_html=True
                )
            
            # Botón para la siguiente mano (CORRECCIÓN: Se agrega user_selections={})
            st.button("Repartir Siguiente Mano", on_click=lambda: st.session_state.update(
                hand_dealt=False, quiz_answered=False, winner_info=None, user_selections={}
            ), key="next_hand_after_eval")


elif mode == "Manual (Próximamente)":
    st.info("El modo manual para ingresar cartas específicas está en construcción. 🏗️")
