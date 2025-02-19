# PostPilot

**PostPilot** é uma ferramenta de automação para postagem em múltiplas redes sociais, com foco em plataformas que suportam vídeos longos, como YouTube, TikTok, e muito mais. O objetivo do projeto é simplificar o processo de upload e gestão de conteúdos em várias plataformas, otimizando tempo e recursos.

<img src="https://github.com/user-attachments/assets/06a118ca-19dc-48a0-894e-2ff03de5921a" alt="Image" width="500">
<img src="https://github.com/user-attachments/assets/60759558-a698-488f-8c18-6d0ed1517428" alt="Image" width="500">
<img src="https://github.com/user-attachments/assets/fe860dfb-0946-438b-b00b-673c39af2c36" alt="Image" width="500">
<img src="https://github.com/user-attachments/assets/3ef38e1e-08de-412d-9de8-fe8e2a5df9f6" alt="Image" width="500">

## 🚧 Estado do Projeto

O PostPilot está em sua **versão 1.0.0-beta**, o que significa que ainda está em desenvolvimento. A interface gráfica e as funcionalidades de automação não estão completamente consolidadas e podem apresentar limitações. Contribuições são bem-vindas para melhorar o projeto e torná-lo mais estável e funcional.

## 📋 Funcionalidades Atuais

- Upload automático de vídeos para plataformas suportadas.
- Seleção de título, descrição, e miniatura para os vídeos.
- Integração com navegadores utilizando Selenium.
- Uso de perfis específicos no Chrome para manter o login e personalizações.
- Interface inicial construída com `customtkinter`.

## 🛠️ Instalação e Configuração

Antes de usar o PostPilot, siga as instruções descritas no arquivo `info.txt`. Ele inclui todos os passos necessários para instalar as dependências e configurar o ambiente.

1. **Instale as dependências necessárias** com o script `install_dependencies.py`. Este script:
   ```bash
   python install_dependencies.py
   ```
   - Instala bibliotecas Python como `selenium`, `customtkinter`, `tkcalendar`, e `Pillow`.
   - Verifica se o Google Chrome está instalado e, caso necessário, realiza a instalação.
   - Garante que o ChromeDriver está configurado corretamente para o Selenium.

3. Após a configuração, você pode iniciar o PostPilot executando o arquivo principal:
   ```bash
   python login.py
   ```

4. Certifique-se de personalizar os caminhos e parâmetros no código Python antes de executar.

## 🐾 Contribuindo

Adoramos contribuições da comunidade! Se você tiver ideias ou melhorias para o PostPilot:
- Faça um fork do repositório.
- Crie um branch para as suas alterações: `git checkout -b minha-feature`.
- Envie suas alterações com um pull request.

> Este projeto é **gratuito e open source**, mas não pode ser usado para fins comerciais. Por favor, leia o arquivo LICENSE para mais detalhes.

## 📄 Licença

O PostPilot está licenciado sob a **[MIT License](LICENSE)**. Isso significa que você é livre para usar, modificar e compartilhar, mas lembre-se de dar os devidos créditos.

## 🐱 Sobre o Projeto

PostPilot foi inspirado na praticidade e eficiência que um gato traz para nossas vidas. Simples, ágil e sempre no controle. Esperamos que o PostPilot seja tão confiável e útil quanto o melhor amigo felino.
