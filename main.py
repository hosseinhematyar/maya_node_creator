# import logging
import maya.cmds as cmds
from PySide2 import QtWidgets

import core


def new_scene():
    cmds.file(f=True, new=True)
    viewport = cmds.getPanel(withFocus=True)
    cmds.modelEditor(viewport, edit=True, wireframeOnShaded=True)


class NodeCreator(QtWidgets.QDialog):
    def __init__(self):
        super(NodeCreator, self).__init__()
        self.setWindowTitle("Maya Node Creator")
        self.setMinimumWidth(100)

        self.object_name = QtWidgets.QLineEdit()

        self.object_type = QtWidgets.QComboBox()
        self.object_type.addItem('')

        self.translate_x = QtWidgets.QSpinBox()
        self.translate_y = QtWidgets.QSpinBox()
        self.translate_z = QtWidgets.QSpinBox()

        self.color_red = QtWidgets.QSpinBox()
        self.color_blue = QtWidgets.QSpinBox()
        self.color_green = QtWidgets.QSpinBox()

        self.create_button = QtWidgets.QPushButton('Create Object')
        self.create_button.clicked.connect(self.create_object)

        self.new_scene_button = QtWidgets.QPushButton('New Scene')
        self.new_scene_button.clicked.connect(new_scene)

        self.delete_button = QtWidgets.QPushButton('Delete Object')
        self.delete_button.clicked.connect('')

        self.move_button = QtWidgets.QPushButton('Move Object')
        self.delete_button.clicked.connect('')

        self.cancel_button = QtWidgets.QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.close)

        self.set_color_button = QtWidgets.QPushButton('Cancel')
        self.set_color_button.clicked.connect('')

        # General Fields
        self.general_layout = QtWidgets.QFormLayout()
        self.general_layout.addRow('Object Name:', self.object_name)
        self.general_layout.addRow('Object Type:', self.object_type)

        # Features Fields
        self.features_layout = QtWidgets.QHBoxLayout()
        self.features_layout.addWidget(QtWidgets.QLabel('Move Options'))
        self.features_layout.addWidget(self.translate_x)
        self.features_layout.addWidget(self.translate_y)
        self.features_layout.addWidget(self.translate_z)
        self.features_layout.addWidget(QtWidgets.QLabel('Set Color Options'))
        self.features_layout.addWidget(self.color_red)
        self.features_layout.addWidget(self.color_blue)
        self.features_layout.addWidget(self.color_green)

        # Button Layout
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.create_button)
        self.button_layout.addWidget(self.new_scene_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.move_button)
        self.button_layout.addWidget(self.set_color_button)

        # Main Layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.general_layout)
        self.main_layout.addLayout(self.features_layout)
        self.main_layout.addLayout(self.button_layout)
        self.setLayout(self.main_layout)

    def create_object(self):
        object_instance = core.Object(self.object_type.currentText(), self.object_name.text())
        object_instance.create()


try:
    app.close()
    app.deleteLater()
except:
    pass

app = NodeCreator()
app.show()
# sys.exit(app.exec_())
