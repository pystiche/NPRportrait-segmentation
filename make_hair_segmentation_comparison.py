import pathlib

import numpy as np
import PIL.Image


def main(
    *,
    images_root,
    segmentations_root,
    masks_root,
    figures_root,
    version,
    level,
    id,
    width=250,
    figure_folder_name="hair_segmentation_comparison",
):
    figure_root = figures_root / figure_folder_name
    figure_root.mkdir(parents=True, exist_ok=True)

    image_path = next(
        path
        for path in (images_root / version / level).glob("*.jpg")
        if path.name.startswith(f"{id:02d}")
    )
    image = PIL.Image.open(image_path)
    height = int(image.height / image.width * width)
    image = image.resize((width, height), PIL.Image.Resampling.BICUBIC)
    image.save(figure_root / "image.jpg")

    segmentation_path = segmentations_root.joinpath(*image_path.parts[-3:]).with_suffix(
        ".png"
    )
    segmentation = PIL.Image.open(segmentation_path).resize(
        (width, height), PIL.Image.Resampling.NEAREST
    )
    segmentation.save(figure_root / "segmentation.png")

    background_path = (
        masks_root.joinpath(*image_path.parts[-3:]).with_suffix("") / "background.png"
    )
    background = PIL.Image.open(background_path).resize(
        (width, height), PIL.Image.Resampling.NEAREST
    )

    image = np.array(image)
    segmentation = np.array(segmentation)
    background = np.array(background)

    segmentation_without_background = np.empty_like(image)
    segmentation_without_background[background] = image[background]
    segmentation_without_background[~background] = segmentation[~background]

    segmentation_without_background = PIL.Image.fromarray(
        segmentation_without_background
    )
    segmentation_without_background.save(
        figure_root / "segmentation_without_background.png"
    )


if __name__ == "__main__":
    project_root = pathlib.Path(__file__).parent
    main(
        images_root=project_root / "images",
        segmentations_root=project_root / "segmentations",
        masks_root=project_root / "masks",
        figures_root=project_root / "figures",
        version="v0.1",
        level="level2",
        id=15,
    )
