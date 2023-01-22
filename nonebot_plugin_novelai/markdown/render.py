import os
from pathlib import Path

vipsbin = Path(__file__).parent / "bin"
os.environ["PATH"] = os.pathsep.join((str(vipsbin), os.environ["PATH"]))
import pyvips
from pyvips import Image

text = "你"
# out = pyvips.Image.new_temp_file(".png")
image: Image = pyvips.Image.text(text,font="Noto Sans CJK SC",rgba=True)
image.
image.write_to_file("x.png")
