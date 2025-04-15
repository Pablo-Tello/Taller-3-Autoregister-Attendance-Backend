import os
import subprocess
import sys
import time
import signal
import re
from dotenv import load_dotenv

load_dotenv()

def extract_url(output):
    """Extrae la URL de ngrok del output de la línea de comandos"""
    # Buscar URLs que comiencen con http o https
    urls = re.findall(r'https?://[^\s]+', output)
    for url in urls:
        if 'ngrok' in url:
            return url
    return None

def main():
    # Verificar si ngrok está instalado
    try:
        # Verificar la versión de ngrok
        version_output = subprocess.check_output(['ngrok', 'version'], text=True)
        print(f"Versión de ngrok: {version_output.strip()}")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Error: ngrok no está instalado o no está en el PATH.")
        print("Por favor, instala ngrok desde https://ngrok.com/download")
        return

    # Obtener el token de autenticación
    token = os.environ.get('NGROK_AUTHTOKEN')
    
    # Iniciar ngrok
    try:
        cmd = ['ngrok', 'http', '8000']
        
        # Iniciar el proceso
        print("Iniciando ngrok...")
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Esperar un momento para que ngrok se inicie
        time.sleep(3)
        
        # Obtener la URL de ngrok
        try:
            # Usar el comando 'ngrok status' para obtener la URL
            status_output = subprocess.check_output(['ngrok', 'status'], text=True)
            url = extract_url(status_output)
            
            if url:
                print(f"\nURL pública de Ngrok: {url}")
                print('\nIMPORTANTE: Abre esta URL en tu navegador y acepta la advertencia una vez.')
                print('Luego, tu frontend podrá hacer solicitudes a esta URL sin problemas.')
                print('\nPara evitar la advertencia en solicitudes programáticas, usa esta URL en tu frontend:')
                print(f'{url}?skip_browser_warning=true')
            else:
                print("No se pudo obtener la URL de ngrok. Verifica manualmente en http://localhost:4040")
        except subprocess.SubprocessError:
            print("No se pudo obtener el estado de ngrok. Verifica manualmente en http://localhost:4040")
        
        print("\nPresiona Ctrl+C para detener ngrok...")
        
        # Mantener el proceso en ejecución hasta que el usuario lo detenga
        process.wait()
        
    except KeyboardInterrupt:
        print("\nDeteniendo ngrok...")
        process.terminate()
        process.wait()
        print("ngrok detenido.")
    except Exception as e:
        print(f"Error al ejecutar ngrok: {e}")

if __name__ == "__main__":
    main()
