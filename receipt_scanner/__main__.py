from parser import get_items_from_text

from cli import get_arguments
from debug import configure_logger
from image import process_image
from image_to_text import get_text

arguments = get_arguments()
configure_logger(debug=arguments.debug)
image = process_image(arguments.image, debug=arguments.debug)
text = get_text(image)
items = get_items_from_text(text)
print("\n".join(items))
