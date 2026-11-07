import random, threading, time
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import GlobalHotKeys, Key, Controller as KeyboardController

CLICK_DELAYS = [50, 60, 70, 80, 90]  # seconds; one is picked at random before each click
COUNTDOWN_STEP = 10  # print how long is left every this many seconds
ENTER_DELAY = 1      # seconds after the click before Enter
BUTTON = Button.left
TOGGLE = "<ctrl>+<alt>+s"   # start/pause
QUIT = "<ctrl>+<alt>+q"     # exit

mouse = MouseController()
keyboard = KeyboardController()
running = False

def wait(seconds, countdown=False):
    end = time.time() + seconds
    next_report = seconds - COUNTDOWN_STEP
    while time.time() < end:
        if not running:
            return False
        left = end - time.time()
        if countdown and next_report > 0 and left <= next_report:
            print(f"{next_report} seconds left...", flush=True)
            next_report -= COUNTDOWN_STEP
        time.sleep(0.1)
    return True

def worker():
    while True:
        if running:
            delay = random.choice(CLICK_DELAYS)
            print(f"Waiting {delay} seconds before clicking...", flush=True)
            if not wait(delay, countdown=True):
                continue
            mouse.click(BUTTON)
            print("Clicked", flush=True)
            if not wait(ENTER_DELAY):
                continue
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            print("Enter pressed", flush=True)
        else:
            time.sleep(0.1)

def toggle():
    global running
    running = not running
    print("Running" if running else "Paused", flush=True)

def quit_program():
    print("Quitting", flush=True)
    hotkeys.stop()

if __name__ == "__main__":
    print("Ready. Press Ctrl+Alt+S to start or pause, Ctrl+Alt+Q to quit.", flush=True)
    threading.Thread(target=worker, daemon=True).start()
    with GlobalHotKeys({TOGGLE: toggle, QUIT: quit_program}) as hotkeys:
        hotkeys.join()
