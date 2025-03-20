import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import tkinter as tk
from tkinter import ttk
import json

class GraphApp:
    def __init__(self, root, config_file="config.json"):
        self.root = root
        self.root.title("Choose columns for 3D plot")
        
        self.config_file = config_file
        self.config = self.load_config()
        self.sheet_url = self.config.get("sheet_url")
        self.gid = self.config.get("gid") or 0

        if not self.sheet_url:
            print("Error: sheet URL not found in configuration file.")
            return
        
        self.headers, self.values = self.get_google_sheets_data()
        
        if self.values.shape[1] < 3:
            print("Error: sheet must have at least 3 numeric columns for 3D plot.")
            return
        
        self.create_ui()
    
    def load_config(self):
        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error on decoding configuration file '{self.config_file}'. Check JSON sintax.")
            return {}

    def get_google_sheets_data(self):
        df = pd.read_csv(self.sheet_url + self.gid, decimal=",")
        df = df.dropna(axis=1, how="all")
        df = df.drop(columns=[col for col in df.columns if "Unnamed" in col], errors="ignore")
        df_numeric = df.select_dtypes(include=[np.number])
        df_numeric = df_numeric.dropna(how="all")
        headers = df.columns.tolist()
        values = df.dropna().to_numpy()
        return headers, values
    
    def create_ui(self):
        # Add plot title input
        self.label_title = ttk.Label(self.root, text="Title:")
        self.label_title.grid(row=0, column=0, padx=0, pady=5)
        self.entry_title = ttk.Entry(self.root)
        self.entry_title.grid(row=0, column=1, padx=10, pady=5)

        self.label_x = ttk.Label(self.root, text="Choose X axis:")
        self.label_x.grid(row=1, column=0, padx=10, pady=5)
        self.combo_x = ttk.Combobox(self.root, values=self.headers)
        self.combo_x.grid(row=1, column=1, padx=10, pady=5)
        
        self.label_y = ttk.Label(self.root, text="Choose Y axis:")
        self.label_y.grid(row=2, column=0, padx=10, pady=5)
        self.combo_y = ttk.Combobox(self.root, values=self.headers)
        self.combo_y.grid(row=2, column=1, padx=10, pady=5)
        
        self.label_z = ttk.Label(self.root, text="Choose Z axis:")
        self.label_z.grid(row=3, column=0, padx=10, pady=5)
        self.combo_z = ttk.Combobox(self.root, values=self.headers)
        self.combo_z.grid(row=3, column=1, padx=10, pady=5)
        
        self.button_plot = ttk.Button(self.root, text="Plot graph", command=self.plot_graph)
        self.button_plot.grid(row=4, column=0, columnspan=2, pady=10)
    
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
        surf = ax.plot_surface(grid_x, grid_y, grid_z, cmap="viridis", edgecolor='none')
        
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
