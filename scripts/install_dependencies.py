import subprocess
import sys
import os

def install_python_dependencies():
    """Instala as dependências do Python"""
    print("Instalando as dependências do Python...")
    dependencies = [
        "selenium",
        "webdriver-manager",
        "customtkinter",
        "tkcalendar",
        "Pillow",
        "psutil"
    ]
    for dep in dependencies:
        subprocess.check_call([sys.executable, "-m", "pip", "install", dep])

def check_chrome_installed():
    """Verifica se o Google Chrome está instalado"""
    try:
        subprocess.check_call(["google-chrome", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Google Chrome já está instalado.")
        return True
    except subprocess.CalledProcessError:
        print("Google Chrome não encontrado.")
        return False

def install_chrome():
    """Instala o Google Chrome, se não estiver instalado"""
    print("Iniciando a instalação do Google Chrome...")
    try:
        subprocess.check_call(["sudo", "apt-get", "update"])  # Atualiza os repositórios
        subprocess.check_call(["sudo", "apt-get", "install", "-y", "google-chrome-stable"])  # Instala o Chrome
        print("Google Chrome foi instalado com sucesso!")
    except subprocess.CalledProcessError:
        print("Erro ao tentar instalar o Google Chrome. Verifique sua conexão com a internet ou permissões do sistema.")

def install_chromedriver():
    """Instala o ChromeDriver usando o webdriver-manager"""
    print("Instalando o ChromeDriver...")
    subprocess.check_call([sys.executable, "-m", "webdriver_manager.chrome"])

def main():
    """Função principal para instalar todas as dependências"""
    install_python_dependencies()
    
    if not check_chrome_installed():
        install_chrome()  # Só tenta instalar o Chrome se não estiver instalado

    install_chromedriver()  # Instala o ChromeDriver
    
    print("Todas as dependências foram instaladas com sucesso!")

if __name__ == "__main__":
    main()