# Form implementation generated from reading ui file 'c:\Users\Gebruiker\Documents\GitHub\Python-Module-Week7\ui\preferences.ui'
#
# Created by: PyQt6 UI code generator 6.9.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PreferencesMenu(object):
    def setupUi(self, PreferencesMenu):
        PreferencesMenu.setObjectName("PreferencesMenu")
        PreferencesMenu.resize(550, 427)
        PreferencesMenu.setMinimumSize(QtCore.QSize(550, 0))
        PreferencesMenu.setMaximumSize(QtCore.QSize(650, 432))
        PreferencesMenu.setStyleSheet("background-color: #4ba6a6;")
        self.verticalLayout = QtWidgets.QVBoxLayout(PreferencesMenu)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frameContainer = QtWidgets.QFrame(parent=PreferencesMenu)
        self.frameContainer.setStyleSheet("\n"
"QFrame {\n"
"    background-color: #3e8c8c;\n"
"    border-radius: 10px;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #7cc7c7;\n"
"    color: white;\n"
"    font-size: 20px;             /* Yazı büyük – butonu dolduracak gibi */\n"
"    border: none;\n"
"    border-radius: 15px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #6bb5b5;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #5aa4a4;\n"
"}")
        self.frameContainer.setObjectName("frameContainer")
        self.frameLayout = QtWidgets.QVBoxLayout(self.frameContainer)
        self.frameLayout.setSpacing(15)
        self.frameLayout.setObjectName("frameLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(parent=self.frameContainer)
        self.label.setMaximumSize(QtCore.QSize(110, 30))
        self.label.setStyleSheet("background-color: transparent;")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("c:\\Users\\Gebruiker\\Documents\\GitHub\\Python-Module-Week7\\ui\\../resorces/logo.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.labelTitle = QtWidgets.QLabel(parent=self.frameContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTitle.sizePolicy().hasHeightForWidth())
        self.labelTitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.labelTitle.setFont(font)
        self.labelTitle.setMouseTracking(False)
        self.labelTitle.setStyleSheet("color: white;")
        self.labelTitle.setScaledContents(False)
        self.labelTitle.setObjectName("labelTitle")
        self.horizontalLayout_2.addWidget(self.labelTitle, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        spacerItem = QtWidgets.QSpacerItem(110, 30, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.frameLayout.addLayout(self.horizontalLayout_2)
        self.btn_applications = QtWidgets.QPushButton(parent=self.frameContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_applications.sizePolicy().hasHeightForWidth())
        self.btn_applications.setSizePolicy(sizePolicy)
        self.btn_applications.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setKerning(True)
        self.btn_applications.setFont(font)
        self.btn_applications.setStyleSheet("")
        self.btn_applications.setObjectName("btn_applications")
        self.frameLayout.addWidget(self.btn_applications)
        self.btn_mentor = QtWidgets.QPushButton(parent=self.frameContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_mentor.sizePolicy().hasHeightForWidth())
        self.btn_mentor.setSizePolicy(sizePolicy)
        self.btn_mentor.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        self.btn_mentor.setFont(font)
        self.btn_mentor.setStyleSheet("")
        self.btn_mentor.setObjectName("btn_mentor")
        self.frameLayout.addWidget(self.btn_mentor)
        self.btn_interviews = QtWidgets.QPushButton(parent=self.frameContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_interviews.sizePolicy().hasHeightForWidth())
        self.btn_interviews.setSizePolicy(sizePolicy)
        self.btn_interviews.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        self.btn_interviews.setFont(font)
        self.btn_interviews.setStyleSheet("")
        self.btn_interviews.setObjectName("btn_interviews")
        self.frameLayout.addWidget(self.btn_interviews)
        self.exitButton = QtWidgets.QPushButton(parent=self.frameContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exitButton.sizePolicy().hasHeightForWidth())
        self.exitButton.setSizePolicy(sizePolicy)
        self.exitButton.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        self.exitButton.setFont(font)
        self.exitButton.setStyleSheet("")
        self.exitButton.setObjectName("exitButton")
        self.frameLayout.addWidget(self.exitButton)
        self.frameLayout.setStretch(0, 14)
        self.frameLayout.setStretch(1, 25)
        self.frameLayout.setStretch(2, 25)
        self.frameLayout.setStretch(3, 25)
        self.frameLayout.setStretch(4, 11)
        self.verticalLayout.addWidget(self.frameContainer)
        self.verticalLayout.setStretch(0, 90)

        self.retranslateUi(PreferencesMenu)
        QtCore.QMetaObject.connectSlotsByName(PreferencesMenu)

    def retranslateUi(self, PreferencesMenu):
        _translate = QtCore.QCoreApplication.translate
        PreferencesMenu.setWindowTitle(_translate("PreferencesMenu", "Preferences Menu"))
        self.labelTitle.setText(_translate("PreferencesMenu", "Tercih Menü"))
        self.btn_applications.setText(_translate("PreferencesMenu", "    📄Başvurular"))
        self.btn_mentor.setText(_translate("PreferencesMenu", "🤝Mentor Görüşmesi"))
        self.btn_interviews.setText(_translate("PreferencesMenu", "🎤Mülakatlar"))
        self.exitButton.setText(_translate("PreferencesMenu", "❌Çıkış"))
