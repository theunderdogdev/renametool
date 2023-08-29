import os
from pathlib import Path
from os import name
from tkinter import filedialog, StringVar, BooleanVar
from tkinter import Event
from tkinter.ttk import (
    Entry,
    Button,
    Labelframe,
    Frame,
    Checkbutton,
    Treeview,
    Scrollbar,
    Radiobutton,
)
from tkinter import font, END, Text, Tk, BOTH, X
import re
import ctypes
from mimetypes import init, guess_type
from rich import traceback, print
traceback.install()


FONT_SIZE = 16

if name == "nt":
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    FONT_SIZE = 11

init()
COLORS = {
    "slate400": "#94a3b8",
    "red600": "#dc2626",
    "amber400": "#fbbf24",
    "emerald500": "#10b981",
    "sky500": "#0ea5e9",
}

"""
color schemes for file types
music -> emerald500
"""

class RenameTool:
    def __init__(self, title) -> None:
        self.__WINDOW = Tk()
        self.__WINDOW.title(title)
        self.__WINDOW.geometry("1000x800")
        self.__WINDOW.tk.call("source", "azure.tcl")
        self.__WINDOW.tk.call("set_theme", "dark")
        new_font = font.nametofont("TkDefaultFont")
        new_font.configure(family="Consolas", size=FONT_SIZE)
        self.__WINDOW.option_add("*Font", new_font)
        self.__WINDOW.columnconfigure(0, weight=1, uniform="horz")
        self.__WINDOW.columnconfigure(1, weight=1, uniform="horz")
        self.__WINDOW.rowconfigure(0, weight=1, uniform="horz")

        self.field_frame = Frame(self.__WINDOW, name="field_frame", relief="solid")
        self.visual_frame = Frame(self.__WINDOW, name="visual_frame", relief="solid")
        self.field_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.visual_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.field_frame.columnconfigure(0, weight=1, uniform="horz")
        self.__file_names = []
        self.visual_frame.columnconfigure(0, weight=1, uniform="vert")
        self.visual_frame.rowconfigure(0, weight=1, uniform="vert")
        self.visual_frame.rowconfigure(1, weight=1, uniform="vert")

        self.label_frames: dict[str, Labelframe] = {}
        self.radio_group: dict[str, dict[str, Radiobutton]] = {}
        self.__str_vars: dict[str, StringVar] = {
            "path": StringVar(),
            "filter": StringVar(),
            "rename": StringVar(),
            "options": StringVar(value="#newpatt"),
            "replace": StringVar(),
        }
        self._file_list: Treeview
        self.__bool_vars: dict[str, BooleanVar] = {
            "use_filter_regex": BooleanVar(value=False),
            "use_rename_regex": BooleanVar(value=False),
        }

    def __create_gui(self):
        # path --------------------
        self.label_frames["path"] = Labelframe(self.field_frame, text="Path")
        path_entry = Entry(
            self.label_frames["path"],
            textvariable=self.__str_vars["path"],
            foreground="#cbd5e1",
        )
        path_entry.bind("<1>", lambda _: self.__browse())
        path_entry.config(state="disabled")
        path_entry.pack(padx=10, pady=5, expand=1, fill=X)
        self.confirm_btn = Button(
            self.label_frames["path"],
            text="Confirm",
            command=self.on_path_confirm,
            style="TButton",
        )
        self.confirm_btn.config(state="disabled")
        self.confirm_btn.pack(padx=10, pady=5, anchor="se", side="right")
        self.label_frames["path"].grid(row=0, column=0, padx=10, pady=5, sticky="new")
        # path --------------------

        # filter --------------------
        self.label_frames["filter"] = Labelframe(self.field_frame, text="Filter")
        filter_entry = Entry(
            self.label_frames["filter"], textvariable=self.__str_vars["filter"]
        )
        filter_entry.pack(padx=10, pady=5, expand=1, fill=X)
        use_filter_reg = Checkbutton(
            self.label_frames["filter"],
            text="Use Regex",
            variable=self.__bool_vars["use_filter_regex"],
            command=self.on_use_regex,
        )
        use_filter_reg.pack(padx=10, pady=10, anchor="sw", side="left")
        apply_filter = Button(
            self.label_frames["filter"], text="Apply", command=self._apply_filter
        )
        apply_filter.pack(padx=10, pady=5, anchor="se")
        self.label_frames["filter"].grid(row=1, column=0, padx=10, pady=5, sticky="new")
        # filter --------------------

        # rename --------------------
        self.label_frames["rename"] = Labelframe(self.field_frame, text="Rename")
        self.label_frames["rename"].columnconfigure(0, weight=1, uniform="rename")
        self.new_name_entry = Entry(
            self.label_frames["rename"], textvariable=self.__str_vars["rename"]
        )
        self.replace_char = Entry(
            self.label_frames["rename"], textvariable=self.__str_vars["replace"]
        )
        self.new_name_entry.config(state="disabled")
        self.new_name_entry.grid(padx=10, pady=10, row=0, column=0, sticky="ew")
        self.replace_char.grid(padx=10, pady=10, row=1, column=0, sticky="ew")
        self.replace_char.grid_remove()
        self.label_frames["options"] = Labelframe(
            self.label_frames["rename"], text="Options"
        )
        self.label_frames["options"].columnconfigure(0, weight=1, uniform="optrad")
        self.label_frames["options"].columnconfigure(1, weight=1, uniform="optrad")
        self.radio_group["options"] = {}
        self.radio_group["options"]["add_prefix"] = Radiobutton(
            self.label_frames["options"],
            text="Add Prefix",
            value="#addprefix",
            variable=self.__str_vars["options"],
            state="disabled",
            command=self.__on_replace_select,
        )
        self.radio_group["options"]["remove_prefix"] = Radiobutton(
            self.label_frames["options"],
            text="Remove Prefix",
            value="#rmprefix",
            variable=self.__str_vars["options"],
            state="disabled",
            command=self.__on_replace_select,
        )
        self.radio_group["options"]["add_suffix"] = Radiobutton(
            self.label_frames["options"],
            text="Add Suffix",
            value="#addsuffix",
            variable=self.__str_vars["options"],
            state="disabled",
            command=self.__on_replace_select,
        )
        self.radio_group["options"]["remove_suffix"] = Radiobutton(
            self.label_frames["options"],
            text="Remove Suffix",
            value="#rmsuffix",
            variable=self.__str_vars["options"],
            state="disabled",
            command=self.__on_replace_select,
        )
        self.radio_group["options"]["replace"] = Radiobutton(
            self.label_frames["options"],
            text="Replace",
            value="#replace",
            variable=self.__str_vars["options"],
            state="disabled",
            command=self.__on_replace_select,
        )
        self.radio_group["options"]["new_name_patt"] = Radiobutton(
            self.label_frames["options"],
            text="New name pattern",
            value="#newpatt",
            variable=self.__str_vars["options"],
            state="disabled",
            command=self.__on_replace_select,
        )
        self.apply_option = Button(
            self.label_frames["options"],
            text="Apply",
            state="disabled",
            command=self.__preview,
        )
        self.confirm_rename = Button(
            self.label_frames["options"], text="Confirm Rename", state="disabled"
        )
        self.clear_new = Button(
            self.label_frames["options"], text="Clear New Names", command=lambda: self._clear_child_items(self._renamed_list)
        )

        self.radio_group["options"]["add_prefix"].grid(
            row=0, column=0, pady=5, padx=15, sticky="ew"
        )
        self.radio_group["options"]["remove_prefix"].grid(
            row=1, column=0, pady=5, padx=15, sticky="ew"
        )
        self.radio_group["options"]["add_suffix"].grid(
            row=2, column=0, pady=5, padx=15, sticky="ew"
        )
        self.radio_group["options"]["remove_suffix"].grid(
            row=3, column=0, pady=5, padx=15, sticky="ew"
        )
        self.radio_group["options"]["replace"].grid(
            row=4, column=0, pady=5, padx=15, sticky="ew"
        )
        self.radio_group["options"]["new_name_patt"].grid(
            row=5, column=0, pady=5, padx=15, sticky="ew"
        )
        self.apply_option.grid(row=3, column=1, pady=5, padx=15, sticky="ew")
        self.confirm_rename.grid(row=4, column=1, pady=5, padx=15, sticky="ew")
        self.clear_new.grid(row=5, column=1, pady=5, padx=15, sticky="ew")
        self.label_frames["options"].grid(
            padx=10, pady=10, row=2, column=0, sticky="ew"
        )
        self.label_frames["rename"].grid(row=3, column=0, padx=10, pady=5, sticky="new")
        # rename --------------------

        # trees ---------------------
        file_container = Frame(self.visual_frame, name="file_container")
        file_container.columnconfigure(0, weight=1, uniform="file_tree")
        file_container.rowconfigure(0, weight=1, uniform="file_tree")

        self._file_list = Treeview(
            file_container, columns=("file_names"), show="headings"
        )
        self._file_list.heading("file_names", text="File Name")
        self._file_list.bind("<<TreeviewSelect>>", self._on_file_list_select)
        tree_scroll = Scrollbar(file_container, orient="vertical")
        tree_scroll.config(command=self._file_list.yview)
        self._file_list.config(yscrollcommand=tree_scroll.set)

        # tags --------------------
        self._file_list.tag_configure("audio", foreground=COLORS["sky500"])
        # tags --------------------

        self._file_list.grid(row=0, column=0, sticky="nsew")
        tree_scroll.grid(row=0, column=1, sticky="nse")
        file_container.grid(row=0, column=0, sticky="nsew")

        # renamed ------------------
        renamed_container = Frame(self.visual_frame, name="renamed_container")
        renamed_container.columnconfigure(0, weight=1, uniform="renamed_tree")
        renamed_container.rowconfigure(0, weight=1, uniform="renamed_tree")

        self._renamed_list = Treeview(
            renamed_container, columns=("new_names"), show="headings"
        )
        self._renamed_list.heading("new_names", text="New Names")
        self._renamed_list.grid(row=0, column=0, sticky="nsew")

        renamed_scroll = Scrollbar(renamed_container, orient="vertical")
        renamed_scroll.config(command=self._renamed_list.yview)
        self._renamed_list.config(yscrollcommand=renamed_scroll.set)

        # tags --------------------
        self._renamed_list.tag_configure("audio", foreground=COLORS["sky500"])
        # tags --------------------

        renamed_scroll.grid(row=0, column=1, sticky="nse")
        renamed_container.grid(row=1, column=0, sticky="nsew")

    def _on_file_list_select(self, evt: Event):
        tree_v: Treeview = evt.widget
        any_selected = len(tree_v.selection())
        btn_state = "normal" if any_selected != 0 else "disabled"
        for key, btn in self.radio_group["options"].items():
            btn.config(state=btn_state)
        if any_selected != 0:
            self.apply_option.config(state="normal")
            self.__bool_vars["use_rename_regex"].set(any_selected > 1)
            if any_selected > 1:
                self.__str_vars["options"].set('#addprefix')
            else:
                self.__str_vars["options"].set('#newpatt')

            self.new_name_entry.config(state="normal")
            self.label_frames["rename"].config(text=f"Rename - {any_selected} items")
            self.label_frames["options"].config(text=f"Options - {any_selected} items")
        else:
            self.apply_option.config(state="disabled")
            self.__bool_vars["use_rename_regex"].set(False)
            self.new_name_entry.config(state="disabled")
            self.label_frames["rename"].config(text="Rename")
            self.label_frames["options"].config(text="Options")
            self.__str_vars["options"].set('#newpatt')

    def __on_replace_select(self):
        if self.__str_vars["options"].get() == "#replace":
            self.replace_char.grid()
        else:
            self.replace_char.grid_remove()
    def _prefill(self, text: str)-> str:
        date_filler = re.compile(r".*(?<=\!d)(\{\d{4}-\d{2}-\d{2}\})?")
        
        return ""
    def __preview(self):
        option = self.__str_vars["options"].get()
        sel_count = len(self._file_list.selection())
        field_value = self.__str_vars["rename"].get()
        rename_list: list[tuple[str, str]] = []
        split_ext = re.compile(r"([^.]*)\.(.*)")
        new_patt_count = 1
        for item in self._file_list.selection():
            value = self._file_list.item(item).get("values")[0]
            match option:
                case "#addprefix":
                    rename_list.append((field_value + value, value))
                case "#rmprefix":
                    file_name = value.removeprefix(field_value)
                    rename_list.append((file_name, value))
                case "#addsuffix":
                    file_match = split_ext.match(value)
                    if file_match is not None:
                        file_name, ext = file_match.group(1), file_match.group(2)
                        file_name = file_name + field_value.rstrip() + "." + ext
                        rename_list.append((file_name, value))
                case "#rmsuffix":
                    file_match = split_ext.match(value)
                    if file_match is not None:
                        file_name, ext = file_match.group(1), file_match.group(2)
                        file_name = file_name.removesuffix(field_value) + "." + ext
                        rename_list.append((file_name, value))
                case "#replace":
                    file_match = split_ext.match(value)
                    if file_match is not None:
                        file_name, ext = file_match.group(1), file_match.group(2)
                        replace_val = self.__str_vars["replace"].get()
                        file_name = (
                            file_name.replace(field_value, replace_val) + "." + ext
                        )
                        rename_list.append((file_name, value))
                case "#newpatt":
                    file_match = split_ext.match(value)
                    if file_match is not None:
                        _, ext = file_match.group(1), file_match.group(2)
                        if sel_count > 1:
                            file_name = f"{field_value}-{new_patt_count}.{ext}"
                            new_patt_count += 1
                        else:
                            file_name = field_value + "." + ext
                        rename_list.append((file_name, value))
                        print(file_name)
                case _:
                    print("No Match")
        self.__add_to_preview(rename_list=rename_list)

    def __add_to_preview(self, rename_list: list[tuple[str, str]]):
        self._renamed_list.config(selectmode="extended")
        self._clear_child_items(self._renamed_list)
        for items in rename_list:
            self._renamed_list.insert("", END, values=items)
        self._renamed_list.config(selectmode="none")

    def _clear_child_items(self, _tree: Treeview):
        _tree.delete(*_tree.get_children())

    def __browse(self):
        file_path = filedialog.askdirectory()
        if file_path != "":
            self.__str_vars["path"].set(file_path)
            self.confirm_btn.config(state="normal")
        else:
            self.confirm_btn.config(state="disabled")
            print("Cancelled")

    def on_use_regex(self):
        print(self.__bool_vars["use_filter_regex"].get())

    def _get_path_contents(self, path: str | Path):
        return os.listdir(path=path)

    def add_to_filelist(self, files_names: list[str]):
        self._clear_child_items(self._file_list)
        for content in files_names:
            self._file_list.insert("", END, values=(content, ""), tags="audio")

    def _apply_filter(self):
        # print("yes")
        file_list = []
        filt_str = self.__str_vars["filter"].get()
        if self.__bool_vars["use_filter_regex"].get():
            filt_str_pat = re.compile(filt_str)
            file_list = list(
                filter(
                    lambda x: re.match(filt_str_pat, x) is not None, self.__file_names
                )
            )
        else:
            file_list = list(
                filter(lambda x: filt_str in x or filt_str == x, self.__file_names)
            )
        # print(file_list)
        self.add_to_filelist(file_list)

    def on_path_confirm(self):
        dir_path = self.__str_vars["path"].get()
        _path: Path = Path(dir_path)
        self.__file_names = self._get_path_contents(_path)
        self.add_to_filelist(self.__file_names)
        self.confirm_btn.config(state="disabled")

    def run(self):
        self.__create_gui()
        self.__WINDOW.mainloop()


if __name__ == "__main__":
    app = RenameTool(title="Rename Tool")
    app.run()
