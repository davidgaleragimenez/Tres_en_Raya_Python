import tkinter as tk
from tkinter import messagebox
import random
import os
import pygame

# Rutas para el audio y el icono
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_MUSICA = os.path.join(RUTA_BASE, "Clip.mp3")
RUTA_ICONO = os.path.join(RUTA_BASE, "icono_3_en_raya.ico")

# Variables para llevar la cuenta de la sesión
victorias_usuario = 0
victorias_pc = 0
empates = 0
partida_iniciada = False

def muestra_tablero(board):
    # Muestra por pantalla el tablero pasado como parámetro (board)
    # Actualiza los botones de la interfaz gráfica con las fichas y colores
    if 'botones_gui' in globals():
        for i in range(3):
            for j in range(3):
                ficha = board[i][j]
                if ficha not in ["X", "O", " "]:
                    botones_gui[i][j].config(text=ficha, fg="#FFD700", bg="#107C41")
                else:
                    botones_gui[i][j].config(text=ficha)
                    if ficha == "X":
                        botones_gui[i][j].config(fg="#00D2FF", bg="#282C34")  
                    elif ficha == "O":
                        botones_gui[i][j].config(fg="#FF6B4A", bg="#282C34")  
                    else:
                        botones_gui[i][j].config(fg="#444444", bg="#282C34")  

def entra_movimiento(board):
    # funcion para que el usuario introduzca su movimiento
    posiciones={1:(0,0),2:(0,1),3:(0,2),4:(1,0),5:(1,1),6:(1,2),7:(2,0),8:(2,1),9:(2,2)}

    # falta tener en cuenta excepciones, como no introducir carácter válido
    # aquí, de momento, consideramos que es correcto
    global movimiento_usuario_gui
    if movimiento_usuario_gui in posiciones:
        fila, columna = posiciones[movimiento_usuario_gui]
        if board[fila][columna] == " ":
            board[fila][columna] = "X"

def lista_de_pos_vacias(board):
    # funcion para comprobar espacios libres
    vacios=[]
    for i in range(0,3):
        for j in range (0,3):
            if str(board[i][j])==" ":
                vacios.append([i,j])
   
    return vacios

def victoria_para(board, ficha):
    # funcion para comprobar quien gana, debe devolver un true o false
    posiciones={(0,0):1,(0,1):2,(0,2):3,(1,0):4,(1,1):5,(1,2):6,(2,0):7,(2,1):8,(2,2):9}
    victorias=({1,2,3},{4,5,6},{7,8,9},{1,4,7},{2,5,8},{3,6,9},{1,5,9},{3,5,7})  # combinaciones de victorias posibles
    
    # guardamos las casillas que el jugador "ficha" tiene ocupadas
    casillas_ficha=set()
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == ficha or (ficha == "X" and board[i][j] == "⭐") or (ficha == "O" and board[i][j] == "✨"):
                casillas_ficha.add(posiciones[(i, j)])

    # vemos si las posibles victorias están en el conjunto de victorias
    for combinacion in victorias:
        if combinacion.issubset(casillas_ficha):
            return combinacion
            
    return False

def dibuja_movimiento_maquina(board):
    # funcion para pintar el movimiento de la máquina 
    # tomamos, de las casillas vacías, una posición random
    vacios = lista_de_pos_vacias(board)
    if vacios:
        movimiento = random.choice(vacios)
        fila, columna = movimiento[0], movimiento[1]
        board[fila][columna] = "O"

def abrir_documentacion(ventana_principal):
    # Ventana secundaria con la guia basica del juego
    doc = tk.Toplevel(ventana_principal)
    doc.title("Guía de Uso | 3 en Raya Clásico")
    doc.geometry("350x480")
    doc.resizable(False, False)
    doc.configure(bg="#1E222A")
    
    try:
        doc.iconbitmap(RUTA_ICONO)
    except Exception:
        pass
    
    doc.transient(ventana_principal)
    doc.grab_set()

    titulo = tk.Label(
        doc, text="CÓMO JUGAR AL 3 EN RAYA", 
        font=("Segoe UI", 12, "bold"), bg="#1E222A", fg="#00D2FF"
    )
    titulo.pack(pady=(15, 10))

    texto_guia = (
        "1. OBJETIVO DEL JUEGO:\n"
        "• Tu meta es colocar tres fichas tuyas (X) seguidas.\n"
        "• Puede ser en línea horizontal, vertical o diagonal.\n\n"
        "2. CONTROLES Y TURNOS:\n"
        "• Haz clic en cualquier casilla vacía para colocar tu 'X'.\n"
        "• Al pulsar, el juego pasará de forma automática el\n"
        "  turno a la Inteligencia Artificial del Ordenador (O).\n\n"
        "3. SIGNIFICADO DE LOS COLORES:\n"
        "• Azul Claro (X): Representa tus movimientos.\n"
        "• Naranja (O): Representa los movimientos de la PC.\n"
        "• Verde con Estrellas (⭐): Indica la línea ganadora.\n\n"
        "4. MARCADOR GENERAL:\n"
        "• Registra permanentemente tus victorias, las de la\n"
        "  máquina y la cantidad de empates de la sesión.\n\n"
        "5. SECCIÓN DE AUDIO (BARRA INFERIOR):\n"
        "• Deslizador: Ajusta el volumen exacto de la música.\n"
        "• Botón Silenciar: Apaga o enciende el sonido al instante."
    )

    contenido = tk.Label(
        doc, text=texto_guia, font=("Segoe UI", 9, "bold"), 
        bg="#282C34", fg="#ABB2BF", justify="left", relief="flat", padx=15, pady=15
    )
    contenido.pack(padx=15, pady=5, fill="both", expand=True)

    boton_cerrar = tk.Button(
        doc, text="Entendido", font=("Segoe UI", 10, "bold"),
        bg="#4B5263", fg="white", bd=0, padx=20, pady=6, cursor="hand2",
        command=doc.destroy
    )
    boton_cerrar.pack(pady=15)

def jugar():
    # creamos matriz de 3x3 inicializada a vacíos
    tablero = [[" " for c in range(3)] for d in range(3)]  
    print("Vamos a jugar al 3 en raya. ¡Mucha suerte!")

    # inicializacion del juego
    global movimiento_usuario_gui, botones_gui, texto_marcador, texto_turno, texto_bienvenida
    global victorias_usuario, victorias_pc, empates, partida_iniciada
    
    movimiento_usuario_gui = None
    partida_iniciada = False  
    
    COLOR_FONDO = "#1E222A"      
    COLOR_LINEA = "#5C6370"      
    COLOR_BOTON = "#282C34"      
    
    ventana = tk.Tk()
    ventana.title("3 en Raya | Modo Clásico")
    
    # Cargo la musica de fondo usando pygame
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(RUTA_MUSICA)  
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Error al cargar la música: {e}")

    # Pongo el icono de la ventana principal
    try:
        ventana.iconbitmap(RUTA_ICONO)  
    except Exception:
        pass
    
    # Calculo para centrar bien la ventana en la pantalla
    ancho_ventana = 380
    alto_ventana = 620  
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    pos_x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
    pos_y = int((alto_pantalla / 2) - (alto_ventana / 2))
    
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")
    ventana.resizable(False, False)
    ventana.configure(bg=COLOR_FONDO)
    
    texto_bienvenida = tk.Label(
        ventana,
        text="¡Vamos a jugar al 3 en raya! ¡Mucha suerte!",
        font=("Segoe UI", 10, "bold"),
        bg=COLOR_FONDO,
        fg="#98C379"  
    )
    texto_bienvenida.pack(pady=(15, 0))
    
    # Diseño de la zona de puntos y turnos
    marco_cabecera = tk.Frame(ventana, bg=COLOR_FONDO)
    marco_cabecera.pack(pady=(10, 5), fill="x", padx=15)
    marco_cabecera.columnconfigure(0, weight=1)
    marco_cabecera.columnconfigure(1, weight=1)
    
    texto_marcador = tk.Label(
        marco_cabecera, 
        text=f"Tú: {victorias_usuario} | PC: {victorias_pc} | Empates: {empates}", 
        font=("Segoe UI", 10, "bold"),
        bg=COLOR_FONDO,
        fg="#ABB2BF"                                                                                                                    
    )
    texto_marcador.grid(row=0, column=0, sticky="w")
    
    texto_turno = tk.Label(
        marco_cabecera,
        text="Turno: JUGADOR (X)",
        font=("Segoe UI", 10, "bold"),
        bg=COLOR_FONDO,
        fg="#00D2FF"  
    )
    texto_turno.grid(row=0, column=1, sticky="e")
    
    # Genero los botones del tablero
    marco_tablero = tk.Frame(ventana, bg=COLOR_LINEA, bd=1)
    marco_tablero.pack(pady=10)
    
    botones_gui = [[None for _ in range(3)] for _ in range(3)]
    coordenadas_a_numero = {(0,0):1, (0,1):2, (0,2):3, (1,0):4, (1,1):5, (1,2):6, (2,0):7, (2,1):8, (2,2):9}
    numero_a_coordenadas = {v: k for k, v in coordenadas_a_numero.items()}
    
    # Destaca las casillas ganadoras al terminar la partida
    def animar_e_iluminar_victoria(linea_ganadora, simbolo_vfx):
        for num_casilla in linea_ganadora:
            f, c = numero_a_coordenadas[num_casilla]
            tablero[f][c] = simbolo_vfx  
            botones_gui[f][c].config(
                text=simbolo_vfx, 
                fg="#FFD700",       
                bg="#107C41",       
                activebackground="#107C41"
            )

    # Controla la logica cuando pulsas una casilla
    def manejar_clic(f, c):
        global movimiento_usuario_gui, texto_marcador, texto_turno, texto_bienvenida
        global victorias_usuario, empates, partida_iniciada
        
        if tablero[f][c] != " " or victoria_para(tablero, "X") or victoria_para(tablero, "O") or not lista_de_pos_vacias(tablero):
            return

        if not partida_iniciada:
            partida_iniciada = True
            texto_bienvenida.config(text="")

        movimiento_usuario_gui = coordenadas_a_numero[(f, c)]
        entra_movimiento(tablero) 
        muestra_tablero(tablero)
        
        linea_x = victoria_para(tablero, "X")
        if linea_x:
            victorias_usuario += 1  
            texto_marcador.config(text=f"Tú: {victorias_usuario} | PC: {victorias_pc} | Empates: {empates}")
            animar_e_iluminar_victoria(linea_x, "⭐")
            ventana.after(600, lambda: messagebox.showinfo("Fin de la partida", "¡Enhorabuena, has ganado!"))
            return
            
        if not lista_de_pos_vacias(tablero):
            empates += 1
            texto_marcador.config(text=f"Tú: {victorias_usuario} | PC: {victorias_pc} | Empates: {empates}")
            messagebox.showinfo("Fin de la partida", "¡Empate! El tablero está completo.")
            return
            
        texto_turno.config(text="Turno: PENSANDO PC...", fg="#FF6B4A")
        ventana.after(850, ejecutar_turno_maquina)

    # Gestiona el movimiento automatizado de la maquina
    def ejecutar_turno_maquina():
        global victorias_pc, empates, texto_marcador, texto_turno
        dibuja_movimiento_maquina(tablero)
        muestra_tablero(tablero)
        
        linea_o = victoria_para(tablero, "O")
        if linea_o:
            victorias_pc += 1  
            texto_marcador.config(text=f"Tú: {victorias_usuario} | PC: {victorias_pc} | Empates: {empates}")
            animar_e_iluminar_victoria(linea_o, "✨")
            ventana.after(600, lambda: messagebox.showinfo("Fin de la partida", "La máquina ha ganado."))
            return
            
        if not lista_de_pos_vacias(tablero):
            empates += 1
            texto_marcador.config(text=f"Tú: {victorias_usuario} | PC: {victorias_pc} | Empates: {empates}")
            messagebox.showinfo("Fin de la partida", "¡Empate! El tablero está completo.")
            return

        texto_turno.config(text="Turno: JUGADOR (X)", fg="#00D2FF")

    # Limpia el tablero para jugar otra ronda
    def reiniciar_tablero_gui():
        global partida_iniciada, texto_bienvenida, texto_turno
        for i in range(3):
            for j in range(3):
                tablero[i][j] = " "
        muestra_tablero(tablero)
        
        partida_iniciada = False
        texto_bienvenida.config(text="¡Vamos a jugar al 3 en raya! ¡Mucha suerte!")
        texto_turno.config(text="Turno: JUGADOR (X)", fg="#00D2FF")

    # Bucle para posicionar los 9 botones en la rejilla gráfica
    for i in range(3):
        for j in range(3):
            botones_gui[i][j] = tk.Button(
                marco_tablero, 
                text=" ", 
                font=("Segoe UI", 24, "bold"),
                width=5, 
                height=2,
                bg=COLOR_BOTON,
                activebackground="#3E4452", 
                bd=0,                                      
                relief="flat",                                
                cursor="hand2",                             
                command=lambda r=i, cb=j: manejar_clic(r, cb)
            )
            botones_gui[i][j].grid(row=i, column=j, padx=2, pady=2)
            
    # Botones inferiores de reiniciar y ayuda
    marco_acciones = tk.Frame(ventana, bg=COLOR_FONDO)
    marco_acciones.pack(pady=10)
    
    boton_reiniciar = tk.Button(
        marco_acciones, 
        text="Reiniciar Tablero", 
        font=("Segoe UI", 10, "bold"), 
        bg="#4B5263",                                 
        fg="white",
        activebackground="#5C6370",
        bd=0,
        padx=15,
        pady=8,
        cursor="hand2",
        command=reiniciar_tablero_gui
    )
    boton_reiniciar.grid(row=0, column=0, padx=5)

    boton_doc = tk.Button(
        marco_acciones, 
        text="❓ Guía del Juego", 
        font=("Segoe UI", 10, "bold"), 
        bg="#282C34",                                 
        fg="#00D2FF",
        activebackground="#3E4452",
        bd=0,
        padx=15,
        pady=8,
        cursor="hand2",
        command=lambda: abrir_documentacion(ventana)
    )
    boton_doc.grid(row=0, column=1, padx=5)
    
    # Barra deslizante para controlar el volumen
    etiqueta_volumen = tk.Label(
        ventana, 
        text="Volumen de la Música",
        font=("Segoe UI", 9, "bold"),
        bg=COLOR_FONDO,
        fg="#ABB2BF"
    )
    etiqueta_volumen.pack(pady=(10, 0))

    marco_sonido = tk.Frame(ventana, bg=COLOR_FONDO)
    marco_sonido.pack(pady=(0, 15), fill="x", padx=40)
    marco_sonido.columnconfigure(0, weight=3)
    marco_sonido.columnconfigure(1, weight=1)

    def cambiar_volumen(valor):
        vol = float(valor) / 100
        pygame.mixer.music.set_volume(vol)
        if vol > 0:
            boton_mute.config(text="🔊 Silenciar", bg="#4B5263")
        else:
            boton_mute.config(text="🔇 Activar", bg="#FF6B4A")

    def alternar_silencio():
        volumen_actual = pygame.mixer.music.get_volume()
        if volumen_actual > 0:
            pygame.mixer.music.set_volume(0.0)
            control_volumen.set(0)
            boton_mute.config(text="🔇 Activar", bg="#FF6B4A")
        else:
            pygame.mixer.music.set_volume(0.2)
            control_volumen.set(20)
            boton_mute.config(text="🔊 Silenciar", bg="#4B5263")

    control_volumen = tk.Scale(
        marco_sonido, 
        from_=0, 
        to=100, 
        orient="horizontal", 
        font=("Segoe UI", 9, "bold"),
        bg=COLOR_FONDO,
        fg="#ABB2BF",
        highlightthickness=0,
        troughcolor="#3F4756",
        activebackground="#00D2FF",
        command=cambiar_volumen
    )
    control_volumen.set(20)  
    control_volumen.grid(row=0, column=0, sticky="ews", padx=(0, 15))

    boton_mute = tk.Button(
        marco_sonido,
        text="🔊 Silenciar",
        font=("Segoe UI", 9, "bold"),
        bg="#4B5263",
        fg="white",
        bd=0,
        padx=12,
        pady=5,  
        cursor="hand2",
        command=alternar_silencio
    )
    boton_mute.grid(row=0, column=1, sticky="es")
    
    muestra_tablero(tablero)

    def cerrar_aplicacion():
        pygame.mixer.music.stop()
        ventana.destroy()

    ventana.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)
    ventana.mainloop()

# PROGRAMA PRINCIPAL
jugar()