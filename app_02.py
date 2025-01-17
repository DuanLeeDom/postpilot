import os
import sys
import time
import customtkinter as ctk
from tkcalendar import Calendar
from tkinter import filedialog, messagebox
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import date

# ------------------------------------------------------------------------------
#                      AUTOMAÇÃO / YouTube
# ------------------------------------------------------------------------------

def start_upload(video_path, title, description, thumbnail_path):
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
        driver.get('https://studio.youtube.com')

        time.sleep(2)
        input_upload = driver.find_element(By.XPATH, '//*[@id="create-icon"]/ytcp-button-shape')
        input_upload.click()

        time.sleep(1)
        input_upload = driver.find_element(By.XPATH, '//*[@id="text-item-0"]/ytcp-ve/tp-yt-paper-item-body/div')
        input_upload.click()

        time.sleep(5)
        # Upload do vídeo
        input_video = driver.find_element(By.NAME, 'Filedata')
        input_video.send_keys(video_path)

        time.sleep(5)
        # Define o título
        # input_title = driver.find_element(By.XPATH, '//*[@aria-label="Add a title that describes your video (type @ to mention a channel)"]')

        # Obtendo os elementos de entrada
        input_title = driver.find_elements(By.CLASS_NAME, 'style-scope ytcp-social-suggestions-textbox')

        # Limpar o campo de título enviando BACKSPACE
        driver.execute_script("arguments[0].value = '';", input_title[0])
        input_title[0].send_keys(input_title)  # Envia o novo título

        # Limpar o campo de descrição enviando BACKSPACE
        driver.execute_script("arguments[0].value = '';", input_title[1])  # Remove o texto atual
        input_title[1].send_keys(description)  # Envia a nova descrição

        '''    
        time.sleep(2)
        # Define a descrição
        input_description = driver.find_element(By.XPATH, '//*[@aria-label="Tell viewers about your video (type @ to mention a channel)"]')
        input_description.clear()
        input_description.send_keys(description)
        '''

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

# ------------------------------------------------------------------------------
#                      MENU / YouTube
# ------------------------------------------------------------------------------

def youtube_interface(right_frame):
    # Adicionar um Scrollable Frame
    scrollable_frame = ctk.CTkScrollableFrame(right_frame, width=1200, height=650)
    scrollable_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")

    '''
    # URL Upload
    ctk.CTkLabel(scrollable_frame, text="URL Upload:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    url_upload = ctk.CTkEntry(scrollable_frame, width=400)
    url_upload.grid(row=1, column=1, padx=10, pady=5)
    '''

    # Caminho do Vídeo
    ctk.CTkLabel(scrollable_frame, text="Caminho do Vídeo:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    video_entry = ctk.CTkEntry(scrollable_frame, width=400)
    video_entry.grid(row=2, column=1, padx=10, pady=5)
    ctk.CTkButton(scrollable_frame, text="Selecionar", command=lambda: select_file(video_entry)).grid(row=2, column=2, padx=10, pady=5)

    # Caminho da Miniatura
    ctk.CTkLabel(scrollable_frame, text="Caminho da Miniatura:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    thumbnail_entry = ctk.CTkEntry(scrollable_frame, width=400)
    thumbnail_entry.grid(row=3, column=1, padx=10, pady=5)
    ctk.CTkButton(scrollable_frame, text="Selecionar", command=lambda: select_file(thumbnail_entry)).grid(row=3, column=2, padx=10, pady=5)

    # Título
    ctk.CTkLabel(scrollable_frame, text="Título:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    title_entry = ctk.CTkEntry(scrollable_frame, width=400)
    title_entry.grid(row=4, column=1, padx=10, pady=5)

    # Descrição
    ctk.CTkLabel(scrollable_frame, text="Descrição:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    description_entry = ctk.CTkTextbox(scrollable_frame, width=400, height=100)  # Ajuste a altura
    description_entry.grid(row=5, column=1, padx=10, pady=5)

    # Público
    ctk.CTkLabel(scrollable_frame, text="Público:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
    audience_var = ctk.IntVar(value=0)
    audience_radiobutton_1 = ctk.CTkRadioButton(
        scrollable_frame,
        text="Sim, é conteúdo para crianças",
        variable=audience_var,
        value=1
    )
    audience_radiobutton_1.grid(row=6, column=1, padx=10, pady=5, sticky="w")
    audience_radiobutton_2 = ctk.CTkRadioButton(
        scrollable_frame,
        text="Não é conteúdo para crianças",
        variable=audience_var,
        value=2
    )
    audience_radiobutton_2.grid(row=7, column=1, padx=10, pady=5, sticky="w")

    # Restrição ao Público Adulto
    ctk.CTkLabel(scrollable_frame, text="Restringir ao Público Adulto:").grid(row=8, column=0, padx=10, pady=5, sticky="w")
    adult_var = ctk.IntVar(value=0)
    adult_radiobutton_1 = ctk.CTkRadioButton(
        scrollable_frame,
        text="Sim, restringir meu vídeo a espectadores maiores de 18 anos",
        variable=adult_var,
        value=1
    )
    adult_radiobutton_1.grid(row=8, column=1, padx=10, pady=5, sticky="w")
    adult_radiobutton_2 = ctk.CTkRadioButton(
        scrollable_frame,
        text="Não, não restrinja meu vídeo apenas a espectadores maiores de 18 anos",
        variable=adult_var,
        value=2
    )
    adult_radiobutton_2.grid(row=9, column=1, padx=10, pady=5, sticky="w")

    # Conteúdo alterado
    ctk.CTkLabel(scrollable_frame, text="Conteúdo alterado:").grid(row=10, column=0, padx=10, pady=5, sticky="w")
    adult_var = ctk.IntVar(value=0)
    adult_radiobutton_1 = ctk.CTkRadioButton(
        scrollable_frame,
        text="Sim",
        variable=adult_var,
        value=1
    )
    adult_radiobutton_1.grid(row=10, column=1, padx=10, pady=5, sticky="w")
    adult_radiobutton_2 = ctk.CTkRadioButton(
        scrollable_frame,
        text="Não",
        variable=adult_var,
        value=2
    )
    adult_radiobutton_2.grid(row=11, column=1, padx=10, pady=5, sticky="w")

    # Tags do vídeo
    ctk.CTkLabel(scrollable_frame, text="Tags:").grid(row=12, column=0, padx=10, pady=5, sticky="w")
    tags_entry = ctk.CTkTextbox(scrollable_frame, width=400, height=50)
    tags_entry.grid(row=12, column=1, padx=10, pady=5)

    # Categoria
    ctk.CTkLabel(scrollable_frame, text="Categoria:").grid(row=13, column=0, padx=10, pady=5, sticky="w")
    category_entry = ctk.CTkOptionMenu(scrollable_frame,
                                       values=["Automóveis e veículos", "Comédia", "Educação", "Entretenimento", "Filme e Animação",
                                               "Jogos", "Como fazer e estilo", "Música", "Notícias e Política",
                                               "Organizações sem fins lucrativos e ativisrno", "Pessoas e Blogs", 
                                               "Animais de estimação e animais", "Ciência e Tecnologia", "Esportes", "Viagens e Eventos"]
                                       )
    category_entry.grid(row=13, column=1, padx=10, pady=5, sticky="w")
    category_entry.set("Escolha a Categoria")

    def check_visibility():
        if visibility_var.get() == 4:
            print("ENTROU | CORRETO!")

    # Visibilidade
    ctk.CTkLabel(scrollable_frame, text="Salvar ou Publicar:").grid(row=14, column=1, padx=10, pady=5, sticky="w")
    
    visibility_var = ctk.IntVar(value=0)
    
    visibility_entry = ctk.CTkRadioButton(
        scrollable_frame,
        text="Público",
        variable=visibility_var,
        value=1,
        command=check_visibility
    ).grid(row=14, column=1, padx=10, pady=5, sticky="w")

    visibility_entry = ctk.CTkRadioButton(
        scrollable_frame,
        text="Não listado",
        variable=visibility_var,
        value=2,
        command=check_visibility
    ).grid(row=15, column=1, padx=10, pady=5, sticky="w")

    visibility_entry = ctk.CTkRadioButton(
        scrollable_frame,
        text="Privado",
        variable=visibility_var,
        value=3,
        command=check_visibility
    ).grid(row=16, column=1, padx=10, pady=5, sticky="w")    

    visibility_entry = ctk.CTkRadioButton(
        scrollable_frame,
        text="Agendar",
        variable=visibility_var,
        value=4,
        command=check_visibility
    ).grid(row=17, column=1, padx=10, pady=5, sticky="w")   

    # Botão de postar
    ctk.CTkButton(
        scrollable_frame,
        text="Iniciar Upload",
        command=lambda: youtube_interface(
            # url_upload.get(),
            video_entry.get(),
            title_entry.get(),
            description_entry.get(),
            thumbnail_entry.get()
        )
    ).grid(row=20, column=0, columnspan=3, pady=20)

def post_automatically(selected_networks):
    """Simula a postagem automática."""
    if not selected_networks:
        messagebox.showwarning("Atenção", "Por favor, selecione pelo menos uma rede social para automação!")
    else:
        messagebox.showinfo("Postagem Automática", f"As seguintes redes serão automatizadas: {', '.join(selected_networks)}")

# ------------------------------------------------------------------------------
#                      HORA E DIA
# ------------------------------------------------------------------------------

def select_day():
    """Exibe o dia atual em uma mensagem."""
    today = date.today()
    messagebox.showinfo("Dia Atual", f"Hoje é {today.strftime('%d/%m/%Y')}")  # Formato: DD/MM/AAAA

def open_calendar_day(entry):
    """Abre um calendário para escolher o dia."""
    def set_day():
        selected_date = calendar.selection_get()
        entry.delete(0, ctk.END)
        entry.insert(0, selected_date.strftime('%d/%m/%Y'))  # Formato do dia selecionado
        calendar_window.destroy()

    calendar_window = ctk.Toplevel()
    calendar_window.title("Selecione o Dia")

    # Adicionar calendário
    calendar = Calendar(calendar_window, date_pattern="dd/mm/yyyy")
    calendar.pack(pady=20)

    # Botão de seleção
    ctk.Button(calendar_window, text="Selecionar", command=set_day).pack(pady=10)

    # Campo de entrada para exibir o dia
    day_entry = ctk.CTkEntry(ctk, width=300)
    day_entry.grid(row=0, column=0, padx=10, pady=10)

    # Botão para exibir o dia atual
    day_button = ctk.CTkButton(
        text="Exibir Dia Atual",
        command=select_day
    )
    day_button.grid(row=1, column=0, padx=10, pady=10)

    # Botão para abrir o calendário e escolher o dia
    calendar_button = ctk.CTkButton(
        text="Escolher Dia",
        command=lambda: open_calendar_day(day_entry)
    )
    calendar_button.grid(row=1, column=1, padx=10, pady=10)

# ------------------------------------------------------------------------------
#                      MENU / INTERFACE NORMAL
# ------------------------------------------------------------------------------

def create_menu():
    """Cria o menu de redes sociais com espaço para interface dinâmica."""
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Menu de Redes Sociais")

    # ----------[ Obtendo as dimensões da tela | Centralizar ]----------
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 1280
    window_height = 720

    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)

    root.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

    # ----------[ Configuração de Layout Principal ]----------
    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand=True)

    # ----------[ Área de Seleção - Esquerda ]----------
    left_frame = ctk.CTkFrame(frame, border_color='#0078D4', width=300, border_width=2)
    left_frame.pack(side="left", fill="y", padx=5, pady=5)

    ctk.CTkLabel(left_frame, text="Selecione as Redes Sociais", font=("Arial", 16)).pack(pady=15)
    
    # Scrollbar
    scrollbar = ctk.CTkScrollbar(left_frame, orientation="vertical", command=left_frame.winfo_y)
    scrollbar.pack(side="right", fill="y")

    # ----------[ Área Dinâmica - Direita ]----------
    right_frame = ctk.CTkFrame(frame, border_color='#cccccc', border_width=2)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    social_networks = [
        {"name": "YouTube", "filename": "youtube.png"},
        {"name": "COS.TV", "filename": "cos_tv.png"},
        {"name": "Odysee", "filename": "odysee.png"},
        {"name": "Rumble", "filename": "rumble.png"},
        {"name": "Tiktok", "filename": "tiktok.png"},
        {"name": "Facebook", "filename": "facebook.png"},
    ]

    icon_dir = "./icons"
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

        # Frame para cada botão de rede social
        item_frame = ctk.CTkFrame(left_frame)
        item_frame.pack(pady=5, fill="x")

        # Ícone
        icon_label = ctk.CTkLabel(item_frame, image=icon_image, text="")
        icon_label.pack(side="left", padx=5)

        # Botão
        button = ctk.CTkButton(
            item_frame, 
            text=network["name"],
            command=lambda n=network["name"]: display_interface(n),
            height=30
            )
        button.pack(side="right", fill="x", expand=True, padx=5)


    root.mainloop()

create_menu()