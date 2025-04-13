import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

class GraphApp:
    def __init__(self, root):
        style = ttk.Style()
        style.configure(
            "Custom.TButton",
            font=("TkDefaultFont", 10, "bold"),
            background="#ffffff",
            foreground="#010180"
        )
        style.map(
            "Custom.TButton",
            background=[("active", "#aaaaaa")],
            foreground=[("active", "#010140")]
        )

        self.root = root
        self.root.configure(bg="#010180")
        self.root.title("3D Graph from Google Sheets")

        self.headers = []
        self.values = None

        self.create_url_input_ui()

    def create_url_input_ui(self):
        self.root.columnconfigure(1, weight=1)

        self.branding_img = PhotoImage(file="./docs/3D-plotter-logo.png")
        self.image_label = ttk.Label(self.root, image=self.branding_img)
        self.image_label.grid(row=0, column=0, rowspan=5, padx=10, pady=5, sticky="n")

        form_frame = tk.Frame(self.root, bg="#010180")
        form_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        form_frame.columnconfigure(0, weight=1)

        title_style = {
            "font": ("TkDefaultFont", 12, "italic bold"),
            "foreground": "#ffffff",
            "background": "#010180"
        }

        label_style = {
            "font": ("TkDefaultFont", 10, "bold"),
            "foreground": "#ffffff",
            "background": "#010180"
        }

        footer_style = {
            "font": ("TkDefaultFont", 8),
            "foreground": "#ffffff",
            "background": "#010180"
        }

        self.label_url = tk.Label(form_frame, text="Welcome to 3D Graph from Google Sheets!", **title_style)
        self.label_url.grid(row=0, column=0, sticky="w", pady=(0, 1))

        self.label_url = tk.Label(form_frame, text="Fill the form below with sheet URL and tab GID.", **title_style)
        self.label_url.grid(row=1, column=0, sticky="w", pady=(0, 1))

        self.label_gid = tk.Label(form_frame, text="", **label_style)
        self.label_gid.grid(row=2, column=0, sticky="w", pady=(0, 1))

        self.label_url = tk.Label(form_frame, text="Google Sheets Base URL:", **label_style)
        self.label_url.grid(row=3, column=0, sticky="w", pady=(0, 1))

        self.entry_url = ttk.Entry(form_frame)
        self.entry_url.grid(row=4, column=0, sticky="ew", pady=(0, 5))

        self.label_gid = tk.Label(form_frame, text="GID:", **label_style)
        self.label_gid.grid(row=5, column=0, sticky="w", pady=(0, 1))

        self.entry_gid = ttk.Entry(form_frame)
        self.entry_gid.grid(row=6, column=0, sticky="ew", pady=(0, 5))

        self.label_gid = tk.Label(form_frame, text="", **label_style)
        self.label_gid.grid(row=7, column=0, sticky="w", pady=(0, 1))
        self.label_gid = tk.Label(form_frame, text="", **label_style)
        self.label_gid.grid(row=8, column=0, sticky="w", pady=(0, 1))

        self.button_load = ttk.Button(form_frame, text="Load Data", command=self.load_data, style="Custom.TButton")
        self.button_load.grid(row=9, column=0, sticky="ew", pady=(5, 0))

        self.footer_label = ttk.Label(
            form_frame,
            text="\n\nby Mauro Imamura @ 2025  [https://github.com/MauroImamura]",
            **footer_style
        )
        self.footer_label.grid(row=10, column=0, columnspan=2, pady=10, sticky="ew")

    def load_data(self):
        base_url = self.entry_url.get().strip().replace("/edit?usp=sharing", "/export?format=csv&gid=")
        gid = self.entry_gid.get().strip() or "0"
        sheet_url = f"{base_url}{gid}"

        try:
            df = pd.read_csv(sheet_url, decimal=",")
        except Exception as e:
            print("Erro ao carregar a planilha:", e)
            return

        df = df.dropna(axis=1, how="all")
        df = df.drop(columns=[col for col in df.columns if "Unnamed" in col], errors="ignore")
        df_numeric = df.select_dtypes(include=[np.number]).dropna(how="all")
        self.headers = df.columns.tolist()
        self.values = df.dropna().to_numpy()

        if self.values.shape[1] < 3:
            print("Erro: planilha precisa ter pelo menos 3 colunas para o gráfico.")
            return

        self.create_ui()

    def create_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.columnconfigure(1, weight=1)

        self.branding_img = PhotoImage(file="./docs/schema.png")
        self.image_label = ttk.Label(self.root, image=self.branding_img)
        self.image_label.grid(row=0, column=0, rowspan=6, padx=10, pady=5, sticky="n")

        form_frame = tk.Frame(self.root, bg="#010180")
        form_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        form_frame.columnconfigure(0, weight=1)

        label_style = {
            "font": ("TkDefaultFont", 10, "bold"),
            "foreground": "#ffffff",
            "background": "#010180"
        }

        footer_style = {
            "font": ("TkDefaultFont", 8),
            "foreground": "#ffffff",
            "background": "#010180"
        }

        self.label_title = ttk.Label(form_frame, text="Title:", **label_style)
        self.label_title.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")

        self.entry_title = ttk.Entry(form_frame)
        self.entry_title.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="ew")

        self.label_x = ttk.Label(form_frame, text="Choose X axis:", **label_style)
        self.label_x.grid(row=2, column=0, padx=10, pady=(5, 0), sticky="w")

        self.combo_x = ttk.Combobox(form_frame, values=self.headers)
        self.combo_x.grid(row=3, column=0, padx=10, pady=(0, 5), sticky="ew")

        self.label_y = ttk.Label(form_frame, text="Choose Y axis:", **label_style)
        self.label_y.grid(row=4, column=0, padx=10, pady=(5, 0), sticky="w")

        self.combo_y = ttk.Combobox(form_frame, values=self.headers)
        self.combo_y.grid(row=5, column=0, padx=10, pady=(0, 5), sticky="ew")

        self.label_z = ttk.Label(form_frame, text="Choose Z axis:", **label_style)
        self.label_z.grid(row=6, column=0, padx=10, pady=(5, 0), sticky="w")

        self.combo_z = ttk.Combobox(form_frame, values=self.headers)
        self.combo_z.grid(row=7, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.button_plot = ttk.Button(form_frame, text="Plot graph", command=self.plot_graph, style="Custom.TButton")
        self.button_plot.grid(row=8, column=0, padx=10, pady=5, sticky="ew")

        self.footer_label = ttk.Label(
            form_frame,
            text="\n\nby Mauro Imamura @ 2025  [https://github.com/MauroImamura]",
            **footer_style
        )
        self.footer_label.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def plot_graph(self):
        col1 = self.headers.index(self.combo_x.get())
        col2 = self.headers.index(self.combo_y.get())
        col3 = self.headers.index(self.combo_z.get())

        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')

        x = self.values[:, col1].astype(float)
        y = self.values[:, col2].astype(float)
        z = self.values[:, col3].astype(float)

        grid_x, grid_y = np.meshgrid(
            np.linspace(min(x), max(x), 50),
            np.linspace(min(y), max(y), 50)
        )

        grid_z = griddata((x, y), z, (grid_x, grid_y), method='cubic')

        surf = ax.plot_surface(grid_x, grid_y, grid_z, cmap="ocean", edgecolor='none')

        ax.set_xlabel(self.combo_x.get(), fontsize=12)
        ax.set_ylabel(self.combo_y.get(), fontsize=12)
        ax.set_zlabel(self.combo_z.get(), fontsize=12)
        ax.set_title(self.entry_title.get(), fontsize=14, fontweight='bold')

        fig.colorbar(surf, shrink=0.5, aspect=5)
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
