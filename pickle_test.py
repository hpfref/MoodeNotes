import os
from tkinter import *
import pickle 


window = Tk()
window.geometry("1280x720")
window.title("test")
window.config(bg='#ebedf0')

if(os.path.exists('fref.txt')):
    print(pickle.load(open('fref.txt',"rb")))

#food_list = ['apple', 'banana', 'orange']
#list1 = StringVar(value=food_list)
list1 = StringVar(value=pickle.load(open('fref.txt',"rb")))

listbox1 = Listbox( window,
                    listvariable=list1,
                    font=("Consolas",14),
                    fg='#23222b',
                    bg='#ebedf0')
listbox1.pack(fill=BOTH,padx=20, anchor=W)
listbox1.config(height=listbox1.size())


pickle.dump(listbox1.get(0,END),open('fref.txt',"wb"))

window.mainloop()
