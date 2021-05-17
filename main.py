import os, time#, json
from ImageHandler import ImageHandler

################################################################################
# configuration
screenshot_dir = 'screenshots'
temp_dir = 'temp'
output_dir = 'output'
width = 1920
height = 1080
image_type = 'png'
label = 'Atlanta Traffic'

################################################################################
# screenshot/manipulation loop
def recur(site, interval, process=True):
	i = 1
	ih = ImageHandler()

	print('starting process...')
	while (1):
		current_time = time.localtime()
		filename = '%s.png' % time.strftime("%H-%M-%S", current_time)
		image_path = os.path.join(screenshot_dir, filename)
		stream = os.popen('node imageFromUrl.js \'{"url":"' + site + '","image_path":"' + image_path + '","type":"' + image_type + '","width":' + str(width) + ',"height":' + str(height) + '}\'')
		output = stream.read()
		# #used to read the results from imageFromUrl.js (useful for troubleshooting)
		# ret_obj = json.loads(output)
		# print('ret_obj', ret_obj['consoleMessages'])

		out_file = os.path.join(output_dir, '%04d.png' % i)
		ih.process_image(label, image_path, out_file)
		i += 1
		time.sleep(round(60 * interval))

################################################################################
# program entrypoint
if __name__ == "__main__":
	site = 'https://www.google.com/maps/@33.7676338,-84.5606888,11z/data=!5m1!1e1'
	interval = 15
	recur(site, interval)