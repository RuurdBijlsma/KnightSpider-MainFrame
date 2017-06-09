import cv2
import numpy as np
from numpy.lib.stride_tricks import as_strided

# fd = open("pic.raw", "rb")
# rows = 1280
# cols = 960
# raw_data_map = np.fromfile(fd, dtype=np.dtype("u1"), count=rows*cols*24)
# # in case of a truncated frame at the end
# usable_bytes = raw_data_map.shape[0]-raw_data_map.shape[0]%24
#
# frames = int(usable_bytes/12)
# raw_bytes = raw_data_map[:usable_bytes]
#
# real_data = as_strided(raw_bytes.view(np.int32), strides=(12,3,), shape=(frames,4))
#
# im = real_data.reshape((cols, rows))

# fd = open('pic.raw', 'rb')
# rows = 720
# cols = 1280
# f = np.fromfile(fd, dtype=np.uint32,count=rows*cols)
# im = f.reshape((rows, cols)) #notice row, column format
# fd.close(\

with open("pic.raw", "rb") as fd:
    cols, rows = (720, 1280)
    buffer = np.fromfile(fd, dtype=np.int32, count=cols*rows)

    im = buffer.reshape((cols, rows))

    cv2.imshow("Hello", im)
    cv2.waitKey()
    cv2.destroyAllWindows()
