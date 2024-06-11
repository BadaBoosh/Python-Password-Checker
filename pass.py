import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar , Style

# Read common words from txt file and load into a set
def LoadCommons(file):
    with open(file, 'r') as file:
        return set(word.strip().lower() for word in file)

# Helper functions to determine appropriate character existence in word
def ContainsUpper(word):
    return any(char.isupper() for char in word)
def ContainsLower(word):
    return any(char.islower() for char in word)
def ContainsSpace(word):
    return any(char.isspace() for char in word)
def ContainsNumber(word):
    return any(char.isdigit() for char in word)
def ContainsSpecialChars(word):
    return any(not char.isalnum() for char in word)
def ContainsCommonWord(word):
    word_lower = word.lower()
    common_words = LoadCommons('common.txt') # load common words from a given text file containing common names and words
    return any(common_word in word_lower for common_word in common_words)

# Main function determining if password meets criteria
def PassCheck(pword):
    # Use bools to be checked as criteria is met
    valLength = True
    hasUpper = True
    hasLower = True
    hasSpace = False
    hasNum = True
    hasSpec = True
    hasCommonWord = False

    messages = []
    strength = 0

    # Logic checks
    if len(pword) < 12:
        valLength = False
        messages.append("Password length should be greater than 12")
    else:
        strength += 16

    if not ContainsUpper(pword):
        hasUpper = False
        messages.append("Password should contain uppercase characters")
    else:
        strength += 16

    if not ContainsLower(pword):
        hasLower = False
        messages.append("Password should contain lowercase characters")
    else:
        strength += 16

    if ContainsSpace(pword):
        hasSpace = True
        messages.append("Password cannot contain a blank space")
    else:
        strength += 16

    if not ContainsNumber(pword):
        hasNum = False
        messages.append("Password should contain a number (0-9)")
    else:
        strength += 16

    if not ContainsSpecialChars(pword):
        hasSpec = False
        messages.append('Password should contain a special character (!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~)')
    else:
        strength += 20

    if ContainsCommonWord(pword):
        hasCommonWord = True
        messages.append("Password should not contian common words, names, or persons")
        strength = max(0, strength-30)

    if valLength and hasUpper and hasLower and not hasSpace and hasNum and hasSpec and not hasCommonWord:
        messages.append("Valid Password")

    return "\n".join(messages) , strength

def evaluate_password():
    password = password_entry.get()
    result , _ = PassCheck(password)
    messagebox.showinfo("Password Evaluation", result)

def update_strength_bar(event):
    password = password_entry.get()
    if password == "":
        strength_bar['value'] = 0
        style.configure("Custom.Horizontal.TProgressbar", background='white')
        strength_label['text'] = ''
    else:
        _ , strength = PassCheck(password)
        strength_bar['value'] = strength
        strength_label['text'] = ''
        if strength < 40:
            style.configure("Custom.Horizontal.TProgressbar", background='red')
            strength_label['text'] = "Weak"
        elif strength < 80:
            style.configure("Custom.Horizontal.TProgressbar", background='yellow')
            strength_label['text'] = "Moderate"
        else:
            style.configure("Custom.Horizontal.TProgressbar", background='green')
            strength_label['text'] = "Strong"
    
if __name__ == "__main__":
    # GUI setup
    root = tk.Tk()
    root.title("Password Checker")
    root.geometry("350x300")
    
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(padx=20, pady=20)

    password_label = tk.Label(frame, text="Enter your password:")
    password_label.pack(pady=5)

    password_entry = tk.Entry(frame, width=30)
    password_entry.pack(pady=5)
    password_entry.bind("<KeyRelease>", update_strength_bar)

    check_button = tk.Button(frame, text="Check Password", command=evaluate_password)
    check_button.pack(pady=10)

    strength_label = tk.Label(frame, text="Password Strength")
    strength_label.pack(pady=5)

    style = Style()
    style.theme_use('clam')

    strength_bar = Progressbar(frame, length=200, mode='determinate', style="Custom.Horizontal.TProgressbar")
    strength_bar.pack(pady=5)

    strength_label = tk.Label(frame, text="", font=("Arial", 10), fg="black", bg="#f0f0f0")
    strength_label.place(in_=strength_bar, relx=0.5, rely=1.6, anchor=tk.CENTER)

    root.mainloop()

    pass
