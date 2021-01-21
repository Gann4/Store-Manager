from tkinter.constants import BOTH, CENTER, HORIZONTAL, TOP
from datetime import datetime
from ttkthemes import ThemedTk
from tkinter import ttk
import win10toast, os, locale
import ldp_json_tool as ldpjson

locale.setlocale(locale.LC_ALL, "es_ES")

class DueDateApp():
    def __init__(self):
        self.toastObject = win10toast.ToastNotifier()

        self.root = ThemedTk(theme="default", background=True)
        self.root.title("Registro de vencimientos")

        # -- Main tree view --

        self.tv_dates = ttk.Treeview(self.root)
        self.tv_dates.bind("<ButtonRelease 1>", self.OnTreeClick)
        self.tv_dates["columns"] = ("Product", "Date")
        self.tv_dates.column("#0", width=0)
        self.tv_dates.column("Product", anchor=CENTER)
        self.tv_dates.column("Date", anchor=CENTER)
        self.tv_dates.heading("Product", text="Producto")
        self.tv_dates.heading("Date", text="Vencimiento")

        self.tv_dates.pack(expand=1, fill=BOTH, side=TOP)

        # -- Registration section --
        self.frame_registerSection = ttk.Frame(self.root)
        self.frame_registerSection.pack(expand=1)

        # Entries
        self.entry_product = ttk.Entry(self.frame_registerSection)
        self.entry_product.bind("<Return>", lambda event: self.entry_day.focus())

        self.frame_date = ttk.Frame(self.frame_registerSection)
        self.entry_day = ttk.Entry(self.frame_date)
        self.entry_day.bind("<Return>", lambda event: self.entry_month.focus())
        self.entry_month = ttk.Entry(self.frame_date)
        self.entry_month.bind("<Return>", lambda event: self.entry_year.focus())
        self.entry_year = ttk.Entry(self.frame_date)
        self.entry_year.bind("<Return>", lambda event: self.RegisterProduct())
        
        self.label_product = ttk.Label(self.frame_registerSection, text="Producto")
        self.label_day = ttk.Label(self.frame_registerSection, text="Fecha (Día/Mes/Año)")

        self.button_register = ttk.Button(self.frame_registerSection, text="Registrar", command=self.RegisterProduct)
        self.button_delete = ttk.Button(self.frame_registerSection, text="Eliminar selección", command=self.DeleteDate)

        self.label_product.grid(row=0, column=0, padx=50)
        self.entry_product.grid(row=0, column=1)
        
        self.label_day.grid(row=1, column=0, padx=50)
        self.frame_date.grid(row=1, column=1)
        self.entry_day.grid(row=0, column=0)
        self.entry_month.grid(row=0, column=1)
        self.entry_year.grid(row=0, column=2)

        self.button_register.grid(row=0, column=2, padx=100)
        self.button_delete.grid(row=1, column=2, padx=100)
        self.button_delete.grid_remove()

        self.DisplayDates()

        self.root.mainloop()

    def OnTreeClick(self, event):
        self.tree_selection = self.tv_dates.selection()[0]
        self.button_delete.grid()
        
    def DeleteDate(self):
        content2replace = []
        with open("logs.txt", "r") as f:
            lines = f.readlines()
            for ln in range(len(lines)):
                ln_str = str(ln)
                if self.tree_selection != ln_str:
                    content2replace.append(lines[ln])
        with open("logs.txt", "w") as f:
            f.write("".join(content2replace))
        self.tv_dates.delete(self.tree_selection)
    
    def RegisterProduct(self):
        if not os.path.exists("logs.txt"):
            f = open("logs.txt", "w+")
            f.close()
        self.entry_product.focus()
        product_name = self.entry_product.get()
        due_day = self.entry_day.get()
        due_month = self.entry_month.get()
        due_year = self.entry_year.get()

        with open("logs.txt", "a") as f:
            f.write(f"{due_day}/{due_month}/{due_year}@{product_name}\n")
        self.tv_dates.insert(
            parent="", 
            index="end", 
            iid=len(self.tv_dates.get_children()), 
            values=(product_name, f"{due_day}/{due_month}/{due_year}")
        )

    def DisplayDates(self):
        if not os.path.exists("logs.txt"):
            f = open("logs.txt", "w+")
            f.close()
            return None
        
        with open("logs.txt", "r") as f:
            lines = f.readlines()
            lines.sort()
            for ln in range(len(lines)):
                due_date, product_name = lines[ln].split("@")
                product_name = product_name.strip("\n")
                self.tv_dates.insert("", "end", iid=ln, values=(product_name, due_date))
                if due_date == self.Get_Today():
                    self.toastObject.show_toast(
                        "Hoy vencen productos!", 
                        f"Productos como '{product_name}' vencen hoy, ¡revisalo!",
                        threaded=True
                    )
        with open("logs.txt", "w") as f:
            f.write("".join(lines))
    def Get_Today(self):
        d, m, y = datetime.now().day, datetime.now().month, datetime.now().year
        return f"{d}/{m}/{y}"

app = DueDateApp()