import glob
import os
import platform
from tkinter import filedialog, messagebox
import tkinter as tk
import atexit


class RenameTool:
    win = tk.Tk()
    root_path = []
    directory = ""
    changes = dict()

    def __init__(self, window_name):
        self.opt_menu = None
        # Window Configuration
        self.win.title(window_name)
        self.win.config(bg='#000000')
        self.win.geometry('950x750')
        self.win.resizable(False, False)

        # Labels
        self.rename_label = tk.Label(text="New Name\n(w/ ext):", bg='black', fg='white', font=('Calibri', '12'))
        self.rename_label.place(x=5, y=440)
        self.label = tk.Label(text="Enter Path:", height=1, bg='black', fg='white', font=('Calibri', '15'))
        self.label.place(x=5, y=5)
        self.label2 = tk.Label(text="Extension:", height=1, bg='black', fg='white', font=('Calibri', '15'))
        self.label2.place(x=5, y=65)

        # Output To List All files from the directory
        self.output = tk.Text(width=75, height=15, padx=10, pady=5, font='Calibri', fg='green') # noqa
        self.output.place(x=115, y=145)
        self.output.bind("<1>", lambda event: self.output.focus_set())

        # Entry Widgets
        self.entry_1 = tk.Text(width=70, height=1, padx=5, pady=10, font='Calibri')
        self.entry_1.place(x=115, y=5)
        self.entry_2 = tk.Text(width=10, height=1, padx=5, pady=10, font='Calibri')
        self.entry_2.place(x=115, y=65)
        self.entry_3 = tk.Text(width=75, height=1, padx=5, pady=5, font='Calibri')
        self.entry_3.place(x=115, y=450)
        # Control Buttons
        self.button = tk.Button(text="Submit", height=2, width=10, command=self.print_widget)
        self.button.place(x=230, y=65)
        self.rename = tk.Button(text="Rename", height=2, width=10, command=self.rename)
        self.rename.place(x=115, y=500)
        self.get_dir_button = tk.Button(text="Open", height=2, width=10, command=self.select_path)
        self.get_dir_button.place(x=325, y=65)

    def provide_option(self, files):
        if platform.system() == "Windows":
            self.opt_menu = tk.Listbox(self.win, width=65, height=10, font='Calibri 12')
        else:
            self.opt_menu = tk.Listbox(self.win, width=65, height=10, font='Calibri 16')
        for file in files:
            if file != 'changes.log':
                self.opt_menu.insert('end', f'  {file}')
        self.opt_menu.place(x=225, y=500)

    def clear_prev(self):
        self.opt_menu.place_forget()


    def select_path(self): # noqa
        self.directory = filedialog.askdirectory()

    def scan_dir(self, path, extension):
        try:
            if extension == "":
                return os.listdir(path)
            else:
                os.chdir(path)
                return glob.glob(f'*.{extension}')

        except FileNotFoundError:
            print("No FIle/Directory resuming again")
            opt_retry = messagebox.askretrycancel('File| Directory Not Found', 'Invalid File/Directory Path..Retry?')
            self.entry_1.delete(1.0, tk.END)
            if opt_retry:
                self.select_path()

    def rename(self):
        if self.opt_menu is not None:
            option = self.opt_menu.get('active').strip()
            fpath = self.root_path[-1]
            name = self.entry_3.get(1.0, tk.END).replace("\n", "")
            if name != "":
                try:
                    os.rename(f'{fpath}/{option}', f'{fpath}/{name}')
                    self.changes[option] = name
                    print(self.changes)
                    self.entry_3.delete(1.0, tk.END)
                    self.refresh_options()
                except FileExistsError:
                    messagebox.showwarning('Duplicate Files', "Cannot rename as file with same name is found")
            else:
                messagebox.showwarning('No File Name', "Please Provide a File Name")

    def print_widget(self):
        dir_path: str = self.entry_1.get(1.0, tk.END)
        file_ext: str = self.entry_2.get(1.0, tk.END)
        file_ext = file_ext.replace('\n', "")
        dir_op = None
        if dir_path == "\n":
            if self.directory != "":
                dir_op = self.scan_dir(self.directory, file_ext)
                self.root_path.append(self.directory)

            else:
                messagebox.showwarning('No Directory', "Please Provide a directory")
                self.select_path()
        else:
            dir_path = dir_path.replace("\n", "/")
            dir_op = self.scan_dir(dir_path, file_ext)
            self.root_path.append(dir_path)
        self.output.config(state="normal")
        self.output.delete(1.0, tk.END)
        print(dir_path)
        if dir_op is not None and len(dir_op) != 0:
            self.provide_option(dir_op)
            for tex in dir_op:
                if tex != 'changes.log':
                    self.output.insert(tk.END, tex+'\n')
            self.output.config(state="disabled")
            self.refresh_options()

    def refresh_options(self):
        dir_op = self.scan_dir(self.root_path[-1], self.entry_2.get(1.0, tk.END).replace("\n", ""))
        self.provide_option(dir_op)

    def write_changes(self):
        if len(self.changes) != 0 and len(self.root_path) != 0:
            mode = 'a' if os.path.exists(self.root_path[-1] + '/changes.log') else 'w'
            log_file = open(self.root_path[-1] + '/changes.log', mode)
            for key, value in self.changes.items():
                log_file.write(f'{key} --> {value}\n')

    def add_widgets(self):
        self.win.mainloop()


obj = RenameTool('Rename Tool')
obj.add_widgets()
atexit.register(obj.write_changes)
