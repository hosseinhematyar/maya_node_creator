import maya.OpenMayaUI as omui
import maya.cmds as cmds
import sys
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance

from . import core


def new_scene():
    cmds.file(f=True, new=True)
    viewport = cmds.getPanel(withFocus=True)
    cmds.modelEditor(viewport, edit=True, wireframeOnShaded=True)
    cmds.scriptEditorInfo(clearHistory=True)


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class NodeCreator(QtWidgets.QDialog):
    def __init__(self):
        super(NodeCreator, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Maya Node Creator")
        self.setMinimumWidth(200)
        self.header_names = ['Name', 'Type', 'TranslateX', 'TranslateY', 'TranslateZ', 'Color']

        self.object_checkbox = QtWidgets.QCheckBox()
        # self.object_checkbox.setCheckState(QtCore.Qt.Unchecked)

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
        self.objects_table.setColumnCount(len(self.header_names))
        self.objects_table.setMinimumWidth(640)
        self.objects_table.setHorizontalHeaderLabels(self.header_names)
        self.objects_table.itemChanged.connect(self.on_item_changed)

        self.create_button = QtWidgets.QPushButton('Create Object')
        self.create_button.clicked.connect(self.create_object)

        self.new_scene_button = QtWidgets.QPushButton('Reset')
        self.new_scene_button.clicked.connect(new_scene)

        self.delete_button = QtWidgets.QPushButton('Delete')
        self.delete_button.clicked.connect('')

        # self.move_button = QtWidgets.QPushButton('Move')
        # self.delete_button.clicked.connect('')

        self.cancel_button = QtWidgets.QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.close)

        self.develop_button = QtWidgets.QPushButton('Develop Test')
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
        object_instance = core.Object(self.object_type.currentText(), self.object_name.text())
        object_instance.create()
        self.object_storage.append(object_instance)
        self.row_count = self.objects_table.rowCount()
        self.objects_table.insertRow(self.row_count)

        transform_item = QtWidgets.QTableWidgetItem(object_instance.object_transform)
        transform_item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        transform_item.setCheckState(QtCore.Qt.Checked)
        self.objects_table.setItem(self.row_count, 0, transform_item)
        transform_item.setData(QtCore.Qt.UserRole, object_instance.set_object_transform)
        transform_item.setTextAlignment(QtCore.Qt.AlignCenter)

        type_item = QtWidgets.QTableWidgetItem(object_instance.object_type)
        self.objects_table.setItem(self.row_count, 1, type_item)
        type_item.setFlags(QtCore.Qt.NoItemFlags)
        type_item.setTextAlignment(QtCore.Qt.AlignCenter)

        tx_item = QtWidgets.QDoubleSpinBox()
        tx_item.valueChanged.connect(self.on_value_changed)
        tx_item.setProperty('translate_x', object_instance.set_translate_x)
        self.objects_table.setCellWidget(self.row_count, 2, tx_item)

        ty_item = QtWidgets.QDoubleSpinBox()
        ty_item.valueChanged.connect(self.on_value_changed)
        ty_item.setProperty('translate_y', object_instance.set_translate_y)
        self.objects_table.setCellWidget(self.row_count, 3, ty_item)

        tz_item = QtWidgets.QDoubleSpinBox()
        tz_item.valueChanged.connect(self.on_value_changed)
        tz_item.setProperty('translate_z', object_instance.set_translate_z)
        self.objects_table.setCellWidget(self.row_count, 4, tz_item)

        color_button = QtWidgets.QPushButton('')
        color_button.clicked.connect(self.on_color_picker)
        color_button.setProperty('color_setter', object_instance.set_color)
        self.objects_table.setCellWidget(self.row_count, 5, color_button)

    def on_item_changed(self, item):
        item_data = item.data(QtCore.Qt.UserRole)
        if not item_data:
            return

        changed_value = item.text()
        if not changed_value:
            return

        if item.column() == self.header_names.index('Name'):
            new_transform_name = item_data(changed_value)
            item.setText(new_transform_name)

    def on_value_changed(self, value):
        sender = self.sender()
        set_tx_function = sender.property('translate_x')
        set_ty_function = sender.property('translate_y')
        set_tz_function = sender.property('translate_z')

        if set_tx_function:
            set_tx_function(value)

        if set_ty_function:
            set_ty_function(value)

        if set_tz_function:
            set_tz_function(value)

    def on_color_picker(self):
        sender = self.sender()
        set_color_function = sender.property('color_setter')

        object_color = QtWidgets.QColorDialog.getColor(parent=maya_main_window())
        if not object_color:
            return

        if not object_color.isValid():
            return

        red, green, blue, alpha = object_color.getRgbF()
        red, green, blue = set_color_function(red=red, green=green, blue=blue)

        object_color.setRgbF(red, green, blue)
        red, green, blue, alpha = object_color.getRgb()
        sender.setStyleSheet(f"background-color:rgb({red},{green},{blue})")

    def develop(self):
        pass


try:
    app.close()
    app.deleteLater()
except:
    pass

app = NodeCreator()
app.show()
# sys.exit(app.exec_())
