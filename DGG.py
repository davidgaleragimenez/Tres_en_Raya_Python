import tkinter as tk
from tkinter import messagebox
import random
import os
import pygame

# Paths for audio and icon files
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
MUSIC_PATH = os.path.join(BASE_PATH, "Clip.mp3")
ICON_PATH = os.path.join(BASE_PATH, "icono_3_en_raya.ico")

# Session score tracking variables
user_wins = 0
pc_wins = 0
ties = 0
game_started = False

def display_board(board):
    # Renders the current state of the board passed as a parameter
    # Updates the GUI buttons with corresponding symbols and colors
    if 'gui_buttons' in globals():
        for i in range(3):
            for j in range(3):
                token = board[i][j]
                if token not in ["X", "O", " "]:
                    gui_buttons[i][j].config(text=token, fg="#FFD700", bg="#107C41")
                else:
                    gui_buttons[i][j].config(text=token)
                    if token == "X":
                        gui_buttons[i][j].config(fg="#00D2FF", bg="#282C34")  
                    elif token == "O":
                        gui_buttons[i][j].config(fg="#FF6B4A", bg="#282C34")  
                    else:
                        gui_buttons[i][j].config(fg="#444444", bg="#282C34")  

def enter_move(board):
    # Handles placing the user's selected move onto the board array
    positions = {1:(0,0), 2:(0,1), 3:(0,2), 4:(1,0), 5:(1,1), 6:(1,2), 7:(2,0), 8:(2,1), 9:(2,2)}

    global gui_user_move
    if gui_user_move in positions:
        row, col = positions[gui_user_move]
        if board[row][col] == " ":
            board[row][col] = "X"

def get_empty_positions(board):
    # Scans the board and returns a list of coordinates for free spaces
    empty_spaces = []
    for i in range(0, 3):
        for j in range(0, 3):
            if str(board[i][j]) == " ":
                empty_spaces.append([i, j])
   
    return empty_spaces

def check_victory(board, token):
    # Evaluates the board state to check if the given token has won
    positions = {(0,0):1, (0,1):2, (0,2):3, (1,0):4, (1,1):5, (1,2):6, (2,0):7, (2,1):8, (2,2):9}
    winning_combinations = ({1,2,3}, {4,5,6}, {7,8,9}, {1,4,7}, {2,5,8}, {3,6,9}, {1,5,9}, {3,5,7})  
    
    # Store the board squares occupied by the target token
    token_squares = set()
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == token or (token == "X" and board[i][j] == "⭐") or (token == "O" and board[i][j] == "✨"):
                token_squares.add(positions[(i, j)])

    # Verify if any winning set is a subset of the occupied squares
    for combination in winning_combinations:
        if combination.issubset(token_squares):
            return combination
            
    return False

def draw_pc_move(board):
    # Selects a random position from available free squares for the AI turn
    empty_spaces = get_empty_positions(board)
    if empty_spaces:
        chosen_move = random.choice(empty_spaces)
        row, col = chosen_move[0], chosen_move[1]
        board[row][col] = "O"

def open_documentation(main_window):
    # Secondary window presenting the basic accessible user guide
    doc = tk.Toplevel(main_window)
    doc.title("User Guide | Classic Tic-Tac-Toe")
    doc.geometry("350x480")
    doc.resizable(False, False)
    doc.configure(bg="#1E222A")
    
    try:
        doc.iconbitmap(ICON_PATH)
    except Exception:
        pass
    
    doc.transient(main_window)
    doc.grab_set()

    title_label = tk.Label(
        doc, text="HOW TO PLAY TIC-TAC-TOE", 
        font=("Segoe UI", 12, "bold"), bg="#1E222A", fg="#00D2FF"
    )
    title_label.pack(pady=(15, 10))

    guide_text = (
        "1. GAME OBJECTIVE:\n"
        "• Your goal is to align three of your tokens (X) in a row.\n"
        "• Lines can be horizontal, vertical, or diagonal.\n\n"
        "2. CONTROLS AND TURNS:\n"
        "• Click on any empty cell to place your 'X'.\n"
        "• Once pressed, the game automatically switches the\n"
        "  turn to the Computer's Artificial Intelligence (O).\n\n"
        "3. COLOR CODING MEANING:\n"
        "• Light Blue (X): Represents your moves.\n"
        "• Orange (O): Represents the PC's moves.\n"
        "• Green with Stars (⭐): Indicates the winning line.\n\n"
        "4. SESSION SCOREBOARD:\n"
        "• Permanently records your wins, the computer's wins,\n"
        "  and the total number of ties in this session.\n\n"
        "5. AUDIO SECTION (BOTTOM BAR):\n"
        "• Slider: Adjusts the precise volume of the music.\n"
        "• Mute Button: Instantly toggles sound on or off."
    )

    content_label = tk.Label(
        doc, text=guide_text, font=("Segoe UI", 9, "bold"), 
        bg="#282C34", fg="#ABB2BF", justify="left", relief="flat", padx=15, pady=15
    )
    content_label.pack(padx=15, pady=5, fill="both", expand=True)

    close_button = tk.Button(
        doc, text="Got it", font=("Segoe UI", 10, "bold"),
        bg="#4B5263", fg="white", bd=0, padx=20, pady=6, cursor="hand2",
        command=doc.destroy
    )
    close_button.pack(pady=15)

def play_game():
    # Initializes the 3x3 board structure matrix with blank spaces
    board = [[" " for col in range(3)] for row in range(3)]  
    print("Let's play Tic-Tac-Toe. Good luck!")

    # Global window components setup
    global gui_user_move, gui_buttons, scoreboard_label, turn_label, welcome_label
    global user_wins, pc_wins, ties, game_started
    
    gui_user_move = None
    game_started = False  
    
    BACKGROUND_COLOR = "#1E222A"      
    LINE_COLOR = "#5C6370"      
    BUTTON_COLOR = "#282C34"      
    
    window = tk.Tk()
    window.title("Tic-Tac-Toe | Classic Mode")
    
    # Initialize background music engine with Pygame
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_PATH)  
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Error loading background music: {e}")

    # Set the master window icon
    try:
        window.iconbitmap(ICON_PATH)  
    except Exception:
        pass
    
    # Calculate geometric values to center the window layout onto the monitor
    window_width = 380
    window_height = 620  
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    pos_x = int((screen_width / 2) - (window_width / 2))
    pos_y = int((screen_height / 2) - (window_height / 2))
    
    window.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
    window.resizable(False, False)
    window.configure(bg=BACKGROUND_COLOR)
    
    welcome_label = tk.Label(
        window,
        text="Let's play Tic-Tac-Toe! Good luck!",
        font=("Segoe UI", 10, "bold"),
        bg=BACKGROUND_COLOR,
        fg="#98C379"  
    )
    welcome_label.pack(pady=(15, 0))
    
    # Header display design containing scores and turn statuses
    header_frame = tk.Frame(window, bg=BACKGROUND_COLOR)
    header_frame.pack(pady=(10, 5), fill="x", padx=15)
    header_frame.columnconfigure(0, weight=1)
    header_frame.columnconfigure(1, weight=1)
    
    scoreboard_label = tk.Label(
        header_frame, 
        text=f"You: {user_wins} | PC: {pc_wins} | Ties: {ties}", 
        font=("Segoe UI", 10, "bold"),
        bg=BACKGROUND_COLOR,
        fg="#ABB2BF"                                                                                                                                                                                                                                    
    )
    scoreboard_label.grid(row=0, column=0, sticky="w")
    
    turn_label = tk.Label(
        header_frame,
        text="Turn: PLAYER (X)",
        font=("Segoe UI", 10, "bold"),
        bg=BACKGROUND_COLOR,
        fg="#00D2FF"  
    )
    turn_label.grid(row=0, column=1, sticky="e")
    
    # Grid construction for the interaction board
    board_frame = tk.Frame(window, bg=LINE_COLOR, bd=1)
    board_frame.pack(pady=10)
    
    gui_buttons = [[None for _ in range(3)] for _ in range(3)]
    coordinates_to_number = {(0,0):1, (0,1):2, (0,2):3, (1,0):4, (1,1):5, (1,2):6, (2,0):7, (2,1):8, (2,2):9}
    number_to_coordinates = {v: k for k, v in coordinates_to_number.items()}
    
    # Visual feedback handler highlighting the winning vector sequence
    def illuminate_victory(winning_line, vfx_symbol):
        for square_number in winning_line:
            r, c = number_to_coordinates[square_number]
            board[r][c] = vfx_symbol  
            gui_buttons[r][c].config(
                text=vfx_symbol, 
                fg="#FFD700",       
                bg="#107C41",       
                activebackground="#107C41"
            )

    # Core logic execution when grid squares receive interaction clicks
    def handle_click(r, c):
        global gui_user_move, scoreboard_label, turn_label, welcome_label
        global user_wins, ties, game_started
        
        if board[r][c] != " " or check_victory(board, "X") or check_victory(board, "O") or not get_empty_positions(board):
            return

        if not game_started:
            game_started = True
            welcome_label.config(text="")

        gui_user_move = coordinates_to_number[(r, c)]
        enter_move(board) 
        display_board(board)
        
        line_x = check_victory(board, "X")
        if line_x:
            user_wins += 1  
            scoreboard_label.config(text=f"You: {user_wins} | PC: {pc_wins} | Ties: {ties}")
            illuminate_victory(line_x, "⭐")
            window.after(600, lambda: messagebox.showinfo("Match Over", "Congratulations, you won!"))
            return
            
        if not get_empty_positions(board):
            ties += 1
            scoreboard_label.config(text=f"You: {user_wins} | PC: {pc_wins} | Ties: {ties}")
            messagebox.showinfo("Match Over", "It's a tie! The board is full.")
            return
            
        turn_label.config(text="Turn: PC THINKING...", fg="#FF6B4A")
        window.after(850, execute_pc_turn)

    # Handles the scheduled automated AI sequence move
    def execute_pc_turn():
        global pc_wins, ties, scoreboard_label, turn_label
        draw_pc_move(board)
        display_board(board)
        
        line_o = check_victory(board, "O")
        if line_o:
            pc_wins += 1  
            scoreboard_label.config(text=f"You: {user_wins} | PC: {pc_wins} | Ties: {ties}")
            illuminate_victory(line_o, "✨")
            window.after(600, lambda: messagebox.showinfo("Match Over", "The computer won."))
            return
            
        if not get_empty_positions(board):
            ties += 1
            scoreboard_label.config(text=f"You: {user_wins} | PC: {pc_wins} | Ties: {ties}")
            messagebox.showinfo("Match Over", "It's a tie! The board is full.")
            return

        turn_label.config(text="Turn: PLAYER (X)", fg="#00D2FF")

    # Resets the active matching board states to clean states
    def reset_board_gui():
        global game_started, welcome_label, turn_label
        for i in range(3):
            for j in range(3):
                board[i][j] = " "
        display_board(board)
        
        game_started = False
        welcome_label.config(text="Let's play Tic-Tac-Toe! Good luck!")
        turn_label.config(text="Turn: PLAYER (X)", fg="#00D2FF")

    # Map grid structures assigning button widgets to matrix points
    for i in range(3):
        for j in range(3):
            gui_buttons[i][j] = tk.Button(
                board_frame, 
                text=" ", 
                font=("Segoe UI", 24, "bold"),
                width=5, 
                height=2,
                bg=BUTTON_COLOR,
                activebackground="#3E4452", 
                bd=0,                                     
                relief="flat",                                
                cursor="hand2",                             
                command=lambda row_idx=i, col_idx=j: handle_click(row_idx, col_idx)
            )
            gui_buttons[i][j].grid(row=i, column=j, padx=2, pady=2)
            
    # Bottom actions layout containment panel
    actions_frame = tk.Frame(window, bg=BACKGROUND_COLOR)
    actions_frame.pack(pady=10)
    
    reset_button = tk.Button(
        actions_frame, 
        text="Reset Board", 
        font=("Segoe UI", 10, "bold"), 
        bg="#4B5263",                                  
        fg="white",
        activebackground="#5C6370",
        bd=0,
        padx=15,
        pady=8,
        cursor="hand2",
        command=reset_board_gui
    )
    reset_button.grid(row=0, column=0, padx=5)

    doc_button = tk.Button(
        actions_frame, 
        text="❓ Game Guide", 
        font=("Segoe UI", 10, "bold"), 
        bg="#282C34",                                  
        fg="#00D2FF",
        activebackground="#3E4452",
        bd=0,
        padx=15,
        pady=8,
        cursor="hand2",
        command=lambda: open_documentation(window)
    )
    doc_button.grid(row=0, column=1, padx=5)
    
    # Accessible volume mixer scale track controller UI elements
    volume_label = tk.Label(
        window, 
        text="Music Volume",
        font=("Segoe UI", 9, "bold"),
        bg=BACKGROUND_COLOR,
        fg="#ABB2BF"
    )
    volume_label.pack(pady=(10, 0))

    audio_frame = tk.Frame(window, bg=BACKGROUND_COLOR)
    audio_frame.pack(pady=(0, 15), fill="x", padx=40)
    audio_frame.columnconfigure(0, weight=3)
    audio_frame.columnconfigure(1, weight=1)

    def change_volume(value):
        vol = float(value) / 100
        pygame.mixer.music.set_volume(vol)
        if vol > 0:
            mute_button.config(text="🔊 Mute", bg="#4B5263")
        else:
            mute_button.config(text="🔇 Unmute", bg="#FF6B4A")

    def toggle_mute():
        current_volume = pygame.mixer.music.get_volume()
        if current_volume > 0:
            pygame.mixer.music.set_volume(0.0)
            volume_control.set(0)
            mute_button.config(text="🔇 Unmute", bg="#FF6B4A")
        else:
            pygame.mixer.music.set_volume(0.2)
            volume_control.set(20)
            mute_button.config(text="🔊 Mute", bg="#4B5263")

    volume_control = tk.Scale(
        audio_frame, 
        from_=0, 
        to=100, 
        orient="horizontal", 
        font=("Segoe UI", 9, "bold"),
        bg=BACKGROUND_COLOR,
        fg="#ABB2BF",
        highlightthickness=0,
        troughcolor="#3F4756",
        activebackground="#00D2FF",
        command=change_volume
    )
    volume_control.set(20)  
    volume_control.grid(row=0, column=0, sticky="ews", padx=(0, 15))

    mute_button = tk.Button(
        audio_frame,
        text="🔊 Mute",
        font=("Segoe UI", 9, "bold"),
        bg="#4B5263",
        fg="white",
        bd=0,
        padx=12,
        pady=5,  
        cursor="hand2",
        command=toggle_mute
    )
    mute_button.grid(row=0, column=1, sticky="es")
    
    display_board(board)

    def close_application():
        pygame.mixer.music.stop()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", close_application)
    window.mainloop()

# MAIN RUNTIME APPLICATION INITIATOR
play_game()
