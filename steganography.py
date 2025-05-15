import cv2
from Crypto.Cipher import AES

class AESCipher:
    def __init__(self, key):
        self.key = key.encode()

    def encrypt(self, msg):
        cipher = AES.new(self.key, AES.MODE_ECB)
        padded_msg = msg + " " * (16 - len(msg) % 16)  # Padding to 16-byte boundary
        return cipher.encrypt(padded_msg.encode()).hex()

    def decrypt(self, cipher_text):
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.decrypt(bytes.fromhex(cipher_text)).decode().strip()

class LSB:
    MAX_BIT_LENGTH = 16

    def __init__(self, img):
        self.image = img
        self.cur_x, self.cur_y, self.cur_channel = 0, 0, 0
        self.size_x, self.size_y, self.size_channel = img.shape

    def next_pixel(self):
        if self.cur_channel < self.size_channel - 1:
            self.cur_channel += 1
        else:
            self.cur_channel = 0
            if self.cur_y < self.size_y - 1:
                self.cur_y += 1
            else:
                self.cur_y = 0
                if self.cur_x < self.size_x - 1:
                    self.cur_x += 1

    def put_bit(self, bit):
        pixel_value = self.image[self.cur_x, self.cur_y, self.cur_channel]
        binary_value = f"{pixel_value:08b}"
        new_value = int(binary_value[:-1] + bit, 2)
        self.image[self.cur_x, self.cur_y, self.cur_channel] = new_value
        self.next_pixel()

    def read_bit(self):
        pixel_value = self.image[self.cur_x, self.cur_y, self.cur_channel]
        bit = f"{pixel_value:08b}"[-1]
        self.next_pixel()
        return bit

    def embed(self, text):
        text_length = len(text)
        length_bits = f"{text_length:016b}"
        self.put_bits(length_bits)
        for char in text:
            self.put_bits(f"{ord(char):08b}")

    def extract(self):
        length = int(self.read_bits(16), 2)
        text = ""
        for _ in range(length):
            char_bits = self.read_bits(8)
            text += chr(int(char_bits, 2))
        return text

    def put_bits(self, bits):
        for bit in bits:
            self.put_bit(bit)

    def read_bits(self, length):
        return "".join(self.read_bit() for _ in range(length))
