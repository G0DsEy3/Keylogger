
"""
Safe example: Tkinter app that records keypresses only when the app is focused.
Do NOT use this to capture keys from other apps or people without consent.

Run: python3 tk_keylogger_safe.py
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import os

LOG_FILENAME = "app_key_log.txt"

def ask_consent():
    msg = (
        "This application will record keypresses only while this window is focused.\n\n"
        "Logs will be saved to: {}\n\n"
        "Do you consent to recording your keystrokes while this app is active?"
    ).format(os.path.abspath(LOG_FILENAME))
    return messagebox.askyesno("Consent required", msg)

def on_key(event):
    # Only log if consent_granted is True (set at start)
    if not app.consent_granted:
        return

    # event.keysym is the key symbol (e.g., 'a', 'Return', 'Shift_L')
    # event.char is the character when available
    timestamp = datetime.utcnow().isoformat() + "Z"
    line = f"{timestamp}\tkeysym={event.keysym}\tchar={repr(event.char)}\n"
    with open(LOG_FILENAME, "a", encoding="utf-8") as f:
        f.write(line)

    # Show current key briefly in the UI for feedback
    status_var.set(f"Last key: {event.keysym}   (logged)")

def clear_log():
    if messagebox.askyesno("Clear log", "Delete the current log file?"):
        try:
            os.remove(LOG_FILENAME)
        except FileNotFoundError:
            pass
        status_var.set("Log cleared.")

def show_log():
    try:
        with open(LOG_FILENAME, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        content = "(log file not found)"
    # show in a simple scrollable window
    w = tk.Toplevel(root)
    w.title("Log contents")
    text = tk.Text(w, wrap="none", width=80, height=25)
    text.insert("1.0", content)
    text.config(state="disabled")
    text.pack(fill="both", expand=True)

# Build UI
root = tk.Tk()
root.title("Safe Key Capture Demo")

frame = tk.Frame(root, padx=12, pady=12)
frame.pack(fill="both", expand=True)

app = simpledialog.SimpleNamespace()
app.consent_granted = False

consent = ask_consent()
if not consent:
    messagebox.showinfo("Consent required", "Cannot proceed without consent. Exiting.")
    root.destroy()
    raise SystemExit("User did not give consent.")

app.consent_granted = True

label = tk.Label(frame, text="Focus this window and type — keypresses will be logged while focused.")
label.pack(pady=(0,8))

status_var = tk.StringVar(value="Waiting for keystrokes...")
status = tk.Label(frame, textvariable=status_var, anchor="w")
status.pack(fill="x")

btn_frame = tk.Frame(frame)
btn_frame.pack(pady=(8,0))

clear_btn = tk.Button(btn_frame, text="Clear log", command=clear_log)
clear_btn.grid(row=0, column=0, padx=6)

show_btn = tk.Button(btn_frame, text="Show log", command=show_log)
show_btn.grid(row=0, column=1, padx=6)

exit_btn = tk.Button(btn_frame, text="Exit", command=root.destroy)
exit_btn.grid(row=0, column=2, padx=6)

# Bind key events for the root window. This only catches keys while the app has keyboard focus.
root.bind_all("<Key>", on_key)

# Ensure the log file exists and add a header entry
with open(LOG_FILENAME, "a", encoding="utf-8") as f:
    f.write(f"--- Started logging at {datetime.utcnow().isoformat()}Z (consent given) ---\n")

root.mainloop()
