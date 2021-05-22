import glob
import os
from tkinter import filedialog, messagebox
import tkinter as tk


class RenameTool:
    win = tk.Tk()
    root_path = []
    directory = ""

    def __init__(self, window_name):
        self.opt_menu = None
        self.win.title(window_name)
        self.win.config(bg='#00ff00')
        self.win.geometry('750x750')
        self.win.resizable(False, False)
        self.rename_label = tk.Label(text="New Name:", height=1, bg='#00ff00', fg='white', font=('Calibri', '15', 'bold'))
        self.rename_label.place(x=5, y=450)
        self.label = tk.Label(text="Enter Path:", height=1, bg='#00ff00', fg='white', font=('Calibri', '15', 'bold'))
        self.label.place(x=5, y=5)
        self.label2 = tk.Label(text="Extension:", height=1, bg='#00ff00', fg='white', font=('Calibri', '15', 'bold'))
        self.label2.place(x=5, y=45)
        self.output = tk.Text(width=75, height=15, padx=10, pady=5, font='Consolas', fg='green') # noqa
        self.output.place(x=25, y=145)
        self.entry_1 = tk.Text(width=75, height=1, padx=5, pady=5)
        self.entry_1.place(x=115, y=5)
        self.entry_2 = tk.Text(width=10, height=1, padx=5, pady=5)
        self.entry_2.place(x=115, y=45)
        self.button = tk.Button(text="Submit", height=2, width=10, command=self.print_widget)
        self.button.place(x=115, y=80)
        self.exit_but = tk.Button(text="Exit", height=2, width=15, command=lambda: exit(0))
        self.exit_but.place(x=350, y=600)
        self.rename = tk.Button(text="Rename", height=2, width=10, command=self.rename)
        self.rename.place(x=115, y=500)
        self.entry_3 = tk.Text(width=75, height=1, padx=5, pady=5)
        self.entry_3.place(x=115, y=450)
        self.get_dir_button = tk.Button(text="Open", height=2, width=10, command=self.select_path)
        self.get_dir_button.place(x=325, y=80)

    def provide_option(self, files):
        if self.opt_menu is not None:
            self.clear_prev()
        question = files
        self.tkvar = tk.StringVar(self.win) # noqa
        self.tkvar.set(question[0])
        self.opt_menu = tk.OptionMenu(self.win, self.tkvar, *question)
        self.opt_menu.config(font=('Consolas', '13'))
        self.opt_menu.place(x=350, y=500)

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
            option = self.tkvar.get()
            fpath = self.root_path[-1]
            name = self.entry_3.get(1.0,tk.END).replace("\n", "")
            if name != "":
                os.rename(f'{fpath}/{option}',f'{fpath}/{name}')
                self.entry_3.delete(1.0, tk.END)
                self.refresh_options()
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
            dir_path = dir_path.replace("\n", "")
            dir_op = self.scan_dir(dir_path, file_ext)
            self.root_path.append(dir_path)
        self.output.config(state="normal")
        self.output.delete(1.0, tk.END)
        if dir_op is not None and len(dir_op) != 0:
            self.provide_option(dir_op)
            for tex in dir_op:
                self.output.insert(tk.END, tex+'\n')
            self.output.config(state="disabled")

    def refresh_options(self):
        dir_op = self.scan_dir(self.root_path[-1], self.entry_2.get(1.0, tk.END).replace("\n",""))
        self.provide_option(dir_op)

    def add_widgets(self):
        self.win.mainloop()


obj = RenameTool('Rename Tool')
obj.add_widgets()
