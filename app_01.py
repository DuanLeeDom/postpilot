import os
import sys
import time
import customtkinter as ctk
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
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

        '''
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
        '''

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
        scrollable_area = driver.find_element(By.ID, "scrollable-content")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", scrollable_area)

        # Carrega a miniatura
        time.sleep(4)
        thumbnail_input = driver.find_element(By.XPATH, '//input[@type="file"]')
        thumbnail_input.send_keys(thumbnail_path)

        # Rola até o final da página para selecionar o público-alvo
        time.sleep(1)
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scrollable_area)

        # Define o público-alvo como "não para crianças"
        time.sleep(2)
        audience_option = driver.find_elements(By.CLASS_NAME, 'style-scope tp-yt-paper-radio-button')
        audience_option[1].click()

        # Adiciona tags ao vídeo
        time.sleep(1)
        tags_input = driver.find_elements(By.XPATH, '//*[@id="tags-input"]/ytcp-chip-bar/div/input')
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

# ========================================================================
#                      MENU INICIAL | OPÇÕES
# ========================================================================

def create_interface():
    ctk.set_appearance_mode("System")  # Modo de aparência (System, Light, Dark)
    ctk.set_default_color_theme("green")  # Tema de cor padrão

    root = ctk.CTk()
    root.title("YouTube Video Uploader")

    # ----------[ Obtendo as dimensões da tela | Centralizar ]----------
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 730
    window_height = 500

    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)

    root.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")  

    # ----------[ Caminho do vídeo ]----------
    ctk.CTkLabel(root, text="Caminho do Vídeo:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    video_entry = ctk.CTkEntry(root, placeholder_text=".MOV | .MPEG4 | .MP4 | .AVI | .WMV | .FLV | .3GPP | .WebM | .MKV", width=400)
    video_entry.grid(row=1, column=1, padx=10, pady=5)
    ctk.CTkButton(root, text="Selecionar", command=lambda: select_file(video_entry)).grid(row=1, column=2, padx=10, pady=5)

    # ----------[ Titulo do vídeo ]----------
    ctk.CTkLabel(root, text="Título:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    title_entry = ctk.CTkEntry(root, placeholder_text="Título do vídeo", width=400)
    title_entry.grid(row=2, column=1, padx=10, pady=5)

    # ----------[ Descrição do vídeo ]----------
    ctk.CTkLabel(root, text="Descrição:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    description_entry = ctk.CTkTextbox(root, width=400)
    description_entry.grid(row=3, column=1, padx=10, pady=5)

    # ----------[ Miniatura do vídeo ]----------
    ctk.CTkLabel(root, text="Caminho da Miniatura:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    thumbnail_entry = ctk.CTkEntry(root, placeholder_text=".JPEG | .PNG | .GIF | .BMP", width=400)
    thumbnail_entry.grid(row=4, column=1, padx=10, pady=5)
    ctk.CTkButton(root, text="Selecionar", command=lambda: select_file(thumbnail_entry)).grid(row=4, column=2, padx=10, pady=5)

    # ----------[ Tags do vídeo ]----------
    ctk.CTkLabel(root, text="Tags:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    tags_entry = ctk.CTkTextbox(root, width=400, height=50)
    tags_entry.grid(row=5, column=1, padx=10, pady=5)

    #       ----------[        ]----------
    #       ----------[ BOTÕES ]----------
    #       ----------[        ]----------

    # ----------[ Botão de Upload YouTube ]----------
    ctk.CTkButton(root, text="Upload YouTube", command=lambda: upload_youtube(
        video_entry.get(), title_entry.get(), description_entry.get("1.0", "end-1c"),
        tags_entry.get("1.0", "end-1c"),
        thumbnail_entry.get()
    )).grid(row=6, column=0, columnspan=2, pady=10)

    '''
    # ----------[ Botão de Upload Cos.Tv ]----------
    ctk.CTkButton(root, text="Upload Cos.Tv", command=lambda: upload_cos_tv(
        video_entry.get(), title_entry.get(), description_entry.get("1.0", "end-1c"),
        tags_entry.get("1.0", "end-1c"),
        thumbnail_entry.get()
    )).grid(row=6, column=1, columnspan=2, pady=10)
    '''
    
    # ----------[ Botão de abrir o Google Chrome ]----------
    ctk.CTkButton(root, text="Abrir Google Chrome", command=lambda: open_google()).grid(row=7, column=0, columnspan=2, pady=10)

    # ----------[ Botão de fechar navegador ]----------
    ctk.CTkButton(root, text="Fechar Navegador", command=lambda: close_browser_tab(driver)).grid(row=7, column=1, columnspan=2, pady=10)

    # ----------[ Botão de Configuração ]----------
    ctk.CTkButton(root, text="Configuração", width=40, height=40, fg_color='#191919', command=lambda: configuration()).grid(row=7, column=2, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_interface()