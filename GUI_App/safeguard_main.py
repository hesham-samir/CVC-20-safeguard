import sys
from os import path


from PyQt5.QtWidgets import QWidget,QGridLayout,QTextEdit,QHBoxLayout,QApplication,QMainWindow,QLabel,QVBoxLayout,QTabWidget,QPushButton
from PyQt5.QtGui import QPalette,QColor,QIcon,QPixmap
from PyQt5.QtCore import Qt, QProcess

from face_detection_widget import MainFaceDetectioWidget

################################### Mask Detector ################################
class MaskDetectorWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.start_button = QPushButton('Start')
        self.runProcess = QProcess()

        layout = QVBoxLayout()
        layout.addStretch()
        button_hbox = QHBoxLayout()
        button_hbox.addStretch()
        button_hbox.addWidget(self.start_button)
        button_hbox.addStretch()
        layout.addLayout(button_hbox)
        self.setLayout(layout)
        self.start_button.clicked.connect(self.on_start_button_clicked)

    def on_start_button_clicked(self):

        self.runProcess.start("python detect_mask_video.py")

################################### ABOUT PAGE ###################################
class AboutWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        about_layout = QGridLayout()

        textEdit = QTextEdit()
        textEdit.setReadOnly(True)
        textEdit.setStyleSheet("background:#393e46;border: 2px solid #29a19c; color: white; max-width: 200ex;font-size: 20px;")
        textEdit.setText("""\nCoronavirus disease (COVID-19) is an infectious disease caused by a new virus. The disease causes respiratory illness (like the flu) with symptoms such as a cough, fever, and in more severe cases, difficulty breathing. You can protect yourself by washing your hands frequently, avoiding touching your face, and avoiding close contact (1 meter or 3 feet) with people who are unwell.
        \nDue to the widely spread pandemic, precautions have been taken to protect people from getting infected including wearing face masks, frequently wash hands, and most importantly, staying at home.
        \nDespite of these advices, some people still have to go to work and spend hours outside their houses which makes them more prone to infection. Also, studies have shown that a regular person touches his face approximately sixteen times per hour. We touch our faces so often that the odds of recontamination of our hands between washings are extremely high.
        \n\nTherefore, our project aims to increase awareness about the basic protective precautions that should be taken to protect people from the Corona virus. The model checks whether a person is wearing a mask or not and warns a person if he tries to touch his face.
        """)
        textEdit.setAlignment(Qt.AlignLeft)

        about_layout.addWidget(textEdit, 0,0)
        self.setLayout(about_layout)


################################### MAIN WIDGET ###################################
class MainWidget(QWidget):
    def __init__(self, haar_cascade_filepath,parent = None):
        super().__init__(parent)

        # Add Safeguard header
        label_and_image_hbox = QHBoxLayout()
        label = QLabel("Safeguard")
        label.setStyleSheet("font: bold italic Impact; color : white; font-size: 50px;")
        image = QLabel()
        pixmap = QPixmap("protect_image.png")
        image.setPixmap(pixmap)
        label_and_image_hbox.addWidget(image)
        label_and_image_hbox.addWidget(label)
        label_and_image_hbox.addStretch()
        main_layout = QVBoxLayout()
        main_layout.addLayout(label_and_image_hbox)

        # Add Tab window
        tab_window = QTabWidget()
        touch_face_detection_widget = MainFaceDetectioWidget(haar_cascade_filepath)
        mask_detection = MaskDetectorWidget()
        about = AboutWidget()
        tab_window.addTab(touch_face_detection_widget,"Touch Face Detection")
        tab_window.addTab(mask_detection,"Mask Detection")
        tab_window.addTab(about,"About")

        # Set Qss Style For Tab window
        main_layout.addWidget(tab_window)
        qss_file = open('style_file.qss').read()
        tab_window.setStyleSheet(qss_file)

        self.setLayout(main_layout)


################################### MAIN FUNCTION ###################################
def main(haar_cascade_filepath):
    app = QApplication(sys.argv)

    # Set Background Color
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#222831"))
    app.setPalette(palette)

    # Set Icon And Title
    main_window = QMainWindow()
    main_window.setWindowTitle("Safeguard")
    main_window.setWindowIcon(QIcon("protect_image.png"))

    # Add Main Window Widget
    main_widget = MainWidget(haar_cascade_filepath)
    main_window.setCentralWidget(main_widget)
    main_window.showMaximized()

    # Run App
    sys.exit(app.exec_())


if __name__ == '__main__':
    script_dir = path.dirname(path.realpath(__file__))
    cascade_filepath = path.join('.\\haarcascade_frontalface_default.xml')

    cascade_filepath = path.abspath(cascade_filepath)
    main(cascade_filepath)
