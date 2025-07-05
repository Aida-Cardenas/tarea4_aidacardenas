import csv
from collections import defaultdict, Counter
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk

class MarkovModel:
    def __init__(self, attributes):
        self.attributes = attributes
        self.states = set()
        self.transitions = defaultdict(Counter)
        self.initialized = False

    def initialize_uniform(self, data):
        for row in data:
            state = tuple(row[attr] for attr in self.attributes)
            self.states.add(state)
        for s1 in self.states:
            for s2 in self.states:
                self.transitions[s1][s2] = 1
        self.initialized = True

    def update_transitions(self, data, day_col):
        data_sorted = sorted(data, key=lambda x: int(x[day_col]))
        for i in range(len(data_sorted) - 1):
            day1 = int(data_sorted[i][day_col])
            day2 = int(data_sorted[i+1][day_col])
            if day2 == day1 + 1:
                s1 = tuple(data_sorted[i][attr] for attr in self.attributes)
                s2 = tuple(data_sorted[i+1][attr] for attr in self.attributes)
                self.transitions[s1][s2] += 1

    def normalize(self):
        self.probabilities = {}
        for s1, counter in self.transitions.items():
            total = sum(counter.values())
            self.probabilities[s1] = {s2: count/total for s2, count in counter.items()}

    def print_model(self):
        print("\nModelo de Markov (Probabilidades de transición):")
        for s1, transitions in self.probabilities.items():
            print(f"Desde {s1}:")
            for s2, prob in transitions.items():
                print(f"  -> {s2}: {prob:.3f}")

    def predict_next(self, current_state):
        if current_state not in self.probabilities:
            print("Estado no encontrado en el modelo.")
            return None
        transitions = self.probabilities[current_state]
        next_state = max(transitions, key=transitions.get)
        return next_state

    def get_model_str(self):
        model_str = ""
        for s1, transitions in self.probabilities.items():
            model_str += f"Desde {s1}:\n"
            for s2, prob in transitions.items():
                model_str += f"  -> {s2}: {prob:.3f}\n"
        return model_str

def read_csv(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data, reader.fieldnames

class MarkovApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modelo de Markov con Aprendizaje por Refuerzo")
        self.root.configure(bg="#f0f4f8")
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background="#f0f4f8")
        style.configure('TButton', background="#1976d2", foreground="white", font=('Arial', 10, 'bold'))
        style.map('TButton', background=[('active', '#1565c0')])
        style.configure('TLabel', background="#f0f4f8", foreground="#222")
        style.configure('TCombobox', fieldbackground="#e3f2fd", background="#e3f2fd")
        self.model = None
        self.data = None
        self.fieldnames = None
        self.day_col = None
        self.attributes = None
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self.root, padding=10, style='TFrame')
        frm.grid()
        self.btn_load = ttk.Button(frm, text="Cargar CSV", command=self.load_csv, style='TButton')
        self.btn_load.grid(row=0, column=0, padx=5, pady=5)
        self.lbl_file = ttk.Label(frm, text="Ningún archivo cargado", style='TLabel')
        self.lbl_file.grid(row=0, column=1, padx=5, pady=5)
        self.cmb_day = ttk.Combobox(frm, state="readonly", style='TCombobox')
        self.cmb_day.grid(row=1, column=0, padx=5, pady=5)
        self.cmb_day.bind("<<ComboboxSelected>>", self.set_day_col)
        self.btn_train = ttk.Button(frm, text="Entrenar Modelo", command=self.train_model, state="disabled", style='TButton')
        self.btn_train.grid(row=1, column=1, padx=5, pady=5)
        self.txt_model = tk.Text(frm, width=70, height=15, bg="#e3f2fd", fg="#222", font=('Consolas', 10))
        self.txt_model.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.btn_predict = ttk.Button(frm, text="Predecir Siguiente Estado", command=self.predict_state, state="disabled", style='TButton')
        self.btn_predict.grid(row=3, column=0, columnspan=2, pady=10)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        try:
            self.data, self.fieldnames = read_csv(file_path)
            self.lbl_file.config(text=os.path.basename(file_path))
            self.cmb_day['values'] = self.fieldnames
            self.cmb_day.set('')
            self.btn_train.config(state="disabled")
            self.btn_predict.config(state="disabled")
            self.txt_model.delete(1.0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

    def set_day_col(self, event):
        self.day_col = self.cmb_day.get()
        self.attributes = [col for col in self.fieldnames if col != self.day_col]
        is_numeric = True
        for row in self.data:
            try:
                int(row[self.day_col])
            except (ValueError, TypeError):
                is_numeric = False
                break
        if is_numeric:
            self.btn_train.config(state="normal")
        else:
            self.btn_train.config(state="disabled")
            messagebox.showerror("Error de columna de día", "La columna seleccionada no es numérica (escoger columna dia) (debe contener solo números).")

    def train_model(self):
        if not self.data or not self.day_col:
            messagebox.showwarning("Advertencia", "Cargue un archivo y seleccione la columna de día.")
            return
        self.model = MarkovModel(self.attributes)
        self.model.initialize_uniform(self.data)
        self.model.update_transitions(self.data, self.day_col)
        self.model.normalize()
        self.txt_model.delete(1.0, tk.END)
        self.txt_model.insert(tk.END, self.model.get_model_str())
        self.btn_predict.config(state="normal")

    def get_attribute_values(self):
        values = {attr: set() for attr in self.attributes}
        for row in self.data:
            for attr in self.attributes:
                values[attr].add(row[attr])
        return {k: sorted(list(v)) for k, v in values.items()}

    def predict_state(self):
        if not self.model:
            return
        attr_values = self.get_attribute_values()
        pred_win = tk.Toplevel(self.root)
        pred_win.title("Predecir Siguiente Estado")
        pred_win.configure(bg="#f0f4f8")
        entries = {}
        for i, attr in enumerate(self.attributes):
            ttk.Label(pred_win, text=attr, style='TLabel').grid(row=i, column=0, padx=5, pady=5)
            cmb = ttk.Combobox(pred_win, values=attr_values[attr], state="readonly", style='TCombobox')
            cmb.grid(row=i, column=1, padx=5, pady=5)
            entries[attr] = cmb
        def do_predict():
            vals = [entries[attr].get() for attr in self.attributes]
            if any(v == '' for v in vals):
                messagebox.showwarning("Predicción", "Debes seleccionar un valor para cada atributo.", parent=pred_win)
                return
            current = tuple(vals)
            next_state = self.model.predict_next(current)
            if next_state:
                messagebox.showinfo("Predicción", f"El estado más probable siguiente es: {next_state}", parent=pred_win)
            else:
                messagebox.showwarning("Predicción", "Estado no encontrado en el modelo.", parent=pred_win)
        ttk.Button(pred_win, text="Predecir", command=do_predict, style='TButton').grid(row=len(self.attributes), column=0, columnspan=2, pady=10)

def main():
    root = tk.Tk()
    app = MarkovApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
