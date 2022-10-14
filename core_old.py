# Maya Node Creator Core

class Visibility:
    Show = 1
    Hide = 0


class ObjectType:
    Cube = polyCube
    Sphere = polySphere
    Cylinder = polyCylinder
    Cone = polyCone
    Torus = polyTorus


class BaseNode:
    def __init__(self):
        self.node_name = ''
        self.node_transform = ''
        self.node_mesh = ''
        self.node_visibility = Visibility.Show


class Object(BaseNode):
    def __init__(self):
        super(Object, self).__init__()
        self.object_label = self.node_name
        self.object_type = ''
        self.object_tx = 0
        self.object_tz = 0
        self.object_ty = 0
        self.object_sx = 0
        self.object_sz = 0
        self.object_sy = 0


class Layer(BaseNode):
    def __init__(self):
        super(Layer, self).__init__()
        self.layer_name = self.node_name

    def create_layer(self):
        pass


class Group(BaseNode):
    def __init__(self):
        super(Group, self).__init__()
        self.group_name = self.node_name

    def create_group(self):
        pass


class Material(BaseNode):
    def __init__(self):
        super(Material, self).__init__()
        self.material_shadingNode = ''
        self.material_shadingEngine = ''
        self.material_color = []

    def create_material(self):
        pass

    def assign_material(self):
        pass


# Coming Soon
class Exporter(BaseNode):
    def __init__(self):
        super(Exporter, self).__init__()
        pass
