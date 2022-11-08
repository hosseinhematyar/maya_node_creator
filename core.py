import logging
import os

import maya.cmds as cmds

ReferenceList = {
    # '-- None --': 'None',
}

reference_location = '/Users/hossein/Desktop/scene_files/'


def get_reference_list():
    os.chdir(reference_location)
    my_list = os.listdir('.')
    for i in range(len(my_list)):
        file_full_name = my_list[i]
        pathname, extension = os.path.splitext(file_full_name)
        filename = pathname.split('/')
        ReferenceList[my_list[i]] = filename[0]


get_reference_list()


class Object:
    def __init__(self, object_reference, object_tx=0, object_ty=0, object_tz=0,
                 color_red=0, color_green=0, color_blue=0):
        self._namespace = ''
        self.object_reference = object_reference
        self.top_transform = self.namespace + 'asset'
        self.object_tx = object_tx
        self.object_ty = object_ty
        self.object_tz = object_tz
        self.color_red = color_red
        self.color_green = color_green
        self.color_blue = color_blue
        self.material_shading_node = ''
        self.material_shading_engine = ''

    @property
    def namespace(self):
        print("Getter method called")
        return self._namespace

    @namespace.setter
    def namespace(self, value):
        print("Setter method called")
        self._namespace = value

        if not cmds.namespace(exists=self._namespace):
            pass

    def is_valid(self):
        if not cmds.namespace(exists=self.namespace):
            logging.warning('IsValid --> This name space is not define')
            return

        return True

    def create(self):
        self._import_reference()
        # self.set_translate(self.object_tx, self.object_ty, self.object_tz)
        # self._create_annotation()
        # self._add_attribute()
        # self._set_attribute()
        # self.get_translate()
        # self._create_material()
        # self.set_color(self.color_red, self.color_green, self.color_blue)
        # self.get_color()

    def _import_reference(self):
        if cmds.namespace(exists=self.namespace):
            logging.warning('Import Reference --> This name space is duplicate in this scene')
            return

        cmds.namespace(add=self.namespace)
        cmds.namespace(set=self.namespace)

        cmds.file(f'{reference_location}{self.object_reference}', reference=True)
        namespace_content = cmds.ls(f'{self.namespace}:*', assemblies=True)
        cmds.namespace(set=':')

        cmds.group(namespace_content, name=self.top_transform)

    def _create_material(self):
        self.material_shading_node = cmds.shadingNode('lambert', asShader=True)
        self.material_shading_engine = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
        cmds.connectAttr(self.material_shading_node + '.outColor', self.material_shading_engine + '.surfaceShader')

        if not cmds.objExists(self.object_transform):
            logging.warning('Create Material --> No surface exists')
            return

        if not self.material_shading_engine:
            logging.warning('Create Material --> No material exists')
            return

        cmds.sets(self.object_transform, edit=True, forceElement=self.material_shading_engine)

    def _create_annotation(self):
        if not cmds.objExists(self.object_transform):
            logging.warning('Select Annotation --> No surface exists')
            return

        # Create Locator and set parent
        self.locator = cmds.spaceLocator()
        self.locator_name = self.locator[0]
        cmds.parent(self.locator_name, self.object_transform, shape=True)

        # Create Annotation and set parent
        self.annotate_name = cmds.annotate(self.object_transform, tx=self.object_transform)
        cmds.parent(self.annotate_name, self.object_transform)
        cmds.parent(self.annotate_name, self.locator_name)

    def _add_attribute(self):
        if not cmds.objExists(self.object_transform):
            logging.warning('Add Attribute --> No surface exists')
            return
        cmds.addAttr(self.object_transform, attributeType='bool', shortName='mnc', longName='MayaNodeCreator')

    def _set_attribute(self):
        if not cmds.objExists(self.object_transform):
            logging.warning('Add Attribute --> No surface exists')
            return
        cmds.setAttr(f'{self.object_transform}.mnc', k=True)
        cmds.setAttr(f'{self.object_transform}.mnc', 1)
        self.mnc_attribute_status = cmds.getAttr(f'{self.object_transform}.mnc')
        return self.mnc_attribute_status

    def get_translate(self):
        if not cmds.objExists(self.object_transform):
            logging.warning('Get Translate --> No surface exists')
            return
        object_translate = cmds.getAttr(f'{self.object_transform}.translate')[0]
        return object_translate

    def set_translate(self, object_tx, object_ty, object_tz):
        if not cmds.objExists(self.object_transform):
            logging.warning('Get Translate --> No surface exists')
            return

        object_translate = cmds.setAttr(f'{self.object_transform}.t', object_tx, object_ty, object_tz, type="double3")
        return object_translate

    def set_translate_x(self, translate_x):
        if not cmds.objExists(self.namespace):
            logging.warning('Set Translate X --> No surface exists')
            return

        cmds.setAttr(f'{self.namespace}.tx', translate_x, edit=True)
        return translate_x

    def set_translate_y(self, translate_y):
        if not cmds.objExists(self.namespace):
            logging.warning('Set Translate Y --> No surface exists')
            return

        cmds.setAttr(f'{self.namespace}.ty', translate_y, edit=True)
        return translate_y

    def set_translate_z(self, translate_z):
        if not cmds.objExists(self.namespace):
            logging.warning('Set Translate Z --> No surface exists')
            return

        cmds.setAttr(f'{self.namespace}.tz', translate_z, edit=True)
        return translate_z

    def get_color(self):
        if not cmds.objExists(self.object_transform):
            logging.warning('Get Color --> No surface exists')
            return

        if not cmds.objExists(self.material_shading_node):
            logging.warning('Get Color --> No Material Shading Node exists')
            return

        red, green, blue = cmds.getAttr(f'{self.material_shading_node}.color')[0]
        return red, green, blue

    def set_color(self, color_red=0, color_green=0, color_blue=0):
        if not self.material_shading_node:
            logging.warning('Set Color --> No material exists')
            return

        cmds.setAttr(self.material_shading_node + ".color", color_red, color_green, color_blue)
        return self.get_color()

    def select(self):
        if not cmds.objExists(self.object_transform):
            logging.warning('Select Object --> No surface exists')
            return

        cmds.select(self.object_transform)

    def delete(self):
        if not cmds.objExists(self.object_transform):
            logging.warning('Delete Object --> No surface exists')
            return

        cmds.delete(self.object_transform)

    # def set_namespace(self, new_namespace):
    #     if not cmds.objExists(self.namespace):
    #         logging.warning('Set NameSpace --> No surface exists')
    #         return self.namespace
    #
    #     self.object_transform = cmds.rename(self.namespace, new_namespace)
    #     return self.namespace
    @namespace.setter
    def namespace(self, value):
        self._namespace = value

    @namespace.setter
    def namespace(self, value):
        self._namespace = value

    @namespace.setter
    def namespace(self, value):
        self._namespace = value


if __name__ == '__main__':
    object_instance = Object('MultiFile.mb', object_tx=5, object_ty=5, object_tz=5, color_red=1,
                             color_green=2, color_blue=3)
    object_instance.namespace = 'my'
    object_instance.create()
    object_instance.select()
    object_instance.delete()
    object_instance.set_translate_x(5.4)
    object_instance.set_translate_y(5)
    object_instance.set_translate_z(5)
    object_instance.set_color(2, 2, 2)
