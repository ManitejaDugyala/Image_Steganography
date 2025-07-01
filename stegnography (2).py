import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
from PIL import ImageTk, Image
from tkinter import messagebox
from io import BytesIO
import os

class Stegno:
    output_image_size = 0

    def __init__(self):
        self.status_var = None

    def set_status(self, msg):
        if self.status_var:
            self.status_var.set(msg)

    def main(self, root):
        root.title('Image Steganography')
        root.geometry('520x650')
        root.resizable(width=False, height=False)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f5f5f5')
        style.configure('TLabel', background='#f5f5f5', font=('Segoe UI', 14))
        style.configure('TButton', font=('Segoe UI', 12), padding=6)
        style.configure('Header.TLabel', font=('Segoe UI', 28, 'bold'), foreground='#2d415a')
        style.configure('SubHeader.TLabel', font=('Segoe UI', 12, 'italic'), foreground='#6c757d')
        style.configure('Status.TLabel', font=('Segoe UI', 10), foreground='#555', background='#e9ecef')
        style.configure('Status.TFrame', background='#e9ecef')

        f = ttk.Frame(root, padding=30)
        f.grid(sticky='nsew')

        title = ttk.Label(f, text='Image Steganography', style='Header.TLabel')
        title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        subtitle = ttk.Label(f, text='Hide and reveal messages in images', style='SubHeader.TLabel')
        subtitle.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        b_encode = ttk.Button(f, text="Encode", command=lambda: self.frame1_encode(f))
        b_decode = ttk.Button(f, text="Decode", command=lambda: self.frame1_decode(f))
        b_encode.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        b_decode.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

        sep = ttk.Separator(f, orient='horizontal')
        sep.grid(row=3, column=0, columnspan=2, sticky='ew', pady=30)

        # Optional: Add a logo or image here if desired
        # logo = ttk.Label(f, image=...)
        # logo.grid(row=4, column=0, columnspan=2)

        # Status bar redesign
        self.status_var = tk.StringVar()
        status_frame = ttk.Frame(root, style='Status.TFrame', relief='sunken')
        status_frame.grid(row=1, column=0, sticky='ew')
        status_frame.grid_columnconfigure(0, weight=0)
        status_frame.grid_columnconfigure(1, weight=1)
        status_frame.grid_columnconfigure(2, weight=0)
        # App icon/emoji
        icon_label = ttk.Label(status_frame, text='🖼️', style='Status.TLabel')
        icon_label.grid(row=0, column=0, padx=(8, 4), pady=2)
        # Status message
        status_bar = ttk.Label(status_frame, textvariable=self.status_var, style='Status.TLabel', anchor='w')
        status_bar.grid(row=0, column=1, sticky='w', padx=4)
        # Help/About button
        help_btn = ttk.Button(status_frame, text='About', style='Status.TLabel', command=self.show_about, width=7)
        help_btn.grid(row=0, column=2, padx=(4, 8), pady=2, sticky='e')
        self.set_status('Ready')

    def home(self, frame):
        frame.destroy()
        self.main(root)

    def frame1_decode(self, f):
        f.destroy()
        d_f2 = ttk.Frame(root, padding=30)
        d_f2.grid(sticky='nsew')
        label_art = ttk.Label(d_f2, text='Decode Message', style='Header.TLabel')
        label_art.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        l1 = ttk.Label(d_f2, text='Select Image with Hidden Text:')
        l1.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        bws_button = ttk.Button(d_f2, text='Select', command=lambda: self.frame2_decode(d_f2))
        bws_button.grid(row=2, column=0, columnspan=2, pady=10)
        back_button = ttk.Button(d_f2, text='Cancel', command=lambda: Stegno.home(self, d_f2))
        back_button.grid(row=3, column=0, columnspan=2, pady=10)

    def frame2_decode(self, d_f2):
        d_f3 = ttk.Frame(root, padding=30)
        myfile = tkinter.filedialog.askopenfilename(filetypes=[('PNG', '*.png'), ('JPEG', '*.jpeg'), ('JPG', '*.jpg'), ('All Files', '*.*')])
        if not myfile:
            messagebox.showerror("Error", "You have selected nothing!")
            self.set_status('No file selected for decoding.')
        else:
            myimg = Image.open(myfile, 'r')
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)
            l4 = ttk.Label(d_f3, text='Selected Image:')
            l4.grid(row=0, column=0, pady=(0, 10))
            panel = ttk.Label(d_f3)
            panel.grid(row=1, column=0)
            panel.img = img
            panel.configure(image=img)
            hidden_data = self.decode(myimg)
            l2 = ttk.Label(d_f3, text='Hidden data is:')
            l2.grid(row=2, column=0, pady=(20, 5))
            text_area = tk.Text(d_f3, width=50, height=10, font=('Segoe UI', 11), wrap='word', bg='#f8f9fa')
            text_area.insert('1.0', hidden_data)
            text_area.configure(state='disabled')
            text_area.grid(row=3, column=0, pady=(0, 10))
            back_button = ttk.Button(d_f3, text='Back', command=lambda: self.page3(d_f3))
            back_button.grid(row=4, column=0, pady=10)
            show_info = ttk.Button(d_f3, text='More Info', command=self.info)
            show_info.grid(row=5, column=0, pady=5)
            d_f3.grid(sticky='nsew')
            d_f2.destroy()
            self.set_status('Decoded message displayed.')

    def decode(self, image):
        data = ''
        imgdata = iter(image.getdata())
        while True:
            pixels = [value for value in next(imgdata)[:3] + next(imgdata)[:3] + next(imgdata)[:3]]
            binstr = ''
            for i in pixels[:8]:
                binstr += '0' if i % 2 == 0 else '1'
            data += chr(int(binstr, 2))
            if pixels[-1] % 2 != 0:
                return data

    def frame1_encode(self, f):
        f.destroy()
        f2 = ttk.Frame(root, padding=30)
        f2.grid(sticky='nsew')
        label_art = ttk.Label(f2, text='Encode Message', style='Header.TLabel')
        label_art.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        l1 = ttk.Label(f2, text='Select the Image in which you want to hide text:')
        l1.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        bws_button = ttk.Button(f2, text='Select', command=lambda: self.frame2_encode(f2))
        bws_button.grid(row=2, column=0, columnspan=2, pady=10)
        back_button = ttk.Button(f2, text='Cancel', command=lambda: Stegno.home(self, f2))
        back_button.grid(row=3, column=0, columnspan=2, pady=10)

    def frame2_encode(self, f2):
        ep = ttk.Frame(root, padding=30)
        myfile = tkinter.filedialog.askopenfilename(filetypes=[('PNG', '*.png'), ('JPEG', '*.jpeg'), ('JPG', '*.jpg'), ('All Files', '*.*')])
        if not myfile:
            messagebox.showerror("Error", "You have selected nothing!")
            self.set_status('No file selected for encoding.')
        else:
            myimg = Image.open(myfile)
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)
            l3 = ttk.Label(ep, text='Selected Image:')
            l3.grid(row=0, column=0, pady=(0, 10))
            panel = ttk.Label(ep)
            panel.grid(row=1, column=0)
            panel.img = img
            panel.configure(image=img)
            self.output_image_size = os.stat(myfile)
            self.o_image_w, self.o_image_h = myimg.size
            l2 = ttk.Label(ep, text='Enter the message:')
            l2.grid(row=2, column=0, pady=(20, 5))
            text_area = tk.Text(ep, width=50, height=10, font=('Segoe UI', 11), wrap='word', bg='#f8f9fa')
            text_area.grid(row=3, column=0, pady=(0, 10))
            encode_button = ttk.Button(ep, text='Encode', command=lambda: [self.enc_fun(text_area, myimg), Stegno.home(self, ep)])
            encode_button.grid(row=4, column=0, pady=10)
            back_button = ttk.Button(ep, text='Cancel', command=lambda: Stegno.home(self, ep))
            back_button.grid(row=5, column=0, pady=5)
            ep.grid(sticky='nsew')
            f2.destroy()

    def info(self):
        try:
            str_info = 'Original image:\nsize: {:.2f} MB\nwidth: {}\nheight: {}\n\nDecoded image:\nsize: {:.2f} MB\nwidth: {}\nheight: {}'.format(
                self.output_image_size.st_size / 1000000,
                self.o_image_w, self.o_image_h,
                self.d_image_size / 1000000,
                self.d_image_w, self.d_image_h)
            messagebox.showinfo('Info', str_info)
        except Exception:
            messagebox.showinfo('Info', 'Unable to get the information')

    def genData(self, data):
        return [format(ord(i), '08b') for i in data]

    def modPix(self, pix, data):
        datalist = self.genData(data)
        lendata = len(datalist)
        imdata = iter(pix)
        for i in range(lendata):
            pix = [value for value in next(imdata)[:3] + next(imdata)[:3] + next(imdata)[:3]]
            for j in range(0, 8):
                if (datalist[i][j] == '0') and (pix[j] % 2 != 0):
                    pix[j] -= 1
                elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1
            if (i == lendata - 1):
                if (pix[-1] % 2 == 0):
                    pix[-1] -= 1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1
            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode_enc(self, newimg, data):
        w = newimg.size[0]
        (x, y) = (0, 0)
        for pixel in self.modPix(newimg.getdata(), data):
            newimg.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1

    def enc_fun(self, text_area, myimg):
        data = text_area.get("1.0", "end-1c")
        if len(data) == 0:
            messagebox.showinfo("Alert", "Kindly enter text in TextBox")
            self.set_status('No message entered for encoding.')
        else:
            newimg = myimg.copy()
            self.encode_enc(newimg, data)
            my_file = BytesIO()
            temp = os.path.splitext(os.path.basename(myimg.filename))[0]
            save_path = tkinter.filedialog.asksaveasfilename(initialfile=temp, filetypes=[('PNG', '*.png')], defaultextension=".png")
            if save_path:
                newimg.save(save_path)
                self.d_image_size = os.path.getsize(save_path)
                self.d_image_w, self.d_image_h = newimg.size
                messagebox.showinfo("Success", f"Encoding Successful\nFile is saved as {os.path.basename(save_path)}")
                self.set_status(f'File saved as {os.path.basename(save_path)}')
            else:
                self.set_status('Encoding cancelled, no file saved.')

    def page3(self, frame):
        frame.destroy()
        self.main(root)

    def show_about(self):
        messagebox.showinfo('About', 'Image Steganography App\n\nHide and reveal messages in images.\n\nDeveloped with ❤️ using Python and Tkinter.')

root = tk.Tk()
o = Stegno()
o.main(root)
root.mainloop()