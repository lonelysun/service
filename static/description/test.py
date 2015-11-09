from PIL import Image
import glob,os
size = 80,80
for infile in glob.glob("*.gif"):
	file,ext = os.path.splitext(infile)
	im = Image.open(infile)

	im.thumbnail(size,Image.ANTIALIAS)
	im.save(file + ".gif","GIF")
