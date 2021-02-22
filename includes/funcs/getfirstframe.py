from cv2 import VideoCapture,imwrite,imread
from os import getcwd
from .appIcons import Icons

def getFirstFrame(videoFile,id):
    id = str(id)
    vidcap = VideoCapture(videoFile)
    success, image = vidcap.read()
    if success:
        imwrite(getcwd() + "\\WhatsAppGui\\fFrame{}.jpg".format(id),image)

    l_img = imread(getcwd() + "\\WhatsAppGui\\fFrame{}.jpg".format(id))
    s_img = imread(Icons["Play"], -1)

    y_offset ,x_offset, _ = l_img.shape
    sy, sx, _ = s_img.shape

    x_offset = x_offset // 2 - sx // 2
    y_offset = y_offset // 2 - sy // 2

    y1, y2 = y_offset, y_offset + s_img.shape[0]
    x1, x2 = x_offset, x_offset + s_img.shape[1]

    alpha_s = s_img[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        l_img[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] +
                                alpha_l * l_img[y1:y2, x1:x2, c])
    
    imwrite(getcwd() + "\\WhatsAppGui\\fFrame{}.jpg".format(id),l_img)