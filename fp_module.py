import os
import io
import ctypes
import fingerprints
import imagehash
from PIL import Image

TIME_OUT = 60
DIR = os.path.dirname(__file__)
LIB_PATH = os.path.join(DIR, 'lib/FPModule_SDK.dll')
TEMP_FOLDER = os.path.join(DIR, 'temp')
TEMP_IMAGE = '%s/temp_image.jpeg' % TEMP_FOLDER
FP_LIB = ctypes.CDLL(LIB_PATH)

def start_detection_flow():
    if not open_device():
        raise Exception('Unable to access fingerprint device')

    if not is_finger_detected():
        raise Exception('Finger is not inserted in device')
    return capture_image()

def open_device():
    return FP_LIB.FPModule_OpenDevice() == 0

def close_device():
    return FP_LIB.FPModule_CloseDevice() == 0

def capture_image():
    pdwWidth = ctypes.pointer(ctypes.c_int())
    pdwHeight = ctypes.pointer(ctypes.c_int())
    pbyImageData = (ctypes.c_char * (3024*3024))()
    FP_LIB.FPModule_CaptureImage(pbyImageData, pdwWidth, pdwHeight)
    return { 
        "raw" : bytes(pbyImageData), 
        "size": (pdwWidth.contents.value, pdwHeight.contents.value)
    } 

def is_finger_detected():
    pdwStatus = ctypes.pointer(ctypes.c_long())
    FP_LIB.FPModule_DetectFinger.argtypes = [ctypes.POINTER(ctypes.c_long)]
    FP_LIB.FPModule_DetectFinger(pdwStatus)
    return pdwStatus.contents.value == 1

def get_sdk_version():
    pbySdkInfo = (ctypes.c_ubyte * 64)()
    FP_LIB.FPModule_GetSDKVersion(pbySdkInfo)
    return bytes(pbySdkInfo).decode('ascii')

def get_device_info():
    pbyDeviceInfo = (ctypes.c_ubyte * 64)()
    FP_LIB.FPModule_GetDeviceInfo(pbyDeviceInfo)
    return bytes(pbyDeviceInfo).decode('ascii')

def save_temp_image(byte_image, imgsize):
    image = Image.frombytes('L', imgsize, byte_image, 'raw')
    image.save(TEMP_IMAGE)
    return image

def get_temp_image_hash():
    return imagehash.average_hash(Image.open(TEMP_IMAGE))

if __name__ == '__main__':
    print(get_sdk_version())