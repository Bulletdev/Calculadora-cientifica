import tkinter as tk
import math
import cmath
from PIL import Image, ImageTk
import time
import threading

class CalculadoraCientifica :
    def __init__(self, master):
        self.master = master
        master.title("BULLET Calculator")
        master.configure(bg='#2F4F4F')
        master.geometry("300x500")
 
        self.shift_active = False
        self.alpha_active = False
        self.hyp_active = False
        self.current_expression = ""
        self.last_answer = 0
        self.memory = 0
        self.angle_mode = "DEG"
        self.calculation_history = []
        self.history_index = -1

        self.display_frame = tk.Frame(master, bg='#2F4F4F', bd=5)
        self.display_frame.pack(pady=(20,10), padx=10, fill=tk.X)

        logo_image = Image.open("Bullet.png")

        width, height = logo_image.size

        new_width = 75

        new_height = int((new_width / width) * height)

        logo_image = logo_image.resize((new_width, new_height), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)

        self.logo = tk.Label(self.display_frame, image=logo_photo, bg='#2F4F4F')
        self.logo.image = logo_photo  
        self.logo.pack(anchor='w')

        self.model = tk.Label(self.display_frame, text="BulletDev", font=('Arial', 10), fg='white', bg='#2F4F4F')
        self.model.pack(anchor='e')

        self.svpam = tk.Label(self.display_frame, text="B-U.L.L.E.T.", font=('Arial', 10), fg='red', bg='#2F4F4F')
        self.svpam.pack(anchor='w')

        self.display = tk.Entry(self.display_frame, width=20, font=('Digital-7', 20), justify='right', bd=0, bg='#C0C0C0')
        self.display.pack(fill=tk.X, padx=5, pady=5)

        self.buttons_frame = tk.Frame(master, bg='#2F4F4F')
        self.buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.buttons = {}
        botoes = [
            ('SHIFT', self.shift, 'orange'), ('ALPHA', self.alpha, 'skyblue'), ('REPLAY', self.replay, 'lightgray'), ('MODE', self.mode, 'lightgray'), ('ON', self.on, 'red'),
            ('x!', self.factorial, 'gray'), ('nCr', self.combination, 'gray'), ('Pol(', self.polar, 'gray'), ('Rec(', self.rectangular, 'gray'), ('x^3', self.cube, 'gray'),
            ('d/c', self.fraction, 'gray'), ('√', self.sqrt, 'gray'), ('x^2', self.square, 'gray'), ('^', self.power, 'gray'), ('log', self.log, 'gray'),
            ('(-)', self.negate, 'gray'), ('°\'\"', self.deg_min_sec, 'gray'), ('hyp', self.hyp, 'gray'), ('sin', self.sin, 'gray'), ('cos', self.cos, 'gray'),
            ('RCL', self.rcl, 'gray'), ('ENG', self.eng, 'gray'), ('(', self.parenthesis, 'gray'), (')', self.parenthesis, 'gray'), ('tan', self.tan, 'gray'),
            ('7', lambda: self.add_to_expression('7'), 'white'), ('8', lambda: self.add_to_expression('8'), 'white'), ('9', lambda: self.add_to_expression('9'), 'white'), ('DEL', self.delete, 'red'), ('AC', self.clear, 'red'),
            ('4', lambda: self.add_to_expression('4'), 'white'), ('5', lambda: self.add_to_expression('5'), 'white'), ('6', lambda: self.add_to_expression('6'), 'white'), ('×', self.multiply, 'gray'), ('÷', self.divide, 'gray'),
            ('1', lambda: self.add_to_expression('1'), 'white'), ('2', lambda: self.add_to_expression('2'), 'white'), ('3', lambda: self.add_to_expression('3'), 'white'), ('+', self.add, 'gray'), ('-', self.subtract, 'gray'),
            ('0', lambda: self.add_to_expression('0'), 'white'), ('.', lambda: self.add_to_expression('.'), 'white'), ('×10^x', self.exp, 'gray'), ('Ans', self.answer, 'gray'), ('=', self.calculate, 'lightgreen')
        ]

        row = 0
        col = 0
        for (text, command, color) in botoes:
            btn = tk.Button(self.buttons_frame, text=text, command=command, width=5, height=2, bg=color, fg='black', font=('Arial', 8, 'bold'))
            btn.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
            self.buttons[text] = btn
            col += 1
            if col > 4:
                col = 0
                row += 1

        for i in range(5):
            self.buttons_frame.grid_columnconfigure(i, weight=1)
        for i in range(8):
            self.buttons_frame.grid_rowconfigure(i, weight=1)

        self.on_button = tk.Button(self.buttons_frame, text="ON", command=self.on, width=5, height=2, bg='red', fg='black', font=('Arial', 8, 'bold'))
        self.on_button.grid(row=0, column=4, padx=1, pady=1, sticky="nsew")

    def shift(self):
        self.shift_active = not self.shift_active
        self.alpha_active = False
        if self.shift_active:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "SHIFT")
            self.update_button_functions(shift=True)
        else:
            self.update_display()
            self.update_button_functions(shift=False)

    def alpha(self):
        self.alpha_active = not self.alpha_active
        self.shift_active = False
        if self.alpha_active:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "ALPHA")
            self.update_button_functions(alpha=True)
        else:
            self.update_display()
            self.update_button_functions(alpha=False)

    def update_button_functions(self, shift=False, alpha=False):
        if shift:
            self.buttons['x!']['text'] = 'P'
            self.buttons['nCr']['text'] = 'C'
            self.buttons['log']['text'] = '10^x'
            self.buttons['(-)']['text'] = 'Abs'
            self.buttons['hyp']['text'] = 'DRG►'
        elif alpha:
            self.buttons['7']['text'] = 'A'
            self.buttons['8']['text'] = 'B'
            self.buttons['9']['text'] = 'C'
            self.buttons['4']['text'] = 'D'
            self.buttons['5']['text'] = 'E'
            self.buttons['6']['text'] = 'F'
        else:
            self.buttons['x!']['text'] = 'x!'
            self.buttons['nCr']['text'] = 'nCr'
            self.buttons['log']['text'] = 'log'
            self.buttons['(-)']['text'] = '(-)'
            self.buttons['hyp']['text'] = 'hyp'
            self.buttons['7']['text'] = '7'
            self.buttons['8']['text'] = '8'
            self.buttons['9']['text'] = '9'
            self.buttons['4']['text'] = '4'
            self.buttons['5']['text'] = '5'
            self.buttons['6']['text'] = '6'

    def add_to_expression(self, value):
        if self.alpha_active:
            alpha_map = {'7': 'A', '8': 'B', '9': 'C', '4': 'D', '5': 'E', '6': 'F'}
            value = alpha_map.get(value, value)
        self.current_expression += str(value)
        self.update_display()

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.current_expression)

    def calculate(self):
        try:
            result = eval(self.current_expression)
            self.last_answer = result
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
            self.calculation_history.append(self.current_expression)
            self.current_expression = str(result)
            self.history_index = -1
        except:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Error")
            self.current_expression = ""

    def clear(self):
        self.current_expression = ""
        self.update_display()

    def delete(self):
        self.current_expression = self.current_expression[:-1]
        self.update_display()

    def replay(self):
        if not self.calculation_history:
            return
        
        if self.history_index == -1:
            self.history_index = len(self.calculation_history) - 1
        else:
            self.history_index = (self.history_index - 1) % len(self.calculation_history)
        
        self.current_expression = self.calculation_history[self.history_index]
        self.update_display()

    def mode(self):
        modes = ["DEG", "RAD", "GRAD"]
        current_index = modes.index(self.angle_mode)
        self.angle_mode = modes[(current_index + 1) % len(modes)]
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, f"Mode: {self.angle_mode}")

    def on(self):
        self.on_button.config(text="OFF")
        self.display.delete(0, tk.END)
        self.show_bye_message()

    def show_bye_message(self):
        message = "BYE"
        for i in range(len(message) + 1):
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, message[:i].rjust(len(message)))
            self.master.update()
            time.sleep(0.3)
        
        self.master.after(2000, self.close_app)

    def close_app(self):
        self.master.destroy()

    def factorial(self):
        try:
            n = int(eval(self.current_expression))
            result = math.factorial(n)
            self.current_expression = str(result)
            self.update_display()
        except:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Error")

    def combination(self):
        self.current_expression += "math.comb("
        self.update_display()

    def polar(self):
        self.current_expression += "cmath.polar("
        self.update_display()

    def rectangular(self):
        self.current_expression += "cmath.rect("
        self.update_display()

    def cube(self):
        self.current_expression += "**3"
        self.update_display()

    def fraction(self):
        try:
            value = eval(self.current_expression)
            frac = self.decimal_to_fraction(value)
            self.current_expression = f"{frac[0]}/{frac[1]}"
            self.update_display()
        except:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Error")

    def sqrt(self):
        self.current_expression += "math.sqrt("
        self.update_display()

    def square(self):
        self.current_expression += "**2"
        self.update_display()

    def power(self):
        self.current_expression += "**"
        self.update_display()

    def log(self):
        if self.shift_active:
            self.current_expression += "10**"
        else:
            self.current_expression += "math.log10("
        self.update_display()

    def negate(self):
        if self.shift_active:
            self.current_expression += "abs("
        else:
            self.current_expression += "(-"
        self.update_display()

    def deg_min_sec(self):
        try:
            value = float(eval(self.current_expression))
            degrees = int(value)
            minutes = int((value - degrees) * 60)
            seconds = ((value - degrees) * 60 - minutes) * 60
            self.current_expression = f"{degrees}°{minutes}'{seconds:.2f}\""
            self.update_display()
        except:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Error")

    def hyp(self):
        if self.shift_active:
            self.angle_mode = "DEG" if self.angle_mode == "RAD" else "RAD"
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, f"Mode: {self.angle_mode}")
        else:
            self.hyp_active = not self.hyp_active

    def sin(self):
        if self.hyp_active:
            self.current_expression += "math.sinh("
        else:
            self.current_expression += "math.sin("
        self.update_display()

    def cos(self):
        if self.hyp_active:
            self.current_expression += "math.cosh("
        else:
            self.current_expression += "math.cos("
        self.update_display()

    def tan(self):
        if self.hyp_active:
            self.current_expression += "math.tanh("
        else:
            self.current_expression += "math.tan("
        self.update_display()

    def rcl(self):
        self.current_expression += str(self.memory)
        self.update_display()

    def eng(self):
        try:
            value = float(eval(self.current_expression))
            eng_value = f"{value:.6e}"
            self.current_expression = eng_value
            self.update_display()
        except:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Error")

    def parenthesis(self):
        if self.current_expression.count('(') > self.current_expression.count(')'):
            self.current_expression += ')'
        else:
            self.current_expression += '('
        self.update_display()

    def multiply(self):
        self.current_expression += "*"
        self.update_display()

    def divide(self):
        self.current_expression += "/"
        self.update_display()

    def add(self):
        self.current_expression += "+"
        self.update_display()

    def subtract(self):
        self.current_expression += "-"
        self.update_display()

    def exp(self):
        self.current_expression += "*10**"
        self.update_display()

    def answer(self):
        self.current_expression += str(self.last_answer)
        self.update_display()

    def decimal_to_fraction(self, x, error=0.000001):
        n = int(math.floor(x))
        x -= n
        if x < error:
            return (n, 1)
        elif 1 - error < x:
            return (n+1, 1)
        lower_n = 0
        lower_d = 1
        upper_n = 1
        upper_d = 1
        while True:
            middle_n = lower_n + upper_n
            middle_d = lower_d + upper_d
            if middle_d * (x + error) < middle_n:
                upper_n = middle_n
                upper_d = middle_d
            elif middle_n < (x - error) * middle_d:
                lower_n = middle_n
                lower_d = middle_d
            else:
                return (n * middle_d + middle_n, middle_d)

root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", root.quit)  
calc = CalculadoraCientifica(root)
root.mainloop()