import os
import ctypes

TIME_OUT = 60
DIR = os.path.dirname(__file__)
LIB_PATH = os.path.join(DIR, 'lib/FPModule_SDK.dll')
FP_LIB = ctypes.CDLL(LIB_PATH)

def start_detection_flow():
    if not open_device():
        raise ('Unable to access fingerprint device')

    if not is_finger_detected():
        raise ('Finger is not inserted in device')
    
    return get_finger_print_token(capture_image())

def open_device():
    return FP_LIB.FPModule_OpenDevice()

def close_device():
    return FP_LIB.FPModule_CloseDevice()

def capture_image():
    pdwWidth = ctypes.pointer(ctypes.c_int())
    pdwHeight = ctypes.pointer(ctypes.c_int())
    pbyImageData = (ctypes.c_ubyte * (90*1024))()
    FP_LIB.FPModule_CaptureImage(pbyImageData, pdwWidth, pdwHeight)
    return bytes(pbyImageData)

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

def get_finger_print_token(img_data):
    return hash(img_data)

if __name__ == '__main__':
    print(get_sdk_version())
    print(get_device_info())
    print(start_detection_flow())
