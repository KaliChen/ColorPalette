import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox as msg
from tkinter.ttk import Notebook
from tkinter import filedialog
from tkinter import ttk
from tkinter.colorchooser import *
from PIL import Image, ImageTk, ImageDraw, ExifTags, ImageColor,ImageFont
import tkinter.messagebox as tkmsg
import tkinter.filedialog as tkfd
import cv2
import os
from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt
from scipy import cluster
import pandas as pd
import math
import colorsys
import click

Numcolors = ( 1, 2, 3, 4, 5)
CanvasWidth = 400
CanvasHeight = 300

class ColorPalette():
    def __init__(self, master):
        self.parent = master
        self.imageFile = str()

        self.init_ColorPalette_tab()

    def init_ColorPalette_tab(self):
        self.ColorPalette_tab = tk.Frame(self.parent)
        self.ColorPalette_tab.pack(side = tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        self.imgfileprocessPanel = tk.LabelFrame(self.ColorPalette_tab, text="Image file Process Panel",font=('Courier', 7))
        self.imgfileprocessPanel.pack(side=tk.TOP, expand=tk.NO)

        self.load_img = tk.StringVar()
        loadimg = tk.Entry(self.imgfileprocessPanel, textvariable=self.load_img,font=('Courier', 7))
        loadimg.grid(row = 0, column = 0, sticky = tk.E+tk.W) 
        self.loadimgButton = tk.Button(self.imgfileprocessPanel, text = "Load...",font=('Courier', 7), command = self.loadimg)
        self.loadimgButton.grid(row = 0, column = 1, sticky = tk.E+tk.W)

        tk.Label(self.imgfileprocessPanel, text = "Number of Colors",font=('Courier', 7)).grid(row = 0, column = 2, sticky = tk.E+tk.W)        
        self.numcolor = tk.Spinbox(self.imgfileprocessPanel, values = Numcolors,  width = 3)
        self.numcolor.grid(row = 0, column = 3, sticky = tk.E+tk.W)

        self.runButton = tk.Button(self.imgfileprocessPanel, text = "Run",font=('Courier', 7), command = self.transferColorPallete)
        self.runButton.grid(row = 0, column = 4, sticky = tk.E+tk.W)        
        self.ImgSwitch = tk.StringVar()
        switch1 = tk.Radiobutton(self.imgfileprocessPanel, text = "from album",font=('Courier', 9), variable = self.ImgSwitch, value = "album", command = self.imgswitch)
        switch1.grid(row = 0, column = 5, sticky = tk.E+tk.W)
        switch2 = tk.Radiobutton(self.imgfileprocessPanel, text = "from load",font=('Courier', 9), variable = self.ImgSwitch, value = "load", command = self.imgswitch)
        switch2.grid(row = 0, column = 6, sticky = tk.E+tk.W)

        drawingpadPanel = tk.Frame(self.ColorPalette_tab)
        drawingpadPanel.pack(side=tk.TOP, expand=tk.NO)

        '''drawing pad setting'''
        self.drawingpadcanvas = tk.Canvas(drawingpadPanel, background = 'white', width = CanvasWidth, height = CanvasHeight)

        drawingpad_sbarV = Scrollbar(drawingpadPanel, orient=tk.VERTICAL)
        drawingpad_sbarH = Scrollbar(drawingpadPanel, orient=tk.HORIZONTAL)
        drawingpad_sbarV.config(command=self.drawingpadcanvas.yview)
        drawingpad_sbarH.config(command=self.drawingpadcanvas.xview)
        self.drawingpadcanvas.config(yscrollcommand=drawingpad_sbarV.set)
        self.drawingpadcanvas.config(xscrollcommand=drawingpad_sbarH.set)
        drawingpad_sbarV.pack(side=tk.RIGHT, fill=tk.Y)
        drawingpad_sbarH.pack(side=tk.BOTTOM, fill=tk.X)        
        self.drawingpadcanvas.pack(side=tk.TOP, expand=tk.NO)        

    def imgswitch(self, event = None):
        if self.ImgSwitch.get() =="album":
            self.filename = self.imageFile

    def loadimg(self, event = None):
        self.filename = filedialog.askopenfilename(initialdir = "/home/kalichen/Desktop",title = "Select file",filetypes = (("img files","*.jpg"),("all files","*.*")))
        self.load_img.set(self.filename)
        image_cv = cv2.imread(self.load_img.get(),cv2.IMREAD_UNCHANGED )#<class 'numpy.ndarray'>
        image_cv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB) # for PIL image
        image_pil = Image.fromarray(image_cv)#<class 'PIL.Image.Image'>

        w, h = image_pil.size
        disp_x = disp_y = 0

        #resize
        if w>h:
            #resize fit CanvasWidth
            h = h*CanvasWidth/w
            w = CanvasWidth
        else:
            #resize fit CanvasHeight
            w = w*CanvasHeight/h
            h = CanvasHeight

        image_pil.thumbnail( (w,h) )

        self.image_tk = ImageTk.PhotoImage(image_pil) #<class 'PIL.ImageTk.PhotoImage'>

        self.drawingpadcanvas.config(scrollregion=(disp_x,disp_y,w,h))
        self.drawingpadcanvas.create_image(disp_x, disp_y, image=self.image_tk, anchor=tk.NW)



    def step(self, r, g, b, repititions=1):
        lum = math.sqrt(0.241 * r + 0.691 * g + 0.068 * b)
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        h2 = int(h * repititions)
        lum2 = int(lum * repititions)
        v2 = int(v * repititions)
        if h2 % 2 == 1:
            v2 = repititions - v2
            lum = repititions - lum
        return (h2, lum, v2)

    def get_hex_color(self, color):
        return '#%02x%02x%02x' % color

    def get_text_width(self, font, text):
        width = 0
        for ch in text: width += font.getsize(ch)[0]
        return width

    def get_text_height(self, font, text):
        height = []
        for ch in text:
            height.append(font.getsize(ch)[1])
        return max(height)

    def transferColorPallete(self):
        num_colors = int(self.numcolor.get())
        display_color=False

        file_path = self.filename.split('/')
        #print(file_path)
        file_prefix = ''
        file_split = ''
        for i in range(len(file_path)):
            if i != len(file_path) - 1:
                file_prefix = file_prefix + file_path[i] + '/'
                #print(file_prefix)
            else:
                file_split = file_path[i]
                #print(file_split)
        file_split = file_split.split('.')
        #print(file_split)


        if file_split[1] != 'jpg' and file_split[1] != 'png':
            raise("The file must be a jpg or png")

        output_palette = file_prefix + file_split[0] + '_palette.' + file_split[1]
        output_combined = file_prefix + file_split[0] + '_with_palette.' + file_split[1]

        img = plt.imread(self.filename)

        red, green, blue = [], [], []
        for line in img:
            for pixel in line:
                r, g, b = pixel
                red.append(r)
                green.append(g)
                blue.append(b)

        df = pd.DataFrame({'red': red, 'green': green, 'blue': blue})

        df['standardized_red'] = cluster.vq.whiten(df['red'])
        df['standardized_green'] = cluster.vq.whiten(df['green'])
        df['standardized_blue'] = cluster.vq.whiten(df['blue'])

        color_pallete, distortion = cluster.vq.kmeans(df[['standardized_red', 'standardized_green', 'standardized_blue']], num_colors)
        colors = []
        red_std, green_std, blue_std = df[['red', 'green', 'blue']].std()
        for color in color_pallete:
            scaled_red, scaled_green, scaled_blue = color
            colors.append((math.ceil(scaled_red * red_std) ,math.ceil(scaled_green * green_std) ,math.ceil(scaled_blue * blue_std) ))

        colors.sort(key=lambda x: self.step(x[0], x[1], x[2], 8))

        # FIXME: need a smart way to resize fonts based on picture size
        font_size = 11
        font = ImageFont.truetype("NICE_font/Roboto-Medium.ttf", font_size)
        sample_text = '#F8F8F7'
        proper_font_size = False


        pil_img = Image.open(self.filename)
        pil_width, pil_height = pil_img.size
        height = 0
        if pil_height > pil_width:
            height = math.floor(pil_height / 6)
        else:
            height = math.floor(pil_height / 4)

        pallete = Image.new('RGB', (pil_width, height), (255, 255, 255))
        single_img_space = math.floor(pil_width / num_colors)
        single_img_offset = math.floor(single_img_space / 14)
        total_offset = single_img_offset * (num_colors + 1)
        single_img_width = math.floor((pil_width - total_offset) / num_colors)
        single_img_space = single_img_width + single_img_offset

        final_img_width = (single_img_width + (pil_width - (single_img_space * num_colors))) - single_img_offset

        while not proper_font_size:
            if self.get_text_width(font, sample_text) > single_img_width and font_size > 1:
                font_size -= 1
                font = ImageFont.truetype("NICE_font/Roboto-Medium.ttf", font_size)
            elif self.get_text_width(font, sample_text) < single_img_width - 20:
                font_size += 1
                font = ImageFont.truetype("NICE_font/Roboto-Medium.ttf", font_size)
            else:
                proper_font_size = True

        x_offset = 0
        for i in range(len(colors)):
            if i == len(colors) - 1:
                new_img = Image.new('RGB', (final_img_width, height), colors[i])
                pallete.paste(new_img, (x_offset, 0))
                if display_color:
                    draw = ImageDraw.Draw(pallete)
                    draw.text((x_offset, height - 20 - self.get_text_height(font, sample_text)), self.get_hex_color(colors[i]), (255, 255, 255), font=font)
            elif i == 0:
                new_img = Image.new('RGB', (single_img_width, height), colors[i])
                pallete.paste(new_img, (single_img_offset, 0))
                if display_color:
                    draw = ImageDraw.Draw(pallete)
                    draw.text((single_img_offset, height - 20 - self.get_text_height(font, sample_text)), self.get_hex_color(colors[i]), (255, 255, 255), font=font)
                x_offset += single_img_space + single_img_offset
            else:
                new_img = Image.new('RGB', (single_img_width, height), colors[i])
                pallete.paste(new_img, (x_offset, 0))
                if display_color:
                    draw = ImageDraw.Draw(pallete)
                    draw.text((x_offset, height - 20 - self.get_text_height(font, sample_text)), self.get_hex_color(colors[i]), (255, 255, 255), font=font)
                x_offset += single_img_space

        pallete.save(output_palette)

        og_img = Image.open(self.filename)
        og_width, og_height = og_img.size
        pallete_img = Image.open(output_palette)
        pallete_width, pallete_height = pallete_img.size

        height_offset = math.ceil(og_height / 20)
        if og_height > og_width:
            height_offset = math.ceil(og_height / 30)

        total_width = og_width
        total_height = og_height + pallete_height + (height_offset * 2)

        combined_img = Image.new('RGB', (total_width, total_height), (255, 255, 255))

        combined_img.paste(og_img, (0, 0))
        combined_img.paste(pallete_img, (0, og_height + height_offset))

        combined_img.save(output_palette)
   
        #-----------------------------
        # Display to the canvas
        #-----------------------------
        image_cv = cv2.imread(output_palette,cv2.IMREAD_UNCHANGED )#<class 'numpy.ndarray'>
        image_cv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB) # for PIL image

        image_pil = Image.fromarray(image_cv)#<class 'PIL.Image.Image'>

        w, h = image_pil.size
        disp_x = disp_y = 0

        #resize
        if w>h:
            #resize fit CanvasWidth
            h = h*CanvasWidth/w
            w = CanvasWidth
        else:
            #resize fit CanvasHeight
            w = w*CanvasHeight/h
            h = CanvasHeight

        image_pil.thumbnail( (w,h) )

        self.image_tk = ImageTk.PhotoImage(image_pil) #<class 'PIL.ImageTk.PhotoImage'>

        self.drawingpadcanvas.config(scrollregion=(disp_x,disp_y, w, h))
        self.drawingpadcanvas.create_image(disp_x, disp_y, image=self.image_tk, anchor=tk.NW)

if __name__ == '__main__':
    root = tk.Tk()
    ColorPalette(root)
    root.mainloop()
