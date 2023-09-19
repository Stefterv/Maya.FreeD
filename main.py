import maya.api.OpenMaya as om
import sys

if sys.modules.get('FreeDListener') is not None:
    del sys.modules['FreeDListener']
if sys.modules.get('FreeDPacket') is not None:
    del sys.modules['FreeDPacket']

from FreeDListener import FreeDListener

def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass

# Initialize the plug-in
def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    global listener
    listener = FreeDListener("0.0.0.0", 40000)


def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    global listener
    listener.stop()


