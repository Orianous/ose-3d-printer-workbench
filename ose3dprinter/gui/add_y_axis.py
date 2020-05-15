from ose3dprinter.app.enums import AxisOrientation

from .handle_add_axis_command_activation import \
    handle_add_axis_command_activation
from .icon import get_icon_path


class AddYAxis:
    """
    Command to add Y Axis object.
    """

    NAME = 'AddYAxis'

    def Activated(self):
        handle_add_axis_command_activation(AxisOrientation.Y)

    def IsActive(self):
        return True

    def GetResources(self):
        return {
            'Pixmap': get_icon_path('YAxis.svg'),
            'MenuText': 'Add Y Axis',
            'ToolTip': 'Add Y Axis'
        }
