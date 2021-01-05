from tkinter.constants import *
from ttkthemes import ThemedTk
from tkinter import BooleanVar, Menu, PhotoImage, StringVar, ttk
from win10toast import ToastNotifier
import tkinter.messagebox as msgbox
import ldp_json_tool as ldpjson
import datetime, os, webbrowser

class LDPManager():
    def __init__(self):
        self.SetupConfig()

        self.root = ThemedTk(theme="default", background=True)
        self.root.title(f"LDP Store Manager v{self.vtitle}")
        self.root.configure(menu=self.CreateMenuBar())
        
        self.root.iconphoto(False, self.Assets_Icon())

        nb_tabs = ttk.Notebook(self.root)
        nb_tabs.pack(expand=YES, fill=BOTH)

        nb_tabs.add(self.GUI_Treeview(nb_tabs), text="Ventas")
        nb_tabs.add(self.GUI_Registering(nb_tabs), text="Registrar")
        # nb_tabs.add(self.GUI_DueDates(nb_tabs), text="Vencimientos") Future feature
        # nb_tabs.add(None, text="Calculadora") # Calcula precios automáticamente sólo introduciendo unos valores.
        nb_tabs.add(self.GUI_Info(nb_tabs), text="Información")
        
        self.root.mainloop()

    def Assets_Icon(self):
        try: png = PhotoImage(file=f"{ldpjson.wkdir}\\icon.png")
        except: 
            png = None
            error_msg = f"""
            No se encontró 'icon.png' en la carpeta '{ldpjson.data_folder}'.
            Vuelve a instalar el programa.
            
            Archivos encontrados en '{ldpjson.data_folder}':
            {os.listdir(ldpjson.wkdir)}
            """
            self.DisplayWarning("Falta un archivo.", error_msg)
        return png        

    def GUI_Treeview(self, parent_widget):
        # ______Top frame_______
        frame_sales = ttk.Frame(parent_widget)
        frame_sales.pack(side=TOP, expand=YES, fill=BOTH)

        # Treeview labelframe
        self.lf_tvDisplay = ttk.LabelFrame(frame_sales, text="Visualizador")
        self.lf_tvDisplay.grid(row=0, column=1, sticky=NSEW)

        # ______Pricing tree view______
        self.treeview = ttk.Treeview(self.lf_tvDisplay)
        self.treeview.bind("<ButtonRelease 1>", self.OnTreeClick)
        self.treeview.bind("<KeyRelease Up>", self.OnTreeClick)
        self.treeview.bind("<KeyRelease Down>", self.OnTreeClick)
        self.treeview["columns"] = ("Date", "Earnings", "Description")

        self.treeview.heading("#0", text="")
        self.treeview.heading("Date", text="Fecha (A/M/D)")
        self.treeview.heading("Earnings", text="Entrada/Salida")
        self.treeview.heading("Description", text="Descripción")
        
        self.treeview.column("#0", width=75, minwidth=75, stretch=NO)
        self.treeview.column("Date", anchor=W)
        self.treeview.column("Earnings", anchor=W)
        self.treeview.column("Description", anchor=W)

        # Tree view scrollbar
        scrollbar_treeview = ttk.Scrollbar(self.lf_tvDisplay, orient="vertical", command=self.treeview.yview)
        scrollbar_treeview.pack(side=RIGHT, fill=Y)
        self.treeview.configure(yscrollcommand=scrollbar_treeview.set)

        self.treeview.pack(side=TOP, expand=YES, fill=BOTH)

        # ______Treeview edit section______
        def update_treeview_record():
            y2r, m2r, d2r, i2r = self.selectedItem.split("-")
            ldpjson.sales.ReplaceData(y2r, m2r, d2r, i2r, int(self.tv_entry_newValue.get()))

            previous_data = self.treeview.item(self.selectedItem, "values")
            self.treeview.item(self.selectedItem, values=(previous_data[0], f"            ${self.tv_entry_newValue.get()}" ,previous_data[2]))
            
            self.UpdateTree()

        self.tv_lf_tvInfo = ttk.LabelFrame(frame_sales, text="Información de Item")
        self.tv_lf_tvInfo.grid(row=0, column=0, sticky=NS, ipadx=10)

        lbl_tooltip = ttk.Label(frame_sales, text="")
        lbl_tooltip.grid(row=1, column=1, pady=25)

        lf_objNameTitle = ttk.LabelFrame(self.tv_lf_tvInfo, text="Nombre:")
        self.tv_lbl_objName = ttk.Label(lf_objNameTitle, text="00-00-00-00")
        self.tv_lbl_objName.bind("<Enter>", lambda e: lbl_tooltip.configure(text="ID o Nombre del item seleccionado."))
        self.tv_lbl_objName.bind("<Leave>", lambda e: lbl_tooltip.configure(text=""))

        lf_objTypeTitle = ttk.LabelFrame(self.tv_lf_tvInfo, text="Tipo:")
        self.tv_lbl_objType = ttk.Label(lf_objTypeTitle, text="Nulo")
        self.tv_lbl_objType.bind("<Enter>", lambda e: lbl_tooltip.configure(text="Descripción del item seleccionado."))
        self.tv_lbl_objType.bind("<Leave>", lambda e: lbl_tooltip.configure(text=""))

        lf_objCurrentValueTitle = ttk.LabelFrame(self.tv_lf_tvInfo, text="Valor (AR$):")
        self.tv_lbl_objCurrentValue = ttk.Label(lf_objCurrentValueTitle, text="$0")
        self.tv_lbl_objCurrentValue.bind("<Enter>", lambda e: lbl_tooltip.configure(text="Valor actual del item seleccionado."))
        self.tv_lbl_objCurrentValue.bind("<Leave>", lambda e: lbl_tooltip.configure(text=""))
        

        lf_objNewValueTitle = ttk.LabelFrame(self.tv_lf_tvInfo, text="Nuevo valor (AR$):")
        self.tv_entry_newValue = ttk.Spinbox(lf_objNewValueTitle, from_=-999999999, to=999999999)
        self.tv_entry_newValue.set(0)
        self.tv_entry_newValue.bind("<Enter>", lambda e: lbl_tooltip.configure(text="Cambiará el valor anterior del item seleccionado por el especificado."))
        self.tv_entry_newValue.bind("<Leave>", lambda e: lbl_tooltip.configure(text=""))

        lf_tvActions = ttk.LabelFrame(self.tv_lf_tvInfo, text="Acciones disponibles")
        self.tv_btn_update = ttk.Button(lf_tvActions, text="Actualizar", command=update_treeview_record)
        self.tv_btn_update.bind("<Enter>", lambda e: lbl_tooltip.configure(text=f"Actualizará el valor del item seleccionado al especificado."))
        self.tv_btn_update.bind("<Leave>", lambda e: lbl_tooltip.configure(text=""))
        self.tv_btn_delete = ttk.Button(lf_tvActions, text="Eliminar", command=self.TreeRemoveItem)
        self.tv_btn_delete.bind("<Enter>", lambda e: lbl_tooltip.configure(text=f"Eliminará el item seleccionado."))
        self.tv_btn_delete.bind("<Leave>", lambda e: lbl_tooltip.configure(text=""))

        lf_objNameTitle.pack(fill=X)
        lf_objCurrentValueTitle.pack(fill=X)
        lf_objTypeTitle.pack(fill=X)
        lf_objNewValueTitle.pack(fill=X)
        lf_tvActions.pack(fill=X)
        padding = 5
        self.tv_lbl_objName.pack(expand=YES, pady=padding)
        self.tv_lbl_objType.pack(expand=YES, pady=padding)
        self.tv_lbl_objCurrentValue.pack(expand=YES, pady=padding)
        self.tv_entry_newValue.pack(expand=YES, pady=padding)
        self.tv_btn_delete.pack(expand=YES)
        self.tv_btn_update.pack(expand=YES)

        self.tv_btn_delete.pack_forget()
        self.tv_btn_update.pack_forget()

        # Load treeview elements
        self.UpdateTree()

        return frame_sales

    def GUI_Registering(self, parent_widget):
        frame_registering = ttk.Frame(parent_widget)
        frame_registering.pack(side=BOTTOM, expand=YES, fill=BOTH)

        # ______Date view/edit group______
        self.lf_date = ttk.LabelFrame(frame_registering, text="Fecha")
        #self.lf_date.grid(row=0, column=0, pady=10, padx=10, ipadx=10, ipady=10)
        self.lf_date.pack(expand=YES, side=LEFT, fill=BOTH)

        # ______Registration edit group______
        self.lf_register = ttk.LabelFrame(frame_registering, text="Registro de acciones")
        #self.lf_register.grid(row=0, column=1, pady=10, padx=10, sticky=NS)
        self.lf_register.pack(expand=YES, side=LEFT, fill=BOTH)

        # ______Date time display______
        def SetDateFields2Today(ctx):
            ctx.var_dateDay.set(ctx.Today()[2])
            ctx.var_dateMonth.set(ctx.Today()[1])
            ctx.var_dateYear.set(ctx.Today()[0])
            
        # Setup variables
        self.var_datetime = StringVar()
        self.var_dateDay = StringVar()
        self.var_dateMonth = StringVar()
        self.var_dateYear = StringVar()
        self.var_dateDay.set(str(self.Today()[2]))
        self.var_dateMonth.set(str(self.Today()[1]))
        self.var_dateYear.set(str(self.Today()[0]))
        
        # Widget creation setup
        label_dateTime = ttk.Label(self.lf_date, textvariable=self.var_datetime)
        lbl_dateDay = ttk.Label(self.lf_date, text="Día")
        lbl_dateMonth = ttk.Label(self.lf_date, text="Mes")
        lbl_dateYear = ttk.Label(self.lf_date, text="Año")
        self.entry_dateDay = ttk.Spinbox(self.lf_date, textvariable=self.var_dateDay, from_=1, to=31, wrap=True)
        self.entry_dateMonth = ttk.Spinbox(self.lf_date, textvariable=self.var_dateMonth, from_=1, to=12, wrap=True)
        self.entry_dateYear = ttk.Spinbox(self.lf_date, textvariable=self.var_dateYear, to=9999)
        self.btn_setDate2Today = ttk.Button(self.lf_date, text="Hoy", command=lambda: SetDateFields2Today(self))
        
        # Widget position setup
        label_dateTime.grid(row=0, column=1)
        lbl_dateDay.grid(row=1, column=0, padx=25)
        lbl_dateMonth.grid(row=2, column=0, padx=25)
        lbl_dateYear.grid(row=3, column=0, padx=25)
        self.entry_dateDay.grid(row=1, column=1, padx=5)
        self.entry_dateMonth.grid(row=2, column=1, padx=5)
        self.entry_dateYear.grid(row=3, column=1, padx=5)
        self.btn_setDate2Today.grid(row=4, column=1)
        
        # ______Sold amount section______
        self.var_soldAmount = StringVar()
        self.var_recievedAmount = StringVar()
        self.var_quickMode = BooleanVar()
        label_soldAmount = ttk.Label(self.lf_register, text="Valor (Compra/Venta) (AR$)")
        label_recievedAmount = ttk.Label(self.lf_register, text="Recibido (AR$)")
        cb_quickMode = ttk.Checkbutton(self.lf_register, text="Modo rápido", variable=self.var_quickMode, onvalue=True, offvalue=False)
        self.entry_soldAmount = ttk.Entry(self.lf_register, textvariable=self.var_soldAmount)
        entry_recievedAmount = ttk.Entry(self.lf_register, textvariable=self.var_recievedAmount)

        def cb_quickmode_click():
            if self.var_quickMode.get() == False:
                label_recievedAmount.grid_remove()
                entry_recievedAmount.grid_remove()
            else:
                label_recievedAmount.grid()
                entry_recievedAmount.grid()

        label_soldAmount.grid(row=0, column=0, padx=10)
        label_recievedAmount.grid(row=1, column=0, padx=10)
        cb_quickMode.grid(row=2, column=1)
        self.entry_soldAmount.grid(row=0, column=1)
        entry_recievedAmount.grid(row=1, column=1)
        self.entry_soldAmount.bind("<Return>", lambda e: entry_recievedAmount.focus())
        entry_recievedAmount.bind("<Return>", lambda e: self.SaveFile())
        
        cb_quickMode.bind("<ButtonRelease 1>", lambda e: cb_quickmode_click())

        # Item save section
        self.lbl_todayEarnings=ttk.Label(self.lf_register, text="Hoy: $-")
        button_log = ttk.Button(self.lf_register, text="Registrar", command=self.SaveFile)
        button_log.grid(row=3, column=1, pady=5)
        self.lbl_todayEarnings.grid(row=3, column=0, padx=10)

        return frame_registering

    def GUI_DueDates(self, parent_widget):
        
        frame_dueDate = ttk.Frame(parent_widget)
        frame_dueDate.pack(expand=YES, fill=BOTH)
        
        lf_dateSelector = ttk.LabelFrame(frame_dueDate, text="Selector de fecha")
        lf_dateSelector.pack(expand=YES, ipadx=10, ipady=10)

        frame_dateSelectorCenteredContainer = ttk.Frame(lf_dateSelector)
        frame_dateSelectorCenteredContainer.pack(expand=YES)

        lbl_day = ttk.Label(frame_dateSelectorCenteredContainer, text="Día")
        lbl_month = ttk.Label(frame_dateSelectorCenteredContainer, text="Mes")
        lbl_year = ttk.Label(frame_dateSelectorCenteredContainer, text="Año")
        entry_day = ttk.Entry(frame_dateSelectorCenteredContainer, width=10)
        entry_month = ttk.Entry(frame_dateSelectorCenteredContainer, width=10)
        entry_year = ttk.Entry(frame_dateSelectorCenteredContainer, width=10)

        lbl_day.grid(row=0, column=0, padx=5, pady=5)
        lbl_month.grid(row=1, column=0, padx=5, pady=5)
        lbl_year.grid(row=2, column=0, padx=5, pady=5)
        entry_day.grid(row=0, column=1, padx=5, pady=5)
        entry_month.grid(row=1, column=1, padx=5, pady=5)
        entry_year.grid(row=2, column=1, padx=5, pady=5)

        return frame_dueDate

    def GUI_Info(self, parent_widget):
        frame_info = ttk.Frame(parent_widget)
        frame_info.pack(expand=YES)

        # Widget creation setup
        info_lbl_localVersion = ttk.Label(frame_info, text=f"Versión instalada: {ldpjson.config.GetLocalCfgData('version')}")

        # ______Update group______
        def do_update():
            warn = self.RequestConfirmation(message="El programa debe cerrarse para actualizar.\n¿Desea continuar?")
            if warn == "yes":
                webbrowser.open(ldpjson.config.GetCloudData("download"))
                self.root.destroy()

        info_lf_update = ttk.LabelFrame(frame_info, text=f"Actualización {self.new_ver} disponible")
        self.info_btn_update = ttk.Button(info_lf_update, text="Actualizar", command=do_update)
        self.info_btn_update.pack(expand=YES, padx=25, pady=25)
        # _____________
        
        # Widget position setup
        info_lbl_localVersion.pack(expand=YES)
        info_lf_update.pack(expand=YES)
        if ldpjson.config.IsOutdated() == False: info_lf_update.pack_forget()

        return frame_info

    def update_today_register_label(self):
            try: self.lbl_todayEarnings.configure(text=f"Hoy: ${ldpjson.sales.GetTotalOf(self.var_dateYear.get(), self.var_dateMonth.get(), self.var_dateDay.get())}")
            except: self.lbl_todayEarnings.configure(text=f"Hoy: $-")

    def SetupConfig(self):
        with open(ldpjson.config.fullpath, "w") as f:
            data = {"version": ldpjson.app_version}
            ldpjson.json.dump(data, f, indent=4)

        self.vtitle = ldpjson.config.GetLocalCfgData("version")
        
        # Notify if app outdated
        notif = ToastNotifier()
        self.new_ver = None
        if ldpjson.config.IsOutdated():
            self.new_ver = ldpjson.config.GetCloudData("version")
            notif.show_toast(
                f"Versión {self.new_ver} disponible",
                f"Hay una nueva versión disponible.\nRevisa la pestaña de información para instalarla.",
                f"{ldpjson.wkdir}\\icon.ico", 
                duration=5, 
                threaded=True
            )

    def RequestConfirmation(self, title="Confirmación", message="¿Seguro que querés realizar esta acción?"):
        questionBox = msgbox.askquestion(title, message)
        print(questionBox)
        return questionBox

    def DisplayWarning(self, title, message):
        message_box = msgbox.showwarning(title, message)
        return message_box

    def DisplayMessage(self, title, message):
        message_box = msgbox.showinfo(title, message)
        return message_box

    def TreeRemoveItem(self):
        if self.RequestConfirmation() == "yes":
            itemData = self.selectedItem.split("-")
            y, m, d, i = itemData[0], itemData[1], itemData[2], itemData[3] if len(itemData) == 4 else None
            ldpjson.sales.RemoveData(y, m, d, i)
            self.treeview.delete(self.selectedItem)
            self.tv_btn_delete.pack_forget()
            self.UpdateTree()
        else:
            print("Treeview delete action canceled.")
    
    def OnTreeClick(self, event):
        self.selectedItem = self.treeview.selection()[0]
        self.tv_lbl_objName.configure(text=self.selectedItem)
        self.tv_lbl_objCurrentValue.configure(text=self.treeview.item(self.selectedItem, "values")[1].strip())
        self.tv_lbl_objType.configure(text=self.treeview.item(self.selectedItem, "values")[-1].strip())
        self.tv_entry_newValue.set(self.tv_lbl_objCurrentValue.cget("text").strip("$"))
        selectedItem_split = self.selectedItem.split("-")
        self.tv_btn_update.pack_forget()
        if len(selectedItem_split) == 3:
            self.tv_btn_delete.pack()
        elif len(selectedItem_split) == 4:
            self.tv_btn_delete.pack()
            self.tv_btn_update.pack()
        else:
            self.tv_btn_delete.pack_forget()

    def CreateMenuBar(self):
        menubar = Menu(self.root)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exportar a Excel (no disponible)", command=self.ExportToExcel)

        thememenu = Menu(menubar, tearoff=0)
        thememenu.add_command(label="Por defecto", command=lambda: self.root.set_theme("default"))
        thememenu.add_command(label="Oscuro", command=lambda: self.root.set_theme("equilux"))
        thememenu.add_command(label="Claro", command=lambda: self.root.set_theme("yaru"))

        menubar.add_cascade(label="Archivo", menu=filemenu)
        menubar.add_cascade(label="Tema", menu=thememenu)

        return menubar
    
    def UpdateTree(self):
        # Delete all
        self.treeview.delete(*self.treeview.get_children())
        
        # Get the json data as a dictionary
        json_data = ldpjson.sales.GetSavedData()

        # Insert everything into a dictionary and then analyze the dictionary
        
        daily_dict = {}
        daily_childs = {}
        # Group daily prices
        for y in json_data.keys():
            for m in json_data[y].keys():
                for d in json_data[y][m].keys():
                    daily_dict[f"{y}-{m}-{d}"] = ldpjson.sales.GetTotalOf(y, m, d)
                    for i in json_data[y][m][d]:
                        if f"{y}-{m}-{d}" in daily_childs: daily_childs[f"{y}-{m}-{d}"].append(i)
                        else: daily_childs[f"{y}-{m}-{d}"] = [i]
        
        monthly_dict = {}
        # Group month prices
        for data in daily_dict:
            y, m, d = data.split("-")
            if data.startswith(f"{y}-{m}"):
                if f"{y}-{m}" in monthly_dict: monthly_dict[f"{y}-{m}"] += daily_dict[data]
                else: monthly_dict[f"{y}-{m}"] = daily_dict[data]

        year_dict = {}
        # Group year prices
        for data in monthly_dict:
            y, m = data.split("-")
            if data.startswith(y):
                if y in year_dict: year_dict[y] += monthly_dict[data]
                else: year_dict[y] = monthly_dict[data]
                    
        # Start displaying treeview

        # Roots (years)
        for data in year_dict:
            self.treeview.insert(
                parent="",
                index="end",
                iid=data,
                values=(f"Año {data}", "$"+str(year_dict[data]), "Anual")
            )
        
        # Year childs (months)
        for data in monthly_dict:
            y, m = data.split("-")
            self.treeview.insert(
                parent=y,
                index="end",
                iid=data,
                values=(f"    Mes {m}", "    $"+str(monthly_dict[data]), "    Mensual")
            )
        
        # Month childs (days)
        for data in daily_childs.keys():
            y, m, d = data.split("-")
            day_log = self.treeview.insert(
                parent=f"{y}-{m}",
                index="end",
                iid=data,
                values=(f"        Día {d}", "        $"+str(daily_dict[data]), "        Diario")
            )
            # Day childs (logs)
            childs = daily_childs[data]
            for i in range(len(childs)):
                total = ldpjson.sales.GetTotalOf(y, m, d, i)
                self.treeview.insert(
                    parent=day_log,
                    index="end",
                    iid=f"{data}-{i}",
                    values=(
                        f"            Índice {i}",
                        f"            ${total}",
                        "            Entrada" if total > 0 else "            Salida"
                    )
                )

        try: self.update_today_register_label()
        except: pass

    def Today(self):
        date = str(datetime.datetime.now()).split(" ")[0].split("-")
        date = [int(i) for i in date]
        return date

    def TodayFormatted(self):
        return f"{self.Today()[0]}-{self.Today()[1]}-{self.Today()[2]}"
    
    def TodayAsDict(self):
        return {
            self.Today()[0] : {
                self.Today()[1] : {
                    self.Today()[2] : []
                }
            }
        }

    def SaveFile(self):

        def save_action():
            ldpjson.sales.AddData(
                self.var_dateYear.get(), 
                self.var_dateMonth.get(), 
                self.var_dateDay.get(), 
                self.var_soldAmount.get() if self.var_soldAmount.get() != "" else 0
            )

            # Update in treeview
            self.UpdateTree()

            # Blank price entry
            self.var_soldAmount.set("")
            self.entry_soldAmount.focus()
            self.var_recievedAmount.set("")

        if self.var_quickMode.get() == True: save_action()
        else:
            try: sldAmount = int(self.var_soldAmount.get())
            except: sldAmount = 0
            try: rcvAmount = int(self.var_recievedAmount.get())
            except: rcvAmount = 0
            rtrnAmount = f"${rcvAmount-sldAmount}"
            if rcvAmount-sldAmount < 0: rtrnAmount = f"Falta ${-(rcvAmount-sldAmount)}"

            self.DisplayMessage("Vuelto", f"{rtrnAmount}")

            d, m, y = self.var_dateDay.get(), self.var_dateMonth.get(), self.var_dateYear.get()
            msg = f"""
            Se recibió ${rcvAmount} para cobrar ${sldAmount}
            Vuelto: {rtrnAmount}

            ¿Desea continuar?
            """
            if self.RequestConfirmation(title=f"Se registrará en '{d}/{m}/{y}'", message=msg) == "yes": save_action()
    
    def ExportToExcel(self):
        msg = """
        Todavía la función de exportar a excel no está disponible.
        En una futura versión puede o no estarlo.
        """
        self.DisplayWarning(
            "Función no disponible", 
            msg
        )

ldp_manager = LDPManager()