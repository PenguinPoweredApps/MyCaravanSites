import tkinter as tk
from tkinter import ttk
import requests
import webbrowser
import pyperclip
import platform
import subprocess


def search_caravan_sites():
    location = location_entry.get()
    api_key = ""

    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"camping and caravan sites near {location}",
        "key": api_key,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        results_listbox.delete(0, tk.END)

        if data["results"]:
            for result in data["results"]:
                name = result["name"]
                address = result["formatted_address"]
                results_listbox.insert(tk.END, f"{name} - {address}")
        else:
            results_listbox.insert(tk.END, "No results found.")
    else:
        results_listbox.insert(tk.END, "Error fetching data.")


def open_map(event):
    selection = results_listbox.curselection()
    if selection:
        index = selection[0]
        item = results_listbox.get(index)
        search_term = item.split(" - ")[0]
        webbrowser.open(f"https://www.google.com/maps/search/{search_term}")


def share_result():
    selection = results_listbox.curselection()
    if selection:
        index = selection[0]
        item = results_listbox.get(index)
        pyperclip.copy(item)

def share_result_via_email():
    selection = results_listbox.curselection()
    if selection:
        index = selection[0]
        item = results_listbox.get(index)
        subject = "Check out this caravan site!"
        body = f"I found this caravan site:\n\n{item}\n\nThought you might be interested!"

        # Determine OS and construct email command
        system = platform.system()
        if system == "Darwin":  # macOS
            email_command = f'open mailto:?subject={subject}&body={body}'
        elif system == "Windows":
            email_command = f'start mailto:?subject={subject}&body={body}'
        else:  # Assuming Linux
            email_command = ["xdg-open", f'mailto:?subject={subject}&body={body}']

        # Open the email client
        subprocess.run(email_command, shell=(system != "Linux"))  # Shell only for macOS and Windows

window = tk.Tk()
window.title("Find My Caravan Site")

location_label = ttk.Label(window, text="Location:")
location_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

location_entry = ttk.Entry(window, width=50)
location_entry.grid(row=0, column=1, padx=5, pady=5)

search_button = ttk.Button(window, text="Search", command=search_caravan_sites)
search_button.grid(row=0, column=2, padx=5, pady=5)

share_button = ttk.Button(window, text="Share", command=share_result)
share_button.grid(row=0, column=3, padx=5, pady=5)

share_email_button = ttk.Button(window, text="Share via Email", command=share_result_via_email)
share_email_button.grid(row=0, column=4, padx=5, pady=5)

results_listbox = tk.Listbox(window, width=100, height=15)  # Increased width for the extra button
results_listbox.grid(row=1, column=0, columnspan=5, padx=5, pady=5)  # Span to cover all buttons
results_listbox.bind("<Double-Button-1>", open_map)

window.mainloop()
