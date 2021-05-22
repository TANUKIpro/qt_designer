# OpenCV_Developer.py
import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
import ImageProc
import FileProc

class Ui(QtWidgets.QMainWindow):
    def __init__(self, to_ui):
        super(Ui, self).__init__()
        self.setMouseTracking(True)
        uic.loadUi(to_ui, self)

        ## INIT Variable##
        self.img_num = 250
        self.dname   = None
        self.img_len = None
        self.th_num = 15
        self.contours_coordination = None

        self.rgb_img    = None
        self.bin_image  = None
        self.ploted_img = None

        ## MENUBAR ##
        self.actionOpen_O.triggered.connect(self.func_file_Open)
        self.actionQuit_Q.triggered.connect(self.func_Quit)

        ## TOOL-BUTTON ##
        self.selectDir_toolButton.clicked.connect(self.func_dir_Open)

        ## SLIDER ##
        self.th_horizontalSlider.valueChanged.connect(self.fucn_Update_ThresholdNumLabel)
        self.th_horizontalSlider.valueChanged.connect(self.func_UpdatePlotedImg)

        ## BUTTON ##
        self.LOAD_pushButton.clicked.connect(self.when_LOAD_pushButton)

        self.Distal_pushButton.clicked.connect(self.when_Distal_pushButton)
        self.Middle_pushButton.clicked.connect(self.when_Middle_pushButton)
        self.Proximal_pushButton.clicked.connect(self.when_Proximal_pushButton)
        self.Metacarpal_pushButton.clicked.connect(self.when_Metacarpal_pushButton)
        self.DEL_pushButton.clicked.connect(self.when_DEL_pushButton)

        self.NEXT_pushButton.clicked.connect(self.when_NEXT_pushButton)

        self.show()

    #### CENTRAL-WIDGET SETTING ####
    def func_ViewDisp(self, input_image):
        if len(input_image.shape) == 2:    # gray image
            image = QImage(input_image.data, ImageProc.img_width, ImageProc.img_height, QImage.Format_Grayscale8)
        elif len(input_image.shape) == 3:  # color image
            image = QImage(input_image.data, ImageProc.img_width, ImageProc.img_height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.viewlabel.setPixmap(pixmap)
    
    def fucn_Update_PoseDirLabel(self, fname):
        self.pose_label.setText(fname)

    def fucn_Update_MousePositionLabel(self, mouse_coordination):
        pass

    def fucn_Update_ThresholdNumLabel(self, th_num):
        self.th_num = th_num
        self.th_slider_num.setText(str(self.th_num))

    def func_Update_ButtonModeLabel(self, mode, color):
        self.button_mode_label.setText(mode)
        self.button_mode_label.setStyleSheet(color)

    def sndMessage(self, message):
        self.message_label.setText(message)

    def when_LOAD_pushButton(self):
        if not self.dname:
            self.sndMessage("Plaese set directory")
        else:
            self.names_list = fp.getContentsList(self.dname, '.png')
            self.img_len = len(self.names_list)
            self.sndMessage("%d images in total"%(self.img_len))
            self.image_progress_label.setText("%d / %d"%(self.img_num, self.img_len))

    def when_Distal_pushButton(self):
        mode = "Distal Phalanx"
        color = "background-color: rgb(0,255,0);"
        self.func_Update_ButtonModeLabel(mode, color)

    def when_Middle_pushButton(self):
        mode = "Middle Phalanx"
        color = "background-color: rgb(255,0,0);"
        self.func_Update_ButtonModeLabel(mode, color)

    def when_Proximal_pushButton(self):
        mode = "Proximal Phalanx"
        color = "background-color: rgb(38,143,255);"
        self.func_Update_ButtonModeLabel(mode, color)

    def when_Metacarpal_pushButton(self):
        mode = "Metacarpal"
        color = "background-color: rgb(255,255,127);"
        self.func_Update_ButtonModeLabel(mode, color)

    def when_DEL_pushButton(self):
        mode = "DEL"
        color = "background-color: rgb(220,220,220);"
        self.func_Update_ButtonModeLabel(mode, color)
    
    def when_NEXT_pushButton(self):
        if not self.img_len:
            self.sndMessage("Plaese load images")
        else:
            if 0 <= self.img_num and self.img_num <= self.img_len:
                self.image_name_label.setText(self.names_list[self.img_num])
                self.rgb_img = ip.LoadImage(self.dname+"/"+self.names_list[self.img_num])
                self.bin_image = ip.Binarization(self.rgb_img, self.th_num)

                self.contours_coordination = ip.getContours_xyz(self.bin_image, self.img_num)
                self.ploted_img = ip.getContoursPlotImage(self.bin_image, self.contours_coordination)
                self.func_ViewDisp(self.ploted_img)
    
    def func_UpdatePlotedImg(self):
        self.bin_image = ip.Binarization(self.rgb_img, self.th_num)
        self.contours_coordination = ip.getContours_xyz(self.bin_image, self.img_num)
        self.ploted_img = ip.getContoursPlotImage(self.bin_image, self.contours_coordination)
        self.func_ViewDisp(self.ploted_img)
    
    #### MENUBAR SETTING ####
    def func_file_Open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname[0]:
            input_image = ip.LoadImage(fname[0])
            self.fucn_Update_PoseDirLabel(fname[0])
            self.func_ViewDisp(input_image)

    def func_dir_Open(self):
        self.dname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open directory', '/home')
        if self.dname:
            self.fucn_Update_PoseDirLabel(self.dname)
            self.sndMessage("Set Dir : %s"%(self.dname))
    
    def func_Quit(self):
        ret = QtWidgets.QMessageBox.information(None, "Quit?", "Press a button", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if ret == QtWidgets.QMessageBox.Yes:
            sys.exit()

    #### MOUSE EVENT ####
    def mouseMoveEvent(self, event):
        self.mouse_position_label.setText('( %d : %d )' % (event.x(), event.y()))

if __name__=="__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = Ui("C:/Users/ryota/Desktop/qt_designer/OpenCV_Developer.ui")
        ip = ImageProc.ImageProc()
        fp = FileProc.FileProc()
        app.exec_()
    except:
        sys.exit()