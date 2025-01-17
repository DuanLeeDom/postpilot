import os
import shutil
import sys

def find_chrome_profile():
    # Caminhos padrão onde o Chrome pode estar instalado no Windows
    chrome_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data"),
        os.path.expandvars(r"%APPDATA%\Google\Chrome\User Data")
    ]
    
    # Verifica se o diretório do perfil do Chrome existe
    for path in chrome_paths:
        if os.path.exists(path):
            return path
    return None

def copy_chrome_profile(source_path, destination_path):
    # Verifica se o diretório do perfil Default existe
    default_profile_path = os.path.join(source_path, "Default")
    if os.path.exists(default_profile_path):
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        
        # Copia o perfil Default para o destino
        try:
            shutil.copytree(default_profile_path, os.path.join(destination_path, "Default"))
            print(f"Perfil copiado para {destination_path}")
        except Exception as e:
            print(f"Erro ao copiar o perfil: {e}")
    else:
        print("Perfil padrão do Chrome não encontrado.")

def main():
    # Localiza o diretório do perfil do Chrome
    chrome_profile_path = find_chrome_profile()
    if not chrome_profile_path:
        print("Não foi possível localizar o perfil do Google Chrome.")
        sys.exit(1)

    # Define o diretório de destino para o perfil copiado
    destination_profile_path = os.path.expanduser(r"~\meus_perfis\chrome_profile")

    # Copia o perfil do Chrome
    copy_chrome_profile(chrome_profile_path, destination_profile_path)

if __name__ == "__main__":
    main()