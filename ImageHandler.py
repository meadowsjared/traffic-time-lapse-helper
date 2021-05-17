import time
from PIL import Image, ImageFont, ImageDraw


class ImageHandler:

	##############################################################################
	# processes a frame, including color analysis and annotation
	def process_image(self, label, in_file, out_file):
		print('processing %s...' % in_file)

		im = Image.open(in_file)
		
		# add text to the image
		current_time = time.localtime()
		iamge_label = label + ' ' + time.strftime("%m-%d %a %-I:%M %p", current_time)
		font = ImageFont.truetype("arial.ttf", 48)
		draw = ImageDraw.Draw(im)
		draw.text((12, 12),iamge_label,(0,0,0),font=font)
		w, h = im.size
		# add an image overlay to the image
		logo = Image.open("ImageOverlay.png")
		im.paste(logo, (w-352,10), logo)
		# save it back
		im.save(out_file, "png")

		print('frame processed. ' + out_file)