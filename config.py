BACKEND_URL = "http://100.89.179.5:5000/"  # arsb.balamserver.top
CAMERA_INDEX = 0
QR_CAMERA_PATH = "/dev/v4l/by-id/usb-Suyin_HD_Camera_200910120001-video-index0"
WASTE_CAMERA_PATH = "/dev/v4l/by-id/usb-Jieli_Technology_USB_Composite_Device-video-index1"

AI_MODEL_PATH = "ai/ars.pt"
CONFIDENCE_THRESHOLD = 0.60
STABLE_FRAMES = 5

SESSION_TIMEOUT=30

DETECTION_COOLDOWN = 5

ESP32_PORT = "/dev/ttyUSB0"
ESP32_BAUDRATE = 115200