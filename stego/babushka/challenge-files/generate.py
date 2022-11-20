import io
import random
import randomname
import shutil
import zipfile

from pathlib import Path
from PIL import Image
from tqdm import tqdm
from zipfile import ZipFile


IMG_DIR = Path("img")
ZIP_DIR = Path("zip")


def randomize_filenames(paths):
    for p in paths:
        new_name = randomname.get_name()
        p.rename(Path(p.parent, new_name + p.suffix))


def partition(ls, n):
    random.shuffle(ls)
    return [ls[i::n] for i in range(n)]


def img2bytes(img):
    byte_arr = io.BytesIO()
    img.save(byte_arr, format="JPEG")
    return byte_arr.getvalue()


def split_dolls():
    im = Image.open("russian_dolls.jpg")
    return [
        im.crop((40, 40, 250, 430)),
        im.crop((245, 100, 405, 410)),
        im.crop((405, 160, 535, 410)),
        im.crop((535, 210, 641, 410)),
        im.crop((641, 250, 728, 410)),
        im.crop((728, 280, 802, 415)),
        im.crop((802, 315, 863, 420)),
        im.crop((863, 345, 912, 430)),
        im.crop((912, 370, 951, 435)),
        im.crop((950, 395, 978, 440))
    ][::-1]


def main():
    levels = 10  # max 10
    randomize_filenames(IMG_DIR.glob("**/*"))
    decoy_file_partitions = partition([*IMG_DIR.glob("**/*")], levels)
    dolls = split_dolls()[:levels]
    final_name = "Бабушка"

    # Innermost ZIP contains flag file
    ZIP_DIR.mkdir(exist_ok=True)
    with ZipFile(ZIP_DIR / "0.zip", "w", compression=zipfile.ZIP_BZIP2) as z:
        z.write("flag.txt")

    # Append previous ZIP to doll file and add to new ZIP with some decoys
    for i, (doll, decoy_files) in tqdm(enumerate(zip(dolls, decoy_file_partitions)), total=len(decoy_file_partitions)):
        with open(ZIP_DIR / f"{i}.zip", "rb") as f, ZipFile(ZIP_DIR / f"{i + 1}.zip", "w", compression=zipfile.ZIP_BZIP2) as z:
            doll_with_hidden_file = img2bytes(doll) + f.read()
            doll_file = (f"{final_name}/" if i == levels - 1 else "") + randomname.get_name() + ".jpg"
            z.writestr(doll_file, doll_with_hidden_file)
            for file in decoy_files:
                z.write(file, (f"{final_name}/" if i == levels - 1 else "") + file.name)

    # Cleanup
    (ZIP_DIR / f"{levels}.zip").rename(f"{final_name}.zip")
    shutil.rmtree(ZIP_DIR)


if __name__ == "__main__":
    main()
