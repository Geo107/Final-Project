# 🧠🖼️ AI Steganography Tool

A powerful and user-friendly steganography tool that allows you to securely hide encrypted messages inside AI-generated images. This project combines cutting-edge AI image generation with classic steganography and encryption techniques, all wrapped in a simple Tkinter GUI.


## 🚀 Features

- 🧠 **AI Image Generation**: Generates images using **Stable Diffusion** via Hugging Face.
- 🔐 **Secure Message Encryption**: Uses **AES Encryption** to protect your message before embedding.
- 🧬 **Steganography with LSB**: Hides encrypted messages using **Least Significant Bit (LSB)** technique.
- 🖥️ **Tkinter GUI**: User-friendly interface for encryption, decryption, and image generation.


## 🛠️ Tech Stack

- 💡 **Python 3.x**
- 🎨 **Hugging Face Transformers / diffusers** for Stable Diffusion
- 🔒 AES encryption
- 🖼️ **Pillow (PIL)** for image processing
- 🧪 **Tkinter** for GUI
- 🧬 **NumPy** for efficient pixel manipulation

## 🔑 How It Works

1. **Image Generation**:

   * User inputs a text prompt.
   * The model generates a realistic image using **Stable Diffusion**.

2. **Encryption**:

   * The message is encrypted using **AES** with a user-provided key.

3. **Embedding**:

   * The encrypted message is embedded in the generated image using **LSB steganography**.

4. **Extraction & Decryption**:

   * The tool extracts the hidden bits from the image and decrypts them using the AES key.

## ⚙️ Usage

### 1. Run the Application

```bash
python main.py
```

### 2. Generate & Encode

* Enter your **text prompt** to generate an image.
* Type your **secret message** and **encryption key**.
* Click `Embed` to hide the message in the image.

### 3. Decode

* Upload the image with the hidden message.
* Enter the correct key and click `Extract`.


## 🔒 Security Note

* AES-128/256 is used for robust encryption.
* Even if someone extracts the hidden message via LSB, they cannot read it without the correct key.



