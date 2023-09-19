import socket
import threading
import maya.api.OpenMaya as om
import maya.utils as utils
import math
from FreeDPacket import FreeDPacket

class FreeDListener:
    def __init__(self, host, port):
        self.active = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((host, port))
        print("Socket created at " + host + ":" + str(port))
        self.thread = threading.Thread(target=self.listen, args=())
        self.thread.start()
    
    def stop(self):
        self.active = False
        self.socket.close()

    def listen(self):
        while self.active:
            data, addr = self.socket.recvfrom(1024) 

            packet = FreeDPacket.decode(bytearray(data))            
            utils.executeDeferred(self.update, packet)

    def update(self, packet):
        name = "FreeDCamera"+str(packet.id)
        camera = None
        object = None

        try:
            existing = om.MSelectionList()
            existing.add(name+"_Camera")

            object = existing.getDependNode(0)
            camera = om.MFnCamera(object)
        except:
            camera = om.MFnCamera()
            object = camera.create()


        camera.setName(name+"_Camera")
        transform = om.MFnTransform(camera.parent(0))
        transform.setName(name)

        transform.setTranslation(om.MVector(packet.posZ / 100, packet.posY / 100, -packet.posX / 100), om.MSpace.kTransform)

        rotation = om.MEulerRotation(packet.yaw / 180 * math.pi, -packet.pitch / 180 * math.pi, -packet.roll / 180 * math.pi, om.MEulerRotation.kZXY)

        transform.setRotation(rotation, om.MSpace.kTransform)