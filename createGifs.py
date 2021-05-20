import glob, os, re
from PIL import Image

# filepaths
fp_in = "*.png"
fp_out = ".gif"

out_dir = "output"
video_dir = "videos/"

directory_contents = glob.glob(out_dir+"/*/") # os.listdir(out_dir)

# Filter for directories
for item in directory_contents:
	if os.path.isdir(item):
		# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
		filename = re.sub("/$", "", re.sub("^output/", "", item)) #name it the same as the directory
		print('processing '+re.sub("/$", "", item)+'...')
		image_ar = sorted(glob.glob(item+fp_in))
		img, *imgs = [Image.open(f) for f in image_ar]
		img.save(fp=video_dir+filename+fp_out, format='GIF', append_images=imgs, save_all=True, duration=300, loop=0)
		print(len(image_ar),'frames saved to', video_dir+filename+fp_out)
