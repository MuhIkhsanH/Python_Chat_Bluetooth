import serial
import threading
import time
import sys
from colorama import init, Fore, Style

# Inisialisasi colorama
init()

ser = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)

prompt = "Anda: "

def terima_data():
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            if data:
                # Hapus baris input sementara
                sys.stdout.write('\r' + ' ' * (len(prompt) + 100) + '\r')
                sys.stdout.flush()
                
                # Tampilkan dalam warna hijau
                print(f"{Fore.GREEN}Bluetooth: {data}{Style.RESET_ALL}")
                
                # Kembalikan prompt input
                sys.stdout.write(prompt)
                sys.stdout.flush()

def kirim_data():
    while True:
        try:
            sys.stdout.write(prompt)
            sys.stdout.flush()
            msg = input()
            if msg.lower() == 'exit':
                print("Menghentikan program...")
                ser.close()
                break
            ser.write((msg + '\n').encode('utf-8'))
        except Exception as e:
            print("Error saat mengirim:", e)

thread_terima = threading.Thread(target=terima_data, daemon=True)
thread_kirim = threading.Thread(target=kirim_data)

thread_terima.start()
thread_kirim.start()

thread_kirim.join()
