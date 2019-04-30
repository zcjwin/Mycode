import cv2
import pytesseract

def process_capimg():
    filepath = './image/img/captcha.png'
    captcha_image = cv2.imread(filepath)
    gray_image = cv2.cvtColor(captcha_image,cv2.COLOR_BGR2GRAY)
    # 二值化
    # ret,binary_image = cv2.threshold(1gray_image,127,255,cv2.THRESH_BINARY_INV)
    binary_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 1)
    # 高斯模糊处理
    image_blur = cv2.GaussianBlur(binary_image, (5, 5), 0)
    # kernel = 1/16*np.array([[1,2,1], [2,4,2], [1,2,1]])
    # image_blur = cv2.filter2D(ii,-1,kernel)
    ret, image_res = cv2.threshold(image_blur, 127, 255, cv2.THRESH_BINARY)
    # 去干扰线
    h, w = image_res.shape[:2]
    for y in range(1, w - 1):
        for x in range(1, h - 1):
            count = 0
            if image_res[x, y - 1] > 245:
                count = count + 1
            if image_res[x, y + 1] > 245:
                count = count + 1
            if image_res[x - 1, y] > 245:
                count = count + 1
            if image_res[x + 1, y] > 245:
                count = count + 1
            if count > 2:
                image_res[x, y] = 255
    interference_point(image_res)
def interference_point(image_res,x = 0,y = 0):
    # 点降噪
    cur_pixel = image_res[x, y] # 当前像素点的值
    height, width = image_res.shape[:2]
    for y in range(0, width - 1):
        for x in range(0,height - 1):
            if y == 0:  # 第一行
                if x == 0:
                    sum = int(cur_pixel) + int(image_res[x, y + 1]) \
                          + int(image_res[x + 1, y]) \
                          + int(image_res[x + 1, y + 1])
                    if sum <= 2 * 245:
                        image_res[x, y] = 0
                elif x == height - 1: # 右上顶点
                    sum = int(cur_pixel) + int(image_res[x, y + 1]) \
                          + int(image_res[x - 1, y]) \
                          + int(image_res[x - 1, y + 1])
                    if sum <= 2 * 245:
                        image_res[x, y] = 0
                else:   # 最上非顶点区域
                    sum = int(image_res[x - 1, y]) \
                          + int(image_res[x - 1, y + 1]) \
                          + int(cur_pixel) \
                          + int(image_res[x, y + 1]) \
                          + int(image_res[x + 1, y]) \
                          + int(image_res[x + 1, y + 1])
                    if sum <= 3 * 245:
                        image_res[x, y] = 0
            elif y == width - 1:    # 最下面一行
                if x == 0: # 左下顶点
                    sum = int(cur_pixel) + int(image_res[x + 1, y]) \
                          + int(image_res[x + 1, y - 1]) \
                          + int(image_res[x, y - 1])
                    if sum <= 2 * 245:
                        image_res[x, y] = 0
                elif x == height - 1:   # 右下顶点
                    sum = int(cur_pixel) + int(image_res[x, y - 1]) \
                          + int(image_res[x - 1, y]) \
                          + int(image_res[x - 1, y - 1])
                    if sum <= 2 * 245:
                        image_res[x, y] = 0
                else:   # 最下不是顶点
                    sum = int(cur_pixel) + int(image_res[x - 1, y]) + int(image_res[x - 1, y]) \
                          + int(image_res[x - 1, y - 1]) + int(image_res[x + 1, y - 1])
                    if sum <= 3 * 245:
                        image_res[x, y] = 0
            else:   # y不在边界
                if x == 0:
                    sum = int(image_res[x, y - 1]) + int(cur_pixel) + int(image_res[x, y - 1]) \
                          + int(image_res[x + 1, y - 1]) + int(image_res[x + 1, y]) + int(image_res[x + 1, y + 1])
                    if sum <= 3 * 245:
                        image_res[x, y] = 0
                elif x == height - 1:   # 右边非顶点
                    sum = int(image_res[x, y - 1]) + int(cur_pixel) + int(image_res[x, y + 1]) \
                          + int(image_res[x - 1, y - 1]) + int(image_res[x - 1, y]) + int(image_res[x - 1, y + 1])
                    if sum <= 3 * 245:
                        image_res[x, y] = 0
                else:   # 具备9领域条件的
                    sum = int(image_res[x - 1, y - 1]) + int(image_res[x - 1, y]) \
                          + int(image_res[x - 1, y + 1]) + int(image_res[x, y - 1]) \
                          + int(cur_pixel) + int(image_res[x, y + 1]) \
                          + int(image_res[x + 1, y - 1]) + int(image_res[x + 1, y]) + int(image_res[x + 1, y + 1])
                    if sum <= 4 * 245:
                        image_res[x, y] = 0
    cv2.imwrite(r'image\capimg\procapimg.png',image_res)
    # image = cv2.imread(r'image\capimg\procapimg.png')
    # result = pytesseract.image_to_string(image)
    # print(result)

    # cv2.namedWindow("capimg",cv2.WINDOW_NORMAL)
    # cv2.imshow("capimg",image_res)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
# for i in range(5):
#     process_capimg()
# image = cv2.imread(r'image\capimg\procapimg.png')
# result = pytesseract.image_to_string(image)
# print(result)
#
# cv2.namedWindow("capimg", cv2.WINDOW_NORMAL)
# cv2.imshow("capimg", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
