# ColorPalette
之前用google vision服務時，有一個功能讓我很感興趣，就是做色彩分析功能，我想做一個配色功能用的輔助工具，如下:
![https://ithelp.ithome.com.tw/upload/images/20200927/20119608QQTu8GhSyd.jpg](https://ithelp.ithome.com.tw/upload/images/20200927/20119608QQTu8GhSyd.jpg)
在github上搜尋也有相關資源，請參照
[https://github.com/rodartha/ColorPalette](http://https://github.com/rodartha/ColorPalette)

以下是程式架構
```
Numcolors = ( 1, 2, 3, 4, 5)
CanvasWidth = 400
CanvasHeight = 300
```
定義出類別
```
class ColorPalette():
    def __init__(self, master):
        self.parent = master
        self.imageFile = str()
        self.init_ColorPalette_tab()
```
主面板
```
    def init_ColorPalette_tab(self):
        self.ColorPalette_tab = tk.Frame(self.parent)
        self.ColorPalette_tab.pack(side = tk.LEFT, expand=tk.YES, fill=tk.BOTH)
```
控制面板
```
        self.imgfileprocessPanel = tk.LabelFrame(self.ColorPalette_tab,
                                                 text="Image file Process Panel",
                                                 font=('Courier', 7))
        self.imgfileprocessPanel.pack(side=tk.TOP, expand=tk.NO)
```
載入圖片路徑
```
        self.load_img = tk.StringVar()
        loadimg = tk.Entry(self.imgfileprocessPanel,
                           textvariable=self.load_img,
                           font=('Courier', 7))
        loadimg.grid(row = 0, column = 0, sticky = tk.E+tk.W) 
```
載入圖片按鈕
```
        self.loadimgButton = tk.Button(self.imgfileprocessPanel,
                                       text = "Load...",
                                       font=('Courier', 7),
                                       command = self.loadimg)
        self.loadimgButton.grid(row = 0, column = 1, sticky = tk.E+tk.W)
```
指定顏色數量
```
        tk.Label(self.imgfileprocessPanel,
                 text = "Number of Colors",
                 font=('Courier', 7)).grid(row=0, column=2, sticky=tk.E+tk.W)
        self.numcolor = tk.Spinbox(self.imgfileprocessPanel,
                                   values = Numcolors,
                                   width = 3)
        self.numcolor.grid(row = 0,
                           column = 3,
                           sticky = tk.E+tk.W)
```
運作
```
        self.runButton = tk.Button(self.imgfileprocessPanel,
                                   text = "Run",
                                   font=('Courier', 7),
                                   command = self.transferColorPallete)
        self.runButton.grid(row = 0, column = 4, sticky = tk.E+tk.W)
```
切換圖片來源，從相本載入或是重新載入一張圖
```
        self.ImgSwitch = tk.StringVar()
        switch1 = tk.Radiobutton(self.imgfileprocessPanel,
                                 text = "from album",
                                 font=('Courier', 9),
                                 variable = self.ImgSwitch,
                                 value = "album",
                                 command = self.imgswitch)
        switch1.grid(row = 0, column = 5, sticky = tk.E+tk.W)
        switch2 = tk.Radiobutton(self.imgfileprocessPanel,
                                 text = "from load",
                                 font=('Courier', 9),
                                 variable = self.ImgSwitch,
                                 value = "load",
                                 command = self.imgswitch)
        switch2.grid(row = 0, column = 6, sticky = tk.E+tk.W)
```
顯示圖片用的畫布
```
        drawingpadPanel = tk.Frame(self.ColorPalette_tab)
        drawingpadPanel.pack(side=tk.TOP, expand=tk.NO)
        
        self.drawingpadcanvas = tk.Canvas(drawingpadPanel,
                                          background = 'white',
                                          width = CanvasWidth,
                                          height = CanvasHeight)
        drawingpad_sbarV = Scrollbar(drawingpadPanel, orient=tk.VERTICAL)
        drawingpad_sbarH = Scrollbar(drawingpadPanel, orient=tk.HORIZONTAL)
        drawingpad_sbarV.config(command=self.drawingpadcanvas.yview)
        drawingpad_sbarH.config(command=self.drawingpadcanvas.xview)
        self.drawingpadcanvas.config(yscrollcommand=drawingpad_sbarV.set)
        self.drawingpadcanvas.config(xscrollcommand=drawingpad_sbarH.set)
        drawingpad_sbarV.pack(side=tk.RIGHT, fill=tk.Y)
        drawingpad_sbarH.pack(side=tk.BOTTOM, fill=tk.X)        
        self.drawingpadcanvas.pack(side=tk.TOP, expand=tk.NO)        
```
切換圖片來源的程式
```
    def imgswitch(self, event = None):
                    .
                    .
                    .
```
載入圖片的程式
```
    def loadimg(self, event = None):
                   .
                   .
                   .
```
轉換色彩分析的程式
```
    def transferColorPallete(self):
                   .
                   .
                   .
``` 

![https://ithelp.ithome.com.tw/upload/images/20200927/20119608acu9CaFH6w.jpg](https://ithelp.ithome.com.tw/upload/images/20200927/20119608acu9CaFH6w.jpg)

注意，以上剛剛為一個寫好的模組，真正在main.py使用時別忘了載入ColorPalette模組
```
import ColorPalette.ColorPalette as clrP
```
建立一個self.ColorPalette_tab分頁並呼叫一個ColorPalette物件
```
def init_ColorPalette(self):
    self.ColorPalette_tab = tk.Frame(self.notebook)
    self.notebook.add(self.ColorPalette_tab, text="ColorPalette")
    self.clrP = clrP.ColorPalette(self.ColorPalette_tab)
```
將ColorPalette模組內的變數(self.clrP.imageFile)指向imageFile
```
def imgswitch(self):
    if self.ImgSwitch.get() =="Img Switch 1":
        imageFile = self.iv1.image_paths[self.iv1.image_idx]
    elif self.ImgSwitch.get() =="Img Switch 2":
        imageFile = self.iv2.image_paths[self.iv2.image_idx]
    elif self.ImgSwitch.get() =="Img Switch 3":
        imageFile = self.iv3.image_paths[self.iv3.image_idx]
    elif self.ImgSwitch.get() =="Img Switch 4":
        imageFile = self.iv4.image_paths[self.iv4.image_idx]
    self.clrP.imageFile = imageFile     
```
