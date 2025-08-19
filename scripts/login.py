import os
import sys
import tkinter
import subprocess
import json
from pathlib import Path
from PIL import Image
import customtkinter

# Configuração visual
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Caminho base (pasta onde o login.py está localizado, sem a pasta 'src')
BASE_DIR = Path(__file__).resolve().parent

# Caminho do arquivo JSON de configurações
CONFIG_FILE_PATH = BASE_DIR / "config" / "settings.json"

# Função para carregar configurações do JSON
def load_config():
    try:
        with open(CONFIG_FILE_PATH, "r") as config_file:
            config = json.load(config_file)
            return config
    except FileNotFoundError:
        print(f"[ERRO] Arquivo de configurações não encontrado: {CONFIG_FILE_PATH}")
        return None
    except json.JSONDecodeError:
        print(f"[ERRO] Erro ao ler o arquivo JSON.")
        return None

# Carregar as configurações
config = load_config()

# Verificar se as configurações foram carregadas com sucesso
if config:
    theme = config.get("theme", "Light")
    color = config.get("color", "green")
    notifications = config.get("notifications", True)
    saved_login = config.get("login", "")
    saved_password = config.get("password", "")
else:
    theme = "Light"
    color = "green"
    notifications = True
    saved_login = ""
    saved_password = ""

# Janela principal
app = customtkinter.CTk()
app.title("Login")

# Tamanho da janela
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
window_width = 1280
window_height = 720
position_top = (screen_height - window_height) // 2
position_left = (screen_width - window_width) // 2
app.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

# Função de login
def on_login():
    try:
        # Caminho completo para o main.py
        main_path = BASE_DIR / "main.py"
        if not main_path.is_file():
            raise FileNotFoundError(f"main.py não encontrado em: {main_path}")

        # Definir o diretório de trabalho como o diretório onde o main.py está localizado
        os.chdir(BASE_DIR)

        # Executa o main.py com o interpretador Python atual
        subprocess.Popen([sys.executable, str(main_path)])

        # Fecha a janela de login
        app.destroy()

    except Exception as e:
        print(f"[ERRO] Falha ao iniciar o main.py: {e}")

# Imagem de fundo
try:
    bg_path = BASE_DIR / "assets" / "wallpaper-02.png"
    bg_image = Image.open(bg_path)
    bg_ctk = customtkinter.CTkImage(bg_image, size=(window_width, window_height))
    background_label = customtkinter.CTkLabel(master=app, image=bg_ctk, text="")
    background_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
except FileNotFoundError:
    print("[Aviso] Imagem de fundo não encontrada.")

# Frame de login
frame = customtkinter.CTkFrame(master=app, width=320, height=360, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# Título
label_title = customtkinter.CTkLabel(master=frame, text="Entrar na sua conta", font=('Century Gothic', 20))
label_title.place(x=62, y=60)

# Campos de entrada com valores salvos do JSON
entry_username = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Nome de Usuário')
entry_username.place(x=50, y=110)
entry_username.insert(0, saved_login)  # Preenche o campo com o nome de usuário salvo

entry_password = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Senha', show="*")
entry_password.place(x=50, y=165)
entry_password.insert(0, saved_password)  # Preenche o campo com a senha salva

# Texto de esquecimento de senha
label_forgot = customtkinter.CTkLabel(master=frame, text="Esqueceu a senha?", font=('Century Gothic', 12))
label_forgot.place(x=155, y=195)

# Botão Entrar
button_login = customtkinter.CTkButton(master=frame, width=220, text="Entrar", command=on_login, corner_radius=6)
button_login.place(x=50, y=240)

# Ícones sociais
img_google = img_facebook = None

try:
    google_path = BASE_DIR / "assets" / "icons" / "google.webp"
    google_icon = Image.open(google_path).resize((20, 20))
    img_google = customtkinter.CTkImage(google_icon)
except FileNotFoundError:
    print("[Aviso] Ícone do Google não encontrado.")

try:
    facebook_path = BASE_DIR / "assets" / "icons" / "facebook.png"
    facebook_icon = Image.open(facebook_path).resize((60, 20))
    img_facebook = customtkinter.CTkImage(facebook_icon)
except FileNotFoundError:
    print("[Aviso] Ícone do Facebook não encontrado.")

# Botões Sociais
if img_google:
    button_google = customtkinter.CTkButton(
        master=frame, image=img_google, text="Google", width=100, height=20,
        compound="left", fg_color='white', text_color='black', hover_color='#AFAFAF'
    )
    button_google.place(x=50, y=290)

if img_facebook:
    button_facebook = customtkinter.CTkButton(
        master=frame, image=img_facebook, text="Facebook", width=100, height=20,
        compound="left", fg_color='white', text_color='black', hover_color='#AFAFAF'
    )
    button_facebook.place(x=170, y=290)

# Loop principal
app.mainloop()