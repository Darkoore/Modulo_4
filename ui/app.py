import tkinter as tk
from ui.menu_frame import MenuFrame
from ui.gestion_clientes_frame import GestionClientesFrame
from ui.compras_frame import ComprasFrame


class App:

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión")

        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        for FrameClass in (MenuFrame, GestionClientesFrame, ComprasFrame):
            frame = FrameClass(self.container, self)
            self.frames[FrameClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuFrame")

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()
