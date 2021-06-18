import glob, os, re, time
from PIL import Image

# filepaths
fp_in = "*.png"
fp_out = ".gif"

out_dir = "output"
video_dir = "videos/"
time_format = "%-I.%M.%S %p"

#creates a gif, given an array of file paths to add
def add_images(image_ar, filename, prev_files, num_frames):
	print('adding images... ', num_frames - len(image_ar) + 1, 'to', num_frames, '(' + str(len(image_ar)) + ' frames)')
	item_start_time = time.time()
	if (len(prev_files) == 0):
		# if oldname == '':
		img, *imgs = [Image.open(f) for f in image_ar]
	else:
		img = Image.open(prev_files[0])
		imgs = [Image.open(f) for f in image_ar]

	if (len(prev_files) > 1):
		# remove the file before the last
		os.remove(prev_files.pop())

	# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
	img.save(fp=filename, format='GIF', append_images=imgs, save_all=True, duration=150, loop=0)

	chunk_time = time.time() - item_start_time
	if (chunk_time > 60):
		print(len(image_ar),'frames saved to', filename, 'in', round((chunk_time)/60, 2), 'minutes')
	else:
		print(len(image_ar),'frames saved to', filename, 'in', round(chunk_time), 'seconds')

# returns an array of chunks of the array of size n
def chunk_using_generators(image_ar, n):
	for i in range(0, len(image_ar), n):
		yield image_ar[i:i + n]

#used to get total run time at the end
main_start_time = time.time()
main_start_localtime = time.localtime()

print('started', time.strftime(time_format, main_start_localtime))
directory_contents = glob.glob(out_dir+"/*/") # os.listdir(out_dir)
# Filter for directories
for item in directory_contents:
	if os.path.isdir(item):
			site_name = re.sub("/$", "", re.sub("^output/", "", item))

			location_start_time = time.time()
			filename = video_dir+re.sub("/$", "", re.sub("^output/", "", item)) #name it the same as the directory
			if os.path.exists(filename):
				# delete the old file to make room for it
				os.remove(filename)
			image_ar = sorted(glob.glob(item+fp_in))
			print('processing '+site_name+' with', len(image_ar), 'total frames')

			num_frames = 0
			prev_files = []
			# use a generator to split it into chunks and add the images
			for chunk in chunk_using_generators(image_ar, 400):
				num_frames += len(chunk)
				add_images(chunk, filename+str(num_frames)+fp_out, prev_files, num_frames)

				#save the filename so we can remove it later once the next one gets created
				prev_files.insert(0, filename+str(num_frames)+fp_out)
				lastFile = filename+str(num_frames)+fp_out
				if (num_frames > 2399): # it looks like it crashes above 2400
					break

			# remove the unnecessary intermediary file
			if (len(prev_files) > 1):
				os.remove(prev_files.pop())

			print(site_name, 'processed in ', round(time.time() - location_start_time), 'seconds\n')

total_time = round(time.time() - main_start_time)
if (total_time > 60):
	print('finished', time.strftime(time_format, main_start_localtime), 'in', round(total_time/60, 2), 'minutes')
else:
	print('finished', time.strftime(time_format, main_start_localtime), 'in', round(total_time), 'seconds')
