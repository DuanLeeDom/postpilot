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

# ------------------------------------------------------------------------------
#                      AUTOMAÇÃO / YouTube
# ------------------------------------------------------------------------------

def start_upload_youtube(url_upload, video_path, title, description, thumbnail_path):
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

# ------------------------------------------------------------------------------
#                      MENU / YouTube
# ------------------------------------------------------------------------------

from tkinter import messagebox
from PIL import Image, ImageTk
import cv2


def youtube_interface(right_frame):
    # Adicionar um Scrollable Frame
    scrollable_frame = ctk.CTkScrollableFrame(right_frame, width=1200, height=650)
    scrollable_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")

    # Funções para atualizar a pré-visualização
    def update_thumbnail_preview(entry):
        """Atualiza a pré-visualização da miniatura."""
        path = entry.get()
        try:
            img = Image.open(path)
            img.thumbnail((200, 200))
            img_tk = ImageTk.PhotoImage(img)
            thumbnail_label.configure(image=img_tk)
            thumbnail_label.image = img_tk
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar a miniatura: {e}")

    def update_video_preview(entry):
        """Atualiza a pré-visualização do vídeo."""
        path = entry.get()
        try:
            cap = cv2.VideoCapture(path)
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (200, 200))
                img_tk = ImageTk.PhotoImage(image=Image.fromarray(frame))
                video_label.configure(image=img_tk)
                video_label.image = img_tk
            else:
                raise ValueError("Não foi possível ler o vídeo.")
            cap.release()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar o vídeo: {e}")

    # URL Upload
    ctk.CTkLabel(scrollable_frame, text="URL Upload:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    url_upload = ctk.CTkEntry(scrollable_frame, width=400)
    url_upload.grid(row=1, column=1, padx=10, pady=5)

    # Caminho do Vídeo
    ctk.CTkLabel(scrollable_frame, text="Caminho do Vídeo:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    video_entry = ctk.CTkEntry(scrollable_frame, width=400)
    video_entry.grid(row=2, column=1, padx=10, pady=5)
    ctk.CTkButton(scrollable_frame, text="Selecionar", command=lambda: update_video_preview(video_entry)).grid(row=2, column=2, padx=10, pady=5)

    # Caminho da Miniatura
    ctk.CTkLabel(scrollable_frame, text="Caminho da Miniatura:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    thumbnail_entry = ctk.CTkEntry(scrollable_frame, width=400)
    thumbnail_entry.grid(row=3, column=1, padx=10, pady=5)
    ctk.CTkButton(scrollable_frame, text="Selecionar", command=lambda: update_thumbnail_preview(thumbnail_entry)).grid(row=3, column=2, padx=10, pady=5)

    # Pré-visualização do Vídeo
    video_label = ctk.CTkLabel(scrollable_frame, text="Preview do Vídeo", width=200, height=200)
    video_label.grid(row=4, column=0, padx=10, pady=5)

    # Pré-visualização da Miniatura
    thumbnail_label = ctk.CTkLabel(scrollable_frame, text="Preview da Miniatura", width=200, height=200)
    thumbnail_label.grid(row=4, column=1, padx=10, pady=5)

    # Outros campos e botões
    # (mantidos os mesmos do código original)
    ctk.CTkLabel(scrollable_frame, text="Título:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    title_entry = ctk.CTkEntry(scrollable_frame, width=400)
    title_entry.grid(row=5, column=1, padx=10, pady=5)

    # Botão de postagem
    ctk.CTkButton(
        scrollable_frame,
        text="Iniciar Upload",
        command=lambda: start_upload_youtube(
            url_upload.get(),
            video_entry.get(),
            title_entry.get(),
            # description_entry.get("1.0", "end-1c"),  # Correção aqui
            thumbnail_entry.get()
        )

    ).grid(row=13, column=0, columnspan=3, pady=20)


def post_automatically(selected_networks):
    """Simula a postagem automática."""
    if not selected_networks:
        messagebox.showwarning("Atenção", "Por favor, selecione pelo menos uma rede social para automação!")
    else:
        messagebox.showinfo("Postagem Automática", f"As seguintes redes serão automatizadas: {', '.join(selected_networks)}")

# ------------------------------------------------------------------------------
#                      MENU / INTERFACE NORMAL
# ------------------------------------------------------------------------------

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
        {"name": "Odysee", "filename": "odysee.png"},
        {"name": "Rumble", "filename": "rumble.png"},
        {"name": "Tiktok", "filename": "tiktok.png"},
        {"name": "Facebook", "filename": "facebook.png"},
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
