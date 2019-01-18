"""Python editor for Pseudocode I have to use

My first attempt of a tkinter app with "normal" surroundings.
Current features:
    - syntax highlighting
    - insert blocks and special characters
    - export highlighted syntax as HTML (with bugs)
that's it."""

import tkinter as tk
import tkinter.messagebox as tk_msg
import tkinter.filedialog as tk_fdia
import threading
import os
import sys
import string
import json
import re
import html
import time
from collections import OrderedDict

sys.stderr = open('error.log', 'a')

MARKUP = {
    'comment': ['//.*?\n', ],
    'keyword': ['if', 'while', 'and', 'or', 'return', 'else',
                'not', 'for', 'to', 'from', 'step'],
    'type': ['int', 'float', 'real', 'bool', 'str',],
    'header': ['def', 'VARS', '@\\w+', ],
    'builtin': ['write', 'read', 'true', 'false', 'random', 'sqrt'],
    'string': [r'"(.*?[^\\])*?"', ],
}
COLORS = OrderedDict({  # important for markup layers
    'comment': 'grey',
    'keyword': 'orange',
    'type': 'purple',
    'header': 'red',
    'builtin': 'green',
    'string': 'lime',
})

regex_unesc_quote_html = re.compile(r'[^\\]'+html.escape('"'))  # &quot; and &#34; and &#x27; possible

try:
    f = open('editor_markup.json', encoding='UTF-8')
except FileNotFoundError:
    pass
else:
    try:
        add = json.load(f)
    except json.JSONDecodeError as e:
        tk_msg.showerror('JSON config',
                         'Error while reading editor_config.json:\n'+str(e))
        add = {}
    for k, v in add.items():
        if k in MARKUP:
            MARKUP[k].extend(v)
    if 'package' in add:
        for v in add['package']:
            MARKUP['builtin'].append(v+r'\.\w+')
    f.close()

for v in MARKUP.values():
    for i, p in enumerate(v):
        if not any(p.endswith(w) for w in list(string.whitespace)+['\\W']):
            v[i] = p+'(\\W|\n)'  # last resort for including newlines (see https://tcl.tk/man/tcl8.5/TkCmd/text.htm#M120 and https://tcl.tk/man/tcl8.5/TclCmd/re_syntax.htm#M88)


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
        self._markup_start = mks = time.time()
        time.sleep(0.5)
        if self._markup_start != mks:  # don't run everything during fast typing
            return
        for tag, patterns in MARKUP.items():
            self.tag_remove(tag, '1.0', 'end')
            for pattern in patterns:
                threading.Thread(target=self.markup_one, args=(pattern, tag)).start()

    def markup_one(self, pattern, tag):
        end = '1.0'
        count = tk.IntVar()
        while True:
            start = self.search(pattern, end, 'end', count=count, regexp=True)
            if start == '' or count.get() == 0:
                return
            end = '%s+%sc' % (start, count.get()-1)
            if self.get('{}-1c'.format(start), start) not in string.ascii_letters or start == '1.0':
                self.tag_add(tag, start, end)

    def reset(self):
        self.had_edit = False
        self.delete('1.0', 'end')
        set_title()


def to_html(text):
    text = text.join(['\x00']*2)
    out = html.escape(text)
    for k, color in COLORS.items():
        for p in MARKUP[k]:
            regex = re.compile('\\W{}'.format(html.escape(p)))
            current_position = 0
            m = regex.search(out)
            while m is not None:
                start = m.start()+1+current_position
                end = m.end()+current_position-1
                print(m, current_position)
                if not (len(regex_unesc_quote_html.findall(out[:start])) % 2  # inside a string
                        and len(regex_unesc_quote_html.findall('\x00'+out[end:])) % 2):  # '\x00' to still capt. if we are at the end
                    out = '{before}<span style="color: {color};">{inside}</span>{after}'.format(
                        before=out[:start], color=color, inside=m.group()[1:-1], after=out[end:])
                    current_position += 30+len(color)  # tag length
                print()
                current_position += m.end()
                m = regex.search(out[current_position:])
    return ('<pre><code style="font-weight: bold;">%s</code></pre>' % (out,)).replace('\x00', '')


def export_as_html(e=None):
    if None is tk_msg.askokcancel('Export as HTML', 'Please wait while we convert your file to HTML...'):
        return
    html = to_html(textbox.get(0.0, 'end'))
    if file is None:
        cur_file = 'New File'
    else:
        cur_file = '{} - {}'.format(file.split(os.path.sep)[-1].rsplit('.', 1)[0], file)
    filename = tk_fdia.asksaveasfilename(filetypes=(('HTML file', '.html'),),
                                         defaultextension='.html', default=file.split('.')[:-1])
    if not filename:
        return
    filename = os.path.sep.join(filename.split('/'))
    with open(filename, 'w', encoding='UTF-8') as f:
        f.write('<!DOCTYPE html><html><head>')
        f.write('<meta charset="utf-8"><title>')
        f.write(cur_file)
        f.write('</title></head><body>')
        f.write(html)
        f.write('</body></html>')
    tk_msg.showinfo('Saved file', 'The file has successfully been exported and saved')

def save_file():
    if file is not None:
        with open(file, 'w', encoding='UTF-8') as f:
            f.write(textbox.get('1.0', 'end'))
        textbox.had_edit = False
        set_title()
    else:
        save_file_as()

def save_file_as():
    global file
    f = os.path.sep.join(
        tk_fdia.asksaveasfilename(filetypes=(('PSEUDO files', '.pseudo'),), defaultextension='.pseudo').split('/'))
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
        save = tk_msg.askyesnocancel('Save on exit?', 'Should the file be saved before exiting?')
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
menu.add_command(label='Export as HTML', command=export_as_html, underline=0)
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
