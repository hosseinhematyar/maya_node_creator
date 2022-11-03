import sys

import maya.OpenMayaUI as omui
import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance

from . import core


def reset():
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
        self.chosen_color = QtGui.QColor()
        self.setWindowTitle("Maya Node Creator")
        self.setMinimumWidth(200)
        self.header_names = ['Name', 'NameSpace', 'Source File', 'TranslateX', 'TranslateY', 'TranslateZ', 'Color']
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)

        groupbox_1 = QtWidgets.QGroupBox("General Setting")
        layout.addWidget(groupbox_1)

        groupbox_2 = QtWidgets.QGroupBox("Transform Setting")
        layout.addWidget(groupbox_2)

        groupbox_3 = QtWidgets.QGroupBox("Color Setting")
        layout.addWidget(groupbox_3)

        groupbox_4 = QtWidgets.QGroupBox("Objects List")
        layout.addWidget(groupbox_4)

        self.object_checkbox = QtWidgets.QCheckBox()

        self.object_name_space = QtWidgets.QLineEdit()

        self.reference_list = QtWidgets.QComboBox()
        self.reference_list.addItems(list(core.ReferenceList.keys()))

        self.object_tx = QtWidgets.QDoubleSpinBox()
        self.object_ty = QtWidgets.QDoubleSpinBox()
        self.object_tz = QtWidgets.QDoubleSpinBox()

        self.select_color = QtWidgets.QPushButton()
        self.select_color.setMaximumWidth(50)
        self.select_color.clicked.connect(self.on_select_color)

        self.random_color = QtWidgets.QCheckBox('Use random color')
        self.random_color.clicked.connect('')

        self.objects_table = QtWidgets.QTableWidget()
        self.objects_table.setColumnCount(len(self.header_names))
        self.objects_table.setMinimumWidth(740)
        self.objects_table.setHorizontalHeaderLabels(self.header_names)
        self.objects_table.itemChanged.connect(self.on_item_changed)

        self.create_button = QtWidgets.QPushButton('Create Object')
        self.create_button.clicked.connect(self.create_object)
        self.create_button.setStyleSheet(f"background-color: green")

        self.delete_button = QtWidgets.QPushButton('Delete')

        self.reset_button = QtWidgets.QPushButton('Reset')
        self.reset_button.clicked.connect(reset)

        self.cancel_button = QtWidgets.QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.close)

        # General Setting
        self.general_layout = QtWidgets.QHBoxLayout()
        self.general_layout.addWidget(QtWidgets.QLabel('Name Space:'))
        self.general_layout.addWidget(self.object_name_space)
        self.general_layout.addWidget(QtWidgets.QLabel('Select object from object directory'))
        self.general_layout.addWidget(self.reference_list)
        groupbox_1.setLayout(self.general_layout)

        # Transform Setting
        self.transform_layout = QtWidgets.QHBoxLayout()
        self.transform_layout.addWidget(QtWidgets.QLabel('Object Location:'))
        self.transform_layout.addWidget(self.object_tx)

        self.transform_layout.addWidget(self.object_ty)
        self.transform_layout.addWidget(self.object_tz)
        groupbox_2.setLayout(self.transform_layout)

        # Color Setting
        self.color_layout = QtWidgets.QHBoxLayout()
        self.color_layout.addWidget(QtWidgets.QLabel('Object Color:'))
        self.color_layout.addWidget(self.select_color)
        self.color_layout.addWidget(self.random_color)
        groupbox_3.setLayout(self.color_layout)

        # Objects Table
        self.objects_list_layout = QtWidgets.QHBoxLayout()
        self.objects_list_layout.addWidget(self.objects_table)

        # Button Layout 2
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.create_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.reset_button)
        self.button_layout.addWidget(self.cancel_button)

        # Main Left Layout
        self.main_left_layout = QtWidgets.QVBoxLayout()
        self.main_left_layout.addLayout(self.general_layout)
        self.main_left_layout.addLayout(self.transform_layout)
        self.main_left_layout.addLayout(self.color_layout)

        # Main Right Layout
        self.main_right_layout = QtWidgets.QVBoxLayout()
        self.main_right_layout.addLayout(self.objects_list_layout)
        self.main_right_layout.addLayout(self.button_layout)

        # Main Layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.main_left_layout)
        self.main_layout.addLayout(self.main_right_layout)
        groupbox_4.setLayout(self.main_layout)

        self.object_storage = []

    def create_object(self):
        object_instance = core.Object(self.object_name_space.text(), self.reference_list.currentText(),
                                      object_tx=self.object_tx.value(),
                                      object_ty=self.object_ty.value(),
                                      object_tz=self.object_tz.value(),
                                      color_red=self.chosen_color.redF(),
                                      color_green=self.chosen_color.greenF(),
                                      color_blue=self.chosen_color.blueF())

        object_instance.create()
        self.object_storage.append(object_instance)

        self.row_count = self.objects_table.rowCount()
        self.objects_table.insertRow(self.row_count)

        transform_item = QtWidgets.QTableWidgetItem(object_instance.object_transform)
        transform_item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        transform_item.setCheckState(QtCore.Qt.Checked)
        self.objects_table.setItem(self.row_count, 0, transform_item)
        # transform_item.setData(QtCore.Qt.UserRole, object_instance.set_object_transform)
        transform_item.setTextAlignment(QtCore.Qt.AlignCenter)

        type_item = QtWidgets.QTableWidgetItem(object_instance.name_space)
        self.objects_table.setItem(self.row_count, 1, type_item)
        type_item.setFlags(QtCore.Qt.NoItemFlags)
        type_item.setTextAlignment(QtCore.Qt.AlignCenter)

        type_item = QtWidgets.QTableWidgetItem(object_instance.object_reference)
        self.objects_table.setItem(self.row_count, 2, type_item)
        type_item.setFlags(QtCore.Qt.NoItemFlags)
        type_item.setTextAlignment(QtCore.Qt.AlignCenter)

        tx_item = QtWidgets.QDoubleSpinBox()
        tx_item.setMinimum(-9999)
        tx_item.valueChanged.connect(self.on_value_changed)
        tx_item.setProperty('translate_x', object_instance.set_translate_x)
        self.objects_table.setCellWidget(self.row_count, 3, tx_item)

        ty_item = QtWidgets.QDoubleSpinBox()
        ty_item.setMinimum(-9999)
        ty_item.valueChanged.connect(self.on_value_changed)
        ty_item.setProperty('translate_y', object_instance.set_translate_y)
        self.objects_table.setCellWidget(self.row_count, 4, ty_item)

        tz_item = QtWidgets.QDoubleSpinBox()
        tz_item.setMinimum(-9999)
        tz_item.valueChanged.connect(self.on_value_changed)
        tz_item.setProperty('translate_z', object_instance.set_translate_z)
        self.objects_table.setCellWidget(self.row_count, 5, tz_item)

        color_button = QtWidgets.QPushButton('')
        color_button.clicked.connect(self.on_color_picker)
        color_button.setProperty('color_setter', object_instance.set_color)
        color_button.setProperty('color_getter', object_instance.get_color)
        self.objects_table.setCellWidget(self.row_count, 6, color_button)

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

    def on_select_color(self):
        sender = self.sender()
        self.chosen_color = QtWidgets.QColorDialog.getColor(parent=maya_main_window())
        if not self.chosen_color:
            return

        if not self.chosen_color.isValid():
            return

        red, green, blue, alpha = self.chosen_color.getRgb()
        sender.setStyleSheet(f"background-color:rgb({red},{green},{blue})")

    def on_color_picker(self):
        sender = self.sender()
        set_color_function = sender.property('color_setter')

        object_color = QtWidgets.QColorDialog.getColor(parent=maya_main_window())
        if not object_color:
            return

        if not object_color.isValid():
            return

        red, green, blue, alpha = object_color.getRgbF()
        red, green, blue = set_color_function(color_red=red, color_green=green, color_blue=blue)

        object_color.setRgbF(red, green, blue)
        red, green, blue, alpha = object_color.getRgb()
        sender.setStyleSheet(f"background-color:rgb({red},{green},{blue})")


try:
    app.close()
    app.deleteLater()
except:
    pass

app = NodeCreator()
app.show()
# sys.exit(app.exec_())
