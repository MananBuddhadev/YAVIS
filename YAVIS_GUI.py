try:
    import Tkinter
except ImportError:
    import tkinter

try:
    import ttk

    py3 = 0
except ImportError:
    import tkinter.ttk as ttk

    py3 = 1

import YAVIS


def vp_start_gui():
    """Starting point when module is the main routine."""
    global val, w, root
    root = tkinter.Tk()
    top = Container(root)
    YAVIS.init(root, top)
    root.mainloop()


w = None


def create_New_Toplevel_1(root, *args, **kwargs):
    """Starting point when module is imported by another program."""
    global w, w_win, rt
    rt = root
    w = tkinter.Toplevel(root)
    top = Container(w)
    YAVIS.init(w, top, *args, **kwargs)
    return w, top


def destroy_New_Toplevel_1():
    global w
    w.destroy()
    w = None


class Container:
    def __init__(self, top=None):
        """This class configures and populates the top-level window. Top is the top-level containing window."""
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#d9d9d9'  # X11 color: 'gray85'
        self.style = ttk.Style()
        if tkinter.sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.map('.', background=[('selected', _compcolor), ('active', _ana2color)])

        top.geometry("600x446+440+93")
        top.title("YAVIS")
        top.configure(background="#d9d9d9")

        self.Button1 = tkinter.Button(top)
        self.Button1.place(relx=0.85, rely=0.88, height=34, width=77)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(command=YAVIS.button__click)
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Send''')
        self.Button1.configure(width=77)

        self.scr49 = ScrolledText(top)
        self.scr49.place(relx=0.02, rely=0.02, relheight=0.83, relwidth=0.97)
        self.scr49.configure(background="white")
        self.scr49.configure(font="TkTextFont")
        self.scr49.configure(foreground="black")
        self.scr49.configure(highlightbackground="#d9d9d9")
        self.scr49.configure(highlightcolor="black")
        self.scr49.configure(insertbackground="black")
        self.scr49.configure(insertborderwidth="3")
        self.scr49.configure(selectbackground="#c4c4c4")
        self.scr49.configure(selectforeground="black")
        self.scr49.configure(width=10)
        self.scr49.configure(wrap=tkinter.NONE)

        self.Entry1 = tkinter.Entry(top)
        self.Entry1.place(relx=0.02, rely=0.87, relheight=0.09, relwidth=0.81)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")
        self.Entry1.configure(width=484)
        self.Entry1.bind('<Return>', YAVIS.button__click)

    @staticmethod
    def popup1(event):
        popupmenu1 = tkinter.Menu(root, tearoff=0)
        popupmenu1.configure(activebackground="#f9f9f9")
        popupmenu1.configure(activeborderwidth="1")
        popupmenu1.configure(activeforeground="black")
        popupmenu1.configure(background="#d9d9d9")
        popupmenu1.configure(borderwidth="1")
        popupmenu1.configure(disabledforeground="#a3a3a3")
        popupmenu1.configure(font="{Segoe UI} 9")
        popupmenu1.configure(foreground="black")
        popupmenu1.post(event.x_root, event.y_root)


# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    """Configure the scrollbars for a widget."""

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        # self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = tkinter.Pack.__dict__.keys() | tkinter.Grid.__dict__.keys() \
                      | tkinter.Place.__dict__.keys()
        else:
            methods = tkinter.Pack.__dict__.keys() + tkinter.Grid.__dict__.keys() \
                      + tkinter.Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        """Hide and show scrollbar as needed."""

        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)

        return wrapped

    def __str__(self):
        return str(self.master)


def _create_container(func):
    """Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget."""

    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        return func(cls, container, **kw)

    return wrapped


class ScrolledText(AutoScroll, tkinter.Text):
    """A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed."""

    @_create_container
    def __init__(self, master, **kw):
        tkinter.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


if __name__ == '__main__':
    vp_start_gui()
