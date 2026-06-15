import tkinter as tk
from tkinter import messagebox, ttk
import firewall_core as fw

fw.load_rules()

# ------------------------- GUI START -------------------------

root = tk.Tk()
root.title("Python Personal Firewall")
root.geometry("600x600")
root.configure(bg="#1e1e1e")

title = tk.Label(root, text="🔥 Python Personal Firewall", 
                 fg="white", bg="#1e1e1e", font=("Arial", 20, "bold"))
title.pack(pady=10)

# ------------------------- MODE SWITCH -------------------------

mode_frame = tk.Frame(root, bg="#1e1e1e")
mode_frame.pack(pady=10)

tk.Label(mode_frame, text="Firewall Mode:", fg="white", bg="#1e1e1e",
         font=("Arial", 12)).grid(row=0, column=0, padx=10)

mode_var = tk.StringVar(value=fw.rules["mode"])

mode_menu = ttk.Combobox(mode_frame, textvariable=mode_var,
                         values=["allow", "block"], state="readonly", width=10)
mode_menu.grid(row=0, column=1)


def change_mode():
    fw.set_mode(mode_var.get())
    messagebox.showinfo("Mode Changed", f"Mode set to: {mode_var.get()}")


tk.Button(mode_frame, text="Apply", command=change_mode).grid(row=0, column=2, padx=10)


# -------------------------- IP MANAGEMENT -------------------------

ip_frame = tk.Frame(root, bg="#1e1e1e")
ip_frame.pack(pady=10)

tk.Label(ip_frame, text="IP Address:", fg="white", bg="#1e1e1e",
         font=("Arial", 12)).grid(row=0, column=0, padx=5)

ip_entry = tk.Entry(ip_frame, width=20)
ip_entry.grid(row=0, column=1, padx=5)


def add_ip():
    ip = ip_entry.get()
    if fw.add_ip(ip):
        refresh_list()
        messagebox.showinfo("Added", f"IP Added: {ip}")
    else:
        messagebox.showerror("Error", "IP already exists")


def remove_ip():
    ip = ip_entry.get()
    if fw.remove_ip(ip):
        refresh_list()
        messagebox.showinfo("Removed", f"IP Removed: {ip}")
    else:
        messagebox.showerror("Error", "IP not found")


tk.Button(ip_frame, text="Add", width=10, command=add_ip).grid(row=0, column=2, padx=5)
tk.Button(ip_frame, text="Remove", width=10, command=remove_ip).grid(row=0, column=3, padx=5)


# --------------------------- IP LIST DISPLAY --------------------------

ip_listbox = tk.Listbox(root, width=50, height=10)
ip_listbox.pack(pady=10)


def refresh_list():
    ip_listbox.delete(0, tk.END)
    for ip in fw.rules["ips"]:
        ip_listbox.insert(tk.END, ip)


refresh_list()


# --------------------------- FIREWALL CONTROL --------------------------

btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=20)


def start_fw():
    fw.start_firewall()
    messagebox.showinfo("Started", "Firewall started")


def stop_fw():
    fw.stop_firewall()
    messagebox.showinfo("Stopped", "Firewall stopped")


tk.Button(btn_frame, text="Start Firewall", width=20, command=start_fw).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Stop Firewall", width=20, command=stop_fw).grid(row=0, column=1, padx=10)


# --------------------------- LOG VIEWER --------------------------

def view_logs():
    try:
        with open("logs.txt", "r") as f:
            data = f.read()
    except:
        data = "No logs found."

    log_win = tk.Toplevel(root)
    log_win.title("Firewall Logs")
    log_win.geometry("500x500")

    txt = tk.Text(log_win)
    txt.pack(fill="both", expand=True)
    txt.insert(tk.END, data)


tk.Button(root, text="View Logs", width=20, command=view_logs).pack(pady=10)


root.mainloop()
