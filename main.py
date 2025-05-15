import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from image_generation import generate_image
from steganography import AESCipher, LSB

class StegoCryptApp:
    def __init__(self, master):
        self.master = master
        self.master.title("StegoCrypt")
        self.image = None
        self.img_panel = None

        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.master, text="Enter your prompt for image generation:").pack(pady=5)
        self.prompt_entry = tk.Entry(self.master, width=50)
        self.prompt_entry.pack(pady=5)

        button_frame1 = tk.Frame(self.master)
        button_frame1.pack(pady=5)
        tk.Button(button_frame1, text="Generate Image", command=self.generate_image).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame1, text="Input Encoded Image", command=self.open_image).pack(side=tk.LEFT, padx=5)

        button_frame2 = tk.Frame(self.master)
        button_frame2.pack(pady=5)
        tk.Button(button_frame2, text="Encode", command=self.encode).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame2, text="Decode", command=self.decode).pack(side=tk.LEFT, padx=5)

        tk.Button(self.master, text="Save Encoded Image", command=self.save_image).pack(pady=5)

        tk.Label(self.master, text="Key (16 characters):").pack(pady=5)
        self.key_input = tk.Entry(self.master, width=40)
        self.key_input.pack(pady=5)
        tk.Label(self.master, text="Secret Message:").pack(pady=5)
        self.message_input = tk.Text(self.master, height=8, width=50)
        self.message_input.pack(pady=5)

        self.img_panel = tk.Label(self.master)
        self.img_panel.pack(pady=5)

    def update_image(self):
        if self.image is None:
            return
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image).resize((300, 300), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(image)
        self.img_panel.configure(image=img_tk)
        self.img_panel.image = img_tk

    def generate_image(self):
        prompt = self.prompt_entry.get()
        if not prompt:
            messagebox.showwarning("Input Needed", "Please enter a prompt.")
            return
        
        try:
            self.image = generate_image(prompt)
            self.update_image()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if path:
            self.image = cv2.imread(path)
            self.update_image()
        else:
            messagebox.showwarning("Warning", "No image selected!")

    def encode(self):
        if self.image is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        message = self.message_input.get("1.0", 'end-1c')
        if not message:
            messagebox.showwarning("Warning", "No message to encode!")
            return
        key = self.key_input.get()
        if len(key) != 16:
            messagebox.showwarning("Warning", "Key must be 16 characters.")
            return

        cipher = AESCipher(key)
        cipher_text = cipher.encrypt(message)

        lsb = LSB(self.image)
        lsb.embed(cipher_text)
        self.image = lsb.image
        self.update_image()
        messagebox.showinfo("Success", "Message encoded successfully!")

    def decode(self):
        if self.image is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        key = self.key_input.get()
        if len(key) != 16:
            messagebox.showwarning("Warning", "Key must be 16 characters.")
            return

        cipher = AESCipher(key)
        lsb = LSB(self.image)
        cipher_text = lsb.extract()
        message = cipher.decrypt(cipher_text)

        self.message_input.delete(1.0, tk.END)
        self.message_input.insert(tk.INSERT, message)

    def save_image(self):
        if self.image is None:
            messagebox.showwarning("Warning", "No image to save!")
            return
        path = filedialog.asksaveasfilename(defaultextension=".png")
        if path:
            cv2.imwrite(path, self.image)
            messagebox.showinfo("Success", f"Image saved at {path}!")

if __name__ == "__main__":
    root = tk.Tk()
    app = StegoCryptApp(root)
    root.mainloop()