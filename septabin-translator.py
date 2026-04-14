import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

# =========================
# SEPTABIN CONSTANTS
# =========================

START = "0000000"
END = "1111111"

CHAR_MAP = {
    "0": "0000001",
    "1": "0000010",
    "2": "0000011",
    "3": "0000100",
    "4": "0000101",
    "5": "0000110",
    "6": "0000111",
    "7": "0001000",
    "8": "0001001",
    "9": "0001010",

    "A": "0001011", "B": "0001100", "C": "0001101", "D": "0001110",
    "E": "0001111", "F": "0010000", "G": "0010001", "H": "0010010",
    "I": "0010011", "J": "0010100", "K": "0010101", "L": "0010110",
    "M": "0010111", "N": "0011000", "O": "0011001", "P": "0011010",
    "Q": "0011011", "R": "0011100", "S": "0011101", "T": "0011110",
    "U": "0011111", "V": "0100000", "W": "0100001", "X": "0100010",
    "Y": "0100011", "Z": "0100100",

    "a": "0100101", "b": "0100110", "c": "0100111", "d": "0101000",
    "e": "0101001", "f": "0101010", "g": "0101011", "h": "0101100",
    "i": "0101101", "j": "0101110", "k": "0101111", "l": "0110000",
    "m": "0110001", "n": "0110010", "o": "0110011", "p": "0110100",
    "q": "0110101", "r": "0110110", "s": "0110111", "t": "0111000",
    "u": "0111001", "v": "0111010", "w": "0111011", "x": "0111100",
    "y": "0111101", "z": "0111110",

    " ": "0111111",
    ".": "1000000",
    "!": "1000001",
    ",": "1000010",
    "?": "1000011",
    "-": "1000100",
}

REVERSE_MAP = {v: k for k, v in CHAR_MAP.items()}


def to_int(b): return int(b, 2)
def to_7bit(n): return format(n % 128, "07b")

def checksum(values):
    return sum(values) % 128


# =========================
# ENCODE / DECODE
# =========================

def encode(text):
    bits = []
    values = []

    for c in text:
        if c not in CHAR_MAP:
            raise ValueError(f"Unsupported character: {c}")
        b = CHAR_MAP[c]
        bits.append(b)
        values.append(to_int(b))

    cs = to_7bit(checksum(values))

    return START + "".join(bits) + cs + END


def decode(data):
    if not (data.startswith(START) and data.endswith(END)):
        raise ValueError("Missing START/END")

    body = data[len(START):-len(END)]
    chunks = [body[i:i+7] for i in range(0, len(body), 7)]

    payload = chunks[:-1]

    return "".join(REVERSE_MAP.get(c, "?") for c in payload)


# =========================
# UI
# =========================

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Septabin Translator v2.2.1")
        self.root.geometry("850x600")
        self.root.configure(bg="#121212")

        # Title
        title = tk.Label(root, text="SEPTABIN TRANSLATOR",
                         bg="#121212", fg="white",
                         font=("Segoe UI", 18, "bold"))
        title.pack(pady=10)

        # INPUT label
        tk.Label(root, text="INPUT",
                 bg="#121212", fg="#aaaaaa",
                 font=("Segoe UI", 10)).pack()

        self.input_box = ScrolledText(root, height=7,
                                      bg="#1e1e1e", fg="white",
                                      insertbackground="white")
        self.input_box.pack(fill="x", padx=10)

        # Buttons
        btn_frame = tk.Frame(root, bg="#121212")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Encode", command=self.encode).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Decode", command=self.decode).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Rules", command=self.open_rules).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Dictionary", command=self.open_dict).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear).grid(row=0, column=4, padx=5)

        # OUTPUT label
        tk.Label(root, text="OUTPUT",
                 bg="#121212", fg="#aaaaaa",
                 font=("Segoe UI", 10)).pack()

        self.output_box = ScrolledText(root, height=7,
                                       bg="#1e1e1e", fg="#00ffcc",
                                       insertbackground="white")
        self.output_box.pack(fill="x", padx=10, pady=10)

    # =========================
    # ACTIONS
    # =========================

    def encode(self):
        try:
            text = self.input_box.get("1.0", tk.END).strip()
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, encode(text))
        except Exception as e:
            self.output_box.insert(tk.END, str(e))

    def decode(self):
        try:
            data = self.input_box.get("1.0", tk.END).strip()
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, decode(data))
        except Exception as e:
            self.output_box.insert(tk.END, str(e))

    def clear(self):
        self.input_box.delete("1.0", tk.END)
        self.output_box.delete("1.0", tk.END)

    # =========================
    # RULES WINDOW (VERBATIM)
    # =========================

    def open_rules(self):
        win = tk.Toplevel(self.root)
        win.title("Septabin Rules")
        win.geometry("650x500")
        win.configure(bg="#121212")

        t = ScrolledText(win, bg="#1e1e1e", fg="white")
        t.pack(expand=True, fill="both")

        t.insert(tk.END, """Septabin Encoding Rules

1. Message Boundaries:
   Each message starts with a START marker (0000000) and ends with an END marker (1111111).

2. No Physical Spaces:
   The encoded binary text contains no physical spaces. SPACE is encoded as its own 7-bit binary value (0111111).

3. Character Set:
   Allowed characters include digits 0-9, uppercase A-Z, lowercase a-z, and punctuation: . ! , ? -

4. Uniform Binary Length:
   Each character is represented by a 7-bit binary code, all of equal length.

5. Case Sensitivity:
   Uppercase and lowercase letters are distinct and have unique codes.

6. Single Start and End Markers:
   Exactly one START and one END marker per message block.

7. Strict 7-Bit Alignment:
   The total length of the encoded binary string is always a multiple of 7 bits.

8. No Extraneous Bits:
   No leading zeros or stray bits outside of START/END boundaries.

9. Message Integrity Check (Checksum):
   A 7-bit checksum is inserted just before the END marker, calculated as:
   - Convert each 7-bit character (excluding START and END) to decimal
   - Sum all values
   - Compute sum modulo 128
   - Convert result to 7-bit binary and insert before END

10. Reserved Values:
    START (0000000) and END (1111111) are reserved markers.

11. Future Expansion:
    Reserve unused 7-bit codes for escape sequences or additional symbols as needed.
""")

    def open_dict(self):
        win = tk.Toplevel(self.root)
        win.title("Dictionary")
        win.geometry("500x500")
        win.configure(bg="#121212")

        t = ScrolledText(win, bg="#1e1e1e", fg="white")
        t.pack(expand=True, fill="both")

        for k, v in CHAR_MAP.items():
            t.insert(tk.END, f"{k} -> {v}\n")


# =========================
# RUN
# =========================

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()