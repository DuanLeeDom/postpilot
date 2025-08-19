
# ===============================
#   IMPORTAÇÕES E DEPENDÊNCIAS   =
# ===============================

import os
import sys
import time
import psutil
import customtkinter as ctk
from tkcalendar import Calendar
from tkinter import filedialog, messagebox
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import date
from selenium.webdriver.common.keys import Keys
import json
import threading
from pathlib import Path


# ===============================
#   CONSTANTES DE CAMINHO        =
# ===============================

BASE_DIR = Path(__file__).resolve().parent
ICONS_DIR = BASE_DIR / "assets" / "icons"


# ===============================
#   FUNÇÕES UTILITÁRIAS          =
# ===============================

def wait_for_element(driver, by, value, timeout=10, condition='presence'):
    """
    Espera de forma inteligente por um elemento no DOM.
    - condition: 'presence', 'visible', 'clickable'
    """
    wait = WebDriverWait(driver, timeout)
    if condition == 'presence':
        return wait.until(EC.presence_of_element_located((by, value)))
    elif condition == 'visible':
        return wait.until(EC.visibility_of_element_located((by, value)))
    elif condition == 'clickable':
        return wait.until(EC.element_to_be_clickable((by, value)))
    else:
        raise ValueError("Condição desconhecida para espera.")


# ========================================================================
#   VERIFICAÇÃO DO GOOGLE CHROME
# ========================================================================

def is_chrome_open():
    """Verifica se o Google Chrome já está aberto."""
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if "chrome" in process.info['name'].lower():
            return True
    return False

def get_driver():
    """Retorna uma instância do WebDriver, reutilizando o Chrome se já estiver aberto."""
    chrome_options = Options()
    main_directory = os.path.join(sys.path[0])

    # Configuração do perfil do Chrome
    chrome_options.add_argument("--user-data-dir=" + main_directory + "/chrome_profile")
    chrome_options.add_argument("--remote-debugging-port=9223")
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Inicializa o driver
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


# ========================================================================
#   OPEN GOOGLE CHROME | SELENIUM
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
#   CONFIGURATION | SELENIUM
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
#   UPLOAD DE VÍDEO PARA O YOUTUBE | SELENIUM
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
        global driver
        driver = get_driver()
        wait = WebDriverWait(driver, 30)

        # Verifica se já há abas abertas e, se sim, fecha a última
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        # Abre o YouTube Studio
        wait = WebDriverWait(driver, 60)
        driver.maximize_window()
        driver.get('https://studio.youtube.com')

        # Inicia o processo de upload
        # time.sleep(2)
        upload_button = wait_for_element(driver, By.XPATH, '//*[@id="create-icon"]/ytcp-button-shape', timeout=10, condition='clickable')
        upload_button.click()

        # time.sleep(1)
        video_upload_option = wait_for_element(driver, By.XPATH, '//*[@id="text-item-0"]/ytcp-ve/tp-yt-paper-item-body/div', timeout=10, condition='clickable')
        video_upload_option.click()

        # Carrega o arquivo de vídeo
        # time.sleep(5)
        video_input = wait_for_element(driver, By.XPATH, '//input[@type="file"]', timeout=10, condition='visible')
        video_input = wait_for_element(driver, By.NAME, 'Filedata', timeout=10, condition='visible')
        video_input.send_keys(video_path)

        # Preenche título e descrição
        # time.sleep(5)
        text_inputs = wait_for_element(driver, By.CLASS_NAME, 'style-scope ytcp-social-suggestions-textbox', timeout=10, condition='visible')

        # Define o título do vídeo
        text_inputs.send_keys(Keys.CONTROL + "a")  # Seleciona todo o texto
        text_inputs.send_keys(Keys.BACKSPACE)      # Remove o texto atual
        text_inputs.send_keys(title)

        # Define a descrição do vídeo
        text_inputs.send_keys(Keys.CONTROL + "a")
        text_inputs.send_keys(Keys.BACKSPACE)
        text_inputs.send_keys(description)

        # Ajusta a visualização para fazer upload da miniatura
        # time.sleep(1)
        element_to_scroll = wait_for_element(driver, By.XPATH, '//input[@type="file"]', timeout=10, condition='visible')
        driver.execute_script("arguments[0].scrollIntoView(true);", element_to_scroll)

        # Carrega a miniatura
        # time.sleep(4)
        thumbnail_input = wait_for_element(driver, By.XPATH, '//input[@type="file"]', timeout=10, condition='visible')
        thumbnail_input.send_keys(thumbnail_path)

        # Rola até o final da página para selecionar o público-alvo
        # time.sleep(1)
        element_to_scroll = wait_for_element(driver, By.CLASS_NAME, 'style-scope tp-yt-paper-radio-button', timeout=10, condition='visible')
        driver.execute_script("arguments[0].scrollIntoView(true);", element_to_scroll)

        # Define o público-alvo como "não para crianças"
        # time.sleep(2)
        audience_option = wait_for_element(driver, By.CLASS_NAME, 'style-scope tp-yt-paper-radio-button', timeout=10, condition='visible')
        audience_option.click()
    
        # Mostrar mais
        # time.sleep(2)
        show_more = wait_for_element(driver, By.XPATH, '//*[@id="toggle-button"]/ytcp-button-shape/button/yt-touch-feedback-shape/div/div[2]', timeout=10, condition='clickable')
        show_more.click()

        # time.sleep(2)
        # scroll
        element_to_scroll = wait_for_element(driver, By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[2]/div', timeout=10, condition='visible')
        driver.execute_script("arguments[0].scrollIntoView(true);", element_to_scroll)

        # Conteudo alterado
        # time.sleep(1)
        altered_content = wait_for_element(driver, By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[2]/ytkp-altered-content-select/div[2]/div[2]/ytcp-ve/tp-yt-paper-radio-button/div[1]/div[1]', timeout=10, condition='clickable')
        altered_content.click()

        # time.sleep(2)
        # scroll
        element_to_scroll = wait_for_element(driver, By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[6]/div[1]', timeout=10, condition='visible')
        driver.execute_script("arguments[0].scrollIntoView(true);", element_to_scroll)

        # Adiciona tags ao vídeo
        # time.sleep(1)
        tags_input = wait_for_element(driver, By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[6]/ytcp-form-input-container/div[1]/div/ytcp-free-text-chip-bar/ytcp-chip-bar/div/input', timeout=10, condition='visible')
        tags_input.send_keys(tags)
        tags_input.send_keys(Keys.ENTER)

        # Avança nas páginas de configuração
        # time.sleep(2)
        for _ in range(3):  # Pressiona "Avançar" três vezes
            next_button = wait_for_element(driver, By.XPATH, '//*[@id="next-button"]/ytcp-button-shape/button', timeout=10, condition='clickable')
            next_button.click()
            time.sleep(2)

        # Define a visibilidade como "Privado" e salva o vídeo
        visibility_option = wait_for_element(driver, By.XPATH, '//*[@id="private-radio-button"]/div[1]', timeout=10, condition='clickable')
        visibility_option.click()

        # time.sleep(2)
        save_button = wait_for_element(driver, By.XPATH, '//*[@id="done-button"]/ytcp-button-shape/button', timeout=10, condition='clickable')
        save_button.click()

        # Confirmação de sucesso
        # time.sleep(2)
        messagebox.showinfo("Sucesso", "Upload concluído com sucesso!")
    except Exception as e:
        # Exibe uma mensagem de erro em caso de falha
        messagebox.showerror("Erro", f"Ocorreu um erro durante o upload: {str(e)}")


# ========================================================================
#   UPLOAD DE VÍDEO PARA O COS.TV | SELENIUM
# ========================================================================

def upload_cos_tv(video_path, title, description, tags, thumbnail_path):
    try:
        global driver
        driver = get_driver()
        wait = WebDriverWait(driver, 30)

        # Verifica se já há abas abertas e, se sim, fecha a última
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        # Navega até o YouTube
        wait = WebDriverWait(driver, 60)
        driver.maximize_window()
        driver.get('https://cos.tv/studio')

        time.sleep(5)
        # Entrar onde faz os uploads
        upload_button = wait_for_element(driver, By.XPATH, '/html/body/div/div/div/div/div[1]/nav/div[1]/div/a[1]', timeout=15, condition='clickable')
        upload_button.click()

        # Carrega o arquivo de vídeo
        video_input = wait_for_element(driver, By.XPATH, '//input[@type="file"]', timeout=10, condition='visible')
        video_input.send_keys(video_path)

        # Preenche título e descrição
        text_input = wait_for_element(driver, By.XPATH, '/html/body/div/div/div/div/div[1]/main/div/div[1]/div/form/div/div/div[2]/div/div[1]/div/div[1]/div/input', timeout=10, condition='visible')
        text_input.send_keys(Keys.CONTROL + "a")  # Seleciona todo o texto
        text_input.send_keys(Keys.BACKSPACE)      # Remove o texto atual
        text_input.send_keys(title)

        description_inputs = wait_for_element(driver, By.XPATH, '/html/body/div/div/div/div/div[1]/main/div/div[1]/div/form/div/div/div[2]/div/div[2]/div/div[1]/div[1]/textarea', timeout=10, condition='visible')
        description_inputs.send_keys(description)

        # Obtém o texto das tags corretamente
        tags_text = tags_entry.get("1.0", "end-1c")
        tags_list = [tag.strip() for tag in tags_text.split(",") if tag.strip()]
        first_three_tags = tags_list[:3]

        try:
            tags_input_xpath = "/html/body/div/div/div/div/div[1]/main/div/div[1]/div/form/div/div[1]/div[2]/div/div[5]/div/div[1]/div[1]/div[1]/input"
            for tag in first_three_tags:
                tags_input = wait_for_element(driver, By.XPATH, tags_input_xpath, timeout=10, condition='visible')
                tags_input.click()
                tags_input.clear()
                tags_input.send_keys(tag)
                tags_input.send_keys(Keys.TAB)
        except Exception as e:
            messagebox.showerror("Erro ao adicionar tags", f"Erro inesperado ao processar as tags: {e}")

        time.sleep(2)
        click_01 = wait_for_element(driver, By.XPATH, '/html/body/div/div/div/div/div[1]/main/div/div[1]/div/form/div/div[1]/div[3]/div[4]/button/span', timeout=10, condition='clickable')
        click_01.click()

        time.sleep(2)
        thumbnail_input = wait_for_element(driver, By.XPATH, '/html/body/div/div/div/div/div[1]/main/div/div[1]/div/form/div/div/div[3]/div[4]/button', timeout=10, condition='visible')
        thumbnail_input.send_keys(thumbnail_path)
        
        time.sleep(2)
        click_02 = wait_for_element(driver, By.XPATH, '/html/body/div/div/div/div[3]/div/div/div[3]/button', timeout=10, condition='clickable')
        click_02.click()

        time.sleep(2)
        publish_input = wait_for_element(driver, By.XPATH, '/html/body/div/div/div/div[1]/div[1]/main/div/div[1]/div/form/div/div/button', timeout=10, condition='clickable')
        publish_input.click()

        messagebox.showinfo("Sucesso", "Upload concluído com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


# ========================================================================
#   FUNÇÕES AUXILIARES
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
#   POST YOUTUBE | SELENIUM
# ========================================================================

def post_youtube(post_box):
    try:
        global driver
        driver = get_driver()
        wait = WebDriverWait(driver, 30)

        # Verifica se já há abas abertas e, se sim, fecha a última
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        # Abre uma nova aba para postar no YouTube
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get('https://www.youtube.com/')

        time.sleep(2)  # Aguarde o carregamento da página

        # Clica no ícone do perfil para abrir o menu
        profile_icon = wait_for_element(driver, By.XPATH, '//button[@id="avatar-btn"]', timeout=10, condition='clickable')
        profile_icon.click()

        time.sleep(3)

        # Obtém o nome do canal (ex: @DuanLeeDom)
        channel_name_element = wait_for_element(driver, By.XPATH, '/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[2]/ytd-active-account-header-renderer/div/yt-formatted-string[3]', timeout=10, condition='visible')
        channel_name = channel_name_element.text.strip()  # Remove espaços extras   

        if not channel_name.startswith("@"):
            messagebox.showerror("Erro", "Não foi possível obter o nome do canal corretamente.")
            return

        time.sleep(3)
        # Formata a URL correta da aba "Comunidade"
        community_url = f"https://www.youtube.com/{channel_name}/community"
        driver.get(community_url)

        time.sleep(3)  # Aguarde o carregamento

        # Clica na caixa de postagem
        post_box_element = wait_for_element(driver, By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-backstage-items/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[7]/ytd-backstage-post-dialog-renderer/div[2]/div[2]/div/div[1]/yt-formatted-string', timeout=10, condition='clickable')
        post_box_element.click()

        time.sleep(3)
        # Seleciona o campo de entrada e insere o texto
        text_area = wait_for_element(driver, By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-backstage-items/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[7]/ytd-backstage-post-dialog-renderer/div[2]/ytd-commentbox/div[2]/div/div[2]/tp-yt-paper-input-container/div[2]/div/div[1]/ytd-emoji-input/yt-user-mention-autosuggest-input/yt-formatted-string/div', timeout=10, condition='visible')
        text_area.send_keys(post_box)

        time.sleep(3)
        post = wait_for_element(driver, By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-backstage-items/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[7]/ytd-backstage-post-dialog-renderer/div[2]/ytd-commentbox/div[2]/div/div[5]/div[5]/ytd-button-renderer[2]/yt-button-shape/button', timeout=10, condition='clickable')
        post.click()

        time.sleep(4)
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


# ========================================================================
#   POST FACEBOOK | SELENIUM
# ========================================================================

def post_facebook(post_box):
    try:
        global driver
        driver = get_driver()
        wait = WebDriverWait(driver, 30)

        # Verifica se já há abas abertas e, se sim, fecha a última
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        wait = WebDriverWait(driver, 30)
        driver.maximize_window()
        driver.get('https://www.facebook.com/')

        time.sleep(5)  # Aguarde o carregamento da página
        # clicar para postar
        post_box_element = wait_for_element(driver, By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div[1]/span', timeout=10, condition='clickable')
        post_box_element.click()

        time.sleep(3)
        post_box_next = wait_for_element(driver, By.XPATH, '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div/div[1]/p', timeout=10, condition='clickable')
        post_box_next.click()
        post_box_next.send_keys(post_box)

        time.sleep(3)
        post_box_publish = wait_for_element(driver, By.XPATH, '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div/div[3]/div[2]/div/div/div', timeout=10, condition='clickable')
        post_box_publish.click()

        time.sleep(4)    
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


# ========================================================================
#   POST LINKEDIN | SELENIUM
# ========================================================================

def post_linkedin(post_box):
    try:
        global driver
        driver = get_driver()
        wait = WebDriverWait(driver, 30)

        # Verifica se já há abas abertas e, se sim, fecha a última
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        wait = WebDriverWait(driver, 30)
        driver.maximize_window()
        driver.get('https://www.linkedin.com/feed/')

        time.sleep(5)  # Aguarde o carregamento da página
        # clicar para postar
        post_box_element = wait_for_element(driver, By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/div[1]/div[2]/div[2]/button/span/span', timeout=10, condition='clickable')
        post_box_element.click()

        time.sleep(3)
        post_box_next = wait_for_element(driver, By.XPATH, '/html/body/div[4]/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div/div/div/div[1]/p', timeout=10, condition='clickable')
        post_box_next.click()
        post_box_next.send_keys(post_box)

        time.sleep(3)
        post_box_publish = wait_for_element(driver, By.XPATH, '/html/body/div[4]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/button', timeout=10, condition='clickable')
        post_box_publish.click()

        time.sleep(4)    
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


# ========================================================================
#   POST X / Twitter | SELENIUM
# ========================================================================

def post_x_twitter(post_box):
    try:
        global driver
        driver = get_driver()
        wait = WebDriverWait(driver, 30)

        # Verifica se já há abas abertas e, se sim, fecha a última
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        wait = WebDriverWait(driver, 30)
        driver.maximize_window()
        driver.get('https://x.com/')

        time.sleep(5)  # Aguarde o carregamento da página
        # clicar para postar
        post_box_element = wait_for_element(driver, By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div', timeout=10, condition='clickable')
        post_box_element.click()

        time.sleep(3)
        post_box_next = wait_for_element(driver, By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div', timeout=10, condition='clickable')
        post_box_next.click()
        post_box_next.send_keys(post_box)

        time.sleep(3)
        post_box_publish = wait_for_element(driver, By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button', timeout=10, condition='clickable')
        post_box_publish.click()

        time.sleep(4)    
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


# ========================================================================
#   POST REDDIT | SELENIUM
# ========================================================================

def post_reddit(post_box, title_post=None):
    try:
        global driver
        driver = get_driver()
        wait = WebDriverWait(driver, 30)

        # Verifica se já há abas abertas e, se sim, fecha a última
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        wait = WebDriverWait(driver, 30)
        driver.maximize_window()
        driver.get('https://reddit.com/')

        time.sleep(5)  # Aguarde o carregamento da página
        # clicar para postar
        post_box_element = wait_for_element(driver, By.XPATH, '/html/body/shreddit-app/reddit-header-large/reddit-header-action-items/header/nav/div[3]/div[1]/span[3]/create-post-entry-point-wrapper/faceplate-tracker/faceplate-tooltip/a', timeout=10, condition='clickable')
        post_box_element.click()

        time.sleep(5)
        # Criar no seu proprio subreddit
        post_community = wait_for_element(driver, By.XPATH, '//*[@id="dropdown-button"]', timeout=10, condition='clickable')
        post_community.click()
        
        time.sleep(2)
        post_community.send_keys(Keys.TAB)
        post_community.send_keys(Keys.ENTER)

        time.sleep(2)
        title_box = wait_for_element(driver, By.XPATH, '/html/body/shreddit-app/div[1]/div[1]/div/main/r-post-composer-form/section/faceplate-form-section[1]/fieldset/div[1]/faceplate-tracker/faceplate-textarea-input', timeout=10, condition='clickable')
        title_box.click()
        # title_box.send_keys(title_post)

        if title_post != None:
            title_box.send_keys(title_post)  # Preenche o título se existir
        else:
            title_box.send_keys("Título Padrão")  # Caso não tenha título, usa um padrão

        time.sleep(2)
        post_text = wait_for_element(driver, By.XPATH, '/html/body/shreddit-app/div[1]/div[1]/div/main/r-post-composer-form/section/faceplate-form-section[2]/fieldset/faceplate-tracker/shreddit-composer/div/p', timeout=10, condition='clickable')
        post_text.click()
        post_text.send_keys(post_box)

        time.sleep(2)
        post_click = wait_for_element(driver, By.XPATH, '/html/body/shreddit-app/div[1]/div[1]/div/main/r-post-composer-form/section/faceplate-form-section[6]/div/div/r-post-form-submit-button[1]', timeout=10, condition='clickable')
        post_click.click()

        time.sleep(4)    
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


# ------------------------------------------------------------------------------
#   Função para abrir a janela de configurações de usuário
# ------------------------------------------------------------------------------

SETTINGS_FILE = os.path.join(sys.path[0], 'settings.json')

def load_settings():
    """Carrega as configurações do arquivo settings.json, se existir."""
    default_settings = {
        "theme": "System",
        "color": "blue",
        "notifications": True
    }
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Garantir que todas as chaves existam
                for k, v in default_settings.items():
                    if k not in data:
                        data[k] = v
                return data
        except Exception:
            return default_settings
    return default_settings


def save_settings_file(settings):
    """Salva as configurações no arquivo settings.json."""
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar configurações: {str(e)}")

def open_settings_window():
    """Cria e exibe uma janela de configurações profissional, com tela dividida e rolagem."""
    # Carregar configurações atuais
    settings = load_settings()
    login = settings.get("login", "")
    password = settings.get("password", "")

    settings_window = ctk.CTkToplevel()
    settings_window.title("Configurações")

    # Centralizar janela
    screen_width = settings_window.winfo_screenwidth()
    screen_height = settings_window.winfo_screenheight()
    window_width = 800
    window_height = 600
    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)
    settings_window.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")
    settings_window.resizable(False, False)

    # Frame com rolagem para todo o conteúdo
    scrollable = ctk.CTkScrollableFrame(settings_window, fg_color=("gray90", "gray13"), width=window_width-40, height=window_height-40)
    scrollable.pack(fill="both", expand=True, padx=10, pady=10)
    scrollable.grid_columnconfigure(0, weight=1)
    scrollable.grid_columnconfigure(1, weight=1)

    # Frame de configurações (esquerda)
    config_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
    config_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 30), pady=0)
    config_row = 0
    ctk.CTkLabel(config_frame, text="Configurações do Sistema", font=("Arial", 18, "bold")).grid(row=config_row, column=0, sticky="w", padx=10, pady=(0, 20))
    config_row += 1
    # Tema
    ctk.CTkLabel(config_frame, text="Tema:", font=("Arial", 14)).grid(row=config_row, column=0, sticky="w", padx=10, pady=5)
    config_row += 1
    theme_var = ctk.StringVar(value=settings["theme"])
    for theme in ["System", "Light", "Dark"]:
        ctk.CTkRadioButton(config_frame, text=theme, variable=theme_var, value=theme).grid(
            row=config_row, column=0, sticky="w", padx=30, pady=2)
        config_row += 1
    # Cores
    ctk.CTkLabel(config_frame, text="Tema de Cores:", font=("Arial", 14)).grid(row=config_row, column=0, sticky="w", padx=10, pady=5)
    config_row += 1
    color_var = ctk.StringVar(value=settings["color"])
    for color in ["blue", "green"]:
        ctk.CTkRadioButton(config_frame, text=color, variable=color_var, value=color).grid(
            row=config_row, column=0, sticky="w", padx=30, pady=2)
        config_row += 1
    # Notificações
    ctk.CTkLabel(config_frame, text="Notificações:", font=("Arial", 14)).grid(row=config_row, column=0, sticky="w", padx=10, pady=5)
    config_row += 1
    notif_var = ctk.BooleanVar(value=settings["notifications"])
    ctk.CTkCheckBox(config_frame, text="Ativar notificações", variable=notif_var).grid(
        row=config_row, column=0, sticky="w", padx=30, pady=5)
    config_row += 1

    # Frame de login (direita)
    login_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
    login_frame.grid(row=0, column=1, sticky="nsew", padx=(30, 0), pady=0)
    login_row = 0
    ctk.CTkLabel(login_frame, text="Login de Usuário", font=("Arial", 18, "bold")).grid(row=login_row, column=0, sticky="w", padx=10, pady=(0, 20))
    login_row += 1
    ctk.CTkLabel(login_frame, text="Usuário:", font=("Arial", 14)).grid(row=login_row, column=0, sticky="w", padx=10, pady=5)
    login_row += 1
    login_var = ctk.StringVar(value=login)
    ctk.CTkEntry(login_frame, textvariable=login_var, placeholder_text="Digite seu usuário", width=300).grid(row=login_row, column=0, padx=30, pady=2, sticky="w")
    login_row += 1
    ctk.CTkLabel(login_frame, text="Senha:", font=("Arial", 14)).grid(row=login_row, column=0, sticky="w", padx=10, pady=5)
    login_row += 1
    password_var = ctk.StringVar(value=password)
    ctk.CTkEntry(login_frame, textvariable=password_var, placeholder_text="Digite sua senha", show="*", width=300).grid(row=login_row, column=0, padx=30, pady=2, sticky="w")
    login_row += 1

    # Seção minimalista de status das redes sociais
    ctk.CTkLabel(login_frame, text="Status das Contas", font=("Arial", 14, "bold")).grid(row=login_row, column=0, sticky="w", padx=10, pady=(20, 5))
    login_row += 1
    social_status_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
    social_status_frame.grid(row=login_row, column=0, sticky="w", padx=10, pady=5)
    # Lista de redes sociais
    social_accounts = [
        {"name": "YouTube", "icon": "youtube.png", "url": "https://studio.youtube.com", "check": "//img[@id='img' and @alt]"},
        {"name": "Facebook", "icon": "facebook.png", "url": "https://www.facebook.com/", "check": "//div[@aria-label='Conta'] | //image[@xlink:href]"},
        {"name": "Linkedin", "icon": "linkedin.png", "url": "https://www.linkedin.com/feed/", "check": "//img[contains(@class, 'global-nav__me-photo')]"},
        {"name": "X", "icon": "x.png", "url": "https://x.com/", "check": "//div[@data-testid='SideNav_AccountSwitcher_Button']"},
        {"name": "Reddit", "icon": "reddit.png", "url": "https://reddit.com/", "check": "//img[contains(@alt, 'User avatar')]"},
    ]
    # Dicionário para status
    social_status = {acc["name"]: False for acc in social_accounts}
    icon_widgets = {}
    status_circles = {}
    tooltips = {}
    for idx, acc in enumerate(social_accounts):
        icon_path = ICONS_DIR / acc["icon"]
        if not icon_path.exists():
            print(f"Ícone não encontrado: {icon_path}")
            continue
        icon_img = ctk.CTkImage(light_image=Image.open(icon_path), size=(36, 36))
        icon_label = ctk.CTkLabel(social_status_frame, image=icon_img, text="")
        icon_label.grid(row=0, column=idx, padx=10, pady=2)
        icon_widgets[acc["name"]] = icon_label
        # Círculo de status (canvas)
        canvas = ctk.CTkCanvas(social_status_frame, width=12, height=12, highlightthickness=0)
        circle = canvas.create_oval(2, 2, 12, 12, fill="#bdc3c7", outline="")
        canvas.grid(row=1, column=idx, pady=(0, 2))
        status_circles[acc["name"]] = (canvas, circle)
        # Tooltip
        def make_tooltip(widget, text):
            def on_enter(e):
                widget.tooltip = ctk.CTkToplevel(widget)
                widget.tooltip.overrideredirect(True)
                widget.tooltip.geometry(f"+{widget.winfo_rootx()+20}+{widget.winfo_rooty()+20}")
                ctk.CTkLabel(widget.tooltip, text=text, font=("Arial", 10), fg_color="#222", text_color="#fff").pack()
            def on_leave(e):
                if hasattr(widget, 'tooltip'):
                    widget.tooltip.destroy()
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
        make_tooltip(icon_label, f"{acc['name']}: Desconectado")
        tooltips[acc["name"]] = icon_label
    login_row += 1

    # Função para atualizar status visual
    def update_status_icon(name, connected):
        canvas, circle = status_circles[name]
        color = "#27ae60" if connected else "#bdc3c7"
        canvas.itemconfig(circle, fill=color)
        # Atualiza tooltip
        label = icon_widgets[name]
        for seq in label.bind():
            label.unbind(seq)
        status_txt = "Conectado" if connected else "Desconectado"
        def make_tooltip(widget, text):
            def on_enter(e):
                widget.tooltip = ctk.CTkToplevel(widget)
                widget.tooltip.overrideredirect(True)
                widget.tooltip.geometry(f"+{widget.winfo_rootx()+20}+{widget.winfo_rooty()+20}")
                ctk.CTkLabel(widget.tooltip, text=text, font=("Arial", 10), fg_color="#222", text_color="#fff").pack()
            def on_leave(e):
                if hasattr(widget, 'tooltip'):
                    widget.tooltip.destroy()
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
        make_tooltip(label, f"{name}: {status_txt}")

    # Função de checagem real de login (background)
    def check_social_status(acc):
        try:
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            import sys, os
            chrome_options = Options()
            main_directory = os.path.join(sys.path[0])
            chrome_options.add_argument("--user-data-dir=" + main_directory + "/chrome_profile")
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--window-size=800,600")
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_experimental_option("useAutomationExtension", False)
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_page_load_timeout(20)
            driver.get(acc["url"])
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, acc["check"])))
                connected = True
            except Exception:
                connected = False
            driver.quit()
        except Exception:
            connected = False
        # Atualizar status visual na thread principal
        social_status[acc["name"]] = connected
        social_status_frame.after(0, lambda: update_status_icon(acc["name"], connected))

    # Iniciar checagem em background para cada rede
    for acc in social_accounts:
        threading.Thread(target=check_social_status, args=(acc,), daemon=True).start()

    # Botões de ação centralizados abaixo das colunas (mais estético e espaçado)
    button_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
    button_frame.grid(row=1, column=0, columnspan=2, pady=20)
    button_frame.columnconfigure((0, 1, 2), weight=1)

    ctk.CTkButton(button_frame, text="Abrir Google Chrome", width=180, command=lambda: open_google()).grid(row=0, column=0, padx=20, pady=5)
    ctk.CTkButton(
        button_frame,
        text="Fechar Navegador",
        width=180,
        command=lambda: close_browser_tab(driver) if 'driver' in globals() else messagebox.showerror("Erro", "O navegador não está aberto.")
    ).grid(row=0, column=1, padx=20, pady=5)
    ctk.CTkButton(button_frame, text="Configuração", width=180, command=lambda: configuration()).grid(row=0, column=2, padx=20, pady=5)


    # Botões finais
    control_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
    control_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
    def save_settings():
        theme = theme_var.get()
        color = color_var.get()
        notifications = notif_var.get()
        login_val = login_var.get()
        password_val = password_var.get()
        # Salvar configurações
        new_settings = {
            "theme": theme,
            "color": color,
            "notifications": notifications,
            "login": login_val,
            "password": password_val
        }
        save_settings_file(new_settings)
        # Aplicar mudanças globalmente
        try:
            ctk.set_appearance_mode(theme)
            ctk.set_default_color_theme(color)
            messagebox.showinfo("Configurações", f"Configurações aplicadas!\nO programa será reiniciado para aplicar as mudanças.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar configurações: {str(e)}")
        settings_window.destroy()
        # Reiniciar o programa
        python = sys.executable
        os.execl(python, python, *sys.argv)
    ctk.CTkButton(control_frame, text="Salvar", command=save_settings).pack(side="left", padx=10)
    ctk.CTkButton(control_frame, text="Fechar", command=settings_window.destroy).pack(side="right", padx=10)
    settings_window.grab_set()
    settings_window.focus_force()


# ------------------------------------------------------------------------------
#   INTERFACE NORMAL
# ------------------------------------------------------------------------------

# Adicione uma variável global para controlar o left_frame atual e o estado de visibilidade
current_left_frame = [None]  # type: ignore  # Pode ser None ou CTkFrame
left_frame_visible = [True]

def create_menu():
    """Cria o menu de redes sociais com espaço para interface dinâmica."""
    # Carregar configurações salvas e aplicar tema/cor
    settings = load_settings()
    ctk.set_appearance_mode(settings.get('theme', 'System'))
    ctk.set_default_color_theme(settings.get('color', 'blue'))

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

    # Caminho base para os ícones
    icon_menu_path = ICONS_DIR / "menu.png"
    icon_user_path = ICONS_DIR / "user.png"
    icon_menu = ctk.CTkImage(light_image=Image.open(icon_menu_path), dark_image=Image.open(icon_menu_path), size=(40, 40))
    def toggle_left_frame():
        if current_left_frame[0] is not None:
            if left_frame_visible[0]:
                current_left_frame[0].pack_forget()
                left_frame_visible[0] = False
            else:
                current_left_frame[0].pack(side="left", fill="y")
                left_frame_visible[0] = True
    ctk.CTkButton(menu_frame, width=60, height=60, text='', image=icon_menu, fg_color="transparent", hover_color="gray", border_width=0, command=toggle_left_frame).pack(side="top")

    # menu bar | Opetions
    post_vision = ctk.CTkButton(menu_frame, width=40, height=40, text="Posts", border_width=0, command=lambda: show_posts(right_frame))
    post_vision.pack(anchor='center', pady=10)
    video_vision = ctk.CTkButton(menu_frame, width=40, height=40, text="Vídeos", border_width=0, command=lambda: show_videos(right_frame))
    video_vision.pack(anchor='center', pady=10)

    icon_user = ctk.CTkImage(light_image=Image.open(icon_user_path), dark_image=Image.open(icon_user_path), size=(40, 40))
    user_button = ctk.CTkButton(menu_frame, width=60, height=60, text='', image=icon_user, fg_color="transparent", hover_color="gray", border_width=0, command=open_settings_window)
    user_button.pack(side="bottom")

    right_frame = ctk.CTkFrame(frame, border_color='#cccccc', border_width=0)
    right_frame.pack(side="right", fill="both", expand=True, padx=0, pady=0)

    root.mainloop()


# ------------------------------------------------------------------------------
#   CARREGAMENTO...
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
#   INTERFACE POSTS
# ------------------------------------------------------------------------------

def show_posts(frame):
    global current_left_frame, left_frame_visible
    """Exibe a interface para posts no frame fornecido."""
    for widget in frame.winfo_children():
        widget.destroy()

    # ----------[ Área de Seleção - Esquerda ]----------
    left_frame = ctk.CTkFrame(frame, width=300)
    left_frame.pack(side="left", fill="y")
    current_left_frame[0] = left_frame  # type: ignore
    left_frame_visible[0] = True

    # Removido o botão de ocultar redes sociais
    ctk.CTkLabel(left_frame, text="Selecione as Opções", font=("Arial", 16)).pack(pady=15, padx=20)

    right_frame = ctk.CTkFrame(frame, border_color='#cccccc', border_width=0)
    right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    social_networks = [
        {"name": "YouTube", "filename": "youtube.png"},
        {"name": "Facebook", "filename": "facebook.png"},
        {"name": "Instagram", "filename": "instagram.png"},
        {"name": "Linkedin", "filename": "linkedin.png"},
        {"name": "X / Twitter", "filename": "x.png"},
        {"name": "Reddit", "filename": "reddit.png"}
    ]

    icon_dir = ICONS_DIR
    
    # Mapeamento de redes sociais para funções
    upload_functions = {
        "YouTube": post_youtube,
        "Facebook": post_facebook,
        "Linkedin": post_linkedin,
        "X / Twitter" : post_x_twitter,
        "Reddit" : post_reddit,
        # Adicione outras funções de post aqui
    }

    # Lista para armazenar as redes selecionadas
    selected_networks = []

    def toggle_network(network_name):
        """Alterna o estado de seleção de uma rede social."""
        if network_name in selected_networks:
            selected_networks.remove(network_name)
        else:
            selected_networks.append(network_name)
        print(f"Redes sociais selecionadas: {selected_networks}")
    
    for index, network in enumerate(social_networks):
        icon_path = icon_dir / network["filename"]
        if not icon_path.exists():
            print(f"Ícone não encontrado: {icon_path}")
            continue

        icon_image = ctk.CTkImage(light_image=Image.open(icon_path), size=(50, 50))

        item_frame = ctk.CTkFrame(left_frame, border_width=2)
        item_frame.pack(fill="x", padx=10, pady=5)

        icon_label = ctk.CTkLabel(item_frame, image=icon_image, text="")
        icon_label.pack(side="left", padx=5, pady=5)

        # Criar o switch
        button = ctk.CTkSwitch(
            item_frame, 
            text=network["name"],
            command=lambda n=network["name"]: toggle_network(n),
            height=30,
            corner_radius=20
        )
        button.pack(side="right", fill="x", expand=True, padx=5)

        # Ativar o YouTube por padrão e adicionar à lista de selecionados
        if network["name"] == "YouTube":
            button.select()
            selected_networks.append(network["name"])

    interface_posts(right_frame, selected_networks, upload_functions)

def interface_posts(frame, selected_networks, upload_functions):
    global post_box, URL_box, title_entries, title_label_main

    # Exibe a interface para posts no frame fornecido.
    for widget in frame.winfo_children():
        widget.destroy()

    main_frame = ctk.CTkFrame(frame, corner_radius=10)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Frame dedicado para campos extras
    extra_fields_frame = ctk.CTkFrame(main_frame)
    extra_fields_frame.pack(pady=(10, 0))

    # Label principal do título (inicialmente invisível)
    title_label_main = ctk.CTkLabel(main_frame, text="", font=("Arial", 20))
    title_label_main.pack(pady=10)

    # Dicionário para armazenar os campos de título extras e seus labels
    title_entries = {}
    title_labels = {}

    # Caixa de texto
    post_box = ctk.CTkTextbox(main_frame, height=400, width=900, font=("Noto Color Emoji", 18))
    post_box.pack(pady=10)

    # Mapeamento de redes para campos extras (fácil de expandir)
    extra_fields = {
        "Reddit": {"label": "Título para Reddit", "placeholder": "Título para Reddit"},
        # Adicione aqui outras redes se quiser campos extras
    }

    def update_dynamic_fields():
        # Limpa o frame antes de adicionar/remover
        for widget in extra_fields_frame.winfo_children():
            widget.destroy()
        title_entries.clear()
        title_labels.clear()
        active_titles = []
        row_idx = 0
        for network, field_info in extra_fields.items():
            if network in selected_networks:
                label = ctk.CTkLabel(extra_fields_frame, text=field_info["label"], font=("Arial", 14, "bold"))
                label.grid(row=row_idx, column=0, padx=10, pady=(5, 0), sticky="w")
                entry = ctk.CTkEntry(extra_fields_frame, placeholder_text=field_info["placeholder"], width=600)
                entry.grid(row=row_idx, column=1, padx=10, pady=(5, 0), sticky="w")
                title_labels[network] = label
                title_entries[network] = entry
                active_titles.append(field_info["label"])
                row_idx += 1
        # Atualiza o título principal com base nas redes ativas
        title_label_main.configure(text=" | ".join(active_titles) if active_titles else "")

    # Função para alternar seleção e atualizar campos extras
    def toggle_network(network_name):
        if network_name in selected_networks:
            selected_networks.remove(network_name)
        else:
            selected_networks.append(network_name)
        update_dynamic_fields()

    # Lista de redes sociais
    social_networks = [
        {"name": "YouTube", "filename": "youtube.png"},
        {"name": "Facebook", "filename": "facebook.png"},
        {"name": "Instagram", "filename": "instagram.png"},
        {"name": "Linkedin", "filename": "linkedin.png"},
        {"name": "X / Twitter", "filename": "x.png"},
        {"name": "Reddit", "filename": "reddit.png"}
    ]
    icon_dir = ICONS_DIR

    for index, network in enumerate(social_networks):
        icon_path = icon_dir / network["filename"]
        if not icon_path.exists():
            print(f"Ícone não encontrado: {icon_path}")
            continue

        icon_image = ctk.CTkImage(light_image=Image.open(icon_path), size=(50, 50))

        item_frame = ctk.CTkFrame(main_frame, border_width=2)
        item_frame.pack(fill="x", padx=10, pady=5)

        icon_label = ctk.CTkLabel(item_frame, image=icon_image, text="")
        icon_label.pack(side="left", padx=5, pady=5)

        # Criar o switch
        button = ctk.CTkSwitch(
            item_frame, 
            text=network["name"],
            command=lambda n=network["name"]: toggle_network(n),
            height=30,
            corner_radius=20
        )
        button.pack(side="right", fill="x", expand=True, padx=5)

        # Ativar o YouTube por padrão e adicionar à lista de selecionados
        if network["name"] == "YouTube":
            button.select()
            if network["name"] not in selected_networks:
                selected_networks.append(network["name"])

    # Inicializa os campos extras de acordo com a seleção inicial
    update_dynamic_fields()

    # Botão para postar
    post_button = ctk.CTkButton(
        main_frame,
        text="Postar",
        corner_radius=5,
        command=lambda: execute_uploads_post(selected_networks, upload_functions)
    )
    post_button.pack(pady=10)


# ------------------------------------------------------------------------------
#   Funções Vinculadas aos Switches | Posts
# ------------------------------------------------------------------------------
def execute_uploads_post(selected_networks, upload_functions):
    """Executa as funções de upload para as redes sociais selecionadas."""
    if not selected_networks:
        messagebox.showwarning("Aviso", "Nenhuma rede social foi selecionada!")
        return

    # Obter os valores diretamente dos campos de entrada
    text = post_box.get("1.0", "end-1c")

    # Verificar se os campos obrigatórios estão preenchidos
    if not text:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios!")
        return

    # Dicionário para armazenar títulos das redes sociais
    titles_dict = {}

    # Captura o título do Reddit, se existir
    if "Reddit" in title_entries:
        titles_dict["Reddit"] = title_entries["Reddit"].get()

    # Iterar sobre as redes sociais selecionadas
    for network in selected_networks:
        if network in upload_functions:
            try:
                print(f"Iniciando upload para {network}...")

                # Se for Reddit, passa o título armazenado
                if network == "Reddit":
                    upload_functions[network](text, titles_dict.get("Reddit", "Título Padrão"))
                else:
                    upload_functions[network](text)

                print(f"Upload concluído para {network}.")
            except Exception as e:
                print(f"Erro ao fazer upload para {network}: {e}")
        else:
            print(f"Nenhuma função de upload configurada para {network}.")


# ------------------------------------------------------------------------------
#   Funções Vinculadas aos Switches | Vídeos
# ------------------------------------------------------------------------------
def execute_uploads_video(selected_networks, upload_functions):
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
#   INTERFACE VIDEOS
# ------------------------------------------------------------------------------

def show_videos(frame):
    global current_left_frame, left_frame_visible
    """Exibe a interface para vídeos no frame fornecido."""
    for widget in frame.winfo_children():
        widget.destroy()
    
    # ----------[ Área de Seleção - Esquerda ]----------
    left_frame = ctk.CTkFrame(frame, width=300)
    left_frame.pack(side="left", fill="y")
    current_left_frame[0] = left_frame  # type: ignore
    left_frame_visible[0] = True

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
        {"name": "Instagram", "filename": "instagram.png"}
    ]

    icon_dir = ICONS_DIR
    
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
        print(f"Redes sociais selecionadas: {selected_networks}")
    
    for index, network in enumerate(social_networks):
        icon_path = icon_dir / network["filename"]
        if not icon_path.exists():
            print(f"Ícone não encontrado: {icon_path}")
            continue

        icon_image = ctk.CTkImage(light_image=Image.open(icon_path), size=(50, 50))

        item_frame = ctk.CTkFrame(left_frame, border_width=2)
        item_frame.pack(fill="x", padx=10, pady=5)

        icon_label = ctk.CTkLabel(item_frame, image=icon_image, text="")
        icon_label.pack(side="left", padx=5, pady=5)

        # Criar o switch
        button = ctk.CTkSwitch(
            item_frame, 
            text=network["name"],
            command=lambda n=network["name"]: toggle_network(n),
            height=30,
            corner_radius=20
        )
        button.pack(side="right", fill="x", expand=True, padx=5)

        # Ativar o YouTube por padrão e adicionar à lista de selecionados
        if network["name"] == "YouTube":
            button.select()
            selected_networks.append(network["name"])

    interface_upload(right_frame, selected_networks, upload_functions)

def interface_upload(right_frame, selected_networks, upload_functions):
    global video_entry, title_entry, description_entry, tags_entry, thumbnail_entry, video_title_entries, video_title_labels

    # Frame dedicado para campos extras
    extra_fields_frame = ctk.CTkFrame(right_frame)
    extra_fields_frame.grid(row=0, column=0, columnspan=3, sticky="ew")

    # Dicionários para campos extras e labels
    video_title_entries = {}
    video_title_labels = {}

    # Mapeamento de redes para campos extras (fácil de expandir)
    extra_fields = {
        "Reddit": {"label": "Título para Reddit", "placeholder": "Título para Reddit"},
        # Adicione aqui outras redes se quiser campos extras
    }

    def update_dynamic_fields_video():
        # Limpa o frame antes de adicionar/remover
        for widget in extra_fields_frame.winfo_children():
            widget.destroy()
        video_title_entries.clear()
        video_title_labels.clear()
        row_idx = 0
        for network, field_info in extra_fields.items():
            if network in selected_networks:
                label = ctk.CTkLabel(extra_fields_frame, text=field_info["label"], font=("Arial", 14, "bold"))
                label.grid(row=row_idx, column=0, padx=10, pady=(10, 0), sticky="w")
                entry = ctk.CTkEntry(extra_fields_frame, placeholder_text=field_info["placeholder"], width=400)
                entry.grid(row=row_idx, column=1, padx=10, pady=(10, 0), sticky="w")
                video_title_labels[network] = label
                video_title_entries[network] = entry
                row_idx += 1
        # Reexecuta a verificação a cada 500ms
        right_frame.after(500, update_dynamic_fields_video)

    update_dynamic_fields_video()

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
        command=lambda: execute_uploads_video(selected_networks, upload_functions)
    ).grid(row=6, column=0, columnspan=2, pady=10)
    
create_menu()