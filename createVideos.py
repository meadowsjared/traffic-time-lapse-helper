import glob, os, re, time, cv2
from PIL import Image

# filepaths
fp_in = "*.png"
fp_out = ".np4"

out_dir = "output"
video_dir = "videos/"
time_format = "%-I.%M.%S %p"

# returns an array of chunks of the array of size n
def chunk_using_generators(image_ar, n):
	for i in range(0, len(image_ar), n):
		yield image_ar[i:i + n]

#creates a mp4 file, given an array of image file paths to add
def create_video(image_ar, width, height, vid_filename):
	print('adding images... ', len(image_ar), 'frames at ('+str(width)+'x'+str(height)+')')
	item_start_time = time.time()

	# choose codec according to format needed
	# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	fourcc = cv2.VideoWriter_fourcc('F','M','P','4')
	video = cv2.VideoWriter(vid_filename, fourcc, 20.0, (width,height))

	num_frames = 0
	for file_path in image_ar:
		num_frames += 1
		img = cv2.imread(file_path)
		print(file_path)
		video.write(img)
		if (num_frames > 5):
			break

	video.release()
	cv2.destroyAllWindows()

	file_exists = os.path.isfile(vid_filename)
	if (file_exists):
		print('file_exists = true')
	else:
		print('file_exists = false')

	chunk_time = time.time() - item_start_time
	if (chunk_time > 60):
		print(len(image_ar),'frames saved to', vid_filename, 'in', round((chunk_time)/60, 2), 'minutes')
	else:
		print(len(image_ar),'frames saved to', vid_filename, 'in', round(chunk_time), 'seconds')


#used to get total run time at the end
main_start_time = time.time()
main_start_localtime = time.localtime()

print('started', time.strftime(time_format, main_start_localtime))
directory_contents = glob.glob(out_dir+"/*/") # os.listdir(out_dir)
# Filter for directories
for item in directory_contents:
	if os.path.isdir(item):
			location_start_time = time.time()
			filename = video_dir+re.sub("/$", "", re.sub("^output/", "", item)) #name it the same as the directory
			if os.path.exists(filename):
				# delete the old file to make room for it
				os.remove(filename)
			image_ar = sorted(glob.glob(item+fp_in))
			site_name = re.sub("/$", "", re.sub("^output/", "", item))
			print('processing '+site_name+' with', len(image_ar), 'total frames')

			if len(image_ar) > 0:
				im = Image.open(image_ar[0])
				width, height = im.size
				im.close()
				create_video(image_ar, width, height, filename+'_'+str(len(image_ar))+fp_out)

			print(site_name, 'processed in ', round(time.time() - location_start_time), 'seconds\n')

total_time = round(time.time() - main_start_time)
if (total_time > 60):
	print('finished', time.strftime(time_format, main_start_localtime), 'in', round(total_time/60, 2), 'minutes')
else:
	print('finished', time.strftime(time_format, main_start_localtime), 'in', round(total_time), 'seconds')
