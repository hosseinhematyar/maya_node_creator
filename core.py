import logging

import maya.cmds as cmds

AllTypes = {
    'Cube': cmds.polyCube,
    'Sphere': cmds.polySphere,
    'Cylinder': cmds.polyCylinder,
    'Cone': cmds.polyCone,
    'Torus': cmds.polyTorus
}


class Object:
    def __init__(self, object_type, object_transform=''):
        self.object_type = object_type
        self.object_transform = object_transform
        self.maya_object_transform = ''
        self.material_shading_node = ''
        self.material_shading_engine = ''

    def create(self):
        self._create_object()
        # self._create_annotation()
        self._add_attribute()
        self._set_attribute()
        self.get_translate()
        self._create_material()
        self.get_color()

    def _create_object(self):
        if self.object_type not in AllTypes:
            logging.warning('Create Object --> Object type is not valid')
            return

        object_creator = AllTypes[self.object_type]
        if not object_creator:
            logging.warning('Create Object --> Object Creator not found')
            return

        kwargs = {}
        if self.object_transform:
            kwargs['name'] = self.object_transform

        self.object_transform, _ = object_creator(**kwargs)

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
        # cmds.parent(self.locator_name, self.object_transform)

        # Create Annotation and set parent
        self.annotate_name = cmds.annotate(self.object_transform, tx=self.object_transform)
        # cmds.parent(self.annotate_name, self.locator_name)

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

    def get_color(self):
        if not cmds.objExists(self.object_transform):
            logging.warning('Get Color --> No surface exists')
            return

        if not cmds.objExists(self.material_shading_node):
            logging.warning('Get Color --> No Material Shading Node exists')
            return

        red, green, blue = cmds.getAttr(f'{self.material_shading_node}.color')[0]
        return red, green, blue

    def set_color(self, red=0, green=0, blue=0):
        if not self.material_shading_node:
            logging.warning('Set Color --> No material exists')
            return

        cmds.setAttr(self.material_shading_node + ".color", red, green, blue)
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

    def set_object_transform(self, new_object_transform):
        if not cmds.objExists(self.object_transform):
            logging.warning('Set Transform Name --> No surface exists')
            return self.object_transform

        self.object_transform = cmds.rename(self.object_transform, new_object_transform)
        return self.object_transform

    def set_translate_x(self, translate_x):
        if not cmds.objExists(self.object_transform):
            logging.warning('Set Translate X --> No surface exists')
            return

        cmds.setAttr(f'{self.object_transform}.tx', translate_x, edit=True)
        return translate_x

    def set_translate_y(self, translate_y):
        if not cmds.objExists(self.object_transform):
            logging.warning('Set Translate Y --> No surface exists')
            return

        cmds.setAttr(f'{self.object_transform}.ty', translate_y, edit=True)
        return translate_y

    def set_translate_z(self, translate_z):
        if not cmds.objExists(self.object_transform):
            logging.warning('Set Translate Z --> No surface exists')
            return

        cmds.setAttr(f'{self.object_transform}.tz', translate_z, edit=True)
        return translate_z


if __name__ == '__main__':
    object_instance = Object('Cube', 'my')
    object_instance.create()
    object_instance.select()
    object_instance.delete()
    object_instance.set_translate_x(5.4)
    object_instance.set_translate_y(5)
    object_instance.set_translate_z(5)
    object_instance.set_color(2, 2, 2)
