# Maya Node Creator Core

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
        self.material_shading_node = ''
        self.material_shading_engine = ''

    def create(self):
        self._create_object()
        self._create_material()
        self._create_annotation()

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
        cmds.parent(self.locator_name, self.object_transform)

        # Create Annotation and set parent
        self.annotate_name = cmds.annotate(self.object_transform, tx=self.object_transform)
        cmds.parent(self.annotate_name, self.locator_name, shape=True)

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

    def move(self, tx=0, tz=0, ty=0):
        if not cmds.objExists(self.object_transform):
            logging.warning('Move Object --> No surface exists')
            return

        cmds.setAttr(f'{self.object_transform}.translate', tx, tz, ty, edit=True, type="double3")

    def set_color(self, r=0, g=0, b=0):
        if not self.material_shading_node:
            logging.warning('Set Color --> No material exists')
            return

        cmds.setAttr(self.material_shading_node + ".color", r, g, b)


if __name__ == '__main__':
    object_instance = Object('Cube', 'my')
    object_instance.create()
    object_instance.select()
    object_instance.delete()
    object_instance.move(5, 5, 5)
    object_instance.set_color(2, 2, 2)
