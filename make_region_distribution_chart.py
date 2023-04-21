import pathlib

import matplotlib.pyplot as plt
import numpy as np

from colormap import COLORMAP

MAX_IMAGES_PER_VERSION_LEVEL = 20

BAR_HEIGHT = 3 / 24

HATCHING_AND_Y_OFFSET = {
    ("v0.1", "level1"): ("///", -8 / 3 * BAR_HEIGHT),
    ("v0.1", "level2"): ("/////", -4 / 3 * BAR_HEIGHT),
    ("v1.0", "level1"): ("xx", 1 / 3 * BAR_HEIGHT),
    ("v1.0", "level2"): ("xxxx", 5 / 3 * BAR_HEIGHT),
    ("v1.0", "level3"): ("xxxxxx", 9 / 3 * BAR_HEIGHT),
}


def main(*, masks_root, figures_root, chart_file_name="region_distribution.png"):
    regions_in_chart, num_occurrences = get_num_occurrences_per_version_level(
        masks_root
    )

    fig, ax = prepare_figure(regions_in_chart)

    plot_num_occurrences(ax, regions_in_chart, num_occurrences)

    add_legend(ax)

    fig.savefig(figures_root / chart_file_name)


def get_num_occurrences_per_version_level(masks_root):
    num_occurrences = {
        id: dict(zip(COLORMAP.keys(), [0] * len(COLORMAP)))
        for id in HATCHING_AND_Y_OFFSET.keys()
    }
    for id, num_occurences_per_version_level in num_occurrences.items():
        version, level = id
        for file in (masks_root / version / level).rglob("*.png"):
            num_occurences_per_version_level[file.stem] += 1

    regions_in_chart = []
    for region in COLORMAP.keys():
        num_occurrences_per_version_level_region = set()
        for num_occurrences_per_version_level in num_occurrences.values():
            num_occurrences_per_version_level_region.add(
                num_occurrences_per_version_level[region]
            )

        if num_occurrences_per_version_level_region != {MAX_IMAGES_PER_VERSION_LEVEL}:
            regions_in_chart.append(region)
            continue

        print(
            f"Excluding region '{region}' from the chart "
            f"since all versions and levels include it in every image."
        )

        for num_occurrences_per_version_level in list(num_occurrences.values()):
            del num_occurrences_per_version_level[region]

    return regions_in_chart, num_occurrences


def prepare_figure(
    regions_in_chart,
    *,
    width_in_pixels=8 * 99,
    height_in_inches=6,
    dpi=200,
    font_size=6,
):
    plt.rc("font", size=font_size)

    fig, ax = plt.subplots(dpi=dpi, figsize=(width_in_pixels / dpi, height_in_inches))

    ax.set_xlim(0, MAX_IMAGES_PER_VERSION_LEVEL + 1)
    ax.set_xticks(
        np.arange(
            0, MAX_IMAGES_PER_VERSION_LEVEL + 1, MAX_IMAGES_PER_VERSION_LEVEL // 4
        )
    )

    ax.set_ylim(
        13 / 3 * BAR_HEIGHT + len(regions_in_chart) - 1,
        -9 / 3 * BAR_HEIGHT,
    )
    ax.set_yticks(
        np.arange(len(regions_in_chart)),
        labels=[region.replace("_", " ") for region in regions_in_chart],
    )

    ax.set_axisbelow(True)
    ax.grid(visible=True, axis="x")

    fig.tight_layout()

    return fig, ax


def plot_num_occurrences(ax, regions_in_chart, num_occurrences):
    barss = []
    for id, (hatch, y_offset) in HATCHING_AND_Y_OFFSET.items():
        num_occurences_per_version_level = num_occurrences[id]

        x = np.arange(len(regions_in_chart)) + y_offset
        bars = ax.barh(
            x,
            [num_occurences_per_version_level[region] for region in regions_in_chart],
            height=BAR_HEIGHT,
            align="edge",
            hatch=hatch,
        )
        barss.append(bars)

        for bar, region in zip(bars, regions_in_chart):
            color = COLORMAP[region]
            bar.set_facecolor((*[a / 255 for a in color], 1.0))

    for bars in barss:
        ax.bar_label(bars)


def add_legend(ax):
    legend_bars = ax.barh(
        np.arange(len(HATCHING_AND_Y_OFFSET)),
        np.zeros(len(HATCHING_AND_Y_OFFSET)),
        edgecolor="black",
        facecolor="white",
    )

    legend_handles_and_labels = []
    for bar, (id, (hatch, _)) in zip(legend_bars, HATCHING_AND_Y_OFFSET.items()):
        bar.set_hatch(hatch)
        legend_handles_and_labels.append((bar, ", ".join(id)))
    ax.legend(*zip(*legend_handles_and_labels))


if __name__ == "__main__":
    project_root = pathlib.Path(__file__).parent
    main(masks_root=project_root / "masks", figures_root=project_root / "figures")
