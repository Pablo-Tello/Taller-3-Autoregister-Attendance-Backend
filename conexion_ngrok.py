import ssl
from pyngrok import ngrok
import os
from dotenv import load_dotenv

load_dotenv()

ssl._create_default_https_context = ssl._create_unverified_context

#Iniciando Ngrok
def main():
    token = os.environ.get('NGROK_AUTHTOKEN')
    ngrok.set_auth_token(token)
    public_url = ngrok.connect(8000)
    public_url_str = str(public_url)
    print('URL pública de Ngrok:', public_url_str)
    input('Presiona Enter para detener Ngrok...')
    ngrok.kill()


if __name__ == '__main__':
    main()