import cv2
import numpy as np
import winsound         # for sound

from utils import detector_utils as detector_utils

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget,QLabel,QHBoxLayout,QPushButton,QVBoxLayout
from PyQt5.QtGui import QImage,QPixmap,QPainter
from record_video import RecordVideo


class FaceDetectionWidget(QWidget):

    def __init__(self, haar_cascade_filepath, parent=None):
        super().__init__(parent)
        # Face Initialization
        self.classifier = cv2.CascadeClassifier(haar_cascade_filepath)
        self.image = QImage()
        self._red = (0, 0, 255)
        self._width = 2
        self._min_size = (50, 50)
        self.l1 = QLabel()

        # Hand Initialization
        self. detection_graph, self.sess = detector_utils.load_inference_graph()

        # Warning Initialization
        self.beeb_flag = False
        self.sound_timer = QTimer(self)
        self.sound_timer.timeout.connect(self.beeb)
        self.sound_timer.start(500)


    def detect_faces(self, image: np.ndarray):
        # Detect Faces
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.equalizeHist(gray_image)
        faces = self.classifier.detectMultiScale(gray_image,scaleFactor=1.3,
                                                 minNeighbors=4,
                                                 flags=cv2.CASCADE_SCALE_IMAGE,
                                                 minSize=(self._min_size))
        # Draw Rectangles On Faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image,(x, y),(x+w, y+h), self._red,self._width)

        # Detect Hands
        try:
            image_np = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        except:
            print("Error converting to RGB")

        boxes, scores = detector_utils.detect_objects(image_np,
                                                     self. detection_graph,
                                                     self.sess)

        # draw bounding boxes on Hands
        detector_utils.draw_box_on_image(2, 0.5,
                                         scores, boxes, 320, 180,
                                         image)
        touched = False
        for (x, y, w, h) in faces:
            for i in range(0,2):
                if self.isTouching(x,y,x+w,y+h,boxes[i][1]*320,boxes[i][0]*180,boxes[i][3]*320,boxes[i][2]*180) and scores[i] > 0.5:
                    touched = True

        if touched:
            self.beeb_flag = True
        else :
            self.beeb_flag = False


        # Update Image Frame
        self.image = self.get_qimage(image)
        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())
        self.update()

    def beeb(self):
        if self.beeb_flag :
            winsound.Beep(440, 200)
            winsound.Beep(660, 200)

    def get_qimage(self, image: np.ndarray):
        height, width, colors = image.shape
        bytesPerLine = 3 * width

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QImage()

    def isTouching(self,minx1,miny1, maxx1, maxy1, minx2,miny2, maxx2, maxy2):

        # If one rectangle is on left side of other
        if(minx1 >= maxx2 or minx2 >= maxx1):
            return False

        # If one rectangle is above other
        if(miny1 >= maxy2 or miny2 >= maxy1):
            return False

        return True


class MainFaceDetectioWidget(QWidget):
    def __init__(self, haarcascade_filepath, parent=None):
        super().__init__(parent)
        fp = haarcascade_filepath

        # Add Safeguard Title
        label_and_image_hbox = QHBoxLayout()
        label = QLabel("DO NOT TOUCH YOUR FACE")
        label.setStyleSheet("font: bold Impact; color : white; font-size: 30px;")
        face_image = QLabel()
        pixmap = QPixmap("do_not_touch_your-face_image.png")
        face_image.setPixmap(pixmap)
        label_and_image_hbox.addWidget(face_image)
        label_and_image_hbox.addWidget(label)
        label_and_image_hbox.addStretch()

        self.face_detection_widget = FaceDetectionWidget(fp)

        self.record_video = RecordVideo()

        image_data_slot = self.face_detection_widget.detect_faces
        self.record_video.image_data.connect(image_data_slot)

        layout = QVBoxLayout()

        layout.addLayout(label_and_image_hbox)
        layout.addStretch()
        layout.addWidget(self.face_detection_widget)
        layout.addStretch()
        self.run_button = QPushButton('Start')
        button_hbox = QHBoxLayout()
        button_hbox.addStretch()
        button_hbox.addWidget(self.run_button)
        button_hbox.addStretch()
        layout.addLayout(button_hbox)

        self.run_button.clicked.connect(self.record_video.start_recording)
        self.setLayout(layout)
