# import logging
# import maya.cmds as cmds
# from NodeCreator import core
from PySide2 import QtWidgets


class NodeCreator(QtWidgets.QDialog):
    def __init__(self):
        super(NodeCreator, self).__init__()

        self.object_name = QtWidgets.QLineEdit('Object Name')
        self.object_name.clicked.connect()

        self.object_type = QtWidgets.QComboBox()
        self.object_type.addItem('')


        self.btn = QtWidgets.QPushButton()
        self.btn.setText("Text")
        self.clicked.connect(self.close)


try:
    app.close()
    app.deleteLater()
except:
    pass

app = NodeCreator()
app.show()
# sys.exit(app.exec_())
