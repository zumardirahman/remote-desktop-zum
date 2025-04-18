import socket
import pickle
from PIL import Image
import io
import tkinter as tk
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyListener

HOST = '192.168.x.x'  # ganti dengan IP server (komputer yang dikendalikan)
PORT = 9001

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

root = tk.Tk()
label = tk.Label(root)
label.pack()

def update_screen():
    data = b''
    while True:
        try:
            part = sock.recv(4096)
            if not part:
                break
            data += part
            if data.endswith(b'END'):
                break
        except:
            break
    try:
        img_data, size = pickle.loads(data)
        img = Image.frombytes('RGB', size, img_data)
        img = img.resize((800, 500))
        photo = tk.PhotoImage(img)
        label.config(image=photo)
        label.image = photo
    except:
        pass
    root.after(100, update_screen)

def send_control(command):
    try:
        sock.sendall(pickle.dumps(command))
    except:
        pass

def on_click(x, y, button, pressed):
    if pressed:
        send_control({'type': 'click'})
    send_control({'type': 'mouse_move', 'pos': (x, y)})

def on_press(key):
    try:
        send_control({'type': 'key', 'key': key.char})
    except:
        pass

update_screen()
MouseListener(on_click=on_click).start()
KeyListener(on_press=on_press).start()
root.mainloop()
