import tkinter as tk
from tkinter import messagebox
import platform
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

# Variable global para almacenar el último mensaje enviado
global_message = "No hay mensajes nuevos."

# Clase para manejar los mensajes en la interfaz gráfica
class MessageHandler:
    def enviarrr(self, mensaje):
        global global_message
        global_message = mensaje  # Actualizamos el mensaje global
        print(f"Nuevo mensaje a cliente: {mensaje}")

# Definimos la clase que maneja las solicitudes HTTP
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Contenido HTML que incluye el mensaje actualizado
            content = f'''
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Formulario</title>
            </head>
            <body>
                <h1>Mensajes recibidos: {global_message}</h1>
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
            self.send_header('Content-Type', 'text/html; charset=utf-8')  # Aseguramos que el navegador lo interprete como UTF-8
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))  # Codificamos siempre en UTF-8 para evitar problemas con caracteres especiales

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')  # Decodificamos correctamente el contenido como UTF-8
        post_data = urllib.parse.parse_qs(post_data)

        user = post_data.get('user', [''])[0]
        info = post_data.get('info', [''])[0]

        print(f'Se ha conectado un compañero con la IP: {self.client_address[0]}')

        # Ejecutamos el proceso de mostrar mensaje en un hilo separado
        threading.Thread(target=self.show_message, args=(user, info)).start()

        # Respuesta al cliente
        response = f'''
        <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Formulario</title>
            </head>
            <body>
                <h1>Mensajes recibidos: {global_message}</h1>
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
        self.send_header('Content-Type', 'text/html; charset=utf-8')  # Encabezado para UTF-8
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))  # Enviamos respuesta codificada en UTF-8

    def show_message(self, user, info):
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
        server_thread = threading.Thread(target=run)
        server_thread.start()

    def hardware_info():
        root2 = tk.Tk()
        root2.configure(bg='yellow')
        root2.geometry('660x550')
        root2.title('Información Hardware')
        label = tk.Label(root2, text=f'Sistema operativo: {platform.system()}', wraplength=400)
        label2 = tk.Label(root2, text=f'Arquitectura: {platform.machine()}', wraplength=400)
        label3 = tk.Label(root2, text=f'CPU: {platform.processor()}', wraplength=200)
        label.grid(row=0, column=0, padx=10, pady=10)
        label2.grid(row=1, column=0, padx=10, pady=10)
        label3.grid(row=2, column=0, padx=10, pady=10)
        root2.mainloop()

    def enviar_mensaje_a_cliente():
        root3 = tk.Tk()
        root3.configure(bg='yellow')
        root3.geometry('660x550')
        root3.title('Enviar mensaje a cliente')

        message_handler = MessageHandler()

        texto = tk.Text(root3, height='2', width='25')
        texto.grid(row=0, column=0, padx=10, pady=10)

        def enviar_mensaje():
            mensaje = texto.get('1.0', 'end-1c')
            message_handler.enviarrr(mensaje)  # Llamar al método enviarrr de MessageHandler

        tk.Button(root3, text='Enviar mensaje', height='2', width='25', command=enviar_mensaje).grid(row=1, padx=10, pady=10)

    # Botones para la interfaz
    tk.Button(root, text='Hardware', height='2', width='10', command=hardware_info).grid(row=0, column=0, padx=10, pady=10)
    tk.Button(root, text='Iniciar servidor', height='2', width='25', command=start_server).grid(row=2, column=0, padx=10, pady=10)
    tk.Button(root, text='Enviar mensaje', height='2', width='25', command=enviar_mensaje_a_cliente).grid(row=3, column=0, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
