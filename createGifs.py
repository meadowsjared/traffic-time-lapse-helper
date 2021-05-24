import glob, os, re, time, gc
from PIL import Image

# filepaths
fp_in = "*.png"
fp_out = ".gif"

out_dir = "output"
video_dir = "videos/"

def add_images(image_ar, filename):
	print('image_ar')
	if os.path.exists(filename):
		img = Image.open(filename)
		imgs = [Image.open(f) for f in image_ar]
	else:
		img, *imgs = [Image.open(f) for f in image_ar]
	
	# print('img, *imgs', img.info)
	# print(gc.get_count())
	# gc.collect()
	# print(gc.get_count())
	img.save(fp=filename, format='GIF', append_images=imgs, save_all=True, duration=150, loop=0)
	# print('img.save')
	# img.close()
	# imgs.clear()
	# time.sleep(1)
	print(len(image_ar),'frames saved to', filename, 'in', round(time.time() - item_start_time), 'seconds')

def chunk_using_generators(image_ar, filename, n):
	for i in range(0, len(image_ar), n):
		yield image_ar[i:i + n]
	# def chunks(image_ar, filename):
	# 	print(image_ar)
	print(len(image_ar),'frames saved to', filename, 'in', round(time.time() - item_start_time), 'seconds')

directory_contents = glob.glob(out_dir+"/*/") # os.listdir(out_dir)
current_time = time.localtime()
print('started', time.strftime("%-I.%M.%S %p", current_time))
# Filter for directories
for item in directory_contents:
	if os.path.isdir(item):
		item_start_time = time.time()
		# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
		filename = video_dir+re.sub("/$", "", re.sub("^output/", "", item))+fp_out #name it the same as the directory
		if os.path.exists(filename):
			# delete it
			os.remove(filename)
		print('processing '+re.sub("/$", "", item)+'...')
		image_ar = sorted(glob.glob(item+fp_in))
		# add_images(image_ar)
		# use a generator to split it into chunks and add the images
		i = 0
		for chunk in chunk_using_generators(image_ar, filename, 100):
			print('len(chunk)', len(chunk))
			add_images(chunk, filename)
		# print(list(chunk_using_generators(image_ar, filename, 10)))
print('finished', time.strftime("%-I.%M.%S %p", current_time))

