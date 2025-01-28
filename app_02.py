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
from selenium.webdriver.common.keys import Keys

# ========================================================================
#                  OPEN GOOGLE CHROME | SELENIUM
# ========================================================================
        
def open_google():
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
        global driver
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # deixar maximizado
        wait = WebDriverWait(driver, 60)
        driver.maximize_window()

# ========================================================================
#                     CONFIGURATION | SELENIUM
# ========================================================================

def configuration():
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
        global driver
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Navega para todos os sites de login
        wait = WebDriverWait(driver, 60)
        driver.maximize_window()

        time.sleep(2)
        # YouTube
        driver.get('https://studio.youtube.com')

        time.sleep(2)
        # abrir uma nova guia
        driver.execute_script("window.open('');")

        # Trocar para a nova aba
        driver.switch_to.window(driver.window_handles[1])

        # Cos.Tv
        driver.get('https://cos.tv')

        time.sleep(2)
        next_01 = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[1]/header/div/button[3]')
        next_01.click()

        next_02 = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div/div[1]')
        next_02.click()

        time.sleep(2)
        # Trocar para a nova aba
        driver.switch_to.window(driver.window_handles[0])

# ========================================================================
#              UPLOAD DE VÍDEO PARA O YOUTUBE | SELENIUM
# ========================================================================

def upload_youtube(video_path, title, description, tags, thumbnail_path):
    """
    Função principal para realizar o upload de vídeos no YouTube utilizando Selenium.
    
    Parâmetros:
    - video_path (str): Caminho do vídeo a ser enviado.
    - title (str): Título do vídeo.
    - description (str): Descrição do vídeo.
    - tags (str): Tags para o vídeo (separadas por vírgulas).
    - thumbnail_path (str): Caminho para a miniatura do vídeo.
    """
    try:
        # Configuração inicial do navegador
        chrome_options = Options()
        main_directory = os.path.join(sys.path[0])

        # Configura o perfil do navegador para evitar logins repetidos
        chrome_options.add_argument("--user-data-dir=" + main_directory + "/chrome_profile")
        # Ativa a porta de depuração para evitar detecção de automação
        chrome_options.add_argument("--remote-debugging-port=9223")
        # Desativa extensões e mensagens de automação
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Cria o serviço para o driver do Chrome
        service = Service(ChromeDriverManager().install())
        # Inicializa o navegador com as opções configuradas
        global driver
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Abre o YouTube Studio
        wait = WebDriverWait(driver, 60)
        driver.maximize_window()
        driver.get('https://studio.youtube.com')

        # Inicia o processo de upload
        time.sleep(2)
        upload_button = driver.find_element(By.XPATH, '//*[@id="create-icon"]/ytcp-button-shape')
        upload_button.click()

        time.sleep(1)
        video_upload_option = driver.find_element(By.XPATH, '//*[@id="text-item-0"]/ytcp-ve/tp-yt-paper-item-body/div')
        video_upload_option.click()

        # Carrega o arquivo de vídeo
        time.sleep(5)
        video_input = driver.find_element(By.NAME, 'Filedata')
        video_input.send_keys(video_path)

        # Preenche título e descrição
        time.sleep(5)
        text_inputs = driver.find_elements(By.CLASS_NAME, 'style-scope ytcp-social-suggestions-textbox')

        # Define o título do vídeo
        text_inputs[0].send_keys(Keys.CONTROL + "a")  # Seleciona todo o texto
        text_inputs[0].send_keys(Keys.BACKSPACE)      # Remove o texto atual
        text_inputs[0].send_keys(title)

        # Define a descrição do vídeo
        text_inputs[1].send_keys(Keys.CONTROL + "a")
        text_inputs[1].send_keys(Keys.BACKSPACE)
        text_inputs[1].send_keys(description)

        # Ajusta a visualização para fazer upload da miniatura
        time.sleep(1)
        element_to_scroll = driver.find_element(By.XPATH, '//input[@type="file"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", element_to_scroll)

        # Carrega a miniatura
        time.sleep(4)
        thumbnail_input = driver.find_element(By.XPATH, '//input[@type="file"]')
        thumbnail_input.send_keys(thumbnail_path)

        # Rola até o final da página para selecionar o público-alvo
        time.sleep(1)
        element_to_scroll = driver.find_element(By.CLASS_NAME, 'style-scope tp-yt-paper-radio-button')
        driver.execute_script("arguments[0].scrollIntoView(true);", element_to_scroll)

        # Define o público-alvo como "não para crianças"
        time.sleep(2)
        audience_option = driver.find_elements(By.CLASS_NAME, 'style-scope tp-yt-paper-radio-button')
        audience_option[1].click()
    
        # Mostrar mais
        time.sleep(2)
        show_more = driver.find_element(By.XPATH, '//*[@id="toggle-button"]/ytcp-button-shape/button/yt-touch-feedback-shape/div/div[2]')
        show_more.click()

        time.sleep(2)
        # scroll
        element_to_scroll = driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[2]/div')
        driver.execute_script("arguments[0].scrollIntoView(true);", element_to_scroll)

        # Conteudo alterado
        time.sleep(1)
        altered_content = driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[2]/ytkp-altered-content-select/div[2]/div[2]/ytcp-ve/tp-yt-paper-radio-button/div[1]/div[1]')
        altered_content.click()

        time.sleep(2)
        # scroll
        element_to_scroll = driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[6]/div[1]')
        driver.execute_script("arguments[0].scrollIntoView(true);", element_to_scroll)

        # Adiciona tags ao vídeo
        time.sleep(1)
        tags_input = driver.find_elements(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[6]/ytcp-form-input-container/div[1]/div/ytcp-free-text-chip-bar/ytcp-chip-bar/div/input')
        tags_input[0].send_keys(tags)
        tags_input[0].send_keys(Keys.ENTER)

        # Avança nas páginas de configuração
        time.sleep(2)
        for _ in range(3):  # Pressiona "Avançar" três vezes
            next_button = driver.find_element(By.XPATH, '//*[@id="next-button"]/ytcp-button-shape/button')
            next_button.click()
            time.sleep(2)

        # Define a visibilidade como "Privado" e salva o vídeo
        visibility_option = driver.find_elements(By.XPATH, '//*[@id="private-radio-button"]/div[1]')
        visibility_option[0].click()

        time.sleep(2)
        save_button = driver.find_element(By.XPATH, '//*[@id="done-button"]/ytcp-button-shape/button')
        save_button.click()

        # Confirmação de sucesso
        time.sleep(2)
        messagebox.showinfo("Sucesso", "Upload concluído com sucesso!")
    except Exception as e:
        # Exibe uma mensagem de erro em caso de falha
        messagebox.showerror("Erro", f"Ocorreu um erro durante o upload: {str(e)}")

# ========================================================================
#              UPLOAD DE VÍDEO PARA O COS.TV | SELENIUM
# ========================================================================

def upload_cos_tv(video_path, title, description, tags, thumbnail_path):
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
        global driver
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Navega até o YouTube
        wait = WebDriverWait(driver, 60)
        driver.maximize_window()
        driver.get('https://cos.tv/studio')

        time.sleep(5)
        # Entrar onde faz os uploads
        upload_button = driver.find_elements(By.XPATH, '//*[@id="app"]/div[1]/div[2]/header/div/div/div[3]/div/div/div/div[2]/div/a')
        upload_button[0].click()

        # Carrega o arquivo de vídeo
        time.sleep(5)
        video_input = driver.find_element(By.NAME, 'File')
        video_input.send_keys(video_path)

        # Preenche título e descrição
        time.sleep(2)
        text_input = driver.find_elements(By.XPATH, '/html/body/div/div/div/div/div[1]/main/div/div[1]/div/form/div/div/div[2]/div/div[1]/div/div[1]/div/input')
        text_input[0].send_keys(title)

        description_inputs = driver.find_elements(By.XPATH, '/html/body/div/div/div/div/div[1]/main/div/div[1]/div/form/div/div/div[2]/div/div[2]/div/div[1]/div[1]/textarea')
        description_inputs[0].send_keys(description)

        time.sleep(2)
        tags_input = driver.find_elements(By.XPATH, '/html/body/div/div/div/div/div[1]/main/div/div[1]/div/form/div/div/div[2]/div/div[5]/div/div[1]/div[1]')
        tags_input[0].send_keys(tags)

        time.sleep(2)
        click_01 = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[1]/main/div/div[1]/div/form/div/div/div[3]/div[3]/div/div/div[1]/div/div[1]/div/div/div/div[1]/div/div')
        click_01.click()

        time.sleep(2)
        thumbnail_input = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[1]/main/div/div[1]/div/form/div/div/div[3]/div[4]/button')
        thumbnail_input.send_keys(thumbnail_path)
        
        time.sleep(2)
        click_02 = driver.find_element(By.XPATH, '/html/body/div/div/div/div[3]/div/div/div[3]/button')
        click_02.click()

        time.sleep(2)
        publish_input = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[1]/main/div/div[1]/div/form/div/div/button')
        publish_input.click()

        messagebox.showinfo("Sucesso", "Upload concluído com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

# ========================================================================
#                          FUNÇÕES AUXILIARES
# ========================================================================

def close_browser_tab(driver):
    """
    Fecha a aba ativa do navegador.
    
    Parâmetros:
    - driver: Instância do navegador.
    """
    try:
        driver.close()
        messagebox.showinfo("Fechar Navegador", "A aba do navegador foi fechada com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível fechar a aba do navegador: {str(e)}")

def select_file(entry):
    """
    Abre uma janela para selecionar um arquivo e insere o caminho no campo correspondente.
    
    Parâmetros:
    - entry: Campo de entrada onde o caminho será inserido.
    """
    filepath = filedialog.askopenfilename()
    entry.delete(0, ctk.END)
    entry.insert(0, filepath)

# ------------------------------------------------------------------------------  
#            Função para abrir a janela de configurações de usuario
# ------------------------------------------------------------------------------

def open_settings_window():
    """Cria e exibe uma janela de configurações."""
    # Janela de configurações
    settings_window = ctk.CTkToplevel()
    settings_window.title("Configurações")
    settings_window.geometry("400x300")

    # ----------[ Obtendo as dimensões da tela | Centralizar ]----------
    screen_width = settings_window.winfo_screenwidth()
    screen_height = settings_window.winfo_screenheight()

    window_width = 900
    window_height = 600

    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)

    settings_window.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

    settings_window.resizable(False, False)
    settings_window.grab_set()

    # Função para salvar as configurações
    def save_settings():
        theme = theme_var.get()
        notifications = notif_var.get()
        ctk.CTkMessagebox.show_info("Configurações", f"Configurações salvas!\n\nTema: {theme}\nNotificações: {'Ativadas' if notifications else 'Desativadas'}")
        settings_window.destroy()

    # Tema
    ctk.CTkLabel(settings_window, text="Tema:", font=("Arial", 14)).pack(anchor="w", padx=10, pady=10)
    theme_var = ctk.StringVar(value="Sistema")
    ctk.CTkRadioButton(settings_window, text="Sistema", variable=theme_var, value="Sistema").pack(anchor="w", padx=20, pady=5)
    ctk.CTkRadioButton(settings_window, text="Claro", variable=theme_var, value="Claro").pack(anchor="w", padx=20, pady=5)
    ctk.CTkRadioButton(settings_window, text="Escuro", variable=theme_var, value="Escuro").pack(anchor="w", padx=20, pady=5)

    # Trocar Cores
    ctk.CTkLabel(settings_window, text="Trocar Cores:", font=("Arial", 14)).pack(anchor="w", padx=10, pady=10)
    color_var = ctk.StringVar(value="Azul")
    ctk.CTkRadioButton(settings_window, text="Azul", variable=color_var, value="Azul").pack(anchor="w", padx=20, pady=5)
    ctk.CTkRadioButton(settings_window, text="Verde", variable=color_var, value="Verde").pack(anchor="w", padx=20, pady=5)

    # Notificações
    ctk.CTkLabel(settings_window, text="Notificações:", font=("Arial", 14)).pack(anchor="w", padx=10, pady=10)
    notif_var = ctk.BooleanVar(value=True)
    ctk.CTkCheckBox(settings_window, text="Ativar notificações", variable=notif_var).pack(anchor="w", padx=20, pady=5)

    # ----------[ Botão de abrir o Google Chrome ]----------
    ctk.CTkButton(settings_window, text="Abrir Google Chrome", command=lambda: open_google()).pack(anchor="w", padx=20, pady=5)

    # ----------[ Botão de fechar navegador ]----------
    ctk.CTkButton(settings_window, text="Fechar Navegador", command=lambda: close_browser_tab(driver)).pack(anchor="w", padx=20, pady=5)

    # ----------[ Botão de Configuração ]----------
    ctk.CTkButton(settings_window, text="Configuração", command=lambda: configuration()).pack(anchor="w", padx=20, pady=5)

    # Botão de salvar
    ctk.CTkButton(settings_window, text="Salvar", command=save_settings).pack(pady=20)

    # Botão de fechar
    ctk.CTkButton(settings_window, text="Fechar", command=settings_window.destroy).pack(pady=10)

# ------------------------------------------------------------------------------
#                          INTERFACE NORMAL
# ------------------------------------------------------------------------------

def create_menu():
    """Cria o menu de redes sociais com espaço para interface dinâmica."""
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("PostPilot")

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

    # ----------[ Área de Menu - Esquerda ]----------
    menu_frame = ctk.CTkFrame(frame, width=50, fg_color='#BFBFBF')
    menu_frame.pack(side="left", fill="y")

    icon_menu = ctk.CTkImage(light_image=Image.open('./icons/menu.png'), dark_image=Image.open('./icons/menu.png'), size=(40, 40))
    ctk.CTkButton(menu_frame, width=60, height=60, text='', image=icon_menu, fg_color="transparent", hover_color="gray", border_width=0).pack(side="top")

    # menu bar | Opetions
    post_vision = ctk.CTkButton(menu_frame, width=40, height=40, text="Posts", border_width=0, command=lambda: show_posts(right_frame)).pack(anchor='center', pady=10)
    video_vision = ctk.CTkButton(menu_frame, width=40, height=40, text="Vídeos", border_width=0, command=lambda: show_videos(right_frame)).pack(anchor='center', pady=10)

    icon_user = ctk.CTkImage(light_image=Image.open('./icons/user.png'), dark_image=Image.open('./icons/user.png'), size=(40, 40))
    user_button = ctk.CTkButton(menu_frame, width=60, height=60, text='', image=icon_user, fg_color="transparent", hover_color="gray", border_width=0, command=open_settings_window).pack(side="bottom")

    right_frame = ctk.CTkFrame(frame, border_color='#cccccc', border_width=0)
    right_frame.pack(side="right", fill="both", expand=True, padx=0, pady=0)

    show_welcome_animation(right_frame)

    root.mainloop()

# ------------------------------------------------------------------------------
#                          CARREGAMENTO...
# ------------------------------------------------------------------------------

def show_welcome_animation(frame):
    """Exibe a animação de boas-vindas no frame fornecido."""
    for widget in frame.winfo_children():
        widget.destroy()

    label = ctk.CTkLabel(frame, text="Bem-vindo ao PostPilot!", font=("Arial", 24))
    label.pack(pady=20)

    # Simulação de animação
    for i in range(3):
        frame.after(500 * i, lambda i=i: label.configure(text=f"Carregando{'.' * (i + 1)}"))

# ------------------------------------------------------------------------------
#                          INTERFACE POSTS
# ------------------------------------------------------------------------------

def show_posts(frame):
    """Exibe a interface para vídeos no frame fornecido."""
    for widget in frame.winfo_children():
        widget.destroy()

    # ctk.CTkLabel(frame, text="Postagem Automática de Vídeos", font=("Arial", 20)).pack(pady=5)
    
    # ----------[ Área de Seleção - Esquerda ]----------
    left_frame = ctk.CTkFrame(frame, width=300)
    left_frame.pack(side="left", fill="y")

    ctk.CTkLabel(left_frame, text="Selecione as Opções", font=("Arial", 16)).pack(pady=15, padx=20)

    right_frame = ctk.CTkFrame(frame, border_color='#cccccc', border_width=0)
    right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    social_networks = [
        {"name": "Facebook", "filename": "facebook.png"},
        {"name": "X", "filename": "x.png"},
        {"name": "Linkedin", "filename": "linkedin.png"},
        {"name": "Reddit", "filename": "reddit.png"},
    ]

    icon_dir = "./icons"
    selected_networks = []
    
    for index, network in enumerate(social_networks):
        icon_path = os.path.join(icon_dir, network["filename"])
        if not os.path.exists(icon_path):
            print(f"Ícone não encontrado: {icon_path}")
            continue

        icon_image = ctk.CTkImage(light_image=Image.open(icon_path), size=(50, 50))

        # Frame para cada botão de rede social
        item_frame = ctk.CTkFrame(left_frame, border_width=2)
        item_frame.pack(fill="x", padx=10, pady=5)

        # Ícone
        icon_label = ctk.CTkLabel(item_frame, image=icon_image, text="")
        icon_label.pack(side="left", padx=5, pady=5)

        # Botão
        button = ctk.CTkSwitch(
            item_frame, 
            text=network["name"],
            #command=lambda n=network["name"]: display_interface(n),
            height=30,
            corner_radius=20
            )
        button.pack(side="right", fill="x", expand=True, padx=5)

    interface_posts(right_frame)

def interface_posts(frame):
    """Exibe a interface para posts no frame fornecido."""
    for widget in frame.winfo_children():
        widget.destroy()

    # Adicione os elementos específicos da interface de posts aqui
    main_frame = ctk.CTkFrame(frame, corner_radius=10)
    main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # Caixa de pergunta no topo
    post_label = ctk.CTkLabel(main_frame, text="O que você quer postar?", font=("Arial", 26))
    post_label.pack(pady=10)

    post_box = ctk.CTkTextbox(main_frame, height=400, width=900, font=("Noto Color Emoji", 18))
    post_box.pack(pady=10)

    URL = ctk.CTkButton(main_frame, text='URL', corner_radius=5).pack(pady=10, padx=10)

    post_button = ctk.CTkButton(main_frame, text="Postar", corner_radius=5)
    post_button.pack(pady=5)

# ------------------------------------------------------------------------------
#                    Funções Vinculadas aos Switches
# ------------------------------------------------------------------------------
def execute_uploads(selected_networks, upload_functions):
    """Executa as funções de upload para as redes sociais selecionadas."""
    if not selected_networks:
        messagebox.showwarning("Aviso", "Nenhuma rede social foi selecionada!")
        return

    # Obter os valores diretamente dos campos de entrada
    video_path = video_entry.get()
    title = title_entry.get()
    description = description_entry.get("1.0", "end-1c")
    tags = tags_entry.get("1.0", "end-1c")
    thumbnail_path = thumbnail_entry.get()

    # Verificar se os campos obrigatórios estão preenchidos
    if not video_path or not title or not description or not tags or not thumbnail_path:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios!")
        return

    # Iterar sobre as redes sociais selecionadas
    for network in selected_networks:
        if network in upload_functions:
            try:
                print(f"Iniciando upload para {network}...")
                upload_functions[network](video_path, title, description, tags, thumbnail_path)
                print(f"Upload concluído para {network}.")
            except Exception as e:
                print(f"Erro ao fazer upload para {network}: {e}")
        else:
            print(f"Nenhuma função de upload configurada para {network}.")

# ------------------------------------------------------------------------------
#                          INTERFACE VIDEOS
# ------------------------------------------------------------------------------

def show_videos(frame):
    """Exibe a interface para vídeos no frame fornecido."""
    for widget in frame.winfo_children():
        widget.destroy()
    
    # ----------[ Área de Seleção - Esquerda ]----------
    left_frame = ctk.CTkFrame(frame, width=300)
    left_frame.pack(side="left", fill="y")

    ctk.CTkLabel(left_frame, text="Selecione as Opções", font=("Arial", 16)).pack(pady=15, padx=20)

    right_frame = ctk.CTkFrame(frame, border_color='#cccccc', border_width=0)
    right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    social_networks = [
        {"name": "YouTube", "filename": "youtube.png"},
        {"name": "COS.TV", "filename": "cos_tv.png"},
        {"name": "Odysee", "filename": "odysee.png"},
        {"name": "Rumble", "filename": "rumble.png"},
        {"name": "Tiktok", "filename": "tiktok.png"},
        {"name": "Facebook", "filename": "facebook.png"},
    ]

    icon_dir = "./icons"
    
    # Mapeamento de redes sociais para funções
    upload_functions = {
        "YouTube": upload_youtube,
        "COS.TV": upload_cos_tv,
    }

    # Lista para armazenar as redes selecionadas
    selected_networks = []

    def toggle_network(network_name):
        """Alterna o estado de seleção de uma rede social."""
        if network_name in selected_networks:
            selected_networks.remove(network_name)
        else:
            selected_networks.append(network_name)
        print(f"Redes sociais selecionadas: {selected_networks}")  # Apenas para debug
    
    for network in social_networks:
        icon_path = os.path.join(icon_dir, network["filename"])
        if not os.path.exists(icon_path):
            print(f"Ícone não encontrado: {icon_path}")
            continue

        icon_image = ctk.CTkImage(light_image=Image.open(icon_path), size=(50, 50))

        # Frame para cada botão de rede social
        item_frame = ctk.CTkFrame(left_frame, border_width=2)
        item_frame.pack(fill="x", padx=10, pady=5)

        # Ícone
        icon_label = ctk.CTkLabel(item_frame, image=icon_image, text="")
        icon_label.pack(side="left", padx=5, pady=5)

        # SOMENTE AQUI ESTÁ O PROBLEMA DE NÃO APARECER O SWITCH ATIVADO POR PADRÃO DO YOUTUBE E MANDAR UMA MENSAGEM CASO NÃO ESTEJA SELECIONADO UMA DAS OPÇÕES

        # Switch
        initial_value = "off" if network["name"] == "YouTube" else "off"

        if network["name"] == "YouTube":
            selected_networks.append(network["name"])  # Adicionar YouTube por padrão

        button = ctk.CTkSwitch(
            item_frame, 
            text=network["name"],
            command=lambda n=network["name"]: toggle_network(n),
            height=30,
            corner_radius=20,
            variable=ctk.StringVar(value=initial_value),
        )
        button.pack(side="right", fill="x", expand=True, padx=5)
    
    interface_upload(right_frame, selected_networks, upload_functions)


def interface_upload(right_frame, selected_networks, upload_functions):
    global video_entry, title_entry, description_entry, tags_entry, thumbnail_entry

    # ----------[ Caminho do vídeo ]----------
    ctk.CTkLabel(right_frame, text="Caminho do Vídeo:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    video_entry = ctk.CTkEntry(right_frame, placeholder_text=".MOV | .MPEG4 | .MP4 | .AVI | .WMV | .FLV | .3GPP | .WebM | .MKV", width=400)
    video_entry.grid(row=1, column=1, padx=10, pady=5)
    ctk.CTkButton(right_frame, text="Selecionar", command=lambda: select_file(video_entry)).grid(row=1, column=2, padx=10, pady=5)

    # ----------[ Título do vídeo ]----------
    ctk.CTkLabel(right_frame, text="Título:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    title_entry = ctk.CTkEntry(right_frame, placeholder_text="Título do vídeo", width=400)
    title_entry.grid(row=2, column=1, padx=10, pady=5)

    # ----------[ Descrição do vídeo ]----------
    ctk.CTkLabel(right_frame, text="Descrição:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    description_entry = ctk.CTkTextbox(right_frame, width=400, height=100)
    description_entry.grid(row=3, column=1, padx=10, pady=5)

    # ----------[ Tags do vídeo ]----------
    ctk.CTkLabel(right_frame, text="Tags:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    tags_entry = ctk.CTkTextbox(right_frame, width=400, height=50)
    tags_entry.grid(row=4, column=1, padx=10, pady=5)

    # ----------[ Caminho da miniatura ]----------
    ctk.CTkLabel(right_frame, text="Caminho da Miniatura:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    thumbnail_entry = ctk.CTkEntry(right_frame, placeholder_text=".JPEG | .PNG | .GIF | .BMP", width=400)
    thumbnail_entry.grid(row=5, column=1, padx=10, pady=5)
    ctk.CTkButton(right_frame, text="Selecionar", command=lambda: select_file(thumbnail_entry)).grid(row=5, column=2, padx=10, pady=5)

    # ----------[ Botão Geral ]----------
    ctk.CTkButton(
        right_frame,
        text="Postar",
        corner_radius=5,
        command=lambda: execute_uploads(selected_networks, upload_functions)
    ).grid(row=6, column=0, columnspan=2, pady=10)
    
create_menu()