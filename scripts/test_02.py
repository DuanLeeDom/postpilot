import os
import sys
import time
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


def start_upload(url_upload, video_path, title, description, thumbnail_path):
    try:
        chrome_options = Options()
        main_directory = os.path.join(sys.path[0])

        # Configura o perfil do Chrome
        chrome_options.add_argument("--user-data-dir=" + main_directory + "/chrome_profile")

        # Abre uma porta de depuração remota para evitar detecção de automação
        chrome_options.add_argument("--remote-debugging-port=9223")
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Cria o serviço para o ChromeDriver
        service = Service(ChromeDriverManager().install())

        # Inicializa o driver do Chrome
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Navega até o YouTube
        wait = WebDriverWait(driver, 60)
        driver.maximize_window()
        driver.get('https://www.youtube.com')
        time.sleep(3)
        driver.get(url_upload)

        time.sleep(5)
        # Upload do vídeo
        input_video = driver.find_element(By.NAME, 'Filedata')
        input_video.send_keys(video_path)

        time.sleep(5)
        # Define o título
        input_title = driver.find_element(By.XPATH, '//*[@aria-label="Add a title that describes your video (type @ to mention a channel)"]')
        input_title.clear()
        input_title.send_keys(title)

        time.sleep(2)
        # Define a descrição
        input_description = driver.find_element(By.XPATH, '//*[@aria-label="Tell viewers about your video (type @ to mention a channel)"]')
        input_description.clear()
        input_description.send_keys(description)

        time.sleep(2)
        # Upload da miniatura
        if thumbnail_path == True:
            input_thumbnail = driver.find_element(By.XPATH, '//input[@type="file"]')
            input_thumbnail.send_keys(thumbnail_path)

        time.sleep(1)
        # movendo o scroll
        still = driver.find_element(By.ID, 'scrollable-content')
        driver.execute_script("arguments[0].scrollIntoView(true);",still)

        time.sleep(5)
        messagebox.showinfo("Sucesso", "Upload concluído com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


def select_file(entry):
    filepath = filedialog.askopenfilename()
    entry.delete(0, ctk.END)
    entry.insert(0, filepath)


def youtube_interface(right_frame):
    """Interface para o upload de vídeo no YouTube dentro de um frame existente."""
    for widget in right_frame.winfo_children():
        widget.destroy()  # Limpa o frame antes de adicionar a interface

    ctk.CTkLabel(right_frame, text="URL Upload:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    url_upload = ctk.CTkEntry(right_frame, width=400)
    url_upload.grid(row=1, column=1, padx=10, pady=5)

    ctk.CTkLabel(right_frame, text="Caminho do Vídeo:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    video_entry = ctk.CTkEntry(right_frame, width=400)
    video_entry.grid(row=2, column=1, padx=10, pady=5)
    ctk.CTkButton(right_frame, text="Selecionar", command=lambda: select_file(video_entry)).grid(row=2, column=2, padx=10, pady=5)

    ctk.CTkLabel(right_frame, text="Título:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    title_entry = ctk.CTkEntry(right_frame, width=400)
    title_entry.grid(row=3, column=1, padx=10, pady=5)

    ctk.CTkLabel(right_frame, text="Descrição:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    description_entry = ctk.CTkTextbox(right_frame, width=400)
    description_entry.grid(row=4, column=1, padx=10, pady=5)

    ctk.CTkLabel(right_frame, text="Caminho da Miniatura:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    thumbnail_entry = ctk.CTkEntry(right_frame, width=400)
    thumbnail_entry.grid(row=5, column=1, padx=10, pady=5)
    ctk.CTkButton(right_frame, text="Selecionar", command=lambda: select_file(thumbnail_entry)).grid(row=5, column=2, padx=10, pady=5)

    audience_entry = ctk.CTkLabel(right_frame, text="Público:").grid(row=6, column=0, padx=10, pady=5, sticky="w")

    # Label para "Público"
    audience_label = ctk.CTkLabel(right_frame, text="Público:")
    audience_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")

    # Variável associada aos botões de rádio
    audience_var = ctk.IntVar(value=0)

    # Botão de rádio 1
    audience_radiobutton_1 = ctk.CTkRadioButton(
        right_frame,
        text="Sim, é conteúdo para crianças",
        variable=audience_var,
        value=1
    )
    audience_radiobutton_1.grid(row=7, column=0, padx=10, pady=5, sticky="w")

    # Botão de rádio 2
    audience_radiobutton_2 = ctk.CTkRadioButton(
        right_frame,
        text="Não é conteúdo para crianças",
        variable=audience_var,
        value=2
    )
    audience_radiobutton_2.grid(row=8, column=0, padx=10, pady=5, sticky="w")

    ctk.CTkButton(right_frame, text="Iniciar Upload", command=lambda: start_upload(
        url_upload.get(), video_entry.get(), title_entry.get(), description_entry.get(), thumbnail_entry.get()
    )).grid(row=10, column=0, columnspan=3, pady=20)


def post_automatically(selected_networks):
    """Simula a postagem automática."""
    if not selected_networks:
        messagebox.showwarning("Atenção", "Por favor, selecione pelo menos uma rede social para automação!")
    else:
        messagebox.showinfo("Postagem Automática", f"As seguintes redes serão automatizadas: {', '.join(selected_networks)}")


def create_menu():
    """Cria o menu de redes sociais com espaço para interface dinâmica."""
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Menu de Redes Sociais")

    # Obtendo as dimensões da tela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 1280
    window_height = 720

    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)

    root.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

    # Configuração de layout
    root_frame = ctk.CTkFrame(root)
    root_frame.pack(fill="both", expand=True)

    left_frame = ctk.CTkFrame(root_frame, width=300)
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

    right_frame = ctk.CTkFrame(root_frame)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    ctk.CTkLabel(left_frame, text="Selecione as Redes Sociais", font=("Arial", 16)).pack(pady=10)

    social_networks = [
        {"name": "YouTube", "filename": "youtube.png"},
        {"name": "COS.TV", "filename": "cos_tv.png"},
        {"name": "Rumble", "filename": "rumble.png"},
        {"name": "Odysee", "filename": "odysee.png"},
        {"name": "Tiktok", "filename": "tiktok.png"},
        {"name": "Tumblr", "filename": "tumblr.png"},
        {"name": "Facebook", "filename": "facebook.png"},
        {"name": "Twitter / X", "filename": "x.png"},
        {"name": "Instagram", "filename": "instagram.png"},
        {"name": "Linkedin", "filename": "linkedin.png"},
        {"name": "Pinterest", "filename": "Pinterest.png"},
        {"name": "Snapchat", "filename": "snapchat.png"},
    ]

    icon_dir = "./Altomator/icons"
    selected_networks = []

    def toggle_network(network):
        """Alterna o estado de seleção de uma rede social."""
        if network in selected_networks:
            selected_networks.remove(network)
        else:
            selected_networks.append(network)

    def display_interface(network_name):
        """Exibe a interface no lado direito com base na rede selecionada."""
        for widget in right_frame.winfo_children():
            widget.destroy()

        if network_name == "YouTube":
            youtube_interface(right_frame)
        else:
            ctk.CTkLabel(right_frame, text=f"Interface para {network_name}", font=("Arial", 20)).pack(pady=20)

    for index, network in enumerate(social_networks):
        icon_path = os.path.join(icon_dir, network["filename"])
        if not os.path.exists(icon_path):
            print(f"Ícone não encontrado: {icon_path}")
            continue

        icon_image = ctk.CTkImage(light_image=Image.open(icon_path), size=(50, 50))

        item_frame = ctk.CTkFrame(left_frame)
        item_frame.pack(pady=10, fill="x")

        icon_label = ctk.CTkLabel(item_frame, image=icon_image, text="")
        icon_label.pack(side="left", padx=5)

        button = ctk.CTkButton(item_frame, text=network["name"],
                               command=lambda n=network["name"]: display_interface(n))
        button.pack(side="right", fill="x", expand=True, padx=10)

    root.mainloop()

create_menu()
