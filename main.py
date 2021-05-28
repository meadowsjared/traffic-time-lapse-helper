import os, time, threading#, json
from ImageHandler import ImageHandler

################################################################################
# configuration
screenshot_dir = 'screenshots'
output_dir = 'output'
width = 1920
height = 1080
image_type = 'png'
interval = 1
labels = [
		'Bakersfield',
		'SE Bakersfield',
		'Landco', 
		'Santa Fe Way', 
		'Shafter', 
		'Morning Drive',
		'Baker',
		'Olive',
	]
sites = [
		'https://www.google.com/maps/@35.385853,-119.0278613,14z/data=!5m1!1e1',
		'https://www.google.com/maps/@35.3615101,-118.9396787,15z/data=!5m1!1e1',
		'https://www.google.com/maps/@35.3833217,-119.06114,17z/data=!5m1!1e1',
		'https://www.google.com/maps/@35.4196532,-119.1724834,15z/data=!5m1!1e1',
		'https://www.google.com/maps/@35.5027193,-119.2747966,17z/data=!5m1!1e1',
		'https://www.google.com/maps/@35.3592089,-118.9138008,17z/data=!5m1!1e1',
		'https://www.google.com/maps/@35.3736062,-118.9963834,16.75z/data=!5m1!1e1',
		'https://www.google.com/maps/@35.4127418,-119.0493261,17.54z/data=!5m1!1e1',
	]


################################################################################
# screenshot/manipulation loop
def process_site(site, i, label='', process=True):
	global screenshot_dir, output_dir, width, height, image_type
	ih = ImageHandler()
	current_time = time.localtime()
	filename = '%s.png' % time.strftime("%Y-%m-%d %a %-I.%M.%S %p", current_time)
	if (label == ''):
		image_path = os.path.join(screenshot_dir, filename)
		out_file = os.path.join(output_dir, filename)
	else:
		image_path = os.path.join(screenshot_dir, label, filename)
		out_file = os.path.join(output_dir, label, '%s.png' % time.strftime(label + " %Y-%m-%d %a %H.%M.%S", current_time))
	stream = os.popen('node imageFromUrl.js \'{"url":"' + site + '","image_path":"' + image_path + '","type":"' + image_type + '","width":' + str(width) + ',"height":' + str(height) + '}\'')
	output = stream.read()
	# #used to read the results from imageFromUrl.js (useful for troubleshooting)
	# ret_obj = json.loads(output)
	# print('ret_obj', ret_obj['consoleMessages'])
	ih.process_image(label, image_path, out_file)

################################################################################
# program entrypoint
if __name__ == "__main__":
	starttime = time.time()
	index = 1
	while (1):
		print('\n'+time.strftime("%-I:%M:%S %p", time.localtime()))
		# launch each process in a separate thread
		for i in range(len(labels)):
			t = threading.Thread(target=process_site, args=(sites[i], index, labels[i]))
			t.start()
		# sleep just enough to fire at the same time each interval
		index += 1
		time.sleep((60.0 * interval) - ((time.time() - starttime) % (60.0 * interval)))
