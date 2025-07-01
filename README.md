# 🖼️ Image Steganography App

A simple, modern, and user-friendly desktop application to hide and reveal secret messages in images using steganography. Built with Python and Tkinter.

---

## ✨ Features

- 🔐 **Encode**: Hide any text message inside a PNG or JPG image.  
- 🔓 **Decode**: Extract hidden messages from images.  
- 💎 **Modern UI**: Clean, attractive, and responsive interface.  
- 📌 **Status Bar**: See app status, quick info, and About dialog.  
- 🖱️ **GUI-Based**: No command line needed – everything is graphical.

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.7 or higher  
- Pillow (for image processing)

### 📦 Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/your-username/image-steganography-app.git
   cd image-steganography-app

## 🖥️ Usage

### To Encode:
1. Launch the app.
2. Click on **Encode**.
3. Select a PNG or JPG image from your system.
4. Enter the secret message you want to hide.
5. Save the new image with the embedded message.

### To Decode:
1. Launch the app.
2. Click on **Decode**.
3. Select the image that contains the hidden message.
4. The secret message will be extracted and displayed.

💡 The **status bar** at the bottom provides real-time feedback, quick info, and access to the About dialog.



image-steganography-app/
│
├── assets/               # Images/icons used in the UI
├── encoder.py            # Encoding logic
├── decoder.py            # Decoding logic
├── ui.py                 # Tkinter GUI components
├── utils.py              # Helper functions
├── main.py               # Entry point for the app
└── README.md             # Project documentation

