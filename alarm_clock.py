import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import time
import threading
import os
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Global variables
alarms = []
current_tone_path = "tones/alarm.mp3"  # Default alarm tone path

def play_alarm():
    global current_tone_path
    try:
        pygame.mixer.music.load(current_tone_path)
        pygame.mixer.music.play()
    except:
        messagebox.showerror("Error", "Unable to play alarm tone.")

def check_alarms():
    while True:
        now = datetime.now().strftime("%H:%M")
        for alarm in alarms:
            if alarm['time'] == now and alarm['enabled']:
                show_alarm_popup(alarm)
                time.sleep(60)  # Wait for a minute to avoid duplicate popups
        time.sleep(1)

def show_alarm_popup(alarm):
    popup = tk.Toplevel(root)
    popup.title("Alarm!")
    popup.geometry("300x150")
    popup.configure(bg="#ffeecc")
    
    tk.Label(popup, text="⏰ Alarm Ringing!", font=("Helvetica", 16), bg="#ffeecc").pack(pady=10)

    # Play alarm sound
    play_alarm()

    def snooze():
        popup.destroy()
        pygame.mixer.music.stop()
        snooze_time = datetime.strptime(alarm["time"], "%H:%M")
        snooze_time = (snooze_time.timestamp() + 300)  # 5 minutes
        alarm["time"] = time.strftime("%H:%M", time.localtime(snooze_time))
        alarm["enabled"] = True

    def dismiss():
        alarm["enabled"] = False
        pygame.mixer.music.stop()
        popup.destroy()

    tk.Button(popup, text="Snooze", command=snooze, width=10).pack(pady=5)
    tk.Button(popup, text="Dismiss", command=dismiss, width=10).pack()

def add_alarm():
    hour = hour_var.get()
    minute = minute_var.get()
    time_str = f"{hour.zfill(2)}:{minute.zfill(2)}"
    alarms.append({"time": time_str, "enabled": True})
    update_alarm_list()

def toggle_alarm(index):
    alarms[index]["enabled"] = not alarms[index]["enabled"]
    update_alarm_list()

def delete_alarm(index):
    alarms.pop(index)
    update_alarm_list()

def update_alarm_list():
    for widget in alarm_list_frame.winfo_children():
        widget.destroy()
    for i, alarm in enumerate(alarms):
        frame = tk.Frame(alarm_list_frame, bg="white")
        frame.pack(fill="x", pady=2)

        tk.Label(frame, text=alarm["time"], width=10, bg="white").pack(side="left", padx=5)
        tk.Checkbutton(frame, text="On", command=lambda i=i: toggle_alarm(i),
                       variable=tk.BooleanVar(value=alarm["enabled"]),
                       bg="white").pack(side="left")
        tk.Button(frame, text="Delete", command=lambda i=i: delete_alarm(i)).pack(side="right")

def choose_tone():
    global current_tone_path
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    if file_path:
        current_tone_path = file_path
        tone_label.config(text=f"Selected: {os.path.basename(current_tone_path)}")

def update_clock():
    now = datetime.now()
    current_time.set(now.strftime("%H:%M:%S"))
    current_date.set(now.strftime("%A, %d %B %Y"))
    root.after(1000, update_clock)

# GUI Setup
root = tk.Tk()
root.title("Alarm Clock")
root.geometry("400x600")
root.config(bg="white")

current_time = tk.StringVar()
current_date = tk.StringVar()

tk.Label(root, textvariable=current_time, font=("Helvetica", 28), bg="white").pack(pady=10)
tk.Label(root, textvariable=current_date, font=("Helvetica", 12), bg="white").pack(pady=5)

tk.Label(root, text="Set Alarm", font=("Helvetica", 16), bg="white").pack(pady=10)
time_picker_frame = tk.Frame(root, bg="white")
time_picker_frame.pack(pady=5)

hour_var = tk.StringVar(value="07")
minute_var = tk.StringVar(value="00")

ttk.Spinbox(time_picker_frame, from_=0, to=23, textvariable=hour_var, width=5, format="%02.0f").pack(side="left", padx=5)
ttk.Spinbox(time_picker_frame, from_=0, to=59, textvariable=minute_var, width=5, format="%02.0f").pack(side="left", padx=5)

tk.Button(root, text="Add Alarm", command=add_alarm).pack(pady=5)

tk.Label(root, text="Alarm Tone", font=("Helvetica", 14), bg="white").pack(pady=5)
tone_label = tk.Label(root, text="Default: alarm.mp3", bg="white")
tone_label.pack()
tk.Button(root, text="Choose Tone", command=choose_tone).pack(pady=5)

tk.Label(root, text="Alarms", font=("Helvetica", 14), bg="white").pack(pady=10)
alarm_list_frame = tk.Frame(root, bg="white")
alarm_list_frame.pack(fill="both", expand=True)

# Start background processes
threading.Thread(target=check_alarms, daemon=True).start()
update_clock()

root.mainloop()
