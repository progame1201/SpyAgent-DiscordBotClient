import os
from io import BytesIO

from PIL import Image
from term_image.image import AutoImage

import config


async def draw_message_attachments(message):
    for attachment in message.attachments:
        if config.DRAW_IMAGES and os.path.splitext(attachment.filename)[1].lower() in [".png", ".jpg", ".jpeg"]:
            img = Image.open(BytesIO(await attachment.read()))
            img = AutoImage(img, height=8)
            img.draw(h_align="left", v_align="top", pad_height=-100, animate=False)
