import tkinter as tk
from tkinter import ttk, messagebox
import sys
from pathlib import Path
import webbrowser
import os

# Add the project root to Python path
project_root = Path.cwd()
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Import the presentation generator
from main import create_presentation

class PresentationGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Presentation Generator")
        self.root.geometry("600x400")
        
        # Configure style
        style = ttk.Style()
        style.configure("TLabel", padding=5)
        style.configure("TButton", padding=5)
        style.configure("TEntry", padding=5)
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Presentation Generator", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Title input
        ttk.Label(main_frame, text="Presentation Title:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.title_var = tk.StringVar()
        title_entry = ttk.Entry(main_frame, textvariable=self.title_var, width=40)
        title_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Number of slides
        ttk.Label(main_frame, text="Number of Slides:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.slides_var = tk.IntVar(value=6)
        slides_spinbox = ttk.Spinbox(main_frame, from_=3, to=10, textvariable=self.slides_var, width=5)
        slides_spinbox.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Style selection
        ttk.Label(main_frame, text="Style:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.style_var = tk.StringVar(value="dark")
        style_combo = ttk.Combobox(main_frame, textvariable=self.style_var, values=["dark", "light"], state="readonly", width=10)
        style_combo.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Generate button
        generate_button = ttk.Button(main_frame, text="Generate Presentation", command=self.generate_presentation)
        generate_button.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Status label
        self.status_var = tk.StringVar()
        status_label = ttk.Label(main_frame, textvariable=self.status_var, wraplength=500)
        status_label.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        
    def generate_presentation(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showerror("Error", "Please enter a presentation title")
            return
        
        try:
            self.status_var.set("Generating presentation... Please wait.")
            self.root.update()
            
            output_path = create_presentation(
                title,
                num_slides=self.slides_var.get(),
                style=self.style_var.get()
            )
            
            self.status_var.set(f"Presentation generated successfully!\nSaved to: {output_path}")
            
            # Ask if user wants to open the presentation
            if messagebox.askyesno("Success", "Would you like to open the presentation?"):
                webbrowser.open(f"file://{output_path}")
                
        except Exception as e:
            self.status_var.set(f"Error generating presentation: {str(e)}")
            messagebox.showerror("Error", f"Failed to generate presentation: {str(e)}")

def main():
    root = tk.Tk()
    app = PresentationGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 