import tkinter as tk
import queue
from part import Part


# from pdf2image import convert_from_path
# from PIL import ImageTk
# Convert PDF to list of images
# images = convert_from_path('power.pdf', 50)
# # Assume we are working with the first page for the demo
# photo = ImageTk.PhotoImage(images[0])
# label = tk.Label(window, image=photo)
# label.pack()

background_colour : str =       "#101010"
background_colour_light : str = "#27272a"
text_colour : str =             "#fef3c7"
error_colour : str =            "#e11d48"
font : tuple[str, int] = ("courier", 20)

# class CreateToolTip(object):
#     """
#     create a tooltip for a given widget
#     """
#     def __init__(self, widget, text='widget info'):
#         self.waittime = 500     #miliseconds
#         self.wraplength = 180   #pixels
#         self.widget = widget
#         self.text = text
#         self.widget.bind("<Enter>", self.enter)
#         self.widget.bind("<Leave>", self.leave)
#         self.widget.bind("<ButtonPress>", self.leave)
#         self.id = None
#         self.tw = None

#     def enter(self, event=None):
#         self.schedule()

#     def leave(self, event=None):
#         self.unschedule()
#         self.hidetip()

#     def schedule(self):
#         self.unschedule()
#         self.id = self.widget.after(self.waittime, self.showtip)

#     def unschedule(self):
#         id = self.id
#         self.id = None
#         if id:
#             self.widget.after_cancel(id)

#     def showtip(self, event=None):
#         x = y = 0
#         x, y, cx, cy = self.widget.bbox("insert")
#         x += self.widget.winfo_rootx() + 25
#         y += self.widget.winfo_rooty() + 20
#         # creates a toplevel window
#         self.tw = tk.Toplevel(self.widget)
#         # Leaves only the label and removes the app window
#         self.tw.wm_overrideredirect(True)
#         self.tw.wm_geometry("+%d+%d" % (x, y))
#         label = tk.Label(self.tw, text=self.text, justify='left',
#                        background="#ffffff", relief='solid', borderwidth=1,
#                        wraplength = self.wraplength)
#         label.pack(ipadx=1)

#     def hidetip(self):
#         tw = self.tw
#         self.tw= None
#         if tw:
#             tw.destroy()

def check_part(var : tk.StringVar, label : tk.Label, entry : tk.Entry, max_length : int):
    if max_length == 0: return
    if len(var.get()) > max_length:
        entry.config(
            highlightbackground=background_colour, 
            highlightcolor=error_colour, 
            highlightthickness=2
        )            
        label.config(
            foreground=error_colour
        )
    else:
        entry.config(
            highlightbackground=background_colour, 
            highlightcolor=text_colour, 
            highlightthickness=2
        )            
        label.config(
            foreground=text_colour
        )

class PartTable:
    class Field:
        def __init__(self, name : str, frame : tk.Frame, row : int , max_length=0) -> None:

            self.var = tk.StringVar()
            self.label = tk.Label(frame, text=name, justify=tk.RIGHT, font=font, bg=background_colour, foreground=text_colour)
            self.entry = tk.Entry(frame, textvariable=self.var, font=font, bg=background_colour_light, foreground=text_colour)
            self.entry.config(highlightbackground=background_colour, highlightcolor=text_colour, highlightthickness=2)            
            self.label.grid(column=0, row=row, sticky=tk.W)
            self.entry.grid(column=1, row=row, padx="10", sticky=tk.E)
            if max_length:
                # self.tool_tip = CreateToolTip(self.entry, f"this must be short than {max_length} chars")
                # self.tool_tip = CreateToolTip(self.label, f"this must be short than {max_length} chars")
                self.var.trace_add(
                "write", 
                
                lambda name, index, mode, var=self.var, label=self.label, entry=self.entry, max_length=max_length: check_part(var, label, entry, max_length) # type: ignore
            )

    def __init__(self, frame : tk.Frame) -> None:
        self.title_content = tk.StringVar(value="part lookup")
        self.title = tk.Label(frame, textvariable=self.title_content, justify=tk.RIGHT, font=font, bg=background_colour, foreground=text_colour)
        self.title.pack()
        self.grid = tk.Frame(master=frame, bg=background_colour)
        self.grid.columnconfigure(0, weight=1)
        self.grid.columnconfigure(1, weight=6)
        self.UID = PartTable.Field("UID", self.grid, 0) 
        self.name = PartTable.Field("name", self.grid, 1, max_length=14)
        self.specs = PartTable.Field("specs", self.grid, 2, max_length=20) 
        self.footprint = PartTable.Field("footprint", self.grid, 3, max_length=16) 
        self.PN = PartTable.Field("PN", self.grid, 4, max_length=16) 
        self.datasheet = PartTable.Field("datasheet", self.grid, 5) 
        self.supplier_links = PartTable.Field("supplier_links", self.grid, 6)
    
    def update_field_vars(self, p : Part):
        self.UID.var.set(p.UID)
        self.name.var.set(p.name)
        self.specs.var.set(p.specs)
        self.footprint.var.set(p.footprint)
        self.PN.var.set(p.PN)
        self.datasheet.var.set(p.datasheet)
        self.supplier_links.var.set(p.supplier_links) # type: ignore

    def pack(self):
        self.grid.pack()

class App:
    def __init__(self, data_base_queue : queue.Queue) -> None:
        self.window = tk.Tk(className="part look up")
        # make_bar(self.window)
        self.window.configure(bg=background_colour)
        # title = tk.Label(self.window, text="part adder")
        # title.pack()
        self.table = PartTable(self.window) # type: ignore
        self.table.pack()
        self.queue = data_base_queue
        #print(f"{id(self.queue)=}")
        self.button_frame = tk.Frame(
            self.window, 
            pady=10, 
            background=background_colour,
        )
        button_clear = tk.Button(
            self.button_frame, 
            command=lambda : clear_values(self),
            text="clear",
            font=font,
            background=background_colour_light,
            foreground=text_colour,
            pady=2
        )
        button_upadate = tk.Button(
            self.button_frame, 
            command=lambda : update_values(self),
            text="update_part",
            font=font,
            background=background_colour_light,
            foreground=text_colour,
            pady=2
        )
        button_upadate.grid(column=1, row=0, padx=10)
        button_clear.grid(column=0, row=0)
        self.button_frame.pack()
        # output = tk.Label(self.window, text="output", pady=10)
        # output.pack()

    def run(self):
        self.window.mainloop()


def update_values(self : App):
    part = Part(
            self.table.UID.var.get(),
            self.table.name.var.get(),
            self.table.specs.var.get(),
            self.table.footprint.var.get(),
            self.table.PN.var.get(),
            self.table.datasheet.var.get(),
            self.table.supplier_links.var.get(), # type: ignore
    )

    #print(self.queue)
    #print("waiting to put in to queue")
    #print(f"{id(self.queue)=}")
    if self.queue : self.queue.put(part)
    #print("put in to queue")
    #print(part)

def clear_values(self : App):
    self.table.UID.var.set("")
    self.table.name.var.set("")
    self.table.specs.var.set("")
    self.table.footprint.var.set("")
    self.table.PN.var.set("")
    self.table.datasheet.var.set("")
    self.table.supplier_links.var.set("")



