import tkinter as tk
from tkinter import ttk, messagebox

# -----------------------------
# Import functions
# -----------------------------

from retirement import (
    fixedInvestor,
    variableInvestor,
    finallyRetired,
    maximumExpensed
)

# ------------------------------------------------------
# GUI Application
# ------------------------------------------------------

class RetirementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Retirement Financial Calculator")
        self.geometry("500x480")

        self.function_var = tk.StringVar()
        self.inputs_frame = None

        # Title
        tk.Label(self, text="Select Function:", font=("Arial", 14, "bold")).pack(pady=10)

        # Dropdown menu
        functions = ["fixedInvestor", "variableInvestor", "finallyRetired", "maximumExpensed"]
        ttk.Combobox(self, textvariable=self.function_var, values=functions, state="readonly").pack()
        self.function_var.trace_add("write", lambda *args: self.show_inputs())


        # Container for inputs
        self.inputs_container = tk.Frame(self)
        self.inputs_container.pack(pady=10)

        # Run button
        tk.Button(self, text="Compute", command=self.compute, bg="#4CAF50", fg="white").pack(pady=10)

        # Output label
        tk.Label(self, text="Result:", font=("Arial", 14, "bold")).pack(pady=10)

        # Output text box
        self.output = tk.Text(self, height=10, width=55, wrap="word")
        self.output.pack()

    # ------------------------------------
    # Build dynamic input fields
    # ------------------------------------
    def show_inputs(self, *args):
        # Remove previous widgets
        for w in self.inputs_container.winfo_children():
            w.destroy()

        func = self.function_var.get()

        # Dictionary of fields per function
        fields = {
            "fixedInvestor": ["principal", "rate", "years"],
            "variableInvestor": ["principal", "rateList (comma-separated)"],
            "finallyRetired": ["balance", "expense", "rate"],
            "maximumExpensed": ["balance", "rate", "years"]
        }

        self.input_entries = {}

        for f in fields[func]:
            row = tk.Frame(self.inputs_container)
            row.pack(fill="x", pady=2)

            tk.Label(row, text=f+":", width=20, anchor="w").pack(side="left")
            entry = tk.Entry(row)
            entry.pack(side="right", fill="x", expand=True)

            self.input_entries[f] = entry

    # ------------------------------------
    # Compute result
    # ------------------------------------
    def compute(self):
        func = self.function_var.get()

        if not func:
            messagebox.showerror("Error", "Please select a function.")
            return

        try:
            # Collect parameters
            params = {}
            for key, entry in self.input_entries.items():
                txt = entry.get().strip()

                if txt == "":
                    raise ValueError(f"Input missing: '{key}'")

                if key == "rateList (comma-separated)":
                    params["rateList"] = [float(x) for x in txt.split(",")]
                elif key in ("principal", "balance", "expense", "rate", "tolerance"):
                    params[key] = float(txt)
                else:
                    params[key] = int(txt)

            # Call appropriate function
            if func == "fixedInvestor":
                result = fixedInvestor(params["principal"], params["rate"], params["years"])

            elif func == "variableInvestor":
                result = variableInvestor(params["principal"], params["rateList"])

            elif func == "finallyRetired":
                result = finallyRetired(params["balance"], params["expense"], params["rate"])

            elif func == "maximumExpensed":
                result = maximumExpensed(params["balance"], params["rate"], params["years"])

            else:
                result = "Unknown function"

            # Display result
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, f"Result: {result}")

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Runtime Error", str(e))


# ------------------------------------------------------
# Run App
# ------------------------------------------------------

if __name__ == "__main__":
    app = RetirementApp()
    app.mainloop()
