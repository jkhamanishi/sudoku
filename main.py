from tkinter import Tk, ttk

root = Tk()  # create parent window
root.title("Tab Widget")
tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Generate')
tabControl.add(tab2, text='Import')
tabControl.pack(expand=1, fill="both")

turn_on = ttk.Button(tab1, text="ON")
turn_on.pack()
turn_off = ttk.Button(tab1, text="OFF", command=root.quit)
turn_off.pack()

# ttk.Label(tab1, text="Welcome to GeeksForGeeks").grid(column=0, row=0, padx=30, pady=30)
ttk.Label(tab2, text="Lets dive into the world of computers").grid(column=0, row=0, padx=30, pady=30)

root.mainloop()

