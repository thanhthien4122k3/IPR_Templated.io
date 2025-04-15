from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1917, 1080)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setEnabled(False)
        self.frame.setGeometry(QtCore.QRect(0, 0, 476, 146))
        self.frame.setMinimumSize(QtCore.QSize(450, 120))
        self.frame.setMaximumSize(QtCore.QSize(476, 146))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frame.setLineWidth(2)
        self.frame.setMidLineWidth(0)
        self.frame.setObjectName("frame")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(parent=self.frame)
        self.label_2.setEnabled(False)
        self.label_2.setMinimumSize(QtCore.QSize(450, 120))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)

        self.frame_2 = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_2.setEnabled(True)
        self.frame_2.setGeometry(QtCore.QRect(475, 0, 1441, 146))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frame_2.setLineWidth(2)
        self.frame_2.setObjectName("frame_2")
        self.pushButton = QtWidgets.QPushButton(parent=self.frame_2)
        self.pushButton.setGeometry(QtCore.QRect(1260, 60, 100, 35))
        self.pushButton.setText("Log In")
        self.pushButton.setObjectName("pushButton")

        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(475, 146, 1441, 931))
        self.stackedWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.stackedWidget.setObjectName("stackedWidget")

        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")

        self.New_template = QtWidgets.QGroupBox(parent=self.page)
        self.New_template.setGeometry(QtCore.QRect(7, 0, 1421, 931))
        self.New_template.setTitle("Create a new template")
        self.New_template.setObjectName("New_template")

        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.New_template)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 1401, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.headerBar = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.headerBar.setContentsMargins(0, 0, 0, 0)
        self.headerBar.setObjectName("headerBar")
        self.Logo = QtWidgets.QToolButton(parent=self.horizontalLayoutWidget)
        self.Logo.setText("...")
        self.Logo.setObjectName("Logo")
        self.headerBar.addWidget(self.Logo)

        self.ImageName = QtWidgets.QLineEdit(parent=self.horizontalLayoutWidget)
        self.ImageName.setText("ImageName")
        self.ImageName.setObjectName("ImageName")
        self.headerBar.addWidget(self.ImageName)

        self.horizontalSpacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                                      QtWidgets.QSizePolicy.Policy.Minimum)
        self.headerBar.addItem(self.horizontalSpacer)

        self.btnUpload = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.btnUpload.setStyleSheet("""
            QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; padding: 5px; }
            QPushButton:hover { background-color: #45a049; }
        """)
        self.btnUpload.setText("Upload")
        self.btnUpload.setObjectName("btnUpload")
        self.headerBar.addWidget(self.btnUpload)

        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(parent=self.New_template)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 120, 1401, 651))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")

        self.LogoLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.LogoLayout.setContentsMargins(0, 0, 0, 0)
        self.LogoLayout.setObjectName("LogoLayout")

        self.widgetPreview = QtWidgets.QWidget(parent=self.horizontalLayoutWidget_2)
        self.widgetPreview.setObjectName("widgetPreview")
        self.labelPreview = QtWidgets.QLabel(parent=self.widgetPreview)
        self.labelPreview.setGeometry(QtCore.QRect(660, 310, 81, 16))
        self.labelPreview.setText("Logo Preview")
        self.labelPreview.setObjectName("labelPreview")
        self.LogoLayout.addWidget(self.widgetPreview)

        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(parent=self.New_template)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 780, 1401, 71))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")

        self.toolbarLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.toolbarLayout.setContentsMargins(0, 0, 0, 0)
        self.toolbarLayout.setObjectName("toolbarLayout")

        self.btnRotate = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_3)
        self.btnRotate.setText("Rotate")
        self.btnRotate.setStyleSheet(self._toolbar_btn_style())
        self.toolbarLayout.addWidget(self.btnRotate)

        self.btnCrop = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_3)
        self.btnCrop.setText("Crop")
        self.btnCrop.setStyleSheet(self._toolbar_btn_style())
        self.toolbarLayout.addWidget(self.btnCrop)

        self.btnSave = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_3)
        self.btnSave.setText("Save")
        self.btnSave.setStyleSheet(self._toolbar_btn_style())
        self.toolbarLayout.addWidget(self.btnSave)

        self.btnDelete = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_3)
        self.btnDelete.setText("Delete")
        self.btnDelete.setStyleSheet("""
            QPushButton { background-color: #f44336; color: white; border-radius: 5px; padding: 5px; }
            QPushButton:hover { background-color: #d32f2f; }
        """)
        self.toolbarLayout.addWidget(self.btnDelete)

        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(parent=self.New_template)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 860, 1401, 61))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")

        self.FooterLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.FooterLayout.setContentsMargins(0, 0, 0, 0)
        self.FooterLayout.setObjectName("FooterLayout")

        self.FooterEdit = QtWidgets.QLineEdit(parent=self.horizontalLayoutWidget_4)
        self.FooterEdit.setText("Footer")
        self.FooterEdit.setObjectName("FooterEdit")
        self.FooterLayout.addWidget(self.FooterEdit)

        self.stackedWidget.addWidget(self.page)

        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.listWidget = QtWidgets.QListWidget(parent=self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(0, 146, 476, 934))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.addItems([
            "My templates", "API integration", "Render", "Embed", "Playground"
        ])

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def _toolbar_btn_style(self):
        return """QPushButton {
            background-color: #2196F3; 
            color: white; 
            border-radius: 5px; 
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #1e88e5;
        }"""

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "_Templated.io"))
