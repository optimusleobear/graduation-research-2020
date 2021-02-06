import PyQt5.QtCore as QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from . import gui_draw
from . import gui_vis
from . import gui_gamut
from . import gui_palette
import time

import sys
sys.path.append('..')
import realsr


class GUIDesign(QWidget):
    def __init__(self, color_model, os_type, gpu, if_realsr, dist_model=None, img_file=None, load_size=256,
                 win_size=256,  save_all=True):

        # draw the layout
        QWidget.__init__(self)

        if_demo = QMessageBox.question(
            self,
            'Demo Mode',
            'Do you want to use it for Demo?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if if_demo == QMessageBox.No:
            img_file = QFileDialog.getOpenFileName(
                self,
                'Choose your photo.'
            )[0]

        if img_file is None or img_file == '':
            print('Error 404: Image Not Found')
            QMessageBox.warning(
                self,
                'ERROR 404',
                'Image Not Found.',
                QMessageBox.Ok,
                QMessageBox.Ok
            )
            sys.exit(0)

        # RealSR before colorization
        if gpu != -1:
            if if_realsr == 'Y' or if_realsr == 'y':
                do_realsr = QMessageBox.question(
                    self,
                    'RealSR',
                    'RealSR may take some time to finish.',
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if do_realsr == QMessageBox.Yes:
                    print('RealSR activated?  True')
                    realsr.realsr(img_file, os_type, gpu)
                    img_file = img_file.rsplit('.', 1)[0] + '_hires.jpg'
                    if_xsave = False
                else:
                    if_xsave = True
                    if_realsr = 'N'
                    print('RealSR activated?  False')
            else:
                do_realsr = QMessageBox.question(
                    self,
                    'RealSR',
                    'Do you want to try RealSR?\nIt may take some time to finish.',
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if do_realsr == QMessageBox.Yes:
                    print('RealSR activated?  True')
                    realsr.realsr(img_file, os_type, gpu)
                    img_file = img_file.rsplit('.', 1)[0] + '_hires.jpg'
                    if_realsr = 'Y'
                    if_xsave = False
                else:
                    if_xsave = True
                    print('RealSR activated?  False')
        else:
            print('RealSR Not Available.')

        self.if_save = False

        # main layout
        mainLayout = QHBoxLayout()
        self.setLayout(mainLayout)
        # gamut layout
        self.gamutWidget = gui_gamut.GUIGamut(gamut_size=160)
        gamutLayout = self.AddWidget(self.gamutWidget, 'ab Color Gamut')
        colorLayout = QVBoxLayout()

        colorLayout.addLayout(gamutLayout)
        mainLayout.addLayout(colorLayout)

        # palette
        self.customPalette = gui_palette.GUIPalette(grid_sz=(10, 1))
        self.usedPalette = gui_palette.GUIPalette(grid_sz=(10, 1))
        cpLayout = self.AddWidget(self.customPalette, 'Suggested colors')
        colorLayout.addLayout(cpLayout)
        upLayout = self.AddWidget(self.usedPalette, 'Recently used colors')
        colorLayout.addLayout(upLayout)

        self.colorPush = QPushButton()  # to visualize the selected color
        self.colorPush.setFixedWidth(self.customPalette.width())
        self.colorPush.setFixedHeight(25)
        self.colorPush.setStyleSheet("background-color: grey")
        colorPushLayout = self.AddWidget(self.colorPush, 'Color')
        colorLayout.addLayout(colorPushLayout)
        colorLayout.setAlignment(Qt.AlignTop)

        # drawPad layout
        drawPadLayout = QVBoxLayout()
        mainLayout.addLayout(drawPadLayout)
        self.drawWidget = gui_draw.GUIDraw(color_model, os_type, gpu, dist_model, load_size=load_size, win_size=win_size)
        drawPadLayout = self.AddWidget(self.drawWidget, 'Drawing Pad')
        mainLayout.addLayout(drawPadLayout)

        drawPadMenu = QHBoxLayout()

        self.bGray = QCheckBox("&Gray")
        self.bGray.setToolTip('show gray-scale image')

        self.bLoad = QPushButton('&Load')
        self.bLoad.setToolTip('load an input image')
        self.bSave = QPushButton("&Save")
        self.bSave.setToolTip('Save the current result.')
        self.bXsave = QPushButton('&XSave')
        self.bXsave.setToolTip('Save with RealSR')

        drawPadMenu.addWidget(self.bGray)
        drawPadMenu.addWidget(self.bLoad)
        drawPadMenu.addWidget(self.bSave)
        if if_xsave:
            drawPadMenu.addWidget(self.bXsave)

        drawPadLayout.addLayout(drawPadMenu)
        self.visWidget = gui_vis.GUI_VIS(win_size=win_size, scale=win_size / float(load_size))
        visWidgetLayout = self.AddWidget(self.visWidget, 'Result')
        mainLayout.addLayout(visWidgetLayout)

        self.bRestart = QPushButton("&Restart")
        self.bRestart.setToolTip('Restart the system')

        self.bQuit = QPushButton("&Quit")
        self.bQuit.setToolTip('Quit the system.')
        visWidgetMenu = QHBoxLayout()
        visWidgetMenu.addWidget(self.bRestart)

        visWidgetMenu.addWidget(self.bQuit)
        visWidgetLayout.addLayout(visWidgetMenu)

        self.drawWidget.update()
        self.visWidget.update()
        self.colorPush.clicked.connect(self.drawWidget.change_color)
        # color indicator
        self.drawWidget.update_color.connect(self.colorPush.setStyleSheet)
        # update result
        self.drawWidget.update_result.connect(self.visWidget.update_result)
        self.drawWidget.update_result.connect(self.gamutWidget.set_ab)
        # self.visWidget.boom.connect(self.gamutWidget.set_ab)
        # self.drawWidget.update_result.connect(self.drawWidget.set_color)
        self.visWidget.update_color.connect(self.colorPush.setStyleSheet)
        # self.visWidget.update_color.connect(self.drawWidget.set_color)
        # update gamut
        self.drawWidget.update_gamut.connect(self.gamutWidget.set_gamut)
        self.drawWidget.update_ab.connect(self.gamutWidget.set_ab)
        self.gamutWidget.update_color.connect(self.drawWidget.set_color)
        # connect palette
        self.drawWidget.suggest_colors.connect(self.customPalette.set_colors)
        # self.connect(self.drawWidget, SIGNAL('change_color_id'), self.customPalette.update_color_id)
        self.customPalette.update_color.connect(self.drawWidget.set_color)
        self.customPalette.update_color.connect(self.gamutWidget.set_ab)

        self.drawWidget.used_colors.connect(self.usedPalette.set_colors)
        self.usedPalette.update_color.connect(self.drawWidget.set_color)
        self.usedPalette.update_color.connect(self.gamutWidget.set_ab)
        # menu events
        self.bGray.setChecked(True)
        self.bRestart.clicked.connect(self.reset)
        self.bQuit.clicked.connect(self.quit)
        self.bGray.toggled.connect(self.enable_gray)
        self.bSave.clicked.connect(self.save)
        self.bLoad.clicked.connect(self.load)
        self.bXsave.clicked.connect(self.xsafe)

        self.start_t = time.time()

        if img_file is not None:
            self.drawWidget.init_result(img_file)

    def AddWidget(self, widget, title):
        widgetLayout = QVBoxLayout()
        widgetBox = QGroupBox()
        widgetBox.setTitle(title)
        vbox_t = QVBoxLayout()
        vbox_t.addWidget(widget)
        widgetBox.setLayout(vbox_t)
        widgetLayout.addWidget(widgetBox)

        return widgetLayout

    def nextImage(self):
        self.drawWidget.nextImage()

    def reset_all(self):
        # self.start_t = time.time()
        print('============================reset all=========================================')
        self.visWidget.reset()
        self.gamutWidget.reset()
        self.customPalette.reset()
        self.usedPalette.reset()
        self.drawWidget.reset()
        self.update()
        self.colorPush.setStyleSheet("background-color: grey")
        self.if_save = False

    def reset(self):
        if self.if_save == False:
            do_reset = QMessageBox.question(
                self,
                'RESET',
                "Image is not saved. Continue?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if do_reset == QMessageBox.Yes:
                self.reset_all()
        else:
            self.reset_all()

    def enable_gray(self):
        self.drawWidget.enable_gray()

    def quit(self):
        if self.if_save == False:
            do_quit = QMessageBox.question(
                self,
                'QUIT',
                "Image is not saved. Continue?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if do_quit == QMessageBox.Yes:
                print('time spent = %3.3f' % (time.time() - self.start_t))
                self.close()
        else:
            print('time spent = %3.3f' % (time.time() - self.start_t))
            self.close()

    def save(self):
        print('time spent = %3.3f' % (time.time() - self.start_t))
        self.drawWidget.save_result()
        self.if_save = True
        QMessageBox.information(
            self,
            'Save',
            'Image saved!',
            QMessageBox.Ok,
            QMessageBox.Ok
        )

    def xsafe(self):
        print('time spent = %3.3f' % (time.time() - self.start_t))
        do_realsr = QMessageBox.question(
            self,
            'RealSR',
            'RealSR may take some time to finish.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if do_realsr == QMessageBox.Yes:
            self.drawWidget.save_result_x()
            self.if_save = True
            QMessageBox.information(
                self,
                'XSave',
                'Save with RealSR finished!',
                QMessageBox.Ok,
                QMessageBox.Ok
            )
        else:
            QMessageBox.information(
                self,
                'XSave',
                'Xsave canceled.',
                QMessageBox.Ok,
                QMessageBox.Ok
            )

    def load(self):
        if self.if_save == False:
            do_load = QMessageBox.question(
                self,
                'LOAD',
                'Image is not saved. Continue?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if do_load == QMessageBox.Yes:
                self.drawWidget.load_image()
                self.if_save == False
        else:
            self.drawWidget.load_image()
            self.if_save == False

    def change_color(self):
        print('change color')
        self.drawWidget.change_color(use_suggest=True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
            self.reset()

        if event.key() == Qt.Key_Q:
            self.save()
            self.quit()

        if event.key() == Qt.Key_S:
            self.save()

        if event.key() == Qt.Key_G:
            self.bGray.toggle()

        if event.key() == Qt.Key_L:
            self.load()

        if event.key() == Qt.Key_X:
            self.xsafe()
