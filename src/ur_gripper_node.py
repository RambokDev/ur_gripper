#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import serial
import time
import binascii


def activateGripper(serial_device):
    print('ici')
    serial_device.write(b"\x09\x10\x03\xE8\x00\x03\x06\x00\x00\x00\x00\x00\x00\x73\x30")
    data_raw = serial_device.readline()
    print(data_raw)
    data = binascii.hexlify(data_raw)
    print("Response", data, '\n')
    time.sleep(0.01)
    serial_device.write(b"\x09\x03\x07\xD0\x00\x01\x85\xCF")
    data_raw = serial_device.readline()
    print(data_raw)
    data = binascii.hexlify(data_raw)
    print("Response", data)
    time.sleep(1)


def closeGripper(serial_device):
    print("Close gripper", '\n')
    serial_device.write(b"\x09\x10\x03\xE8\x00\x03\x06\x09\x00\x00\xFF\xFF\xFF\x42\x29")
    data_raw = serial_device.readline()
    print(data_raw)
    data = binascii.hexlify(data_raw)
    print("Response", data, '\n')
    time.sleep(2)


def openGripper(serial_device):
    print("Open gripper \n")
    serial_device.write(b"\x09\x10\x03\xE8\x00\x03\x06\x09\x00\x00\x00\xFF\xFF\x72\x19")
    data_raw = serial_device.readline()
    print(data_raw)
    data = binascii.hexlify(data_raw)
    print("Response", data, '\n')
    time.sleep(2)


def callback(data, ser):

    if data.data == "open":
        openGripper(ser)
        rospy.loginfo(rospy.get_caller_id() + "success %s", data.data)
    else:
        closeGripper(ser)
        rospy.loginfo(rospy.get_caller_id() + "success %s", data.data)


def listener():
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=1, parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
    activateGripper(ser)

    rospy.init_node('listener', anonymous=True)
    callback_lambda = lambda x: callback(x, ser)

    rospy.Subscriber("chatter", String, callback_lambda)

    rospy.spin()


if __name__ == '__main__':
    listener()
