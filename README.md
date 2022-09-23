# Flood-Fill-Python
Make color fill for an image not only fill the same color pixels, but also make color fill for the similar color pixels


1. In line 13  img = cv2.imread("/Users/chriswang/Downloads/110-Zernike-2022-8-112.png") , change "/Users/chriswang/Downloads/110-Zernike-2022-8-112.png" to your image url.

2. In line 114  is_similar(start_color, matrix[x][y], 100, 100) , change the "100, 100" as your range that do the flood fill for similar color pixels. The first number is limit of smaller pixels and the second number is the limit of the bigger pixels.

3. In line 131 and 132, change x, y. This is the start position or start pixel. All the pixels will be compared with it to decide to do or not to do flood fill function.

4. Run the code.


