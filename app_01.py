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
        input_title[0].send_keys(title)  # Envia o novo título

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

def create_interface():
    ctk.set_appearance_mode("System")  # Modo de aparência (System, Light, Dark)
    ctk.set_default_color_theme("blue")  # Tema de cor padrão

    root = ctk.CTk()
    root.title("YouTube Video Uploader")
    root.geometry("900x400")    

    # Caminho do URL de upload salvo
    ctk.CTkLabel(root, text="URL Upload:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    url_upload = ctk.CTkEntry(root, width=400)
    url_upload.grid(row=0, column=1, padx=10, pady=5)

    # Caminho do vídeo
    ctk.CTkLabel(root, text="Caminho do Vídeo:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    video_entry = ctk.CTkEntry(root, width=400)
    video_entry.grid(row=1, column=1, padx=10, pady=5)
    ctk.CTkButton(root, text="Selecionar", command=lambda: select_file(video_entry)).grid(row=1, column=2, padx=10, pady=5)

    # Título do vídeo
    ctk.CTkLabel(root, text="Título:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    title_entry = ctk.CTkEntry(root, width=400)
    title_entry.grid(row=2, column=1, padx=10, pady=5)

    # Descrição do vídeo
    ctk.CTkLabel(root, text="Descrição:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    description_entry = ctk.CTkEntry(root, width=400)
    description_entry.grid(row=3, column=1, padx=10, pady=5)

    # Caminho da miniatura
    ctk.CTkLabel(root, text="Caminho da Miniatura:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    thumbnail_entry = ctk.CTkEntry(root, width=400)
    thumbnail_entry.grid(row=4, column=1, padx=10, pady=5)
    ctk.CTkButton(root, text="Selecionar", command=lambda: select_file(thumbnail_entry)).grid(row=4, column=2, padx=10, pady=5)

    # Botão de iniciar
    ctk.CTkButton(root, text="Iniciar Upload", command=lambda: start_upload(url_upload.get(),
        video_entry.get(), title_entry.get(), description_entry.get(), thumbnail_entry.get()
    )).grid(row=5, column=0, columnspan=3, pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_interface()