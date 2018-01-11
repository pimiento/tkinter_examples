#!/usr/bin/env python3
# coding: utf-8

# Simple text editor using Tkinter
import os
import tkinter.filedialog
import tkinter.messagebox
from tkinter import (
    Tk, Menu, PhotoImage, Frame, Text, Scrollbar,
    IntVar, StringVar, Toplevel, Label, Entry, Checkbutton, Button,
    INSERT
)

PROGRAM_NAME = " Footprint Editor "
DPATH = "./Tkinter GUI Application Development Blueprints_code/B04945_02_Code/"
FILE_NAME = None

root = Tk()
root.geometry('350x350')

BEGIN = '1.0'
END = 'end'
SELECTION_TAG = 'sel'
MATCH_TAG = 'match'
HIGHLIGHT_TAG = 'active_line'


def change_theme(event=None):
    selected_theme = theme_choice.get()
    fg_bg_colors = color_schemes.get(selected_theme)
    fg_color, bg_color = fg_bg_colors.split('.')
    content_text.config(
        background=bg_color, fg=fg_color
    )


def show_popup_menu(event):
    popup_menu.tk_popup(event.x_root, event.y_root)


def show_cursor_info_bar():
    show_cursor_info_checked = show_cursor_info.get()
    if show_cursor_info_checked:
        cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')
    else:
        cursor_info_bar.pack_forget()


def update_cursor_info_bar(event=None):
    row, col = content_text.index(INSERT).split('.')
    line_num, col_num = str(int(row)), str(int(col) + 1)
    infotext = "Line: {0} | Column {1}".format(line_num, col_num)
    cursor_info_bar.config(text=infotext)


def toggle_highlight(event=None):
    if to_highlight_line.get():
        highlight_line()
    else:
        undo_highlight()


def highlight_line(interval=100):
    content_text.tag_remove(HIGHLIGHT_TAG, BEGIN, END)
    content_text.tag_add(
        HIGHLIGHT_TAG, "insert linestart", "insert lineend+1c"
    )
    content_text.after(interval, toggle_highlight)


def undo_highlight():
    content_text.tag_remove(HIGHLIGHT_TAG, BEGIN, END)


def on_content_changed(event=None):
    update_line_numbers()
    update_cursor_info_bar()


def update_line_numbers(event=None):
    if show_line_number.get():
        line_numbers = get_line_numbers()
    else:
        line_numbers = ''
    line_number_bar.config(state='normal')
    line_number_bar.delete(BEGIN, END)
    line_number_bar.insert(BEGIN, line_numbers)
    line_number_bar.config(state='disabled')


def get_line_numbers():
    output = ''
    row, _ = content_text.index(END).split('.')
    for i in range(1, int(row)):
        output += str(i) + '\n'
    return output


def display_about_messagebox(event=None):
    tkinter.messagebox.showinfo(
        "About", PROGRAM_NAME + "\nЯбать ты лох!"
    )


def display_help_messagebox(event=None):
    tkinter.messagebox.showinfo(
        "Help", "Help is there:\nhttps://pimiento.github.io", icon='question'
    )


def exit_editor(event=None):
    if tkinter.messagebox.askokcancel("Quit?", "Really quit?"):
        root.destroy()


# new_file, open_file, save, save_as
def new_file(event=None):
    root.title("Untitled")
    global FILE_NAME
    FILE_NAME = None
    content_text.delete(BEGIN, END)
    on_content_changed()


def open_file(event=None):
    input_file_name = tkinter.filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")]
    )
    if input_file_name:
        global FILE_NAME
        FILE_NAME = input_file_name
        root.title('{} - {}'.format(os.path.basename(FILE_NAME), PROGRAM_NAME))
        content_text.delete(BEGIN, END)
        with open(FILE_NAME) as _file:
            content_text.insert(BEGIN, _file.read())
        on_content_changed()


def write_to_file(file_name):
    try:
        content = content_text.get(BEGIN, END)
        with open(file_name, 'w') as _file:
            _file.write(content)
    except IOError:
        pass


def save_as(event=None):
    input_file_name = tkinter.filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")]
    )
    if input_file_name:
        global FILE_NAME
        FILE_NAME = input_file_name
        write_to_file(FILE_NAME)
        root.title('{} - {}'.format(os.path.basename(FILE_NAME), PROGRAM_NAME))
    return "break"


def save(event=None):
    global FILE_NAME
    if FILE_NAME is None:
        save_as()
    else:
        write_to_file(FILE_NAME)
    return "break"


def select_all(event=None):
    content_text.tag_add(SELECTION_TAG, BEGIN, END)
    return "break"


def find_text(event=None):
    search_toplevel = Toplevel(root)
    search_toplevel.title('Find Text')
    search_toplevel.transient(root)
    search_toplevel.resizable(False, False)
    Label(search_toplevel, text="Find All:").grid(row=0, column=0, sticky='e')
    search_entry_widget = Entry(search_toplevel, width=25)
    search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value = IntVar()
    Checkbutton(
        search_toplevel, text='Ignore Case', variable=ignore_case_value
    ).grid(row=0, column=3, sticky='e', padx=2, pady=2)
    Button(
        search_toplevel, text='Find All', underline=0,
        command=lambda: search_output(
            search_entry_widget.get(), ignore_case_value.get(),
            content_text, search_toplevel, search_entry_widget
        )
    ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

    def close_search_window():
        content_text.tag_remove(MATCH_TAG, BEGIN, END)
        search_toplevel.destroy()
    search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)


def search_output(needle, is_icase, content_text, search_toplevel, search_box):
    content_text.tag_remove(MATCH_TAG, BEGIN, END)
    matches_found = 0
    if needle:
        start_pos = BEGIN
        while True:
            start_pos = content_text.search(
                needle, start_pos, nocase=is_icase, stopindex=END
            )
            if not start_pos:
                break
            end_pos = '{}+{}c'.format(start_pos, len(needle))
            content_text.tag_add(MATCH_TAG, start_pos, end_pos)
            matches_found += 1
            start_pos = end_pos
        content_text.tag_config(
            MATCH_TAG, foreground='red', background='yellow'
        )
    search_box.focus_set()
    search_toplevel.title('{} matches found'.format(matches_found))


def base_event(name):
    def generate(*args, **kwargs):
        content_text.event_generate("<<"+name+">>")
        on_content_changed()
        return "break"
    generate.__name__ = name.lower()
    return generate


cut = base_event("Cut")
copy = base_event("Copy")
paste = base_event("Paste")
undo = base_event("Undo")
redo = base_event("Redo")


new_file_icon = PhotoImage(file=os.path.join(DPATH, 'icons/new_file.gif'))
open_file_icon = PhotoImage(file=os.path.join(DPATH, 'icons/open_file.gif'))
save_file_icon = PhotoImage(file=os.path.join(DPATH, 'icons/save.gif'))
cut_icon = PhotoImage(file=os.path.join(DPATH, 'icons/cut.gif'))
copy_icon = PhotoImage(file=os.path.join(DPATH, 'icons/copy.gif'))
paste_icon = PhotoImage(file=os.path.join(DPATH, 'icons/paste.gif'))
undo_icon = PhotoImage(file=os.path.join(DPATH, 'icons/undo.gif'))
redo_icon = PhotoImage(file=os.path.join(DPATH, 'icons/redo.gif'))

# Adding Menubar in the window
menu_bar = Menu(root)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='New', accelerator='Ctrl-N', compound='left',
                      image=new_file_icon, underline=0, command=new_file)
file_menu.add_command(label='Open', accelerator='Ctrl-O', compound='left',
                      image=open_file_icon, underline=0, command=open_file)
file_menu.add_command(label='Save', accelerator='Ctrl-S', compound='left',
                      image=save_file_icon, underline=0, command=save)
file_menu.add_command(
    label='Save as', accelerator='Shift+Ctrl+S', command=save_as
)
file_menu.add_separator()
file_menu.add_command(label='Exit', accelerator='Alt+F4', command=exit_editor)
menu_bar.add_cascade(label='File', menu=file_menu, underline=0)

edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(label='Undo', accelerator='Ctrl+Z',
                      compound='left', image=undo_icon, command=undo)
edit_menu.add_command(label='Redo', accelerator='Ctrl+Y',
                      compound='left', image=redo_icon, command=redo)
edit_menu.add_separator()
edit_menu.add_command(label='Cut', accelerator='Ctrl+X',
                      compound='left', image=cut_icon, command=cut)
edit_menu.add_command(label='Copy', accelerator='Ctrl+C',
                      compound='left', image=copy_icon, command=copy)
edit_menu.add_command(label='Paste', accelerator='Ctrl+V',
                      compound='left', image=paste_icon, command=paste)
edit_menu.add_separator()
edit_menu.add_command(
    label='Find', underline=0, accelerator='Ctrl+F', command=find_text
)
edit_menu.add_separator()
edit_menu.add_command(
    label='Select All', underline=7, accelerator='Ctrl+A',
    command=select_all
)
menu_bar.add_cascade(label='Edit', menu=edit_menu, underline=0)

# View Menuwith Checkbutton, Radiobutton and Cascade menu-items under it
view_menu = Menu(menu_bar, tearoff=0)
# do or don't show line number
show_line_number = IntVar()
show_line_number.set(1)
view_menu.add_checkbutton(
    label='Show Line Number', variable=show_line_number,
    command=on_content_changed
)
# do or don't show cursor location at bottom
show_cursor_info = IntVar()
show_cursor_info.set(1)
view_menu.add_checkbutton(
    label='Show Cursor Location at Bottom', variable=show_cursor_info,
    command=show_cursor_info_bar
)
# do or don't highlight current line
to_highlight_line = IntVar()
view_menu.add_checkbutton(
    label='Highlight Current Line', onvalue=1,
    offvalue=0, variable=to_highlight_line, command=toggle_highlight
)
# choose themes
themes_menu = Menu(menu_bar, tearoff=0)
view_menu.add_cascade(label='Themes', menu=themes_menu)
color_schemes = {               # Name: foreground_color.background_color
    'Default': '#000000.#FFFFFF',
    'Greygarious': '#83406A.#D1D4D1',
    'Aquamarine': '#5B8340.#D1E7E0',
    'Bold Beige': '#4B4620.#FFF0E1',
    'Cobalt Blue': '#ffffBB.#3333aa',
    'Olive Green': '#D1E7E0.#5B8340',
    'Night Mode': '#FFFFFF.#000000',
}
theme_choice = StringVar()
theme_choice.set('Default')
for k in sorted(color_schemes):
    themes_menu.add_radiobutton(
        label=k, variable=theme_choice, command=change_theme
    )

menu_bar.add_cascade(label='View', menu=view_menu, underline=0)

about_menu = Menu(menu_bar, tearoff=0)
about_menu.add_command(label='About', command=display_about_messagebox)
about_menu.add_command(label='Help', command=display_help_messagebox)
menu_bar.add_cascade(label='About', menu=about_menu)

root.config(menu=menu_bar)

# add top shortcut bar & left line number bar
shortcut_bar = Frame(root, height=25, background='light sea green')
shortcut_bar.pack(expand='no', fill='x')
icon_cmd = (new_file, open_file, save, cut, copy, paste, undo, redo, find_text)
for cmd in icon_cmd:
    tool_bar_icon = PhotoImage(
        file=os.path.join(DPATH, 'icons', '{}.gif'.format(cmd.__name__))
    )
    tool_bar = Button(shortcut_bar, image=tool_bar_icon, command=cmd)
    tool_bar.image = tool_bar_icon
    tool_bar.pack(side='left')

line_number_bar = Text(
    root, width=4, padx=3, takefocus=0, border=0,
    background='khaki', state='disabled', wrap='none'
)
line_number_bar.pack(side='left', fill='y')

# add the main context Text widget and Scrollbar widget
content_text = Text(root, wrap='word', undo=1)
content_text.pack(expand='yes', fill='both')
scroll_bar = Scrollbar(content_text)
content_text.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=content_text.yview)
scroll_bar.pack(side='right', fill='y')
# add cursor info label
cursor_info_bar = Label(content_text, text='Line: 1 | Column: 1')
cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')

# key bindings
content_text.bind('<Control-y>', redo)
content_text.bind('<Control-Y>', redo)
content_text.bind('<Control-A>', select_all)
content_text.bind('<Control-a>', select_all)
content_text.bind('<Control-F>', find_text)
content_text.bind('<Control-f>', find_text)
content_text.bind('<Control-N>', new_file)
content_text.bind('<Control-n>', new_file)
content_text.bind('<Control-O>', open_file)
content_text.bind('<Control-o>', open_file)
content_text.bind('<Control-S>', save)
content_text.bind('<Control-s>', save)
content_text.bind('<KeyPress-F1>', display_help_messagebox)
content_text.bind('<Any-KeyPress>', on_content_changed)

content_text.tag_configure(HIGHLIGHT_TAG, background='ivory2')

popup_menu = Menu(content_text)
for cmd in (cut, copy, paste, undo, redo):
    popup_menu.add_command(label=cmd.__name__, compound='left', command=cmd)
popup_menu.add_separator()
popup_menu.add_command(label='Select All', underline=7, command=select_all)
content_text.bind('<Button-3>', show_popup_menu)
content_text.focus_set()

root.title(PROGRAM_NAME)
root.protocol("WM_DELETE_WINDOW", exit_editor)
root.mainloop()
