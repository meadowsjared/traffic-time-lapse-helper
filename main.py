import os, time, threading#, json
from ImageHandler import ImageHandler

################################################################################
# configuration
screenshot_dir = 'screenshots'
output_dir = 'output'
width = 1920
height = 1080
image_type = 'png'

################################################################################
# screenshot/manipulation loop
def recur(site, interval, label='', process=True):
	global screenshot_dir, output_dir, width, height, image_type
	i = 1
	ih = ImageHandler()

	print('starting process...')
	while (1):
		current_time = time.localtime()
		filename = '%s.png' % time.strftime("%H-%M-%S", current_time)
		if (label == ''):
			image_path = os.path.join(screenshot_dir, filename)
		else:
			image_path = os.path.join(screenshot_dir, label, filename)

		stream = os.popen('node imageFromUrl.js \'{"url":"' + site + '","image_path":"' + image_path + '","type":"' + image_type + '","width":' + str(width) + ',"height":' + str(height) + '}\'')
		output = stream.read()
		# #used to read the results from imageFromUrl.js (useful for troubleshooting)
		# ret_obj = json.loads(output)
		# print('ret_obj', ret_obj['consoleMessages'])
		if (label == ''):
			out_file = os.path.join(output_dir, '%04d.png' % i)
		else:
			out_file = os.path.join(output_dir, label, '%04d.png' % i)
		ih.process_image(label, image_path, out_file)
		i += 1
		time.sleep(round(60 * interval))

################################################################################
# program entrypoint
if __name__ == "__main__":
	threads = []
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
	interval = 15
	# recur(site, interval)
	for i in range(len(labels)):
		t = threading.Thread(target=recur, args=(sites[i], interval, labels[i]))
		threads.append(t)
		t.start()