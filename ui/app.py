import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

from core import Parametros as prm
from core.Modelos import p_mantenimiento, q_mantenimiento, p_impermeable, q_impermeable


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación Yacimiento Lineal")
        self.root.geometry("1100x700")
        self.create_widgets()

    def create_widgets(self):
        # === Panel izquierdo (parámetros) ===
        self.frame_params = ttk.Frame(self.root, padding=10)
        self.frame_params.grid(row=0, column=0, sticky="nsew")

        # === Panel derecho (gráficas) ===
        self.frame_graficas = ttk.Frame(self.root)
        self.frame_graficas.grid(row=0, column=1, sticky="nsew", padx=15)
        self.frame_graficas.columnconfigure(0, weight=1)
        self.frame_graficas.rowconfigure(0, weight=1)
        self.frame_graficas.rowconfigure(1, weight=1)

        self.build_param_inputs()
        self.build_controls()

    def build_param_inputs(self):
        ttk.Label(
            self.frame_params,
            text="🔧 Parámetros del yacimiento",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=5)

        params = [
            ("Porosidad (φ)", "phi", prm.phi),
            ("Viscosidad (μ) [cp]", "mu", prm.mu),
            ("Compresibilidad (ct) [psi⁻¹]", "ct", prm.ct),
            ("Permeabilidad (k) [md]", "k", prm.k),
            ("Longitud (L) [ft]", "L", prm.L),
            ("Ancho (b) [ft]", "b", prm.b),
            ("Altura (h) [ft]", "h", prm.h),
            ("Factor Vol. (B)", "B", prm.B),
            ("Presión inicial (pi)", "pi", prm.pi),
            ("Presión fondo fluyente (pwf)", "pwf", prm.pwf)
        ]

        self.param_entries = {}
        for i, (label, key, val) in enumerate(params):
            ttk.Label(self.frame_params, text=label).grid(row=i+1, column=0, sticky="w", pady=2)
            entry = ttk.Entry(self.frame_params, width=15)
            entry.insert(0, str(val))
            entry.grid(row=i+1, column=1, pady=2, padx=5)
            self.param_entries[key] = entry

    def build_controls(self):
        row = len(self.param_entries) + 2
        ttk.Label(self.frame_params, text="Tipo de yacimiento").grid(row=row, column=0, sticky="w", pady=(10, 0))

        self.caso_var = tk.StringVar(value="1")
        ttk.Radiobutton(
            self.frame_params,
            text="Presión externa (mantenimiento)",
            variable=self.caso_var, value="1"
        ).grid(row=row+1, column=0, sticky="w")
        ttk.Radiobutton(
            self.frame_params,
            text="Frontera impermeable",
            variable=self.caso_var, value="2"
        ).grid(row=row+2, column=0, sticky="w")

        self.run_btn = ttk.Button(
            self.frame_params,
            text="Ejecutar Simulación",
            command=self.run_simulation
        )
        self.run_btn.grid(row=row+3, column=0, columnspan=2, pady=10)

    def actualizar_parametros(self):
        for key, entry in self.param_entries.items():
            try:
                val = float(entry.get())
                setattr(prm, key, val)
            except ValueError:
                messagebox.showerror("Error", f"Valor inválido en {key}")
                return False

        # Recalcular parámetros derivados
        prm.eta = 0.00633 * prm.k / (prm.phi * prm.mu * prm.ct)
        prm.delta_p = prm.pi - prm.pwf
        prm.A = prm.b * prm.h
        prm.conversion_factor = 0.001127 * prm.k * prm.A / (prm.mu * prm.B * prm.L)
        return True

    def run_simulation(self):
        if not self.actualizar_parametros():
            return

        caso = int(self.caso_var.get())
        tiempos = [0, 0.01, 0.1, 1, 10, 100, 1000]
        x_vals = np.linspace(0, prm.L, 300)
        t_vals = np.logspace(-2, 3, 200)

        # === Gráfica de presión ===
        fig_p, ax_p = plt.subplots(figsize=(5.8, 3.3))
        fig_p.subplots_adjust(left=0.14, right=0.96, top=0.88, bottom=0.18)

        colors = plt.cm.viridis(np.linspace(0, 1, len(tiempos))) if caso == 1 else plt.cm.plasma(np.linspace(0, 1, len(tiempos)))

        for i, t in enumerate(tiempos):
            if caso == 1:
                p_vals = [p_mantenimiento(x, t) for x in x_vals]
            else:
                p_vals = [p_impermeable(x, t) for x in x_vals]
            ax_p.plot(x_vals, p_vals, color=colors[i], label=f"t={t} días")

        ax_p.set_xlabel("Distancia x [ft]")
        ax_p.set_ylabel("Presión [psia]")
        ax_p.set_title("Perfil de Presión", pad=10)
        ax_p.grid(True, alpha=0.3)
        ax_p.legend(fontsize=8, loc='best')

        # === Gráfica de gasto ===
        fig_q, ax_q = plt.subplots(figsize=(5.8, 3.3))
        fig_q.subplots_adjust(left=0.14, right=0.96, top=0.88, bottom=0.18)

        if caso == 1:
            q_vals = [q_mantenimiento(t) for t in t_vals]
            ax_q.semilogx(t_vals, q_vals, 'r', linewidth=2)
        else:
            q_vals = [q_impermeable(t) for t in t_vals]
            ax_q.semilogx(t_vals, q_vals, 'b', linewidth=2)

        ax_q.set_xlabel("Tiempo [días]")
        ax_q.set_ylabel("Gasto [BPD]")
        ax_q.set_title("Curva de Gasto vs Tiempo", pad=10)
        ax_q.grid(True, alpha=0.3)

        # === Limpiar y mostrar dentro del Frame ===
        for child in self.frame_graficas.winfo_children():
            child.destroy()

        canvas1 = FigureCanvasTkAgg(fig_p, master=self.frame_graficas)
        canvas1.get_tk_widget().grid(row=0, column=0, sticky="nsew", pady=(0, 25))
        canvas1.draw()

        canvas2 = FigureCanvasTkAgg(fig_q, master=self.frame_graficas)
        canvas2.get_tk_widget().grid(row=1, column=0, sticky="nsew", pady=(15, 0))
        canvas2.draw()

        messagebox.showinfo("Éxito", "Simulación completada con éxito")
        
