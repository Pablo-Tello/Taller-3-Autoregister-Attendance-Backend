import ssl
from pyngrok import ngrok, conf
import os
from dotenv import load_dotenv

load_dotenv()

ssl._create_default_https_context = ssl._create_unverified_context

# Iniciando Ngrok
def main():
    # Obtener el token de autenticación
    token = os.environ.get('NGROK_AUTHTOKEN')
    if token:
        ngrok.set_auth_token(token)
    
    # Configurar ngrok
    pyngrok_config = conf.PyngrokConfig()
    
    # Iniciar el túnel
    try:
        # Intentar primero con http
        public_url = ngrok.connect(8000, "http", pyngrok_config=pyngrok_config)
        public_url_str = str(public_url)
        
        print('URL pública de Ngrok:', public_url_str)
        print('\nIMPORTANTE: Abre esta URL en tu navegador y acepta la advertencia una vez.')
        print('Luego, tu frontend podrá hacer solicitudes a esta URL sin problemas.')
        print('\nPara evitar la advertencia en solicitudes programáticas, usa esta URL en tu frontend:')
        print(f'{public_url_str}?skip_browser_warning=true')
        
        input('\nPresiona Enter para detener Ngrok...')
    except Exception as e:
        print(f"Error al iniciar ngrok: {e}")
    finally:
        # Asegurarse de que ngrok se cierre correctamente
        ngrok.kill()

if __name__ == '__main__':
    main()
