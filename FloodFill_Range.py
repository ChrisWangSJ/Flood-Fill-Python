import numpy as np
import cv2
import sys
import math

#np.seterr(over='ignore')
sys.setrecursionlimit(1500000)
circle_solidity_reference = 4 * math.pi

if __name__ == '__main__':
    # Read an image

    img = cv2.imread("/Users/chriswang/Downloads/110-Zernike-2022-8-112.png")
    img_1 = img.copy()
    cv2.imshow("Test", img)

    # Simple Thresholding
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img_binarized = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

    # Find contours
    cnts, _ = cv2.findContours(img_binarized, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    count = 0
    contour_mask = np.zeros(img_binarized.shape, dtype="uint8")
    areas = []
    contour_perimeters = []
    contour_perimeter_squareds = []
    contour_solidity_0s = []
    contour_solidity_1s = []
    contour_solidity_distances = []
    for cnt in cnts:
        # Calculate bounding box components
        x, y, w, h = cv2.boundingRect(cnt)
        # Contour area
        area = cv2.contourArea(cnt)
        areas.append(area)
        # Contour perimeters
        contour_perimeter = cv2.arcLength(cnt, True)
        contour_perimeters.append(contour_perimeter)
        # perimeter squared
        contour_perimeter_squared = contour_perimeter * contour_perimeter
        contour_perimeter_squareds.append(contour_perimeter_squared)
        # Contour solidity (P^2)
        contour_solidity_0 = contour_perimeter / area if int(area) != 0 else 0
        contour_solidity_0s.append(contour_solidity_0)
        contour_solidity_1 = contour_perimeter_squared / area if int(area) != 0 else 0
        contour_solidity_1s.append(contour_solidity_1)

        # Calculate the solidity distance from 4 pi
        contour_solidity_distance = abs(circle_solidity_reference - contour_solidity_1)
        contour_solidity_distances.append(contour_solidity_distance)

        # Display each contour
        current_contour_mask = np.zeros(img_binarized.shape, dtype="uint8")
        cv2.drawContours(current_contour_mask, [cnt], -1, 255, -1)
        cv2.imshow("contour {:}".format(count), current_contour_mask)
        # Print solidity for each contour
        print("contour {:} has solidity(P^2/A) = {:.1f}".format(count, contour_solidity_1))
        print("contour {:} has distance from 4pi = {:.1f}".format(count, contour_solidity_distance))
        print("contour {:} has perimeter = {:.1f}".format(count, contour_perimeter))
        print("contour {:} has perimeter^2 = {:.1f}".format(count, contour_perimeter_squared))
        print("contour {:} has area = {:.1f}".format(count, area))
        print("contour {:} has solidity(P/A) = {:.1f}".format(count, contour_solidity_0))
        count += 1
        # Draw bounding box on the last result output
        cv2.rectangle(img_1, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw the rectangle

    cv2.imshow("Bbox", img_1)

    # Print average value for all solidity parameters
    print("contour average has solidity(P^2/A) = {:.1f}".format(np.mean(contour_solidity_1s)))
    print("contour average has avg distance from 4pi = {:.1f}".format(np.mean(contour_solidity_distances)))
    print("contour average has avg perimeter = {:.1f}".format(np.mean(contour_perimeters)))
    print("contour average has avg perimeter^2 = {:.1f}".format(np.mean(contour_perimeter_squareds)))
    print("contour average has avg area = {:.1f}".format(np.mean(areas)))
    print("contour average has avg solidity(P/A) = {:.1f}".format(np.mean(contour_solidity_0s)))


    def isEqual(data1, data2):
        if (data1[0] != data2[0]):
            return False
        elif (data1[1] != data2[1]):
            return False
        elif (data1[2] != data2[2]):
            return False
        else:
            return True


    def is_similar(start_color, new_color, upper_color_range, lower_color_range):
        #threshold = 20

        #red, green, blue = start_color
        redUpper = start_color[0] + upper_color_range
        greenUpper = start_color[1] + upper_color_range
        blueUpper  = start_color[2] + upper_color_range
        redLower = start_color[0] - lower_color_range
        greenLower= start_color[1] - lower_color_range
        blueLower = start_color[2] - lower_color_range
        new_red, new_green, new_blue = new_color
        if redLower <= new_red <= redUpper and greenLower <= new_green <= greenUpper and blueLower <= new_blue <= blueUpper:
            return True
        return False

    def flood_recursive_image(matrix):
        width = len(matrix)
        height = len(matrix[0])

        def fill(x, y, start_color, color_to_update):
            # if the square is not the same color as the starting point

            #if isEqual(matrix[x][y], start_color) == False:
            if is_similar(start_color, matrix[x][y], 100, 100) == False:
                return
            # if the square is not the new color
            elif isEqual(matrix[x][y], color_to_update) == True:
                return
            else:
                # update the color of the current square to the replacement color
                matrix[x][y] = color_to_update
                neighbors = [(x - 1, y), (x + 1, y), (x - 1, y - 1), (x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1),
                             (x, y - 1), (x, y + 1)]
                for n in neighbors:
                    if 0 <= n[0] <= width - 1 and 0 <= n[1] <= height - 1:
                        fill(n[0], n[1], start_color, color_to_update)

        # start_x = random.randint(0,width-1)
        # start_y = random.randint(0,height-1)

        start_x = 20
        start_y = 10
        start_color = matrix[start_x][start_y].copy()
        fill(start_x, start_y, start_color, [0, 0, 255])
        return matrix


    resultArray = flood_recursive_image(img)




    cv2.imshow("FloodFill", resultArray)
    key = cv2.waitKey(-1) & 0xFF




    cv2.waitKey(0)
    cv2.destroyAllWindows()