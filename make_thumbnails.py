import contextlib
import pathlib
import zipfile
from collections import defaultdict
from urllib.parse import urlparse

import numpy as np
import PIL.Image
import requests
import tqdm

from colormap import COLORMAP


def main(
    *,
    project_root,
    images_root,
    segmentations_root,
    thumbnails_root,
    background_color=COLORMAP["background"],
    width=99,
    columns=4,
):
    overview = {}
    for segmentation_file in tqdm.tqdm(list(segmentations_root.rglob("*.png"))):
        rel_thumbnail_path = segmentation_file.relative_to(segmentations_root)

        version, level, name = rel_thumbnail_path.parts
        levels = overview.setdefault(version, defaultdict(list))

        image_file = get_image_file(images_root, version, level, name)

        image_thumbnail = thumbnails_root / "images" / rel_thumbnail_path
        image_thumbnail.parent.mkdir(parents=True, exist_ok=True)

        image = PIL.Image.open(image_file)
        image = to_thumbnail(image, resample=PIL.Image.Resampling.BICUBIC, width=width)
        image.save(image_thumbnail)

        segmentation_thumbnail = thumbnails_root / "segmentations" / rel_thumbnail_path
        segmentation_thumbnail.parent.mkdir(parents=True, exist_ok=True)

        segmentation = PIL.Image.open(segmentation_file)
        segmentation = to_thumbnail(
            segmentation, resample=PIL.Image.Resampling.NEAREST, width=width
        )
        segmentation = remove_background(
            segmentation, background_color=background_color
        )
        segmentation.save(segmentation_thumbnail)

        levels[level].append((image_thumbnail, segmentation_thumbnail))

    print_overview(overview, project_root=project_root, columns=columns)


def download(url, path, *, chunk_size=32 * 1024):
    with requests.get(url, stream=True) as response, open(path, "wb") as f:
        with tqdm.tqdm(
            total=int(response.headers["Content-Length"]),
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            dynamic_ncols=True,
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size):
                f.write(chunk)
                progress_bar.update(len(chunk))


def get_image_file(images_root, version, level, name):
    folder = images_root / version / level
    stem = name.split(".")[0]
    with contextlib.suppress(StopIteration):
        return next(folder.glob(f"{stem}*"))

    mapped_version = {
        "v0.1": "V01",
        "v1.0": "V1",
    }[version]
    mapped_level = int(level[-1])
    url = f"https://users.cs.cf.ac.uk/Paul.Rosin/NPRportrait{mapped_version}/NPRportrait{mapped_level}.zip"

    folder.mkdir(parents=True, exist_ok=True)
    archive = folder / pathlib.Path(urlparse(url).path).name

    if not archive.exists():
        download(url, archive)

    with zipfile.ZipFile(archive) as zip:
        for info in zip.infolist():
            if pathlib.Path(info.filename).suffix in {".jpg", ".png"}:
                zip.extract(info, path=folder)

    return next(folder.glob(f"{stem}*"))


def to_thumbnail(image, *, resample, width):
    height = int(image.height / image.width * width)
    return image.resize((width, height), resample=resample)


def remove_background(image, *, background_color):
    rgb = np.array(image)
    background_flat = np.all(rgb.reshape(-1, 3) == np.array(background_color), axis=1)
    alpha = ((~background_flat).astype(np.uint8) * 255).reshape(*rgb.shape[:-1], 1)
    return PIL.Image.fromarray(np.concatenate([rgb, alpha], axis=2), mode="RGBA")


def print_overview(overview, *, project_root, columns):
    for version, levels in sorted(overview.items()):
        print(f"### Version {version}\n")
        for level, thumbnails in sorted(levels.items()):
            print(f"#### Level {level[-1]}\n")
            for idx, (image_thumbnail, segmentation_thumbnail) in enumerate(
                sorted(thumbnails, key=lambda thumbnails: int(thumbnails[0].name[:2])),
                1,
            ):
                print(
                    f"![{image_thumbnail.stem} image]({image_thumbnail.relative_to(project_root)}) "
                    f"![{segmentation_thumbnail.stem} segmentation]({segmentation_thumbnail.relative_to(project_root)})",
                    end="\n\n" if idx > 0 and idx % columns == 0 else " ",
                )
            print("")


if __name__ == "__main__":
    project_root = pathlib.Path(__file__).parent
    main(
        project_root=project_root,
        images_root=project_root / "images",
        segmentations_root=project_root / "segmentations",
        thumbnails_root=project_root / "thumbnails",
    )
