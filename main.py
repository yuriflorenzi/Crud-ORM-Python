# main.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from controllers import ClienteController, PedidoController
from ttkthemes import ThemedTk


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión")
        self.root.geometry("650x500")

        # Configurar el estilo
        style = ttk.Style()
        style.configure(".", background="#e8f5e9")  # Verde claro para el fondo
        style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff")
        style.configure("TFrame", background="#e8f5e9")
        style.configure("TLabel", background="#e8f5e9")
        style.configure("TLabelframe", background="#e8f5e9")
        style.configure("TButton", background="#4caf50", foreground="black")

        # Inicializar la base de datos y los controladores
        db = Database()
        self.cliente_controller = ClienteController(db.session)
        self.pedido_controller = PedidoController(db.session)

        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)

        # Crear pestañas
        self.tab_clientes = ttk.Frame(self.notebook)
        self.tab_pedidos = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_clientes, text='Gestión de Clientes')
        self.notebook.add(self.tab_pedidos, text='Gestión de Pedidos')

        # Inicializar las vistas
        self.init_vista_clientes()
        self.init_vista_pedidos()

    def init_vista_clientes(self):
        # Frame para el formulario de clientes
        form_frame = ttk.LabelFrame(self.tab_clientes, text="Datos del Cliente", padding="10")
        form_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # Campos del formulario
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky="w")
        self.nombre_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.nombre_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky="w")
        self.email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.email_var).grid(row=1, column=1, padx=5, pady=5)

        # Botones de cliente
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Crear", command=self.crear_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_cliente).pack(side=tk.LEFT, padx=5)

        # Tabla de clientes
        self.tree_clientes = self.crear_tabla(
            self.tab_clientes,
            ("ID", "Nombre", "Email"),
            [50, 200, 200],
            1, 0
        )
        self.tree_clientes.bind('<<TreeviewSelect>>', self.cliente_seleccionado)
        self.cargar_clientes()

    def init_vista_pedidos(self):
        # Frame para el formulario de pedidos
        form_frame = ttk.LabelFrame(self.tab_pedidos, text="Datos del Pedido", padding="10")
        form_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # Campos del formulario
        ttk.Label(form_frame, text="Cliente:").grid(row=0, column=0, sticky="w")
        self.cliente_pedido_var = tk.StringVar()
        self.combo_clientes = ttk.Combobox(form_frame, textvariable=self.cliente_pedido_var)
        self.combo_clientes.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Producto:").grid(row=1, column=0, sticky="w")
        self.producto_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.producto_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Cantidad:").grid(row=2, column=0, sticky="w")
        self.cantidad_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.cantidad_var).grid(row=2, column=1, padx=5, pady=5)

        # Botones de pedido
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Crear", command=self.crear_pedido).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar_pedido).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_pedido).pack(side=tk.LEFT, padx=5)

        # Tabla de pedidos
        self.tree_pedidos = self.crear_tabla(
            self.tab_pedidos,
            ("ID", "Cliente", "Producto", "Cantidad"),
            [50, 200, 200, 100],
            1, 0
        )
        self.tree_pedidos.bind('<<TreeviewSelect>>', self.pedido_seleccionado)
        self.actualizar_combo_clientes()
        self.cargar_pedidos()

    def crear_tabla(self, parent, columnas, anchos, row, column):
        table_frame = ttk.Frame(parent)
        table_frame.grid(row=row, column=column, padx=10, pady=5, sticky="nsew")

        tree = ttk.Treeview(table_frame, columns=columnas, show="headings")

        for col, ancho in zip(columnas, anchos):
            tree.heading(col, text=col)
            tree.column(col, width=ancho)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        return tree

    # Métodos para clientes
    def cargar_clientes(self):
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)

        clientes = self.cliente_controller.obtener_todos()
        for cliente in clientes:
            self.tree_clientes.insert("", "end", values=(cliente.id, cliente.nombre, cliente.email))

    def crear_cliente(self):
        nombre = self.nombre_var.get()
        email = self.email_var.get()

        if nombre and email:
            self.cliente_controller.crear(nombre, email)
            self.cargar_clientes()
            self.limpiar_campos_cliente()
            self.actualizar_combo_clientes()
            messagebox.showinfo("Éxito", "Cliente creado correctamente")
        else:
            messagebox.showerror("Error", "Todos los campos son requeridos")

    def actualizar_cliente(self):
        seleccion = self.tree_clientes.selection()
        if not seleccion:
            messagebox.showerror("Error", "Por favor seleccione un cliente")
            return

        cliente_id = self.tree_clientes.item(seleccion[0])['values'][0]
        nombre = self.nombre_var.get()
        email = self.email_var.get()

        if nombre and email:
            self.cliente_controller.actualizar(cliente_id, nombre, email)
            self.cargar_clientes()
            self.limpiar_campos_cliente()
            self.actualizar_combo_clientes()
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
        else:
            messagebox.showerror("Error", "Todos los campos son requeridos")

    def eliminar_cliente(self):
        seleccion = self.tree_clientes.selection()
        if not seleccion:
            messagebox.showerror("Error", "Por favor seleccione un cliente")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?"):
            cliente_id = self.tree_clientes.item(seleccion[0])['values'][0]
            self.cliente_controller.eliminar(cliente_id)
            self.cargar_clientes()
            self.limpiar_campos_cliente()
            self.actualizar_combo_clientes()
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente")

    # Métodos para pedidos
    def cargar_pedidos(self):
        for item in self.tree_pedidos.get_children():
            self.tree_pedidos.delete(item)

        pedidos = self.pedido_controller.obtener_todos()
        for pedido in pedidos:
            self.tree_pedidos.insert("", "end", values=(
                pedido.id,
                pedido.cliente.nombre,
                pedido.producto,
                pedido.cantidad
            ))

    def crear_pedido(self):
        cliente_nombre = self.cliente_pedido_var.get()
        producto = self.producto_var.get()
        cantidad = self.cantidad_var.get()

        if cliente_nombre and producto and cantidad:
            try:
                cantidad = int(cantidad)
                cliente = self.cliente_controller.obtener_por_nombre(cliente_nombre)
                if cliente:
                    self.pedido_controller.crear(cliente.id, producto, cantidad)
                    self.cargar_pedidos()
                    self.limpiar_campos_pedido()
                    messagebox.showinfo("Éxito", "Pedido creado correctamente")
                else:
                    messagebox.showerror("Error", "Cliente no encontrado")
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número")
        else:
            messagebox.showerror("Error", "Todos los campos son requeridos")

    def actualizar_pedido(self):
        seleccion = self.tree_pedidos.selection()
        if not seleccion:
            messagebox.showerror("Error", "Por favor seleccione un pedido")
            return

        pedido_id = self.tree_pedidos.item(seleccion[0])['values'][0]
        cliente_nombre = self.cliente_pedido_var.get()
        producto = self.producto_var.get()
        cantidad = self.cantidad_var.get()

        if cliente_nombre and producto and cantidad:
            try:
                cantidad = int(cantidad)
                cliente = self.cliente_controller.obtener_por_nombre(cliente_nombre)
                if cliente:
                    self.pedido_controller.actualizar(pedido_id, cliente.id, producto, cantidad)
                    self.cargar_pedidos()
                    self.limpiar_campos_pedido()
                    messagebox.showinfo("Éxito", "Pedido actualizado correctamente")
                else:
                    messagebox.showerror("Error", "Cliente no encontrado")
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número")
        else:
            messagebox.showerror("Error", "Todos los campos son requeridos")

    def eliminar_pedido(self):
        seleccion = self.tree_pedidos.selection()
        if not seleccion:
            messagebox.showerror("Error", "Por favor seleccione un pedido")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este pedido?"):
            pedido_id = self.tree_pedidos.item(seleccion[0])['values'][0]
            self.pedido_controller.eliminar(pedido_id)
            self.cargar_pedidos()
            self.limpiar_campos_pedido()
            messagebox.showinfo("Éxito", "Pedido eliminado correctamente")

    def actualizar_combo_clientes(self):
        clientes = self.cliente_controller.obtener_todos()
        self.combo_clientes['values'] = [cliente.nombre for cliente in clientes]

    # Métodos auxiliares
    def cliente_seleccionado(self, event):
        seleccion = self.tree_clientes.selection()
        if seleccion:
            item = self.tree_clientes.item(seleccion[0])
            self.nombre_var.set(item['values'][1])
            self.email_var.set(item['values'][2])

    def pedido_seleccionado(self, event):
        seleccion = self.tree_pedidos.selection()
        if seleccion:
            item = self.tree_pedidos.item(seleccion[0])
            self.cliente_pedido_var.set(item['values'][1])
            self.producto_var.set(item['values'][2])
            self.cantidad_var.set(item['values'][3])

    def limpiar_campos_cliente(self):
        self.nombre_var.set("")
        self.email_var.set("")

    def limpiar_campos_pedido(self):
        self.cliente_pedido_var.set("")
        self.producto_var.set("")
        self.cantidad_var.set("")


if __name__ == "__main__":
    root = ThemedTk(theme="clam")
    app = App(root)
    root.mainloop()