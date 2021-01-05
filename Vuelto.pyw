from ttkthemes import ThemedTk
from tkinter import ttk, StringVar, Menu

class SimpleCalc():
    def __init__(self):
        self.root = ThemedTk(theme="yaru", background=True)
        self.root.title("LDP - Vueltos")
        self.root.wm_attributes("-topmost", 1) # Stay on top

        # Menu bar creation
        self.root.config(menu=self.CreateMenubar())

        # -- Widget creation --
        
        # Amount to retrieve variable
        self.var_paymentPrice = StringVar()
        self.var_recievedAmount = StringVar()
        self.var_a2r = StringVar()

        label_paymentPrice = ttk.Label(self.root, text="Precio a pagar ($) ")
        label_recievedAmount = ttk.Label(self.root, text="Monto recibido ($) ")
        label_amount2retrieve = ttk.Label(self.root, text="Vuelto: ")
        label_a2rbig = ttk.Label(self.root, textvariable=self.var_a2r)

        entry_paymentPrice = ttk.Entry(self.root, textvariable=self.var_paymentPrice)
        entry_recievedAmount = ttk.Entry(self.root, textvariable=self.var_recievedAmount)
        
        entry_paymentPrice.focus()
        entry_paymentPrice.bind("<Return>", lambda e: entry_recievedAmount.focus())
        entry_recievedAmount.bind("<Return>", lambda e: entry_paymentPrice.focus())

        # -- Widget placement --

        label_paymentPrice.grid(row=0, column=0)
        label_recievedAmount.grid(row=1, column=0)
        label_amount2retrieve.grid(row=2, column=0)
        label_a2rbig.grid(row=2, column=1)
        entry_paymentPrice.grid(row=0, column=1)
        entry_recievedAmount.grid(row=1, column=1)

        self.root.after(100, self.AppUpdate)
        
        self.root.mainloop()
        
    def CreateMenubar(self):
        menubar = Menu(self.root)

        thememenu = Menu(menubar, tearoff=0)
        thememenu.add_command(label="Sistema", command=lambda: self.root.set_theme("default"))
        thememenu.add_command(label="Oscuro", command=lambda: self.root.set_theme("equilux"))
        thememenu.add_command(label="Claro", command=lambda: self.root.set_theme("yaru"))

        menubar.add_cascade(label="Tema", menu=thememenu)
        
        return menubar
        
    def AppUpdate(self):
        self.root.after(100, self.AppUpdate)
        try:
            paymentPrice = int(self.var_paymentPrice.get())
            recievedAmount = int(self.var_recievedAmount.get())
            a2r = int(recievedAmount-paymentPrice)
            if a2r < 0:
                self.var_a2r.set(f"Faltan ${-a2r}")
            else:
                self.var_a2r.set(f"${a2r}")
        except:
            self.var_a2r.set("No aplicable")

app = SimpleCalc()
