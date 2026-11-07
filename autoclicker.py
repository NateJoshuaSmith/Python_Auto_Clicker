import threading, time
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Listener, Key, Controller as KeyboardController

CLICK_DELAY = 90     # seconds before each click (1 min 30 sec)
ENTER_DELAY = 1      # seconds after the click before Enter
BUTTON = Button.left
TOGGLE = Key.f6      # start/pause
QUIT = Key.f7        # exit

mouse = MouseController()
keyboard = KeyboardController()
running = False

def wait(seconds):
    end = time.time() + seconds
    while time.time() < end:
        if not running:
            return False
        time.sleep(0.1)
    return True

def worker():
    while True:
        if running:
            if not wait(CLICK_DELAY):
                continue
            mouse.click(BUTTON)
            print("Clicked")
            if not wait(ENTER_DELAY):
                continue
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            print("Enter pressed")
        else:
            time.sleep(0.1)

def on_press(key):
    global running
    if key == TOGGLE:
        running = not running
        print("Running" if running else "Paused")
    elif key == QUIT:
        return False

if __name__ == "__main__":
    print(f"Ready. Press {TOGGLE} to start or pause, {QUIT} to quit.")
    threading.Thread(target=worker, daemon=True).start()
    with Listener(on_press=on_press) as listener:
        listener.join()
