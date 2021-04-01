import cv2
import numpy as np

class ImageProc:
    def __init__(self):
        pass

    def LoadImage(self, filename):
        global input_image
        global img_height, img_width
        input_image = cv2.imread(filename, 0)
        img_height, img_width = input_image.shape[:2]
        return input_image
    
    def Binarization(self, input_image, th):
        global bin_image
        _, bin_image = cv2.threshold(input_image, th, 255, cv2.THRESH_BINARY)
        return bin_image

    def getContours_xyz(self, bin_img, z_pos, epsilon_rate=0.0001, err_permission=15):
        global contours_coordination
        contours, _ = cv2.findContours(bin_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_coordination = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < err_permission:
                continue
            else:
                x = cnt[:,:,0][:,0].tolist()
                y = cnt[:,:,1][:,0].tolist()
                z = np.full_like(x, z_pos).tolist()
                contours_coordination.append([x, y, z])
        return contours_coordination

    def getContoursPlotImage(self, input_image, cnt_coordination):
        rgb_img = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
        for cnt in cnt_coordination:
            cnt = np.array(cnt)
            poly = []
            for i in range(len(cnt)):
                x, y = cnt[:,i][0], cnt[:,i][1]
                #poly.append(tuple(cnt[:,i][:2]))
                poly.append([x, y])
            poly = np.array(poly, dtype=np.int32).reshape((-1,1,2))
            rgb_img = cv2.polylines(rgb_img, [poly], True, (255, 0, 0))
        return rgb_img

if __name__=="__main__":
    ip = ImageProc()
    gry_img = ip.LoadImage("C:/Users/ryota/Desktop/MRI_dataset/subject01/pose01/subject01.pose01.slice0156.png")
    bin_img = ip.Binarization(gry_img, 15)
    contours = ip.getContours_xyz(bin_image, 0)
    #print(contours)
    ploted_img = ip.getContoursPlotImage(bin_img, contours)

    cv2.imshow("img", ploted_img)
    cv2.waitKey(0)