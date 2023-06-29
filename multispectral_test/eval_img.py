import cv2

img = cv2.imread("C:\\Users\\matt\\Documents\\GitHub\\New-ortho\\tlt\\code\\odm_orthophoto\\odm_orthophoto.tif", cv2.IMREAD_UNCHANGED)

# get dimensions of image
dimensions = img.shape
 
# height, width, number of channels in image
height = img.shape[0]
width = img.shape[1]
channels = img.shape[2]
 
print('Image Dimension    : ',dimensions)
print('Image Height       : ',height)
print('Image Width        : ',width)
print('Number of Channels : ',channels)

#import PIL.Image
#img = PIL.Image.open("C:\\Users\\matt\\Documents\\GitHub\\New-ortho\\tlt\\code\\images\\IMG_0000_4.tif")
#exif_data = img.getexif()
#exif = {
#    PIL.ExifTags.TAGS[k]: v
#    for k, v in img.getexif().items()
#    if k in PIL.ExifTags.TAGS
#}
#print(exif)