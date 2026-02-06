from pynput import keyboard
import time
import threading

LOG_FILE = "key_log.txt"
start_time = None
key_count = 0
running = True


def banner():
    print("=" * 50)
    print(" Interactive Keyboard Logger (Educational Use)")
    print("=" * 50)
    print("• Keys will be shown on screen")
    print("• Keys will be saved to:", LOG_FILE)
    print("• Press ESC anytime to stop logging")
    print("=" * 50)
    print()


def on_press(key):
    global key_count

    try:
        char = key.char
    except AttributeError:
        char = f"[{key.name.upper()}]"

    # Show live keystrokes
    print(char, end='', flush=True)

    # Write to file
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        if key == keyboard.Key.space:
            f.write(" ")
        elif key == keyboard.Key.enter:
            f.write("\n")
        else:
            f.write(char)

    key_count += 1


def on_release(key):
    global running
    if key == keyboard.Key.esc:
        running = False
        print("\n\n🛑 Logger stopped by user (ESC pressed)")
        return False


def session_timer():
    while running:
        time.sleep(1)


def summary():
    duration = int(time.time() - start_time)
    print("\n" + "-" * 40)
    print(" Session Summary")
    print("-" * 40)
    print(f"• Total keys captured : {key_count}")
    print(f"• Session duration    : {duration} seconds")
    print(f"• Log file saved as   : {LOG_FILE}")
    print("-" * 40)


# -------- MAIN PROGRAM --------
banner()
input("Press ENTER to start logging...")

start_time = time.time()

timer_thread = threading.Thread(target=session_timer)
timer_thread.daemon = True
timer_thread.start()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

summary()