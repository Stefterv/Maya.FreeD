import struct

class FreeDPacket:
    def __init__(self):
        self.id = 0
        self.pitch = 0.0
        self.yaw = 0.0
        self.roll = 0.0
        self.posZ = 0.0
        self.posX = 0.0
        self.posY = 0.0
        self.zoom = 0
        self.focus = 0

    @staticmethod
    def decode(data):
        tracking_data = FreeDPacket()
        tracking_data.id = data[1]
        tracking_data.pitch = FreeDPacket.get_rotation(data, 2)
        tracking_data.yaw = FreeDPacket.get_rotation(data, 5)
        tracking_data.roll = FreeDPacket.get_rotation(data, 8)
        tracking_data.posZ = FreeDPacket.get_position(data, 11)
        tracking_data.posX = FreeDPacket.get_position(data, 14)
        tracking_data.posY = FreeDPacket.get_position(data, 17)
        tracking_data.zoom = FreeDPacket.get_encoder(data, 20)
        tracking_data.focus = FreeDPacket.get_encoder(data, 23)
        return tracking_data

    def __str__(self):
        return (f"pitch: {self.pitch}, yaw: {self.yaw}, roll: {self.roll}, "
                f"posX: {self.posX}, posY: {self.posY}, posZ: {self.posZ}, "
                f"zoom: {self.zoom}, focus: {self.focus}")

    @staticmethod
    def encode(data):
        buffer = bytearray()
        buffer.append(0xD1)  # Identifier
        buffer.append(data.id)  # ID
        buffer.extend(FreeDPacket.set_rotation(data.pitch))
        buffer.extend(FreeDPacket.set_rotation(data.yaw))
        buffer.extend(FreeDPacket.set_rotation(data.roll))
        buffer.extend(FreeDPacket.set_position(data.posZ))
        buffer.extend(FreeDPacket.set_position(data.posX))
        buffer.extend(FreeDPacket.set_position(data.posY))
        buffer.extend(FreeDPacket.set_encoder(data.zoom))
        buffer.extend(FreeDPacket.set_encoder(data.focus))
        buffer.append(0x00)  # Reserved
        buffer.append(0x00)  # Reserved
        buffer.append(FreeDPacket.checksum(buffer))
        return bytes(buffer)

    @staticmethod
    def set_position(pos):
        position = int(pos * 64 * 256)
        data = struct.pack('>Q', position)
        return bytes([data[4], data[5], data[6]])

    @staticmethod
    def set_rotation(rot):
        rotation = int(rot * 32768 * 256)
        data = struct.pack('>Q', rotation)
        return bytes([data[4], data[5], data[6]])

    @staticmethod
    def set_encoder(enc):
        return struct.pack('>I', enc)

    @staticmethod
    def get_position(data, offset):
        value = (data[offset] << 24) | (data[offset + 1] << 16) | (data[offset + 2] << 8)
        return float(struct.unpack('>i', struct.pack('>I', value))[0]) / 64 / 256

    @staticmethod
    def get_rotation(data, offset):
        value = (data[offset] << 24) | (data[offset + 1] << 16) | (data[offset + 2] << 8)
        return float(struct.unpack('>i', struct.pack('>I', value))[0]) / 32768 / 256


    @staticmethod
    def get_encoder(data, offset):
        value = struct.unpack('>I', bytes([0x00, data[offset + 1], data[offset + 2], data[offset + 3]]))[0]
        return value

    @staticmethod
    def checksum(data):
        total = 64
        for byte in data[:-1]:
            total -= byte
        return total % 256