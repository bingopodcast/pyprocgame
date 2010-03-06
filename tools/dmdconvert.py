import sys
import os
sys.path.append(sys.path[0]+'/..') # Set the path so we can find procgame.  We are assuming (stupidly?) that the first member is our directory.
import procgame.dmd
import time
#import pygame.image
import Image

class ImageSequence:
	"""Iterates over all images in a sequence (of PIL Images)."""
	# Source: http://www.pythonware.com/library/pil/handbook/introduction.htm
	def __init__(self, im):
		self.im = im
	def __getitem__(self, ix):
		try:
			if ix:
				self.im.seek(ix)
			return self.im
		except EOFError:
			raise IndexError # end of sequence

def image_to_dmd(src_filename, dst_filename):
	"""docstring for image_to_dmd"""
	last_filename = None
	anim = procgame.dmd.Animation()
	for frame_index in range(1000):
		if '%d' in src_filename:
			filename = src_filename % (frame_index)
		else:
			filename = src_filename
		if filename == last_filename:
			break
		if not os.path.exists(filename):
			break
		print "Appending ", filename
		src = Image.open(filename)
		last_filename = filename
		(w, h) = src.size
		
		for src_im in ImageSequence(src):
			reduced = src.convert("L") #.quantize(palette=pal_im).convert("P", palette=Image.ADAPTIVE, colors=4)#
			
			frame = procgame.dmd.Frame(w, h)
			
			for x in range(w):
				for y in range(h):
					color = int((reduced.getpixel((x,y))/255.0)*15)
					frame.set_dot(x=x, y=y, value=color)
			
			(anim.width, anim.height) = (w, h)
			anim.frames += [frame]
		
	anim.save(dst_filename)
	print "Saved."

def main():
	if len(sys.argv) < 3:
		print("Usage: %s <image.png> <output.dmd>"%(sys.argv[0]))
		print("  image.png may include %d format specifiers to create animations.  Example:")
		print("    %s Animation%%03d.png Animation.dmd" % (sys.argv[0]))
		print("  Creates an animation of up to 999 frames with sequential names.")
		return
	image_to_dmd(src_filename=sys.argv[1], dst_filename=sys.argv[2])


if __name__ == "__main__":
	main()