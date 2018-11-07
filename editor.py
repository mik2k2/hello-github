"""Python editor for Pseudocode I have to use

My first attempt of a tkinter app with "normal" surroundings.
Current features:
    - syntax highlighting
    - insert blocks and special characters
that's it."""

import tkinter as tk
import tkinter.messagebox as tk_msg
import tkinter.filedialog as tk_fdia
import threading
import os
import sys
import string
import json

MARKUP = {
    'keyword': ['if', 'while', 'and', 'or', 'return', 'else', 'elif', 'not', ],
    'type': sum(([s, s.upper()] for s in
                 ('int', 'integer', 'boolean', 'float', 'real', 'bool',
                  'void', 'str', 'string')), []),
    'header': ['FUNC', 'PARAMS', 'VARS', 'CODE', 'RETURN', '#\\w+', ],
    'builtin': ['write', 'read', 'random', 'true', 'false', ],
    'string': ['".*?"', ],
    'comment': ['//.*?\n', ],
}
COLORS = {
    'keyword': 'orange',
    'type': 'purple',
    'header': 'red',
    'builtin': 'green',
    'string': 'lime',
    'comment': 'grey',
}

try:
    f = open('editor_markup.json', encoding='UTF-8')
except FileNotFoundError:
    pass
else:
    add = json.load(f)
    for k, v in add.items():
        if k in MARKUP:
            MARKUP[k].extend(v)
    if 'package' in add:
        for v in add['package']:
            MARKUP['builtin'].append(v+r'\.\w+')
    f.close()


class CodeText(tk.Text):
    TAB = ' '*4

    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, undo=True, **kwargs)
        self.had_edit = False
        for name, fg in COLORS.items():
            self.tag_config(name, foreground=fg)
        self.bind('<Tab>', self._tab)
        self.bind('<Shift-Tab>', self._undo_tab)
        self.bind('<Return>', self._enter)
        self.bind('<Key>', self.keypress)

    def _tab(self, event):
        self.keypress()
        self.insert('insert', self.TAB)
        return 'break'

    def _enter(self, event):
        self.keypress()
        prev_line = self.get('1.0', 'insert').split('\n')[-1]
        self.insert('insert', '\n'+' '*(len(prev_line)-len(prev_line.lstrip())))
        if prev_line.endswith(':'):
            self._tab(None)
        self.see('insert')
        return 'break'

    def _undo_tab(self, event=None):
        if self.get('insert-4c', 'insert') == self.TAB:
            self.keypress()
            self.delete('insert-4c', 'insert')
        return 'break'

    def keypress(self, event=None):
        if event is None or event.keysym.lower() in list(string.ascii_letters)+'tab backspace " ) ( space'.split():
            if not self.had_edit:
                self.had_edit = True
                set_title()
            self.markup()

    def markup(self, event=None):
        for tag, patterns in MARKUP.items():
            self.tag_remove(tag, '1.0', 'end')
            for pattern in patterns:
                threading.Thread(target=self.markup_one, args=(pattern+'(\n|\\W)', tag)).start()

    def markup_one(self, pattern, tag, regexp=True):
        end = '1.0'
        count = tk.IntVar()
        while True:
            start = self.search(pattern, end, 'end', count=count, regexp=regexp)
            if start == '' or count.get() == 0:
                return
            end = f'{start}+{count.get()-1}c'
            if self.get('{}-1c'.format(start), start) not in string.ascii_letters or start == '1.0':
                self.tag_add(tag, start, end)

    def reset(self):
        self.had_edit = False
        self.delete('1.0', 'end')
        set_title()


def save_file():
    if file is not None:
        with open(file, 'w', encoding='UTF-8') as f:
            f.write(textbox.get('1.0', 'end'))
        textbox.had_edit = False
        set_title()
    else:
        tk_msg.showwarning('No file opened.', 'Select Save As')

def save_file_as():
    global file
    f = tk_fdia.asksaveasfilename(filetypes=(('PSEUDO files', '.pseudo'),), defaultextension='.pesudo').replace('/', '\\')
    if not f:
        return
    file = f
    save_file()

def open_file(path=None):
    global file
    if path is None:
        f = tk_fdia.askopenfilename(filetypes=(('PSEUDO files', '.pseudo'), ('all files', '.*'))).replace('/', os.path.sep)
        if not f:
            return
        file = f
    else:
        file = path
    set_title()
    textbox.reset()
    with open(file, encoding='UTF-8') as f:
        textbox.insert('1.0', f.read())
        textbox.delete('end-1c', 'end')
        textbox.markup(None)

def new_file():
    global file
    file = None
    textbox.reset()

def set_title():
    if file is None:
        root.title('New File')
    else:
        t = '* ' if textbox.had_edit else ''
        root.title(t+' - '.join((os.path.split(file)[-1], file)))

def on_close():
    if textbox.had_edit:
        save =  tk_msg.askyesnocancel('Save on exit?', 'Should the file be saved before exiting?')
        if save is None:
            return
        if save:
            if file is not None:
                save_file()
            else:
                save_file_as()
    root.destroy()



def insert(char):
    return lambda e=0: (textbox.insert('insert', char), textbox.markup())  # could be bound and get an event

root = tk.Tk()

root.bind('<Control-s>', lambda e: save_file())
root.bind('<Control-e>', insert(' ⬅ '))
root.protocol('WM_DELETE_WINDOW', on_close)

menubar = tk.Menu(root, relief='sunken')
menu = tk.Menu(menubar, tearoff=0)
menu.add_command(label='New', command=new_file, underline=0)
menu.add_command(label='Open', command=open_file, underline=0)
menu.add_command(label='Save  Ctrl-S', command=save_file, underline=0)
menu.add_command(label='Save As', command=save_file_as, underline=5)
menubar.add_cascade(label='File', menu=menu, underline=0, )
menu = tk.Menu(menubar, tearoff=0)
menu1 = tk.Menu(menu, tearoff=0)
menu1.add_command(label='⬅ - assign (Ctrl-e)', command=insert(' ⬅ '), underline=4)
menu1.add_command(label='≠ - unequals', command=insert(' ≠ '), underline=4)
menu.add_cascade(label='Char/Sign', menu=menu1, underline=0)
menu1 = tk.Menu(menu, tearoff=0)
for head in MARKUP['header']:
    menu1.add_command(label=head, command=insert(head+':'), underline=0)
menu.add_cascade(label='header', menu=menu1, underline=0)
menubar.add_cascade(label='Insert', menu=menu, underline=0)

text_frame = tk.Frame(root)
textbox = CodeText(text_frame, height=30)
text_scroll = tk.Scrollbar(text_frame, orient='vertical', command=textbox.yview)

file = ''  # stop PyCharm complaints; set as global in methods
if len(sys.argv) > 1:
    open_file(sys.argv[1])
else:
    file = None
    root.title('New File')

root.config(menu=menubar)
textbox.pack(side='left', fill='both', expand=True)
text_scroll.pack(side='right', fill='y')
text_frame.pack(fill='both', expand=True)

tk.mainloop()
