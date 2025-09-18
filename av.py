# media_player.py

import tkinter as tk
from PIL import Image, ImageTk
import sys
has_pygame = True
try:
    import pygame
except ModuleNotFoundError:
    has_pygame = False
import threading
import os
import atexit # Import the atexit module

# --- Configuration ---
FADEOUT_DURATION_MS = 1000

# --- Module Globals ---
# We initialize these to None. They will be set up by the init() function.
main_window = None
image_label = None
channel1 = None
channel2 = None
active_channel = None
current_song_path = None

def init():
    """
    Initializes the media player's components (Pygame and Tkinter).
    This function MUST be called before using other module functions.
    """
    global main_window, image_label, channel1, channel2, active_channel

    print("Initializing media player...")
    
    # --- Setup Tkinter Window ---
    main_window = tk.Tk()
    main_window.title("Hando")
    main_window.geometry("600x600")
    if sys.platform == "win32":
        main_window.wm_attributes("-toolwindow", 1)
    elif sys.platform == "darwin":
        main_window.wm_attributes("-type", "utility")
    image_label = tk.Label(main_window)
    image_label.pack(fill="both", expand=True)

    # --- Setup Pygame Mixer ---
    if has_pygame:
        pygame.init()
        pygame.mixer.init()
        channel1 = pygame.mixer.Channel(0)
        channel2 = pygame.mixer.Channel(1)
        active_channel = channel1
    
    # --- Register the cleanup function to be called on exit ---
    atexit.register(cleanup)
    print("Player ready. Cleanup function registered.")

def cleanup():
    """A cleanup function to be called automatically on script exit."""
    print("Exiting... Shutting down Pygame.")
    if has_pygame:
        pygame.quit()

def _fade_and_switch(filepath):
    """(Internal) Threaded function to handle the song transition."""
    global active_channel, current_song_path

    channel_to_fade = active_channel
    new_active_channel = channel2 if active_channel == channel1 else channel1

    channel_to_fade.fadeout(FADEOUT_DURATION_MS)
    pygame.time.wait(FADEOUT_DURATION_MS)
    channel_to_fade.stop()

    try:
        new_song = pygame.mixer.Sound(filepath)
        new_active_channel.play(new_song, loops=-1)

        active_channel = new_active_channel
        current_song_path = filepath
    except pygame.error as e:
        current_song_path = None

def play_music(filepath):
    """Starts a background thread to play a new song."""
    if not has_pygame:
        return
    global current_song_path
    if filepath == current_song_path:
        #print(f"'{os.path.basename(filepath)}' is already playing.")
        return
    current_song_path = filepath
    transition_thread = threading.Thread(target=_fade_and_switch, args=(filepath,))
    transition_thread.start()

def display_image(path_to_image):
    """Displays an image in the Tkinter window."""
    try:
        window_width = main_window.winfo_width()
        window_height = main_window.winfo_height()
        original_img = Image.open(path_to_image)
        img_width, img_height = original_img.size
        
        scale_ratio = min(window_width / img_width, window_height / img_height)
        new_width = int(img_width * scale_ratio)
        new_height = int(img_height * scale_ratio)
        
        resized_img = original_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(resized_img)
        
        image_label.config(image=img_tk)
        image_label.image = img_tk
        # Update the window to show the new image
        main_window.update()
    except Exception as e:
        print(f"Could not open image. Error: {e}")

if __name__ == "__main__":
    # Initialize the media player once at the start.
    # This sets up Pygame, Tkinter, and registers the atexit cleanup.
    init()

    print("\n--- Console Media Control ---")
    print("Enter a path to an image or an MP3 file. Type 'exit' to quit.")
    
    while True:
        prompt = input("> ").strip()

        if prompt.lower() == 'exit':
            # No need to call cleanup here! atexit handles it.
            break
        
        if not os.path.exists(prompt):
            print(f"Error: File or directory not found at '{prompt}'")
            continue

        if prompt.lower().endswith((".mp3", ".wav", ".ogg")):
            play_music(prompt)
        else:
            display_image(prompt)
            
