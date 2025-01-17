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
        # Verificação se todos os campos necessários estão preenchidos
        if not url_upload or not video_path or not title or not description or not thumbnail_path:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return
        
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
        input_thumbnail = driver.find_element(By.XPATH, '//input[@type="file"]')
        input_thumbnail.send_keys(thumbnail_path)

        time.sleep(5)
        messagebox.showinfo("Sucesso", "Upload concluído com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


def select_file(entry):
    filepath = filedialog.askopenfilename()
    entry.delete(0, ctk.END)
    entry.insert(0, filepath)


def create_upload_interface(right_frame, url_upload, video_entry, title_entry, description_entry, thumbnail_entry):
    """Interface para o upload de vídeo no YouTube."""
    
    # Limpa o conteúdo atual do painel à direita
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Adiciona o conteúdo do formulário de upload
    ctk.CTkLabel(right_frame, text="URL Upload:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    url_upload.grid(row=0, column=1, padx=10, pady=5)

    # Caminho do vídeo
    ctk.CTkLabel(right_frame, text="Caminho do Vídeo:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    video_entry.grid(row=1, column=1, padx=10, pady=5)
    ctk.CTkButton(right_frame, text="Selecionar", command=lambda: select_file(video_entry)).grid(row=1, column=2, padx=10, pady=5)

    # Título do vídeo
    ctk.CTkLabel(right_frame, text="Título:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    title_entry.grid(row=2, column=1, padx=10, pady=5)

    # Descrição do vídeo
    ctk.CTkLabel(right_frame, text="Descrição:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    description_entry.grid(row=3, column=1, padx=10, pady=5)

    # Caminho da miniatura
    ctk.CTkLabel(right_frame, text="Caminho da Miniatura:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    thumbnail_entry.grid(row=4, column=1, padx=10, pady=5)
    ctk.CTkButton(right_frame, text="Selecionar", command=lambda: select_file(thumbnail_entry)).grid(row=4, column=2, padx=10, pady=5)

    # Botão de iniciar
    ctk.CTkButton(right_frame, text="Iniciar Upload", command=lambda: start_upload(url_upload.get(),
        video_entry.get(), title_entry.get(), description_entry.get(), thumbnail_entry.get()
    )).grid(row=5, column=0, columnspan=3, pady=20)


def post_automatically(selected_networks):
    """Simula a postagem automática."""
    if not selected_networks:
        messagebox.showwarning("Atenção", "Por favor, selecione pelo menos uma rede social para automação!")
    else:
        messagebox.showinfo("Postagem Automática", f"As seguintes redes serão automatizadas: {', '.join(selected_networks)}")


def create_menu():
    """Cria o menu de redes sociais."""
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

    ctk.CTkLabel(root, text="Selecione as Redes Sociais para Automação", font=("Arial", 20)).pack(pady=5)

    # Lista de Redes Sociais com os caminhos dos ícones na pasta local
    social_networks = [
        {"name": "youtube", "filename": "youtube.png"},
        {"name": "Facebook", "filename": "facebook.png"},
        {"name": "Twitter / X", "filename": "x.png"},
        {"name": "Instagram", "filename": "instagram.png"},
        {"name": "LinkedIn", "filename": "linkedin.png"},
        {"name": "TikTok", "filename": "tiktok.png"},
        {"name": "Snapchat", "filename": "snapchat.png"},
        {"name": "Pinterest", "filename": "pinterest.png"},
        {"name": "Reddit", "filename": "reddit.png"},
        {"name": "Tumblr", "filename": "tumblr.png"},
        {"name": "Rumble", "filename": "rumble.png"},
        {"name": "Odysee", "filename": "odysee.png"},
        {"name": "COS.TV", "filename": "cos_tv.png"}
    ]

    icon_dir = "./Secao_08_YouTube/icons"  # Diretório onde os ícones estão localizados
    selected_networks = []

    def toggle_network(network):
        """Alterna o estado de seleção de uma rede social.""" 
        if network in selected_networks:
            selected_networks.remove(network)
        else:
            selected_networks.append(network)

    def youtube_selected():
        """Exibe a interface de upload quando o YouTube é selecionado.""" 
        create_upload_interface(right_frame, url_upload, video_entry, title_entry, description_entry, thumbnail_entry)

    grid_frame = ctk.CTkFrame(root)
    grid_frame.pack(pady=20, padx=10, fill="both", expand=True, side="left", width=400)

    right_frame = ctk.CTkFrame(root)
    right_frame.pack(pady=20, padx=10, fill="both", expand=True, side="right")

    url_upload = ctk.CTkEntry(right_frame, width=400)
    video_entry = ctk.CTkEntry(right_frame, width=400)
    title_entry = ctk.CTkEntry(right_frame, width=400)
    description_entry = ctk.CTkEntry(right_frame, width=400)
    thumbnail_entry = ctk.CTkEntry(right_frame, width=400)

    columns = 4  # Número de colunas na grade
    for index, network in enumerate(social_networks):
        row = index // columns
        col = index % columns

        icon_path = os.path.join(icon_dir, network["filename"])
        if not os.path.exists(icon_path):
            print(f"Ícone não encontrado: {icon_path}")
            continue

        icon_image = ctk.CTkImage(light_image=Image.open(icon_path), size=(50, 50))

        item_frame = ctk.CTkFrame(grid_frame)
        item_frame.grid(row=row, column=col, padx=10, pady=10)

        icon_label = ctk.CTkLabel(item_frame, image=icon_image, text="")
        icon_label.pack()

        checkbox = ctk.CTkCheckBox(item_frame, text=network["name"], command=lambda network=network["name"]: toggle_network(network))
        checkbox.pack()

    # Botão de Postagem Automática
    ctk.CTkButton(root, text="Postar Automaticamente", command=lambda: post_automatically(selected_networks)).pack(pady=10)

    root.mainloop()

# Inicia o menu
create_menu()
