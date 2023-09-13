import tkinter as tk
#
# # Create the main window
# window = tk.Tk()
# window.title("name")
# window.geometry("300x270")
# # Create a label
# image1=tk.PhotoImage(file="bg.png")
# label = tk.Label(text="Enter the Name : ",font=("Times New Roman",20),justify="center",pady=5,image=image1)
# label.pack()
# entry_field = tk.Entry(window)
# entry_field.pack()
# # Create a btton
# def on_button_click():
#     # Get the input from the entry field
#     input_text = entry_field.get()
#     number = input_text
#     print(number)
#     return (number)
#
# button = tk.Button(window,text="Submit", command=on_button_click)
# button.pack()
#
# # Start the main loop
# window.mainloop()

######################################

windoww = tk.Tk()
windoww.title("name")
windoww.geometry("500x500")
# Create a label
image2=tk.PhotoImage(file="bg.png")
labell = tk.Label(text="Enter not the name : ",font=("Times New Roman",20),justify="center",pady=15,image=image2)
labell.pack()
entry = tk.Entry(windoww)
entry.pack()
# Create a btton
def hehe():
    def on_button_click():
        # Get the input from the entry field
        input_text = entry.get()
        number = input_text
        print(number)
        return (number)

    but = tk.Button(windoww,text="Submit", command=on_button_click)
    but.pack()
    # Start the main loop
    windoww.mainloop()

hehe()