import os
import pickle
from tkinter import *

class MoodeNotesApp:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("800x600")
        self.window.title("Moode Notes")
        self.window.iconphoto(True, PhotoImage(file='img/hamood.png'))
        self.window.config(bg='#2c3e50')

        self.lists = {'Urgent': [], 'Long Term': []}

        self.create_labels()
        self.create_note_entry('Urgent')
        self.create_note_entry('Long Term')

        self.load_lists()
        self.setup_save_function()

    def create_labels(self):
        label = Label(self.window, text="The Brain Dump :o", font=('Helvetica', 22, 'bold', 'italic'),
                    fg='#ecf0f1', bg='#2c3e50')
        label.pack(side='top', anchor='n', pady=(20, 10)) #center


    def create_note_entry(self, label_text):
        frame = Frame(self.window, bg='#2c3e50')
        frame.pack(fill='both', padx=20, pady=(10, 0), expand=False)

        label = Label(frame, text=label_text, font=('Helvetica', 18, 'bold'), fg='#ecf0f1', bg='#2c3e50', width=12)
        label.grid(row=0, column=0, pady=(10, 5), padx=(0, 10), sticky=NW)

        placeholder = "Type your note here..."
        entry = Entry(frame, font=("Helvetica", 14), fg='#ecf0f1', bg='#2c3e50', relief='flat', bd=0, highlightthickness=0, width=40)
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event, e=entry, p=placeholder: self.on_entry_click(e, p))
        entry.bind("<FocusOut>", lambda event, e=entry, p=placeholder: self.on_focus_out(e, p))
        entry.grid(row=1, column=0, pady=(0, 5), padx=(10, 0), sticky=NW)

        listbox = Listbox(frame, font=("Helvetica", 14), fg='#ecf0f1', bg='#2c3e50', selectbackground='#3498db',
                        relief='flat', bd=0, selectmode=SINGLE, highlightthickness=0, height=7, width=50)
        listbox.grid(row=1, column=1, pady=(0, 5), padx=(0, 10), sticky=NW)

        # Vertical Scrollbar
        v_scrollbar = Scrollbar(frame, orient="vertical", command=listbox.yview, width=2, troughcolor='#2c3e50', activerelief='flat', bd=0)
        v_scrollbar.grid(row=1, column=2, sticky='ns')
        listbox.config(yscrollcommand=v_scrollbar.set)

        # Horizontal Scrollbar
        h_scrollbar = Scrollbar(frame, orient="horizontal", command=listbox.xview, width=2, troughcolor='#2c3e50', activerelief='flat', bd=0)
        h_scrollbar.grid(row=2, column=1, sticky='ew')
        listbox.config(xscrollcommand=h_scrollbar.set)
        
        """
        def update_listbox_width(event):
            listbox_contents = listbox.get(0, 'end')
            max_element_length = max(len(item) for item in listbox_contents) if listbox_contents else 0
            entry_text_width = max_element_length 
            listbox.config(width=max(entry_text_width, 1))  # minimum width
        """

        #frame.bind("<Configure>", update_listbox_width)
        entry.bind("<Return>", lambda event, box=listbox: self.add_note(event, entry, box))
        listbox.bind("<BackSpace>", lambda event, box=listbox: self.del_note(event, listbox))

        self.lists[label_text] = {'entry': entry, 'listbox': listbox}


    def add_note(self, event, entry, listbox):
        text = entry.get()

        if text and text != "Type your note here...":
            listbox.insert(END, f"{listbox.size() + 1}. {text}")
            entry.delete(0, END)
            #listbox.config(height=listbox.size())
            entry.grid(row=1, column=0, pady=(0, 5), padx=(10, 0), sticky=NW)

    def del_note(self, event, listbox):
        try:
            index = listbox.curselection()[0]
            listbox.delete(index)
            for i in range(index, listbox.size()):
                listbox.insert(i, f"{i + 1}. {listbox.get(i)[3:]}")
                listbox.delete(i + 1)

            #listbox.config(height=listbox.size())
        except IndexError:
            pass

    def load_lists(self):
        for label_text, data in self.lists.items():
            file_path = f'lb{label_text.replace(" ", "")}.txt'
            if os.path.exists(file_path):
                data['listbox'].insert(END, *pickle.load(open(file_path, "rb")))

    def save_lists(self):
        for label_text, data in self.lists.items():
            file_path = f'lb{label_text.replace(" ", "")}.txt'
            pickle.dump(data['listbox'].get(0, END), open(file_path, "wb"))

    def on_entry_click(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, "end")  # delete all the text in the entry
            entry.config(fg='#ecf0f1')  # change text color to white

    def on_focus_out(self, entry, placeholder):
        if entry.get() == '':
            entry.insert(0, placeholder)
            entry.config(fg='#7f8c8d')  # change text color to gray

    def setup_save_function(self):
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def on_closing(self):
        self.save_lists()
        self.window.destroy()


if __name__ == '__main__':
    app = MoodeNotesApp()