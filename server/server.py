import socket
import threading
import mss
import pickle
import pyautogui
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController

HOST = '0.0.0.0'  # biarkan server menerima koneksi dari IP manapun
PORT = 9001

mouse = MouseController()
keyboard = KeyboardController()

def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        return sct_img.rgb, sct_img.size

def handle_client(conn):
    print("[*] Klien terhubung.")
    while True:
        try:
            img_data, size = capture_screen()
            conn.sendall(pickle.dumps((img_data, size)))

            # terima perintah kontrol
            data = conn.recv(1024)
            if not data:
                break
            command = pickle.loads(data)

            if command['type'] == 'mouse_move':
                mouse.position = command['pos']
            elif command['type'] == 'click':
                pyautogui.click()
            elif command['type'] == 'key':
                keyboard.type(command['key'])

        except Exception as e:
            print(f"[*] Koneksi terputus: {e}")
            break
    conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"[*] Menunggu koneksi di {HOST}:{PORT}")
        conn, _ = s.accept()
        handle_client(conn)

if __name__ == "__main__":
    start_server()
