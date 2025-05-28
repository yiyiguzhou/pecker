# -*- coding: UTF-8 -*-

"""
File Name:      test.py
Author:         gufangmei_sx
Create Date:    2018/9/7
"""
import aircv as ac


class Test():
    def matchImg(imgsrc, imgobj, confidencevalue=0.5):  # imgsrc=原始图像，imgobj=待查找的图片
        imsrc = ac.imread(imgsrc)
        imobj = ac.imread(imgobj)

        match_result = ac.find_template(imsrc, imobj, confidencevalue)
        if match_result is not None:
            match_result['shape'] = (imsrc.shape[1], imsrc.shape[0])  # 0为高，1为宽

        # 匹配区域置黑
        start_y = match_result['rectangle'][0][0]
        start_x = match_result['rectangle'][0][1]
        end_y = match_result['rectangle'][2][0]
        end_x = match_result['rectangle'][1][1]
        for i in range(start_x, end_x):
            for j in range(start_y, end_y):
                imsrc[i, j, 0] = 255
                imsrc[i, j, 1] = 0
                imsrc[i, j, 2] = 0
        ac.show(imsrc)

        return match_result

    if __name__ == "__main__":

        src = "1.png"
        des = "1c.png"
        match_result = matchImg(src, des, confidencevalue=0.5)
        print(match_result)


