import maya.cmds as cmds
from PySide2 import QtWidgets

from . import core

from functools import partial


def new_scene():
    cmds.file(f=True, new=True)
    viewport = cmds.getPanel(withFocus=True)
    cmds.modelEditor(viewport, edit=True, wireframeOnShaded=True)


class NodeCreator(QtWidgets.QDialog):
    def __init__(self):
        super(NodeCreator, self).__init__()
        self.tx_item = 0
        self.setWindowTitle("Maya Node Creator")
        self.setMinimumWidth(200)
        self.header_names = ['', 'Name', 'Type', 'TranslateX', 'TranslateY', 'TranslateZ', 'Color']

        self.object_name = QtWidgets.QLineEdit()

        self.object_type = QtWidgets.QComboBox()
        self.object_type.addItems(list(core.AllTypes.keys()))

        self.translate_x = QtWidgets.QDoubleSpinBox()
        self.translate_y = QtWidgets.QDoubleSpinBox()
        self.translate_z = QtWidgets.QDoubleSpinBox()

        self.color_red = QtWidgets.QSpinBox()
        self.color_blue = QtWidgets.QSpinBox()
        self.color_green = QtWidgets.QSpinBox()

        self.objects_table = QtWidgets.QTableWidget()
        self.objects_table.setColumnCount(7)
        self.objects_table.setMinimumWidth(720)
        self.objects_table.setColumnWidth(0, 40)
        self.objects_table.setColumnWidth(1, 160)
        # self.objects_table.setColumnWidth(6, 100)
        self.objects_table.setHorizontalHeaderLabels(self.header_names)
        self.objects_table.cellChanged.connect(self.edit_object)

        self.create_button = QtWidgets.QPushButton('Create Object')
        self.create_button.clicked.connect(self.create_object)

        self.new_scene_button = QtWidgets.QPushButton('New Scene')
        self.new_scene_button.clicked.connect(new_scene)

        self.delete_button = QtWidgets.QPushButton('Delete')
        self.delete_button.clicked.connect('')

        # self.move_button = QtWidgets.QPushButton('Move')
        # self.delete_button.clicked.connect('')

        self.cancel_button = QtWidgets.QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.close)

        self.develop_button = QtWidgets.QPushButton('<<-- DEVELOP -->>')
        self.develop_button.clicked.connect(self.develop)

        self.export_button = QtWidgets.QPushButton('Export')
        self.export_button.clicked.connect('')

        # General Fields
        self.general_layout = QtWidgets.QFormLayout()
        self.general_layout.addRow('Object Name:', self.object_name)
        self.general_layout.addRow('Object Type:', self.object_type)

        # Features Fields
        self.features_layout = QtWidgets.QVBoxLayout()
        self.features_layout.addWidget(QtWidgets.QLabel('Move Options:'))
        self.features_layout.addWidget(self.translate_x)
        self.features_layout.addWidget(self.translate_y)
        self.features_layout.addWidget(self.translate_z)
        self.features_layout.addWidget(QtWidgets.QLabel('Set Color Options:'))
        self.features_layout.addWidget(self.color_red)
        self.features_layout.addWidget(self.color_blue)
        self.features_layout.addWidget(self.color_green)

        # Objects Table
        self.objects_list_layout = QtWidgets.QHBoxLayout()
        self.objects_list_layout.addWidget(self.objects_table)

        # Button Layout 1
        self.button_layout_1 = QtWidgets.QHBoxLayout()
        self.button_layout_1.addWidget(self.new_scene_button)
        self.button_layout_1.addWidget(self.create_button)

        # Button Layout 2
        self.button_layout_2 = QtWidgets.QHBoxLayout()
        self.button_layout_2.addWidget(self.develop_button)
        self.button_layout_2.addWidget(self.delete_button)
        # self.button_layout_2.addWidget(self.move_button)
        self.button_layout_2.addWidget(self.export_button)
        self.button_layout_2.addWidget(self.cancel_button)

        # Main Left Layout
        self.main_left_layout = QtWidgets.QVBoxLayout()
        self.main_left_layout.addLayout(self.general_layout)
        self.main_left_layout.addLayout(self.features_layout)
        self.main_left_layout.addLayout(self.button_layout_1)
        # self.setLayout(self.main_left_layout)

        # Main Right Layout
        self.main_right_layout = QtWidgets.QVBoxLayout()
        self.main_right_layout.addLayout(self.objects_list_layout)
        self.main_right_layout.addLayout(self.button_layout_2)
        # self.setLayout(self.main_right_layout)

        # Main Layout
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.main_left_layout)
        self.main_layout.addLayout(self.main_right_layout)
        self.setLayout(self.main_layout)

        self.object_storage = []

    def create_object(self):
        # Create object instance using core
        object_instance = core.Object(self.object_type.currentText(), self.object_name.text())
        object_instance.create()

        # Keep track of created instances in object storage
        self.object_storage.append(object_instance)

        # Add object instance data to table
        # self.objects_table.setRowCount(0)
        self.row_count = self.objects_table.rowCount()
        self.objects_table.insertRow(self.row_count)
        transform_item = QtWidgets.QTableWidgetItem(object_instance.object_transform)
        self.objects_table.setItem(self.row_count, 1, transform_item)

        type_item = QtWidgets.QTableWidgetItem(object_instance.object_type)
        self.objects_table.setItem(self.row_count, 2, type_item)

        tx_item = QtWidgets.QTableWidgetItem(str(object_instance.get_translate()[0]))
        self.objects_table.setItem(self.row_count, 3, tx_item)

        ty_item = QtWidgets.QTableWidgetItem(str(object_instance.get_translate()[1]))
        self.objects_table.setItem(self.row_count, 4, ty_item)

        tz_item = QtWidgets.QTableWidgetItem(str(object_instance.get_translate()[2]))
        self.objects_table.setItem(self.row_count, 5, tz_item)

        color_item = QtWidgets.QTableWidgetItem(str(object_instance.get_color()))
        self.objects_table.setItem(self.row_count, 6, color_item)

    def edit_object(self, row, column):
        tx_cell_item = self.objects_table.item(row, column).text()
        if column == self.header_names.index('TranslateX'):
            pass
        print('row -->', row)
        print('column -->', column)
        print('changed to -->', tx_cell_item)

    def develop(self):
        pass
        # tx_cell_item = float(self.objects_table.item(0, 3).text())
        # print(self.tx_item)
        # print(type(self.tx_item))


try:
    app.close()
    app.deleteLater()
except:
    pass

app = NodeCreator()
app.show()
# sys.exit(app.exec_())
