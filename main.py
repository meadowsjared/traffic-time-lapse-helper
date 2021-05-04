import os, time
# from WebHandler import WebHandler
# from ImageHandler import ImageHandler

################################################################################
# locations configuration
ImageMagick = r'd:\files\4\programs\terminal-utilities\imagemagick\convert.exe'

screenshotDir = 'screenshots'
tempDir = 'temp'
outputDir = 'output'

################################################################################
# screenshot/manipulation loop
def recur(site, interval, process=True):
wh = WebHandler(visual=False)
ih = ImageHandler(ImageMagick, os.path.join(tempDir, 'temp.png'))

print('starting process...')
i = 1
while(1):
	current_time = time.localtime()
	print('\nstarting frame at %s...' % time.strftime("%H:%M:%S", current_time))
	filename = '%s.png' % time.strftime("%H-%M-%S", current_time)
	path = os.path.join(screenshotDir, filename)
	wh.screenshot(site, path)

	# process the image if desired
	if process:
		hour = time.strftime("%H", current_time)
		minute = time.strftime("%M", current_time)
		out_file = os.path.join(outputDir, '%04d.png' % i)
		ih.processImage(path, out_file, [hour, minute])
		i += 1
	time.sleep(round(60 * interval))

################################################################################
# program entrypoint
if __name__ == "__main__":

site = 'https://maps.google.com/maps?q=atlanta+traffic'
interval = 15
recur(site, interval)