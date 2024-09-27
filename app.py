from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import tkinter as tk
from tkinter import messagebox
import platform
import threading

# Definimos la clase que maneja las solicitudes HTTP
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Contenido HTML minimalista con solo un input y un label
            content = '''
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Formulario</title>
            </head>
            <body>
                <form method="POST" action="/">
                    <label for="input-user">Introduce tu nombre de usuario:</label>
                    <input type="text" id="input-user" name="user" required>
                    <label for="input-info">Introduce tu información:</label>
                    <input type="text" id="input-info" name="info" required>
                    <button type="submit">Enviar</button>
                </form>
            </body>
            </html>
            '''
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))

    def do_POST(self):
        # Leer los datos del formulario
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_data = urllib.parse.parse_qs(post_data)

        user = post_data.get('user', [''])[0]
        info = post_data.get('info', [''])[0]

        # Imprimir los datos en la consola
        print(f'Se ha conectado un compañero con la IP: {self.client_address[0]}')

        # Mostrar el mensaje en una ventana de tkinter
        threading.Thread(target=self.show_message, args=(user, info)).start()

        # Responder con un mensaje de confirmación
        response = '''
        <html>
        <h1>Datos recibidos correctamente</h1>
        </html>
        '''
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

    def show_message(self, user, info):
        # Crear una ventana para mostrar el mensaje
        messagebox.showinfo('Mensaje de compañero', f'Mensaje de {user}: {info}')

# Función para iniciar el servidor en un hilo separado
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servidor corriendo en http://localhost:{port}/')
    httpd.serve_forever()

# Crear la interfaz gráfica
def create_gui():
    root = tk.Tk()
    root.configure(bg='yellow')
    root.geometry('660x550')
    root.title('Servidor')

    def start_server():
        # Iniciar el servidor en un hilo separado
        server_thread = threading.Thread(target=run)
        server_thread.start()

    def hardware_info():
        root2 = tk.Tk()
        root2.configure(bg='yellow')
        root2.geometry('660x550')
        label = tk.Label(root2, text=f'Sistema operativo: {platform.system()}', wraplength=400)
        label2 = tk.Label(root2, text=f'Arquitectura: {platform.machine()}', wraplength=400)
        label3 = tk.Label(root2, text=f'CPU: {platform.processor()}', wraplength=200)
        label.grid(row=0, column=0, padx=10, pady=10)
        label2.grid(row=1, column=0, padx=10, pady=10)
        label3.grid(row=2, column=0, padx=10, pady=10)
        root2.mainloop()

    # Botones para la interfaz
    botón = tk.Button(root, text='Hardware', height='2', width='10', command=hardware_info)
    botón.grid(row=0, column=0, padx=10, pady=10)

    botón2 = tk.Button(root, text='Iniciar servidor', height='2', width='25', command=start_server)
    botón2.grid(row=2, column=0, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()