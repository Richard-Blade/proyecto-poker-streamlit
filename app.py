import streamlit as st
from poker_logic.cards import Deck
from poker_logic.evaluator import evaluate_hand

# --- Configuración de la Página (Tarea 1: Nuevo Icono) ---
st.set_page_config(
    page_title="Entrenador de Crupier de Poker",
    page_icon="🃏", # Usamos el comodín para mejor estética
    layout="wide"
)

st.title("Mi Entrenador de Poker 🃏")

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
# Inicializamos TODAS las variables de estado

if 'hand_dealt' not in st.session_state:
    st.session_state.hand_dealt = False
    st.session_state.board = []
    st.session_state.player_hands = []
    st.session_state.winner_info = None
    st.session_state.quiz_answered = False
    # Tarea 2: Inicializar las selecciones del usuario (Diccionario vacío)
    st.session_state.user_selections = {} 

# --- Barra Lateral (Configuración) ---

with st.sidebar:
    st.header("Configuración")
    # Número de Jugadores (donde se define la cantidad)
    num_players = st.slider(
        "Número de Jugadores",
        min_value=2,
        max_value=9,
        value=3  
    )
    
    mode = st.radio(
        "Modo de Juego",
        ("Aleatorio (Quiz)", "Manual (Próximamente)")
    )

# --- Lógica Principal de la App ---

if mode == "Aleatorio (Quiz)":
    
    # Botón para repartir una nueva mano
    # Al hacer clic, se resetea el estado del quiz
    if st.button("Repartir Siguiente Mano"):
        deck = Deck()
        st.session_state.board = deck.deal(5)
        
        st.session_state.player_hands = []
        for _ in range(num_players):
            st.session_state.player_hands.append(deck.deal(2))
            
        # Resetear el estado del quiz y las selecciones
        st.session_state.hand_dealt = True
        st.session_state.quiz_answered = False
        st.session_state.winner_info = None
        # Necesario resetear las selecciones para que no arrastre la respuesta anterior
        st.session_state.user_selections = {} 
        # Forzamos una re-ejecución para limpiar la interfaz
        st.rerun() 

    # Si ya se repartió una mano, la mostramos
    if st.session_state.hand_dealt:      
        board_str = " ".join([card.to_colored_markdown() for card in st.session_state.board])
        st.markdown(f"### Mesa: {board_str}", unsafe_allow_html=True) 
        st.markdown("---")

        # Preparar columnas para el Quiz
        cols = st.columns(num_players)
        
        # Mostrar manos y checkboxes
        for i, hand in enumerate(st.session_state.player_hands):
            player_name = f"Jugador {i + 1}"
            hand_str = " ".join([card.to_colored_markdown() for card in hand])
            
            with cols[i]:
                st.subheader(player_name)
                # Mostramos las cartas del jugador
                st.markdown(hand_str, unsafe_allow_html=True)
                
                # CORRECCIÓN: Si el quiz NO ha sido respondido, mostramos el checkbox.
                # Si SÍ fue respondido, no mostramos nada aquí (se verá en el Detalle).
                is_selected = st.session_state.user_selections.get(i, False)
                
                if not st.session_state.quiz_answered:
                    st.session_state.user_selections[i] = st.checkbox(
                        f"Ganador", 
                        key=f"winner_checkbox_{i}",
                        value=is_selected 
                    )

        # --- Botón Evaluar y Lógica (Tarea 2) ---
        
        # El botón de Evaluación solo se muestra si el quiz NO ha sido respondido
        if not st.session_state.quiz_answered:
            col_eval = st.columns(num_players) 
            
            with col_eval[0]:
                if st.button("Evaluar Ganadores", key="evaluate_button"):
                    
                    # 1. Encontrar al ganador(es) real(es)
                    winner_indices, winner_hand_name, all_scores = find_winner(
                        st.session_state.player_hands, 
                        st.session_state.board
                    )
                    
                    # 2. Obtener las selecciones del usuario (los índices marcados)
                    user_selections_indices = [
                        i for i, is_checked in st.session_state.user_selections.items() if is_checked
                    ]

                    # 3. Comprobar la corrección: ¿Coinciden EXACTAMENTE las listas?
                    is_correct = sorted(user_selections_indices) == sorted(winner_indices)

                    # 4. Guardar la información del resultado
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
            
            # Formato de la lista de ganadores (ej. "Jugadores 1 y 3")
            winner_names = [f"Jugador {i + 1}" for i in info['winner_indices']]
            
            # Unimos los nombres para la cadena final (e.g., "Jugador 1 y 3" o "Jugador 2")
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
