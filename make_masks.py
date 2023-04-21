import pathlib

import numpy as np
import PIL.Image
import tqdm

from colormap import COLORMAP


COLOR_TO_REGION = {color: region for region, color in COLORMAP.items()}


def main(*, segmentations_root, masks_root):
    for segmentation_file in tqdm.tqdm(list(segmentations_root.rglob("*.png"))):
        masks_folder = masks_root.joinpath(
            segmentation_file.relative_to(segmentations_root)
        ).with_suffix("")
        masks_folder.mkdir(parents=True, exist_ok=True)

        segmentation = np.array(PIL.Image.open(segmentation_file))
        segmentation_flat = segmentation.reshape(-1, 3)

        for color in np.unique(segmentation_flat, axis=0):
            try:
                region = COLOR_TO_REGION[tuple(color)]
            except KeyError:
                raise RuntimeError(
                    f"Color {color} is part of the image, but has no corresponding region in the color map"
                ) from None
            mask_file = masks_folder / f"{region}.png"

            mask_flat = np.all(segmentation_flat == color, axis=1)
            mask = mask_flat.reshape(segmentation.shape[:2])

            PIL.Image.fromarray(mask).save(mask_file)


if __name__ == "__main__":
    project_root = pathlib.Path(__file__).parent
    main(
        segmentations_root=project_root / "segmentations",
        masks_root=project_root / "masks",
    )
