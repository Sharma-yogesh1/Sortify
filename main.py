import os
import re
import shutil
import json
import pandas as pd
import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox, Text, Scrollbar, Button, Label, Entry, END, StringVar, BooleanVar,simpledialog
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Frame, Checkbutton, Notebook, Combobox
from tabulate import tabulate

# === App Initialization ===
root = tk.Tk()
root.title("Sortify")
root.geometry("1200x700")

# === Style Configuration ===
style = Style("flatly")  # Default theme is Light Mode
root = style.master
is_dark_mode = BooleanVar(value=False)  # Track the current theme mode


# Dynamic background color for the main window
def update_background():
    if is_dark_mode.get():
        root.configure(bg="#2b2b2b")  # Dark gray background for dark mode
    else:
        root.configure(bg="#f8f9fa")  # Light background (default for light mode)

# Dynamic tab color and font adjustment
def update_tab_style():
    if is_dark_mode.get():
        style.configure("TNotebook.Tab", font=("Arial", 10, "normal"))  # Normal font for dark mode
    else:
        style.configure("TNotebook.Tab", font=("Arial", 10, "bold"))  # Bold font for light mode

# === Notebook ===
notebook = Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

# === Theme Toggle Functionality ===
def toggle_theme():
    if is_dark_mode.get():  # Switch to Dark Mode
        style.theme_use("darkly")
        theme_toggle_btn.config(
            text="🌙 Switch to Light Mode", bg="#4f4f4f", fg="#ffffff",
            activebackground="#434343", activeforeground="#ffffff"
        )
        update_background()  # Update background for dark mode
        update_tab_style()  # Update tab colors and font for dark mode
    else:  # Switch to Light Mode
        style.theme_use("flatly")
        theme_toggle_btn.config(
            text="☀️ Switch to Dark Mode", bg="#e0e0e0", fg="#000000",
            activebackground="#d6d6d6", activeforeground="#000000"
        )
        update_background()  # Update background for light mode
        update_tab_style()  # Update tab colors and font for light mode
    # Reapply accent color after theme change
    apply_accent_color()


# === Theme Toggle Button ===
theme_toggle_btn = Button(
    root,
    text="☀️ Switch to Dark Mode",
    command=lambda: [is_dark_mode.set(not is_dark_mode.get()), toggle_theme()],
    bg="#e0e0e0",
    fg="#000000",
    padx=10,
    pady=5,
    activebackground="#d6d6d6",
    activeforeground="#000000",
    relief="flat",
    font=("Arial", 10, "bold"),
)
theme_toggle_btn.place(relx=1.0, rely=0.0, anchor="ne")  # Position in the top-right corner

# === LIGHT THEME STYLING ===
def apply_light_theme_styles():
    try:
        if style.theme_use() == "flatly":
            for tab in (tab1, tab2, tab3, tab4, tab6, tab7):
                tab.configure(padding=10)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to apply light theme styles: {e}")


# ====================== TAB 1: Search and Copy ======================
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Search and Copy")

# Info Button Function
def show_info_tab1():
    messagebox.showinfo(
        "Search and Copy - Info",
        "This tab allows you to:\n"
        "- Upload a CSV file.\n"
        "- Select input/output folders.\n"
        "- Enter search terms.\n"
        "- Choose file types (PDF, TXT, CSV).\n"
        "- Automatically copy matching files to the output folder."
    )

# Add Info Button to top-right corner of tab1
info_button_tab1 = tk.Button(tab1, text="i", width=2, command=show_info_tab1, font=("Arial", 10, "bold"))
info_button_tab1.place(relx=1.0, x=-30, y=5, anchor="ne")  # Adjusted to top-right

def upload_csv():
    file_path = filedialog.askopenfilename(title="Select a CSV file", filetypes=[("CSV files", "*.csv")])
    if file_path:
        csv_file_entry.delete(0, tk.END)
        csv_file_entry.insert(0, os.path.basename(file_path))

def select_input_folder():
    folder_path = filedialog.askdirectory(title="Select Input Folder")
    if folder_path:
        input_folder_entry.delete(0, tk.END)
        input_folder_entry.insert(0, folder_path)

def select_output_folder():
    folder_path = filedialog.askdirectory(title="Select Output Folder")
    if folder_path:
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, folder_path)

def search_and_copy():
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    search_terms = search_terms_entry.get("1.0", tk.END).strip().split('\n')
    selected_types = [ext for ext, var in selected_file_types.items() if var.get()]
    if not input_folder or not output_folder or not search_terms:
        messagebox.showerror("Error", "Please select input/output folders and enter search terms.")
        return
    copied_files = 0
    for root_dir, _, files in os.walk(input_folder):
        for file in files:
            if any(term in file for term in search_terms) and file.split('.')[-1] in selected_types:
                shutil.copy(os.path.join(root_dir, file), output_folder)
                copied_files += 1
    messagebox.showinfo("Success", f"Copied {copied_files} matching files to {output_folder}.")

# Add side columns for spacing
tab1.grid_columnconfigure(0, weight=1)  # Left spacer
tab1.grid_columnconfigure(1, weight=0)  # Label
tab1.grid_columnconfigure(2, weight=2)  # Entry/Text
tab1.grid_columnconfigure(3, weight=0)  # Button
tab1.grid_columnconfigure(4, weight=1)  # Right spacer

# Upload CSV row
tk.Label(tab1, text="CSV File:", font=("Arial", 12), anchor='w').grid(row=0, column=1, padx=(20,5), pady=10, sticky='e')
csv_file_entry = tk.Entry(tab1, width=50, font=("Arial", 12))
csv_file_entry.grid(row=0, column=2, padx=5, pady=10, sticky='we')
tk.Button(tab1, text="Select", command=upload_csv, font=("Arial", 12)).grid(row=0, column=3, padx=(5,20), pady=10, sticky='w')

# Input Folder row
tk.Label(tab1, text="Input Folder:", font=("Arial", 12), anchor='w').grid(row=1, column=1, padx=(20,5), pady=10, sticky='e')
input_folder_entry = tk.Entry(tab1, width=50, font=("Arial", 12))
input_folder_entry.grid(row=1, column=2, padx=5, pady=10, sticky='we')
tk.Button(tab1, text="Select", command=select_input_folder, font=("Arial", 12)).grid(row=1, column=3, padx=(5,20), pady=10, sticky='w')

# Output Folder row
tk.Label(tab1, text="Output Folder:", font=("Arial", 12), anchor='w').grid(row=2, column=1, padx=(20,5), pady=10, sticky='e')
output_folder_entry = tk.Entry(tab1, width=50, font=("Arial", 12))
output_folder_entry.grid(row=2, column=2, padx=5, pady=10, sticky='we')
tk.Button(tab1, text="Select", command=select_output_folder, font=("Arial", 12)).grid(row=2, column=3, padx=(5,20), pady=10, sticky='w')

# File type selection checkboxes
selected_file_types = {'pdf': tk.BooleanVar(), 'csv': tk.BooleanVar(), 'txt': tk.BooleanVar()}
file_type_frame = tk.Frame(tab1)
file_type_frame.grid(row=3, column=1, columnspan=3, pady=10)
for i, ext in enumerate(selected_file_types):
    tk.Checkbutton(file_type_frame, text=ext.upper(), variable=selected_file_types[ext], font=("Arial", 12)).grid(row=0, column=i, padx=10)

# Search terms text box
tk.Label(tab1, text="Search Text:", font=("Arial", 12), anchor='nw').grid(row=4, column=1, padx=(20,5), pady=10, sticky='ne')
search_terms_entry = tk.Text(tab1, width=50, height=5, font=("Arial", 12))
search_terms_entry.grid(row=4, column=2, columnspan=2, padx=(5,20), pady=10, sticky='we')

# Execute button
execute_frame = tk.Frame(tab1)
execute_frame.grid(row=5, column=1, columnspan=3, pady=20)
tk.Button(execute_frame, text="Execute", command=search_and_copy, font=("Arial", 14, "bold"), width=15).pack(pady=5)


# ====================== TAB 2: Find Files ======================
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Find Files")

# Info Button Function
def show_info_tab2():
    messagebox.showinfo(
        "Find Files - Info",
        "This tab helps you find files by name:\n"
        "- Select a folder\n"
        "- Enter search terms (one per line)\n"
        "- Click Search to list matching files"
    )

# Simple 'i' Button in top-right corner
info_button_tab2 = tk.Button(
    tab2,
    text="i",
    font=("Arial", 10, "bold"),
    width=2,
    command=show_info_tab2
)
info_button_tab2.place(relx=1.0, x=-30, y=5, anchor="ne")  # Top-right corner

def find_files():
    folder = folder_entry.get()
    search_terms = search_text_entry.get("1.0", tk.END).strip().split('\n')
    results_listbox.delete(0, tk.END)
    if not folder or not search_terms:
        messagebox.showerror("Error", "Please select a folder and enter search terms.")
        return
    for root_dir, _, files in os.walk(folder):
        for file in files:
            if any(term in file for term in search_terms):
                results_listbox.insert(tk.END, os.path.join(root_dir, file))

tab2.grid_columnconfigure(0, weight=1)
tab2.grid_columnconfigure(1, weight=0)
tab2.grid_columnconfigure(2, weight=2)
tab2.grid_columnconfigure(3, weight=0)
tab2.grid_columnconfigure(4, weight=1)
tk.Label(tab2, text="Folder:", font=("Arial", 12)).grid(row=0, column=1, padx=10, pady=10, sticky="e")
folder_entry = tk.Entry(tab2, width=50, font=("Arial", 12))
folder_entry.grid(row=0, column=2, padx=5, pady=10, sticky="we")
tk.Button(tab2, text="Select", command=lambda: folder_entry.insert(0, filedialog.askdirectory()), font=("Arial", 12)).grid(row=0, column=3, padx=5, pady=10, sticky="w")
tk.Label(tab2, text="Search Text:", font=("Arial", 12)).grid(row=1, column=1, padx=10, pady=5, sticky="ne")
search_text_entry = tk.Text(tab2, width=50, height=8, font=("Arial", 12))
search_text_entry.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="we")
tk.Button(tab2, text="Search", command=find_files, font=("Arial", 12)).grid(row=2, column=2, pady=10)
results_listbox = tk.Listbox(tab2, width=50, height=10, font=("Arial", 12))
results_listbox.grid(row=3, column=2, columnspan=2, padx=5, pady=10, sticky="we")

# ====================== TAB 3: Comparison ======================
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="Comparison")

# Info Button Function
def show_info_tab3():
    messagebox.showinfo(
        "Comparison - Info",
        "This tab compares file lists or folders:\n"
        "- Use List Mode for direct list input.\n"
        "- Use Folder Mode to compare filenames in two folders.\n"
        "- Click buttons to see common or unique items."
    )

# Simple 'i' Button in top-right corner
info_button_tab3 = tk.Button(
    tab3,
    text="i",
    font=("Arial", 10, "bold"),
    width=2,
    command=show_info_tab3
)
info_button_tab3.place(relx=1.0, x=-30, y=5, anchor="ne")


mode = tk.StringVar(value="list")
def switch_mode():
    if mode.get() == "list":
        list_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky="nsew")
        folder_frame.grid_forget()
    else:
        folder_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky="nsew")
        list_frame.grid_forget()

tab3.grid_columnconfigure(0, weight=1)
tab3.grid_columnconfigure(1, weight=8)
tab3.grid_columnconfigure(2, weight=1)

top_frame = tk.Frame(tab3)
top_frame.grid(row=0, column=1, sticky="ew", pady=10)
tk.Label(top_frame, text="Select Comparison Mode:").pack(side="left", padx=(0, 10))
tk.Radiobutton(top_frame, text="List Mode", variable=mode, value="list", command=switch_mode).pack(side="left", padx=(0, 10))
tk.Radiobutton(top_frame, text="Folder Mode", variable=mode, value="folder", command=switch_mode).pack(side="left")

input_frame = tk.LabelFrame(tab3, text="Input", padx=10, pady=10)
input_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
input_frame.grid_columnconfigure(0, weight=1)
list_frame = tk.Frame(input_frame)
tk.Label(list_frame, text="List 1:").grid(row=0, column=0, pady=5, sticky="w")
name1_entry = tk.Text(list_frame, width=1, height=10)
name1_entry.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
tk.Label(list_frame, text="List 2:").grid(row=0, column=1, pady=5, sticky="w")
name2_entry = tk.Text(list_frame, width=1, height=10)
name2_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
list_frame.grid_columnconfigure(0, weight=1)
list_frame.grid_columnconfigure(1, weight=1)

folder_frame = tk.Frame(input_frame)
folder1_path = tk.StringVar()
folder2_path = tk.StringVar()
tk.Label(folder_frame, text="Folder 1:").grid(row=0, column=0, sticky="w", padx=5)
tk.Entry(folder_frame, textvariable=folder1_path).grid(row=1, column=0, padx=5, sticky="ew")
tk.Button(folder_frame, text="Browse", command=lambda: browse_folder(folder1_path)).grid(row=1, column=1, padx=5)
folder1_listbox = tk.Listbox(folder_frame, height=10)
folder1_listbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
tk.Label(folder_frame, text="Folder 2:").grid(row=0, column=2, sticky="w", padx=5)
tk.Entry(folder_frame, textvariable=folder2_path).grid(row=1, column=2, padx=5, sticky="ew")
tk.Button(folder_frame, text="Browse", command=lambda: browse_folder(folder2_path)).grid(row=1, column=3, padx=5)
folder2_listbox = tk.Listbox(folder_frame, height=10)
folder2_listbox.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")
folder_frame.grid_columnconfigure(0, weight=1)
folder_frame.grid_columnconfigure(2, weight=1)

output_frame = tk.LabelFrame(tab3, text="Output", padx=10, pady=10)
output_frame.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")
output_frame.grid_columnconfigure((0, 1, 2), weight=1)
tk.Button(output_frame, text="Common", command=lambda: compare("common")).grid(row=0, column=0, pady=5)
tk.Button(output_frame, text="Unique in List/Folder 1", command=lambda: compare("unique1")).grid(row=0, column=1, pady=5)
tk.Button(output_frame, text="Unique in List/Folder 2", command=lambda: compare("unique2")).grid(row=0, column=2, pady=5)
comparison_result_text_box = tk.Text(output_frame, height=10)
comparison_result_text_box.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

def browse_folder(var):
    folder = filedialog.askdirectory()
    if folder:
        var.set(folder)
        if var == folder1_path:
            update_folder_listbox(folder, folder1_listbox)
        elif var == folder2_path:
            update_folder_listbox(folder, folder2_listbox)

def update_folder_listbox(folder, listbox):
    listbox.delete(0, tk.END)
    try:
        files = sorted(os.listdir(folder))
        for file in files:
            listbox.insert(tk.END, file)
    except Exception as e:
        messagebox.showerror("Error", f"Unable to list files:\n{e}")

def get_filenames(folder):
    try:
        return set(os.listdir(folder))
    except Exception as e:
        messagebox.showerror("Error", f"Unable to access folder:\n{e}")
        return set()

def compare(operation):
    if mode.get() == "list":
        list1 = set(filter(None, map(str.strip, name1_entry.get("1.0", tk.END).strip().split("\n"))))
        list2 = set(filter(None, map(str.strip, name2_entry.get("1.0", tk.END).strip().split("\n"))))
        if not list1 or not list2:
            messagebox.showerror("Error", "Please enter values in both lists.")
            return
    else:
        path1 = folder1_path.get()
        path2 = folder2_path.get()
        if not path1 or not path2:
            messagebox.showerror("Error", "Please select both folders.")
            return
        list1 = get_filenames(path1)
        list2 = get_filenames(path2)

    if operation == "common":
        result = list1 & list2
    elif operation == "unique1":
        result = list1 - list2
    elif operation == "unique2":
        result = list2 - list1

    comparison_result_text_box.delete("1.0", tk.END)
    comparison_result_text_box.insert(tk.END, "\n".join(sorted(result)) if result else "No matching results.")

# Call switch_mode explicitly to ensure the initial state is correctly set
switch_mode()

# ====================== TAB 4: Rename Files ======================
tab4 = ttk.Frame(notebook)
notebook.add(tab4, text="Rename Files")

# Info Button Function
def show_info_tab4():
    messagebox.showinfo(
        "Rename Files - Info",
        "This tab allows you to rename a list of files:\n"
        "- Paste or type file names in the textbox.\n"
        "- Use checkboxes to modify the names:\n"
        "   • Remove path\n"
        "   • Remove extensions\n"
        "   • Replace spaces with underscores\n"
        "   • Convert to lowercase\n"
        "- Click 'Rename' to preview the result."
    )

# Simple 'i' button in top-right corner
info_button_tab4 = tk.Button(
    tab4,
    text="i",
    font=("Arial", 10, "bold"),
    width=2,
    command=show_info_tab4
)
info_button_tab4.place(relx=1.0, x=-30, y=5, anchor="ne")


container4 = tk.Frame(tab4)
container4.pack(expand=True, padx=20, pady=20)

tk.Label(container4, text="Enter File Names:").pack()
rename_text_entry = tk.Text(container4, width=50, height=10)
rename_text_entry.pack()

remove_extensions_var = tk.BooleanVar()
replace_spaces_var = tk.BooleanVar()
convert_lowercase_var = tk.BooleanVar()
remove_path_var = tk.BooleanVar()


tk.Checkbutton(container4, text="Remove Path", variable=remove_path_var).pack()
tk.Checkbutton(container4, text="Remove Extensions", variable=remove_extensions_var).pack()
tk.Checkbutton(container4, text="Replace Spaces with _", variable=replace_spaces_var).pack()
tk.Checkbutton(container4, text="Convert to Lowercase", variable=convert_lowercase_var).pack()

def rename_files():
    filenames = rename_text_entry.get("1.0", tk.END).strip().split("\n")
    if not filenames or filenames == ['']:
        messagebox.showerror("Error", "Please enter file names.")
        return
    renamed_files = []
    for file in filenames:
        new_name = file.strip()
        if remove_path_var.get():
            new_name = os.path.basename(new_name)
        if replace_spaces_var.get():
            new_name = new_name.replace(" ", "_")
        if remove_extensions_var.get() and "." in new_name:
            new_name = new_name.rsplit(".", 1)[0]
        if convert_lowercase_var.get():
            new_name = new_name.lower()
        renamed_files.append(new_name)
    renamed_files_text.delete("1.0", tk.END)
    renamed_files_text.insert(tk.END, "\n".join(renamed_files))

tk.Button(container4, text="Rename", command=rename_files).pack(pady=5)
renamed_files_text = tk.Text(container4, width=50, height=10)
renamed_files_text.pack()

# === Tab 5: Text Compare & Highlight ===
tab5 = ttk.Frame(notebook)
notebook.add(tab5, text="Text Compare & Highlight")

# Info Button Function
def show_info_tab5():
    messagebox.showinfo(
        "Text Compare & Highlight - Info",
        "This tab allows side-by-side comparison of .txt files:\n"
        "- Select two folders containing text files\n"
        "- Choose files from Folder 1 (auto-loads from Folder 2 if available)\n"
        "- Use Compare_Files to highlight differences\n"
        "- Navigate using Previous/Next buttons\n"
        "- Use Search List to preload a specific list of filenames\n"
        "- Matched_Files shows common file names\n"
        "- You can also open a matching PDF if available"
    )

# Simple 'i' button (top-right corner)
info_button_tab5 = tk.Button(
    tab5,
    text="i",
    font=("Arial", 10, "bold"),
    width=2,
    command=show_info_tab5
)
info_button_tab5.place(relx=1.0, x=-30, y=5, anchor="ne")

folder1_label_var = tk.StringVar(value="Folder 1")
folder2_label_var = tk.StringVar(value="Folder 2")
pdf_folder_var = tk.StringVar()

status_var = tk.StringVar(value="")  # NEW: Status label for showing file position
def select_folder(folder_var, file_dropdown, file_list, label_var, label_text):
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_var.set(folder_path)
        folder_name = os.path.basename(folder_path)
        label_var.set(f"{label_text} ({folder_name})")
        files = [f for f in os.listdir(folder_path) if f.lower().endswith('.txt')]
        file_list.clear()
        file_list.extend(files)
        file_dropdown['values'] = files
        file_dropdown.set('')
        update_file_status()  # Update counter


def browse_pdf_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        pdf_folder_var.set(folder_path)
        pdf_label.config(text=f"PDF Folder: {os.path.basename(folder_path)}")


def open_matching_pdf():
    current_file = file_dropdown1.get()
    if not current_file:
        return
    filename_wo_ext = os.path.splitext(current_file)[0]
    pdf_filename = filename_wo_ext + ".pdf"
    pdf_path = os.path.join(pdf_folder_var.get(), pdf_filename)
    if os.path.exists(pdf_path):
        webbrowser.open(pdf_path)
    else:
        tk.messagebox.showwarning("PDF Not Found", f"No matching PDF found:\n{pdf_filename}")



def load_file_from_folder(folder_path, filename, text_box, line_box):
    file_path = os.path.join(folder_path, filename)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, content)
            update_line_numbers(text_box, line_box)
def update_line_numbers(text_box, line_box):
    line_box.config(state='normal')
    line_box.delete('1.0', tk.END)
    lines = text_box.get('1.0', tk.END).split('\n')
    for i in range(1, len(lines)):
        line_box.insert(tk.END, f"{i}\n")
    line_box.config(state='disabled')
def normalize(word):
    return word.replace(' ', '').replace(',', '').replace('|', '').lower()

def load_list1_file(event=None):
    filename = file_dropdown1.get()
    if not filename:
        return

    file1_found = filename in list1_files
    file2_found = filename in list2_files

    if not file1_found and not file2_found:
        messagebox.showwarning("File Not Found", f"'{filename}' not found in Folder 1 or Folder 2.")
        return
    elif not file1_found:
        messagebox.showwarning("File Not Found", f"'{filename}' not found in Folder 1.")
        return
    elif not file2_found:
        messagebox.showwarning("File Not Found", f"'{filename}' not found in Folder 2.\nOnly File 1 will be loaded.")

    # Load File 1
    load_file_from_folder(folder1_var.get(), filename, text_box1, line_box1)
    file_label1.config(text=f"File: {filename}")
    update_file_status()

    # Load File 2 (only if found)
    if file2_found:
        load_file_from_folder(folder2_var.get(), filename, text_box2, line_box2)
        file_dropdown2.set(filename)
        file_label2.config(text=f"File: {filename}")
    else:
        text_box2.delete("1.0", tk.END)
        line_box2.delete("1.0", tk.END)
        file_dropdown2.set('')
        file_label2.config(text="")


def update_file_status():
    current_file = file_dropdown1.get()
    if current_file and current_file in list1_files:
        current_index = list1_files.index(current_file) + 1
        total_files = len(list1_files)
        status_var.set(f"File {current_index} of {total_files}")
    else:
        status_var.set("")
def get_highlighted_lines(text_widget):
    highlight_ranges = text_widget.tag_ranges("highlight")
    lines = set()
    for i in range(0, len(highlight_ranges), 2):
        start = highlight_ranges[i]
        line_number = int(str(start).split('.')[0])
        lines.add(line_number)
    return sorted(lines)
def show_highlight_summary():
    text1_lines = text_box1.get("1.0", tk.END).splitlines()
    text2_lines = text_box2.get("1.0", tk.END).splitlines()

    highlighted_lines1 = get_highlighted_lines(text_box1)
    highlighted_lines2 = get_highlighted_lines(text_box2)

    summary = tk.Toplevel(root)
    summary.title("Detailed Highlight Summary")
    summary.geometry("900x600")

    text_area = tk.Text(summary, wrap="word", font=("Courier", 10))
    text_area.pack(fill=tk.BOTH, expand=True)

    def find_matching_line(src_line, other_lines):
        for line in other_lines:
            if normalize(src_line) in normalize(line) or normalize(line) in normalize(src_line):
                return line.strip()
        return None

    # Show line numbers at the top
    text_area.insert(tk.END, "=== Highlighted Line Numbers ===\n\n")
    text_area.insert(tk.END, f"File 1: {', '.join(map(str, highlighted_lines1)) or 'None'}\n")
    text_area.insert(tk.END, f"File 2: {', '.join(map(str, highlighted_lines2)) or 'None'}\n\n")

    # Then detailed comparison
    text_area.insert(tk.END, "=== Detailed Comparison ===\n\n")

    used_lines2 = set()

    for line_no1 in highlighted_lines1:
        src1 = text1_lines[line_no1 - 1].strip()
        matching_line2 = find_matching_line(src1, text2_lines)
        if matching_line2:
            line_no2 = text2_lines.index(matching_line2) + 1
            used_lines2.add(line_no2)
            text_area.insert(tk.END, f"File 1: Line {line_no1}: {src1}\n")
            text_area.insert(tk.END, f"File 2: Line {line_no2}: {matching_line2}\n\n")
        else:
            # Use next unused highlighted line
            remaining = [l for l in highlighted_lines2 if l not in used_lines2]
            if remaining:
                line_no2 = remaining[0]
                line2 = text2_lines[line_no2 - 1].strip()
                used_lines2.add(line_no2)
                text_area.insert(tk.END, f"File 1: Line {line_no1}: {src1}\n")
                text_area.insert(tk.END, f"File 2: Line {line_no2}: {line2}\n\n")
            else:
                text_area.insert(tk.END, f"File 1: Line {line_no1}: {src1}\n")
                text_area.insert(tk.END, "No matching line found in File 2.\n\n")

    # Remaining File 2 lines
    for line_no2 in highlighted_lines2:
        if line_no2 in used_lines2:
            continue
        src2 = text2_lines[line_no2 - 1].strip()
        matching_line1 = find_matching_line(src2, text1_lines)
        if matching_line1:
            line_no1 = text1_lines.index(matching_line1) + 1
            text_area.insert(tk.END, f"File 2: Line {line_no2}: {src2}\n")
            text_area.insert(tk.END, f"File 1: Line {line_no1}: {matching_line1}\n\n")
        else:
            text_area.insert(tk.END, f"File 2: Line {line_no2}: {src2}\n")
            text_area.insert(tk.END, "No matching line found in File 1.\n\n")

    text_area.config(state='disabled')
    tk.Button(summary, text="Close", command=summary.destroy).pack(pady=5)

def compare_data():
    text1_lines = text_box1.get("1.0", tk.END).splitlines()
    text2_lines = text_box2.get("1.0", tk.END).splitlines()

    # Normalize lines for comparison
    norm_text1_lines = [normalize(line) for line in text1_lines]
    norm_text2_lines = [normalize(line) for line in text2_lines]

    text_box1.tag_remove("highlight", "1.0", tk.END)
    text_box2.tag_remove("highlight", "1.0", tk.END)

    # Highlight lines in text_box1 that are not in text2
    for i, line in enumerate(norm_text1_lines):
        if line not in norm_text2_lines:
            text_box1.tag_add("highlight", f"{i+1}.0", f"{i+1}.end")

    # Highlight lines in text_box2 that are not in text1
    for i, line in enumerate(norm_text2_lines):
        if line not in norm_text1_lines:
            text_box2.tag_add("highlight", f"{i+1}.0", f"{i+1}.end")

    text_box1.tag_config("highlight", background="orange", foreground="white")
    text_box2.tag_config("highlight", background="orange", foreground="white")
    
    show_highlight_summary()
def load_next_file():
    current_file = file_dropdown1.get()
    if not current_file:
        return
    try:
        current_index = list1_files.index(current_file)
        next_index = current_index + 1
        if next_index >= len(list1_files):
            return
        next_file = list1_files[next_index]
    except ValueError:
        return
    file_dropdown1.set(next_file)
    load_list1_file()
def load_previous_file():
    global search_index
    if search_list:
        if search_index <= 1:
            return
        search_index -= 1
        prev_file = search_list[search_index - 1].strip()
        if prev_file in list1_files:
            file_dropdown1.set(prev_file)
            load_list1_file()
        return

    current_file = file_dropdown1.get()
    if not current_file:
        return
    try:
        current_index = list1_files.index(current_file)
        prev_index = current_index - 1
        if prev_index < 0:
            return
        prev_file = list1_files[prev_index]
    except ValueError:
        return
    file_dropdown1.set(prev_file)
    load_list1_file()
def show_matching_files():
    matched_files = list(set(list1_files) & set(list2_files))
    count = len(matched_files)
    popup = tk.Toplevel(root)
    popup.title("Matched Files")
    popup.geometry("400x300")
    tk.Label(popup, text=f"Total Matched Files: {count}", font=("Helvetica", 12, "bold")).pack(pady=(10, 5))
    listbox = tk.Listbox(popup, width=50, height=10)
    listbox.pack(pady=5, padx=10)
    for f in sorted(matched_files):
        listbox.insert(tk.END, f)
    tk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)
def sync_scroll(event, src, *targets):
    for target in targets:
        target.yview_moveto(src.yview()[0])
    return "break"

# === UI Layout ===
folder1_var = tk.StringVar()
folder2_var = tk.StringVar()
list1_files = []
list2_files = []
frame1 = tk.Frame(tab5)
frame1.pack(pady=5)
tk.Label(frame1, textvariable=folder1_label_var).pack(side=tk.LEFT)
tk.Button(frame1, text="Browse", command=lambda: select_folder(folder1_var, file_dropdown1, list1_files, folder1_label_var, "Folder 1")).pack(side=tk.LEFT)
file_dropdown1 = ttk.Combobox(frame1, width=30)
file_dropdown1.pack(side=tk.LEFT, padx=10)
file_dropdown1.bind("<<ComboboxSelected>>", load_list1_file)
tk.Label(frame1, textvariable=folder2_label_var).pack(side=tk.LEFT)
tk.Button(frame1, text="Browse", command=lambda: select_folder(folder2_var, file_dropdown2, list2_files, folder2_label_var, "Folder 2")).pack(side=tk.LEFT)
file_dropdown2 = ttk.Combobox(frame1, width=30)
file_dropdown2.pack(side=tk.LEFT, padx=10)


pdf_frame = tk.Frame(tab5)
pdf_frame.pack(fill=tk.X, padx=10, pady=5)

pdf_label = tk.Label(pdf_frame, text="PDF Folder: Not selected")
pdf_label.pack(side=tk.LEFT, padx=(0,10))

tk.Button(pdf_frame, text="Browse PDF Folder", command=browse_pdf_folder, bg="grey", fg="white").pack(side=tk.LEFT)

tk.Button(pdf_frame, text="Open PDF", command=open_matching_pdf, bg="grey", fg="white").pack(side=tk.LEFT, padx=10)



text_frame = tk.Frame(tab5)
text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))
line_box1 = tk.Text(text_frame, width=4)
line_box1.pack(side=tk.LEFT, fill=tk.Y)
text_box1 = tk.Text(text_frame, wrap="none")
text_box1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
line_box2 = tk.Text(text_frame, width=4)
line_box2.pack(side=tk.LEFT, fill=tk.Y)
text_box2 = tk.Text(text_frame, wrap="none")
text_box2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll = tk.Scrollbar(text_frame, orient="vertical")
scroll.pack(side=tk.RIGHT, fill=tk.Y)
text_box1.config(yscrollcommand=scroll.set)
text_box2.config(yscrollcommand=scroll.set)
scroll.config(command=lambda *args: [
    text_box1.yview(*args),
    text_box2.yview(*args),
    line_box1.yview(*args),
    line_box2.yview(*args)
])
root.bind_all("<MouseWheel>", lambda e: sync_scroll(e, text_box1, text_box2, line_box1, line_box2))
root.bind_all("<Button-4>", lambda e: sync_scroll(e, text_box1, text_box2, line_box1, line_box2))
root.bind_all("<Button-5>", lambda e: sync_scroll(e, text_box1, text_box2, line_box1, line_box2))
label_frame = tk.Frame(tab5)
label_frame.pack(fill=tk.X, padx=10, pady=5)
file_label1 = tk.Label(label_frame, text="", font=("Helvetica", 10, "bold"), anchor="w")
file_label1.pack(side=tk.LEFT, expand=True, fill=tk.X)
button_frame = tk.Frame(tab5)
button_frame.pack(pady=5)


# === Add these lines after all import statements ===
search_list = []
search_index = 0

# === Add this function after update_file_status() ===
def load_next_file():
    global search_index
    if search_list:
        if search_index >= len(search_list):
            return
        next_file = search_list[search_index].strip()
        search_index += 1
        if next_file in list1_files:
            file_dropdown1.set(next_file)
            load_list1_file()
        return

    current_file = file_dropdown1.get()
    if not current_file:
        return
    try:
        current_index = list1_files.index(current_file)
        next_index = current_index + 1
        if next_index >= len(list1_files):
            return
        next_file = list1_files[next_index]
    except ValueError:
        return
    file_dropdown1.set(next_file)
    load_list1_file()



# === Add this function to handle search input ===
def load_search_list():
    global search_list, search_index
    content = search_text.get("1.0", tk.END)
    raw_list = [line.strip() for line in content.strip().splitlines() if line.strip()]

    # Ensure all entries end with .txt
    search_list = [f"{line}.txt" if not line.lower().endswith('.txt') else line for line in raw_list]
    
    search_index = 0
    if search_list:
        file_dropdown1.set(search_list[0])
        load_list1_file()
        search_index = 1

# === Add this in the UI Layout section (before root.mainloop()) ===
search_frame = tk.Frame(tab5)
search_frame.pack(fill=tk.X, padx=10, pady=5)

tk.Label(search_frame, text="Search Files:-").pack(anchor="w")
search_text = tk.Text(search_frame, height=4)
search_text.pack(fill=tk.X, pady=2)

tk.Button(search_frame, text="Load Search Files", command=load_search_list, bg="grey", fg="white").pack(pady=2)


tk.Button(button_frame, text="Previous_File", command=load_previous_file, bg="grey", fg="white").pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Compare_Files", command=compare_data, bg="grey", fg="white").pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Next_File", command=load_next_file, bg="grey", fg="white").pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Matched_Files", command=show_matching_files, bg="grey", fg="white").pack(side=tk.LEFT, padx=10)
# Bottom Status Label
status_label = tk.Label(tab5, textvariable=status_var, font=("Helvetica", 10, "bold"), anchor='w', fg="blue")
status_label.pack(side=tk.LEFT, padx=10, pady=5)




# === TAB 8: PDF Search & Open ===
tab8 = Frame(notebook)
notebook.add(tab8, text="PDF Search & Open")

# Info Button Function
def show_info_tab8():
    messagebox.showinfo(
        "PDF Search & Open - Info",
        "This tab allows you to:\n"
        "- Select a folder containing PDF files\n"
        "- Open a selected PDF from a dropdown list\n"
        "- Load a list of PDF filenames to search\n"
        "- Navigate through PDFs with Previous/Next buttons\n"
        "- Automatically open the selected PDF"
    )

# Simple 'i' button (top-right corner)
info_button_tab8 = Button(
    tab8,
    text="i",
    font=("Arial", 10, "bold"),
    width=2,
    command=show_info_tab8
)
info_button_tab8.place(relx=1.0, x=-30, y=5, anchor="ne")


pdf_search_folder_var = tk.StringVar()
current_pdf_label_var = tk.StringVar(value="No PDF loaded")
pdf_names_list = []
pdf_index = 0

selected_pdf_dropdown_var = tk.StringVar()
pdf_dropdown = None  # Will be initialized later

def browse_pdf_folder_tab8():
    folder = filedialog.askdirectory()
    if folder:
        pdf_search_folder_var.set(folder)
        # Scan for PDF files
        pdf_files = [f for f in os.listdir(folder) if f.lower().endswith('.pdf')]
        if pdf_files:
            selected_pdf_dropdown_var.set(pdf_files[0])  # Set first as default
            pdf_dropdown['values'] = pdf_files
        else:
            selected_pdf_dropdown_var.set("No PDFs found")
            pdf_dropdown['values'] = []

def open_pdf_from_dropdown(event=None):
    folder = pdf_search_folder_var.get().strip()
    selected_pdf = selected_pdf_dropdown_var.get()
    if not folder or not os.path.isdir(folder):
        messagebox.showerror("Error", "Please select a valid PDF folder.")
        return
    if not selected_pdf or selected_pdf == "No PDFs found":
        return
    full_path = os.path.join(folder, selected_pdf)
    if os.path.exists(full_path):
        webbrowser.open(full_path)
    else:
        messagebox.showwarning("Not Found", f"{selected_pdf} not found in selected folder.")

def load_pdf_names():
    global pdf_names_list, pdf_index
    content = pdf_name_text.get("1.0", END).strip()
    raw_list = [name.strip() for part in content.splitlines() for name in part.split(',') if name.strip()]
    pdf_names_list = [f"{name}.pdf" if not name.lower().endswith(".pdf") else name for name in raw_list]
    pdf_index = 0
    if pdf_names_list:
        update_current_pdf_label()

def update_current_pdf_label():
    if pdf_names_list:
        current_pdf_label_var.set(f"Selected_PDF: {pdf_names_list[pdf_index]}")
    else:
        current_pdf_label_var.set("No PDF loaded")

def open_selected_pdf():
    if not pdf_names_list:
        messagebox.showinfo("Info", "No PDF names loaded.")
        return
    folder = pdf_search_folder_var.get().strip()
    if not folder or not os.path.isdir(folder):
        messagebox.showerror("Error", "Please select a valid PDF folder.")
        return
    current_file = pdf_names_list[pdf_index]
    full_path = os.path.join(folder, current_file)
    if os.path.exists(full_path):
        webbrowser.open(full_path)
    else:
        messagebox.showwarning("Not Found", f"{current_file} not found in selected folder.")

def open_next_pdf():
    global pdf_index
    if pdf_index < len(pdf_names_list) - 1:
        pdf_index += 1
        update_current_pdf_label()

def open_previous_pdf():
    global pdf_index
    if pdf_index > 0:
        pdf_index -= 1
        update_current_pdf_label()

# === UI Layout ===
Label(tab8, text="PDF Folder:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
Entry(tab8, textvariable=pdf_search_folder_var, width=50).grid(row=0, column=1, padx=5, pady=10, sticky="w")
Button(tab8, text="Browse", command=browse_pdf_folder_tab8).grid(row=0, column=2, padx=5, pady=10)

Label(tab8, text="Select PDF from Folder:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
pdf_dropdown = ttk.Combobox(tab8, textvariable=selected_pdf_dropdown_var, state="readonly", width=50)
pdf_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")
pdf_dropdown.bind("<<ComboboxSelected>>", open_pdf_from_dropdown)  # Bind selection event

Label(tab8, text="Enter PDF File Names", font=("Arial", 12)).grid(row=2, column=0, columnspan=3, padx=10, sticky="w")
pdf_name_text = Text(tab8, width=70, height=6, font=("Arial", 11))
pdf_name_text.grid(row=3, column=0, columnspan=3, padx=10, pady=5)


for i in range(4):
    tab8.grid_columnconfigure(i, weight=1, uniform="equal")

# Buttons with equal spacing and stretching
Button(tab8, text="Load File_Names", command=load_pdf_names).grid(row=4, column=0, padx=10, pady=10, sticky="ew")
Button(tab8, text="Previous_PDF", command=open_previous_pdf).grid(row=4, column=1, padx=10, pady=10, sticky="ew")
Button(tab8, text="Next_PDF", command=open_next_pdf).grid(row=4, column=2, padx=10, pady=10, sticky="ew")
Button(tab8, text="Open PDF", command=open_selected_pdf).grid(row=4, column=3, padx=10, pady=10, sticky="ew")


Label(tab8, textvariable=current_pdf_label_var, font=("Arial", 11, "italic"), fg="blue").grid(row=5, column=0, columnspan=3, pady=5)


# === TAB 6: CSV Analysis ===
tab6 = Frame(notebook)
notebook.add(tab6, text="CSV Analysis")

def show_info_tab6():
    messagebox.showinfo(
        "- Load and Analyze CSV File",
        "- Generate Detailed reports With:\n"
        "- True/False Counts\n"
        "- Percentages.\n"
        "- Total File Counts\n"
        "- Features :\n"
        "- select Specific Parameter For Analysis\n"
        "- Save Reports as CSV Files"
        )

# Simple 'i' button (top-right corner)
info_button_tab6 = tk.Button(
    tab6,
    text="i",
    font=("Arial", 10, "bold"),
    width=2,
    command=show_info_tab6
)
info_button_tab6.place(relx=1.0, x=-30, y=5, anchor="ne")


output_df_tab6 = None
df_tab6 = None  # Initialize the dataframe variable

Label(tab6, text="CSV Analysis Tool", font=("Arial", 16, "bold")).pack(pady=10)

Button(tab6, text="Browse CSV File", command=lambda: browse_csv_tab6()).pack(pady=5)

# === Parameter Selection & Filter Frame ===
param_frame_tab6 = Frame(tab6)
param_frame_tab6.pack(pady=5)

Label(param_frame_tab6, text="Select Parameters:", font=("Arial", 12)).grid(row=0, column=0, columnspan=3)

param_vars_tab6 = {}  # Dictionary to hold dynamic parameter variables

def set_all_param_vars(state=True):
    for var in param_vars_tab6.values():
        var.set(state)

Button(param_frame_tab6, text="Select All", command=lambda: set_all_param_vars(True)).grid(row=1, column=0, padx=5)
Button(param_frame_tab6, text="Deselect All", command=lambda: set_all_param_vars(False)).grid(row=1, column=1, padx=5)

# === Toggle Option to View Selected or All ===
view_all_var_tab6 = BooleanVar(value=False)
Checkbutton(tab6, text="View All Parameters", variable=view_all_var_tab6).pack(pady=5)

Button(tab6, text="Generate Report", command=lambda: generate_report_tab6()).pack(pady=5)

# === Result Display Frame (Fixed Height) ===
frame_result_tab6 = Frame(tab6, height=300)
frame_result_tab6.pack(fill="x", padx=10, pady=(5, 0))

result_box_tab6 = Text(frame_result_tab6, wrap="none", height=15)
result_box_tab6.pack(side="left", fill="both", expand=True)

scroll_y_tab6 = Scrollbar(frame_result_tab6, orient="vertical", command=result_box_tab6.yview)
scroll_y_tab6.pack(side="right", fill="y")

result_box_tab6.config(yscrollcommand=scroll_y_tab6.set)

# Horizontal scrollbar below the result box
scroll_x_tab6 = Scrollbar(tab6, orient="horizontal", command=result_box_tab6.xview)
scroll_x_tab6.pack(fill="x", padx=10)
result_box_tab6.config(xscrollcommand=scroll_x_tab6.set)

# Save button now visible
Button(tab6, text="Save Result CSV", command=lambda: save_result_tab6()).pack(pady=10)

# === Functional Logic ===
def browse_csv_tab6():
    global df_tab6, param_vars_tab6
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            df_tab6 = pd.read_csv(file_path)
            messagebox.showinfo("Success", "File loaded. Now select parameters and click 'Generate Report'.")
            generate_param_checkboxes()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file:\n{e}")
            df_tab6 = None

def generate_param_checkboxes():
    # Clear existing checkboxes
    for widget in param_frame_tab6.winfo_children():
        widget.destroy()

    # Add Select/Deselect All Buttons again
    Button(param_frame_tab6, text="Select All", command=lambda: set_all_param_vars(True)).grid(row=1, column=0, padx=5)
    Button(param_frame_tab6, text="Deselect All", command=lambda: set_all_param_vars(False)).grid(row=1, column=1, padx=5)

    if df_tab6 is not None:
        param_vars_tab6.clear()
        # Use all columns from the DataFrame
        all_columns = list(df_tab6.columns)

        if not all_columns:
            messagebox.showinfo("Info", "No columns detected in the file. Please check the file content.")
            return

        for i, param in enumerate(all_columns):
            var = BooleanVar(value=True)
            param_vars_tab6[param] = var
            row, col = divmod(i, 2)
            Checkbutton(param_frame_tab6, text=param.replace("_", " "), variable=var).grid(row=row + 2, column=col, sticky="w", padx=10, pady=2)

def generate_report_tab6():
    """
    Generate a report based on the selected parameters in the CSV file.
    Always show Parameters and Total Files, even if True/False counts are not valid.
    """
    global output_df_tab6
    if df_tab6 is None:
        messagebox.showwarning("Warning", "Please load a CSV file first.")
        return

    # Get selected parameters or all available columns
    selected_params = [k for k, v in param_vars_tab6.items() if v.get()]
    view_all = view_all_var_tab6.get()

    # Handle "View All Parameters" option
    parameters = selected_params if not view_all else list(df_tab6.columns)

    if not parameters:
        messagebox.showwarning("Warning", "No parameters selected!")
        return

    # Generate the summary
    output_df_tab6 = get_summary(parameters)
    display_result_tab6()


def get_summary(parameters):
    """
    Create a summary DataFrame with Parameter and Total Files always included.
    Add True Count, False Count, and True Percentage if valid.
    """
    summary_data = []
    total_files = len(df_tab6)

    for param in parameters:
        if param not in df_tab6.columns:
            continue  # Skip missing columns

        # Check if column contains Boolean-like values
        if df_tab6[param].dropna().isin([True, False, 0, 1, "True", "False", "true", "false"]).all():
            true_count = df_tab6[param].sum()
            false_count = total_files - true_count
            true_percentage = (true_count / total_files) * 100
            summary_data.append({
                "Parameter": param,
                "True Count": int(true_count),
                "False Count": int(false_count),
                "True Percentage": f"{true_percentage:.2f}%",
                "Total Files": total_files
            })
        else:
            # If not Boolean-like, set True/False Count and Percentage as "N/A"
            summary_data.append({
                "Parameter": param,
                "True Count": "N/A",
                "False Count": "N/A",
                "True Percentage": "N/A",
                "Total Files": total_files
            })

    # Ensure the DataFrame columns are in the correct sequence
    return pd.DataFrame(summary_data, columns=["Parameter", "True Count", "False Count", "True Percentage", "Total Files"])
    
def display_result_tab6():
    # Use a monospace font for proper alignment
    result_box_tab6.config(font=("Courier", 10))  # Set font to Courier (monospace)

    # Clear previous content
    result_box_tab6.delete("1.0", END)

    if output_df_tab6 is not None and not output_df_tab6.empty:
        try:
            # Generate a clean, aligned table using tabulate
            result_string = tabulate(
                output_df_tab6,
                headers="keys",
                tablefmt="plain",  # Use plain format for alignment
                showindex=False
            )

            # Insert the result into the Text widget
            result_box_tab6.insert(END, result_string)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while displaying the result:\n{e}")
    else:
        result_box_tab6.insert(END, "No analysis available or parameters not found.")
def save_result_tab6():
    if output_df_tab6 is None or output_df_tab6.empty:
        messagebox.showwarning("Warning", "No analysis result to save!")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if save_path:
        output_df_tab6.to_csv(save_path, index=False)
        messagebox.showinfo("Success", f"Result saved at:\n{save_path}")

# --- Settings Config (Save/Load) ---
CONFIG_FILE = "config.json"

def save_settings():
    config = {
        "dark_mode": is_dark_mode.get(),
        "font_size": font_size_var.get(),
        "accent_color": accent_color_var.get()
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
    messagebox.showinfo("Settings", "Preferences saved.")

def load_settings():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            is_dark_mode.set(config.get("dark_mode", True))
            font_size_var.set(config.get("font_size", "Medium"))
            accent_color_var.set(config.get("accent_color", "primary"))
            toggle_theme()
            apply_font_size()
            apply_accent_color()

# --- Tab 7: Settings ---
tab7 = Frame(notebook)
notebook.add(tab7, text="Settings")


def show_info_tab7():
    messagebox.showinfo(
        "- Customization Options:\n",
        "- Accent Color(Primary , Sucess,Warming, Etc.):\n"
        "- Theme(Light Or Dark Mode)\n"
        "- Preference Management.\n"
        "- Save and reset settings\n"
        "- User Preference are persistent across sessions :"
        )

# Simple 'i' button (top-right corner)
info_button_tab7 = tk.Button(
    tab7,
    text="i",
    font=("Arial", 10, "bold"),
    width=2,
    command=show_info_tab7
)
info_button_tab7.place(relx=1.0, x=-30, y=5, anchor="ne")


# Font Size Option
Label(tab7, text="Font Size:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
font_size_var = tk.StringVar(value="Medium")
font_size_options = ["Small", "Medium", "Large"]
Combobox(tab7, textvariable=font_size_var, values=font_size_options, state="readonly", width=15)\
    .grid(row=0, column=1, padx=10, pady=10, sticky="w")

def apply_font_size():
    size_map = {"Small": 9, "Medium": 11, "Large": 13}
    selected_size = size_map.get(font_size_var.get(), 11)
    style.configure(".", font=("Segoe UI", selected_size))

ttk.Button(tab7, text="Apply Font Size", command=apply_font_size).grid(row=0, column=2, padx=10, pady=10)

# Theme Toggle
Label(tab7, text="Theme:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
Checkbutton(tab7, text="Dark Mode", variable=is_dark_mode, command=toggle_theme).grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Accent Color Picker
Label(tab7, text="Accent Color:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
accent_color_var = tk.StringVar(value="Default")
accent_colors = ["Default", "Primary", "Success", "Info", "Warning", "Danger"]
Combobox(tab7, textvariable=accent_color_var, values=accent_colors, state="readonly", width=15)\
    .grid(row=2, column=1, padx=10, pady=10, sticky="w")

def apply_accent_color():
    try:
        color_map = {
            "primary": "#0275d8",
            "success": "#5cb85c",
            "info": "#5bc0de",
            "warning": "#f0ad4e",
            "danger": "#d9534f",
            "secondary": "#6c757d",  # neutral gray
        }

        selected_color = accent_color_var.get().lower()
        if selected_color == "default":
            selected_color = "secondary"
        color_code = color_map.get(selected_color, "#6c757d")

        style = ttk.Style()
        style.configure(f"{selected_color}.TButton", background=color_code, foreground="white")

        def update_widget_colors(widget):
            if isinstance(widget, ttk.Button):
                widget.configure(bootstyle=selected_color)
            elif isinstance(widget, tk.Button):
                try:
                    widget.configure(bg=color_code, fg="white", activebackground=color_code, activeforeground="white")
                except:
                    pass
            elif isinstance(widget, tk.Label):
                try:
                    widget.configure(fg=color_code)
                except:
                    pass

            if not isinstance(widget, (tk.Text, tk.Entry)):
                for child in widget.winfo_children():
                    update_widget_colors(child)

        update_widget_colors(root)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to apply accent color: {e}")

ttk.Button(tab7, text="Apply Accent", command=apply_accent_color).grid(row=2, column=2, padx=10, pady=10)

# Reset All Inputs
def reset_all_inputs():
    try:
        for entry in [csv_file_entry, input_folder_entry, output_folder_entry, folder_entry]:
            entry.delete(0, tk.END)
        for text_widget in [search_terms_entry, search_text_entry, name1_entry, name2_entry, rename_text_entry]:
            text_widget.delete("1.0", tk.END)
        for var in selected_file_types.values():
            var.set(False)
        replace_spaces_var.set(False)
        remove_extensions_var.set(False)
        results_listbox.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to reset inputs: {e}")

ttk.Button(tab7, text="Reset All", command=reset_all_inputs, bootstyle="danger").grid(row=3, column=0, columnspan=2, padx=10, pady=20)

# Save Settings
ttk.Button(tab7, text="Save Settings", command=save_settings, bootstyle="success").grid(row=4, column=0, padx=10, pady=10)

# Load settings at startup
try:
    load_settings()
except Exception as e:
    messagebox.showerror("Error", f"Failed to load settings: {e}")

# === LIGHT THEME STYLING ===
def apply_light_theme_styles():
    try:
        if style.theme_use() == "flatly":
            notebook.configure(bootstyle="info")
            for tab in (tab1, tab2, tab3, tab4, tab6, tab7):
                tab.configure(style="light.TFrame", padding=10)
            for btn in styled_buttons:
                btn.configure(bootstyle="info-outline", padding=5)
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bootstyle="primary-outline"))
                btn.bind("<Leave>", lambda e, b=btn: b.configure(bootstyle="info-outline"))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to apply light theme styles: {e}")

# === Update Background and Tab Style Based on Default Theme ===
try:
    update_background()
    update_tab_style()
except Exception as e:
    messagebox.showerror("Error", f"Failed to update styles: {e}")
 
# === Main Loop ===
root.mainloop()
