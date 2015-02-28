from PIL import Image
 
def convert_avatar(in_img, out_img, width, height):

	try:
		img = Image.open(in_img)
		w, h = img.size
		h_prec = float(h/height)
		w_perc = float(w/width)
		final_perc = w_perc if h_prec>w_perc else h_prec

		img = img.crop((int(float(w - width*final_perc)/2),
					   int(float(h - height*final_perc)/2),
					   int(float(w + width*final_perc)/2),
					   int(float(h + height*final_perc)/2)))

		img = img.resize((width, height), Image.BILINEAR)

		img.save(out_img)

	except Exception, e:
		return False
		
	return True