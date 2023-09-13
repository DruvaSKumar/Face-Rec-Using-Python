from tkinter import *
def submit_value(value):
    # code to handle value goes here
    print(value)
rootat = Tk()
button = Button(rootat, text="Submit", command=lambda:submit_value(value.get()))
value = StringVar()
entry = Entry(rootat, textvariable=value)
entry.pack()
button.pack()
rootat.mainloop()