# NPRportrait segmentation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7852139.svg)](https://doi.org/10.5281/zenodo.7852139)

- [Introduction](#introduction)
- [Methodology](#methodology)
- [Usage](#usage)
- [Overview](#overview)
- [License](#license)
- [Citation](#citation)

## Introduction

Style Transfer (ST) algorithms from the field of Non-photorealistic Rendering (NPR) are notoriously hard to compare because there is no objective metric to do so. In a first step, Mould and Rosin introduced the [_NPRgeneral_](https://doi.org/10.1016/j.cag.2017.05.025) dataset, that contains 20 diverse images of various motifs. With it, algorithms can at least be evaluated on set of standard images rather than every author picking their own and, unwillingly or not, introduce even more subjective bias in the comparison. As a follow-up Rosin et al. later also introduced the [_NPRportrait_](https://dl.acm.org/doi/10.1145/3092919.3092921) dataset, that, as the name implies, only contains portraits. In 2022 Rosin et al. released an [updated version](https://doi.org/10.1007/s41095-021-0255-3), dubbing the initial version [_0.1_](https://github.com/pystiche/NPRportrait-segmentation#nprportrait-01) and the new one [_1.0_](https://github.com/pystiche/NPRportrait-segmentation#nprportrait-10). Both datasets use a leveled approach, in which each level includes 20 images that increase in difficulty, e.g. partially or fully covered facial features. _0.1_ comes with two and _1.0_ with three levels.

ST algorithms, e.g. Neural Style Transfer (NST) algorithms, can be applied to an image as is. However, if the image exhibits stark differences between multiple regions, e.g. different facial features, this often leads to artifacts. To avoid this without painstakingly and manually fine-tuning the hyperparameters of an algorithm that should automate the task at hand, one can also guide the algorithm using segmentation masks of the image. Albeit not for portraits, this technique was recently used by [Gatys et al.](https://doi.org/10.1109/CVPR.2017.397) to improve the results of their NST algorithm and even being able to mix different styles in the stylized image per region.

Unfortunately, so far there are no segmentation masks available for the standard datasets detailed above. As the name implies _NPRportrait-segmentation_ fills this gap for the portrait benchmark datasets.

## Methodology

There are a number of datasets out there that provide segmentation masks for portraits, e.g. [FASSEG](http://massimomauro.github.io/FASSEG-repository/) or [CelebAMask-HQ](https://github.com/switchablenorms/CelebAMask-HQ). However, they are often suboptimal for ST algorithms:

1. Some datasets are too coarse and lump features like the lips and teeth together in one region, although they have vastly different styles.
2. Some datasets are too fine-grained and differentiate between left and right facial features, although this has no impact on the ST.

For _NPRportrait-segmentation_ we settled on 14 different regions excluding the background that we found the most important ones during our research:

- skin
- clothing
- eyeballs
- nose
- ears
- hair
- eyebrows
- facial hair
- lips
- teeth
- mouth cavity
- accessories
- headgear
- glasses

Due to the fine division, a coarser division of the regions is possible at any time by merging the masks. This makes these segmentations usable for various applications.

The segmentations for all 100 images were manually created. Apart from the inherent annotation bias, it was difficult in some images to introduce a clear cut between the _hair_ and _background_ region (cf. Figure 1). We opted to only label a region as _hair_ if there is a significant hair density, with no intention to make "significant" more concrete.

| ![image](figures/hair_segmentation_comparison/image.jpg) ![segmentation](figures/hair_segmentation_comparison/segmentation.png) ![segmentation without background](figures/hair_segmentation_comparison/segmentation_without_background.png) |
|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:| 
|     Figure 1: An image (left), its corresponding segmentation (middle), and the segmentation without background (right). Areas of low hair density were not annotated as belonging to the _hair_, but rather to the _background_ region.     |

## Usage

_NPRportrait-segmentation_ provides the segmentation in two formats:

1. As a single segmentation image which separates the regions by colour. The color map is detailed below. You can find these images inside the `segmentations/` directory.
2. As multiple boolean masks per image where each mask is white for the respective region and black everywhere else. You can find these images inside the `masks/` directory.

### Colormap

| region                                                                                                          | RGB code          |
|-----------------------------------------------------------------------------------------------------------------|-------------------|
| [![background](https://img.shields.io/badge/region-background-000000)](https://colornames.org/color/000000)     | `(  0,   0,   0)` |
| [![skin](https://img.shields.io/badge/region-skin-3182bd)](https://colornames.org/color/3182bd)                 | `( 49, 130, 189)` |
| [![clothing](https://img.shields.io/badge/region-clothing-6baed6)](https://colornames.org/color/6baed6)         | `(107, 174, 214)` |
| [![eyeballs](https://img.shields.io/badge/region-eyeballs-e6550d)](https://colornames.org/color/e6550d)         | `(230,  85,  13)` |
| [![nose](https://img.shields.io/badge/region-nose-fd8d3c)](https://colornames.org/color/fd8d3c)                 | `(253, 141,  60)` |
| [![ears](https://img.shields.io/badge/region-ears-fdae6b)](https://colornames.org/color/fdae6b)                 | `(253, 174, 107)` |
| [![hair](https://img.shields.io/badge/region-hair-31a354)](https://colornames.org/color/31a354)                 | `( 49, 163,  84)` |
| [![eyebrows](https://img.shields.io/badge/region-eyebrows-74c476)](https://colornames.org/color/74c476)         | `(116, 196, 118)` |
| [![facial_hair](https://img.shields.io/badge/region-facial_hair-a1d99b)](https://colornames.org/color/a1d99b)   | `(161, 217, 155)` |
| [![lips](https://img.shields.io/badge/region-lips-756bb1)](https://colornames.org/color/756bb1)                 | `(117, 107, 177)` |
| [![teeth](https://img.shields.io/badge/region-teeth-9e9ac8)](https://colornames.org/color/9e9ac8)               | `(158, 154, 200)` |
| [![mouth_cavity](https://img.shields.io/badge/region-mouth_cavity-bcbddc)](https://colornames.org/color/bcbddc) | `(188, 189, 220)` |
| [![accessories](https://img.shields.io/badge/region-accessories-636363)](https://colornames.org/color/636363)   | `( 99,  99,  99)` |
| [![headgear](https://img.shields.io/badge/region-headgear-969696)](https://colornames.org/color/969696)         | `(150, 150, 150)` |
| [![glasses](https://img.shields.io/badge/region-glasses-bdbdbd)](https://colornames.org/color/bdbdbd)           | `(189, 189, 189)` |

### Region distribution

|                                                                              ![region distribution](figures/region_distribution.png)                                                                              |
|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| Figure 2: Distribution of regions throughout _NPRportrait-segmentation_. The regions _background_, _skin_, _nose_, and _lips_ are not shown since they are present in every image regardless of version or level. |

## Overview

### Version v0.1

#### Level 1

![01-12866391563_7312cae13a_o image](thumbnails/images/v0.1/level1/01-12866391563_7312cae13a_o.png) ![01-12866391563_7312cae13a_o segmentation](thumbnails/segmentations/v0.1/level1/01-12866391563_7312cae13a_o.png) ![02-19879809258_3de6bc082b_o image](thumbnails/images/v0.1/level1/02-19879809258_3de6bc082b_o.png) ![02-19879809258_3de6bc082b_o segmentation](thumbnails/segmentations/v0.1/level1/02-19879809258_3de6bc082b_o.png) ![03-25018815523_80542cf933_o image](thumbnails/images/v0.1/level1/03-25018815523_80542cf933_o.png) ![03-25018815523_80542cf933_o segmentation](thumbnails/segmentations/v0.1/level1/03-25018815523_80542cf933_o.png) ![04-wikimedia image](thumbnails/images/v0.1/level1/04-wikimedia.png) ![04-wikimedia segmentation](thumbnails/segmentations/v0.1/level1/04-wikimedia.png)

![05-34783750806_954ea83724_o image](thumbnails/images/v0.1/level1/05-34783750806_954ea83724_o.png) ![05-34783750806_954ea83724_o segmentation](thumbnails/segmentations/v0.1/level1/05-34783750806_954ea83724_o.png) ![06-19876234959_388a248a3e_k image](thumbnails/images/v0.1/level1/06-19876234959_388a248a3e_k.png) ![06-19876234959_388a248a3e_k segmentation](thumbnails/segmentations/v0.1/level1/06-19876234959_388a248a3e_k.png) ![07-pixabay-1869761 image](thumbnails/images/v0.1/level1/07-pixabay-1869761.png) ![07-pixabay-1869761 segmentation](thumbnails/segmentations/v0.1/level1/07-pixabay-1869761.png) ![08-14717382472_3119d35971_o image](thumbnails/images/v0.1/level1/08-14717382472_3119d35971_o.png) ![08-14717382472_3119d35971_o segmentation](thumbnails/segmentations/v0.1/level1/08-14717382472_3119d35971_o.png)

![09-20052719652_d69fe9705c_k image](thumbnails/images/v0.1/level1/09-20052719652_d69fe9705c_k.png) ![09-20052719652_d69fe9705c_k segmentation](thumbnails/segmentations/v0.1/level1/09-20052719652_d69fe9705c_k.png) ![10-2233221399_3600271088_o image](thumbnails/images/v0.1/level1/10-2233221399_3600271088_o.png) ![10-2233221399_3600271088_o segmentation](thumbnails/segmentations/v0.1/level1/10-2233221399_3600271088_o.png) ![11-10733769754_d8b219de27_o image](thumbnails/images/v0.1/level1/11-10733769754_d8b219de27_o.png) ![11-10733769754_d8b219de27_o segmentation](thumbnails/segmentations/v0.1/level1/11-10733769754_d8b219de27_o.png) ![12-4727363362_42d266fc1d_o image](thumbnails/images/v0.1/level1/12-4727363362_42d266fc1d_o.png) ![12-4727363362_42d266fc1d_o segmentation](thumbnails/segmentations/v0.1/level1/12-4727363362_42d266fc1d_o.png)

![13-4727365078_655e6cd0f5_o image](thumbnails/images/v0.1/level1/13-4727365078_655e6cd0f5_o.png) ![13-4727365078_655e6cd0f5_o segmentation](thumbnails/segmentations/v0.1/level1/13-4727365078_655e6cd0f5_o.png) ![14-pixabay-1436663 image](thumbnails/images/v0.1/level1/14-pixabay-1436663.png) ![14-pixabay-1436663 segmentation](thumbnails/segmentations/v0.1/level1/14-pixabay-1436663.png) ![15-4013774662_6abb307517_o image](thumbnails/images/v0.1/level1/15-4013774662_6abb307517_o.png) ![15-4013774662_6abb307517_o segmentation](thumbnails/segmentations/v0.1/level1/15-4013774662_6abb307517_o.png) ![16-24898722630_e8d16050f1_o image](thumbnails/images/v0.1/level1/16-24898722630_e8d16050f1_o.png) ![16-24898722630_e8d16050f1_o segmentation](thumbnails/segmentations/v0.1/level1/16-24898722630_e8d16050f1_o.png)

![17-34589588971_cc1b6b99f7_o image](thumbnails/images/v0.1/level1/17-34589588971_cc1b6b99f7_o.png) ![17-34589588971_cc1b6b99f7_o segmentation](thumbnails/segmentations/v0.1/level1/17-34589588971_cc1b6b99f7_o.png) ![18-20356338610_54af76bcf3_k image](thumbnails/images/v0.1/level1/18-20356338610_54af76bcf3_k.png) ![18-20356338610_54af76bcf3_k segmentation](thumbnails/segmentations/v0.1/level1/18-20356338610_54af76bcf3_k.png) ![19-7581750218_9ba155cd23_o image](thumbnails/images/v0.1/level1/19-7581750218_9ba155cd23_o.png) ![19-7581750218_9ba155cd23_o segmentation](thumbnails/segmentations/v0.1/level1/19-7581750218_9ba155cd23_o.png) ![20-15350967367_f9df8a8f06_o image](thumbnails/images/v0.1/level1/20-15350967367_f9df8a8f06_o.png) ![20-15350967367_f9df8a8f06_o segmentation](thumbnails/segmentations/v0.1/level1/20-15350967367_f9df8a8f06_o.png)


#### Level 2

![01-wikimedia image](thumbnails/images/v0.1/level2/01-wikimedia.png) ![01-wikimedia segmentation](thumbnails/segmentations/v0.1/level2/01-wikimedia.png) ![02-8115174843_7abf278359_o image](thumbnails/images/v0.1/level2/02-8115174843_7abf278359_o.png) ![02-8115174843_7abf278359_o segmentation](thumbnails/segmentations/v0.1/level2/02-8115174843_7abf278359_o.png) ![03-34694233905_6f774ba164_o image](thumbnails/images/v0.1/level2/03-34694233905_6f774ba164_o.png) ![03-34694233905_6f774ba164_o segmentation](thumbnails/segmentations/v0.1/level2/03-34694233905_6f774ba164_o.png) ![04-33916867564_c6af07fd52_o image](thumbnails/images/v0.1/level2/04-33916867564_c6af07fd52_o.png) ![04-33916867564_c6af07fd52_o segmentation](thumbnails/segmentations/v0.1/level2/04-33916867564_c6af07fd52_o.png)

![05-3217118459_7952198317_o image](thumbnails/images/v0.1/level2/05-3217118459_7952198317_o.png) ![05-3217118459_7952198317_o segmentation](thumbnails/segmentations/v0.1/level2/05-3217118459_7952198317_o.png) ![06-15158628486_c93546d21d_o image](thumbnails/images/v0.1/level2/06-15158628486_c93546d21d_o.png) ![06-15158628486_c93546d21d_o segmentation](thumbnails/segmentations/v0.1/level2/06-15158628486_c93546d21d_o.png) ![07-9467963321_63d0375465_o image](thumbnails/images/v0.1/level2/07-9467963321_63d0375465_o.png) ![07-9467963321_63d0375465_o segmentation](thumbnails/segmentations/v0.1/level2/07-9467963321_63d0375465_o.png) ![08-16022313531_5aa50d89d3_o image](thumbnails/images/v0.1/level2/08-16022313531_5aa50d89d3_o.png) ![08-16022313531_5aa50d89d3_o segmentation](thumbnails/segmentations/v0.1/level2/08-16022313531_5aa50d89d3_o.png)

![09-306039906_24c5e9600c_o image](thumbnails/images/v0.1/level2/09-306039906_24c5e9600c_o.png) ![09-306039906_24c5e9600c_o segmentation](thumbnails/segmentations/v0.1/level2/09-306039906_24c5e9600c_o.png) ![10-27552868751_703ad00cde_k image](thumbnails/images/v0.1/level2/10-27552868751_703ad00cde_k.png) ![10-27552868751_703ad00cde_k segmentation](thumbnails/segmentations/v0.1/level2/10-27552868751_703ad00cde_k.png) ![11-2389874253_759d8164ab_o image](thumbnails/images/v0.1/level2/11-2389874253_759d8164ab_o.png) ![11-2389874253_759d8164ab_o segmentation](thumbnails/segmentations/v0.1/level2/11-2389874253_759d8164ab_o.png) ![12-14452459445_1bb06c6302_o image](thumbnails/images/v0.1/level2/12-14452459445_1bb06c6302_o.png) ![12-14452459445_1bb06c6302_o segmentation](thumbnails/segmentations/v0.1/level2/12-14452459445_1bb06c6302_o.png)

![13-pexels-355020 image](thumbnails/images/v0.1/level2/13-pexels-355020.png) ![13-pexels-355020 segmentation](thumbnails/segmentations/v0.1/level2/13-pexels-355020.png) ![14-230501453_85963e7ee3_o image](thumbnails/images/v0.1/level2/14-230501453_85963e7ee3_o.png) ![14-230501453_85963e7ee3_o segmentation](thumbnails/segmentations/v0.1/level2/14-230501453_85963e7ee3_o.png) ![15-15339171978_a04047dc31_k image](thumbnails/images/v0.1/level2/15-15339171978_a04047dc31_k.png) ![15-15339171978_a04047dc31_k segmentation](thumbnails/segmentations/v0.1/level2/15-15339171978_a04047dc31_k.png) ![16-14610754861_8fd4939744_k image](thumbnails/images/v0.1/level2/16-14610754861_8fd4939744_k.png) ![16-14610754861_8fd4939744_k segmentation](thumbnails/segmentations/v0.1/level2/16-14610754861_8fd4939744_k.png)

![17-wikimedia image](thumbnails/images/v0.1/level2/17-wikimedia.png) ![17-wikimedia segmentation](thumbnails/segmentations/v0.1/level2/17-wikimedia.png) ![18-8047854084_76a56e69bb_k image](thumbnails/images/v0.1/level2/18-8047854084_76a56e69bb_k.png) ![18-8047854084_76a56e69bb_k segmentation](thumbnails/segmentations/v0.1/level2/18-8047854084_76a56e69bb_k.png) ![19-7741742246_502b485404_h image](thumbnails/images/v0.1/level2/19-7741742246_502b485404_h.png) ![19-7741742246_502b485404_h segmentation](thumbnails/segmentations/v0.1/level2/19-7741742246_502b485404_h.png) ![20-3900823607_9f9d376bb8_o image](thumbnails/images/v0.1/level2/20-3900823607_9f9d376bb8_o.png) ![20-3900823607_9f9d376bb8_o segmentation](thumbnails/segmentations/v0.1/level2/20-3900823607_9f9d376bb8_o.png)


### Version v1.0

#### Level 1

![01-Kimberly-Howell image](thumbnails/images/v1.0/level1/01-Kimberly-Howell.png) ![01-Kimberly-Howell segmentation](thumbnails/segmentations/v1.0/level1/01-Kimberly-Howell.png) ![02-22636558997-80ee36b602-o image](thumbnails/images/v1.0/level1/02-22636558997-80ee36b602-o.png) ![02-22636558997-80ee36b602-o segmentation](thumbnails/segmentations/v1.0/level1/02-22636558997-80ee36b602-o.png) ![03-Rosin image](thumbnails/images/v1.0/level1/03-Rosin.png) ![03-Rosin segmentation](thumbnails/segmentations/v1.0/level1/03-Rosin.png) ![04-Rosin image](thumbnails/images/v1.0/level1/04-Rosin.png) ![04-Rosin segmentation](thumbnails/segmentations/v1.0/level1/04-Rosin.png)

![05-Major-General-Edward-Rice image](thumbnails/images/v1.0/level1/05-Major-General-Edward-Rice.png) ![05-Major-General-Edward-Rice segmentation](thumbnails/segmentations/v1.0/level1/05-Major-General-Edward-Rice.png) ![06-Team-Karim image](thumbnails/images/v1.0/level1/06-Team-Karim.png) ![06-Team-Karim segmentation](thumbnails/segmentations/v1.0/level1/06-Team-Karim.png) ![07-24930764475-3bfbc008f8-o image](thumbnails/images/v1.0/level1/07-24930764475-3bfbc008f8-o.png) ![07-24930764475-3bfbc008f8-o segmentation](thumbnails/segmentations/v1.0/level1/07-24930764475-3bfbc008f8-o.png) ![08-Moid-Rasheedi image](thumbnails/images/v1.0/level1/08-Moid-Rasheedi.png) ![08-Moid-Rasheedi segmentation](thumbnails/segmentations/v1.0/level1/08-Moid-Rasheedi.png)

![09-Aswini-Phy-ALC image](thumbnails/images/v1.0/level1/09-Aswini-Phy-ALC.png) ![09-Aswini-Phy-ALC segmentation](thumbnails/segmentations/v1.0/level1/09-Aswini-Phy-ALC.png) ![10-Saira-Shah-Halim image](thumbnails/images/v1.0/level1/10-Saira-Shah-Halim.png) ![10-Saira-Shah-Halim segmentation](thumbnails/segmentations/v1.0/level1/10-Saira-Shah-Halim.png) ![11-Michelle-Chan image](thumbnails/images/v1.0/level1/11-Michelle-Chan.png) ![11-Michelle-Chan segmentation](thumbnails/segmentations/v1.0/level1/11-Michelle-Chan.png) ![12-38753438484-f65be5b961-o image](thumbnails/images/v1.0/level1/12-38753438484-f65be5b961-o.png) ![12-38753438484-f65be5b961-o segmentation](thumbnails/segmentations/v1.0/level1/12-38753438484-f65be5b961-o.png)

![13-6884042760-1ee2b00829-o image](thumbnails/images/v1.0/level1/13-6884042760-1ee2b00829-o.png) ![13-6884042760-1ee2b00829-o segmentation](thumbnails/segmentations/v1.0/level1/13-6884042760-1ee2b00829-o.png) ![14-Rosin image](thumbnails/images/v1.0/level1/14-Rosin.png) ![14-Rosin segmentation](thumbnails/segmentations/v1.0/level1/14-Rosin.png) ![15-Shimizu-kurumi image](thumbnails/images/v1.0/level1/15-Shimizu-kurumi.png) ![15-Shimizu-kurumi segmentation](thumbnails/segmentations/v1.0/level1/15-Shimizu-kurumi.png) ![16-Yoon-Yeoil image](thumbnails/images/v1.0/level1/16-Yoon-Yeoil.png) ![16-Yoon-Yeoil segmentation](thumbnails/segmentations/v1.0/level1/16-Yoon-Yeoil.png)

![17-4891358118-32c20e9d8e-o image](thumbnails/images/v1.0/level1/17-4891358118-32c20e9d8e-o.png) ![17-4891358118-32c20e9d8e-o segmentation](thumbnails/segmentations/v1.0/level1/17-4891358118-32c20e9d8e-o.png) ![18-Huw-Evans image](thumbnails/images/v1.0/level1/18-Huw-Evans.png) ![18-Huw-Evans segmentation](thumbnails/segmentations/v1.0/level1/18-Huw-Evans.png) ![19-Zboralski-waldemar-2012 image](thumbnails/images/v1.0/level1/19-Zboralski-waldemar-2012.png) ![19-Zboralski-waldemar-2012 segmentation](thumbnails/segmentations/v1.0/level1/19-Zboralski-waldemar-2012.png) ![20-8552893573-1473209795-o image](thumbnails/images/v1.0/level1/20-8552893573-1473209795-o.png) ![20-8552893573-1473209795-o segmentation](thumbnails/segmentations/v1.0/level1/20-8552893573-1473209795-o.png)


#### Level 2

![01-wikimedia image](thumbnails/images/v1.0/level2/01-wikimedia.png) ![01-wikimedia segmentation](thumbnails/segmentations/v1.0/level2/01-wikimedia.png) ![02-8115174843_7abf278359_o image](thumbnails/images/v1.0/level2/02-8115174843_7abf278359_o.png) ![02-8115174843_7abf278359_o segmentation](thumbnails/segmentations/v1.0/level2/02-8115174843_7abf278359_o.png) ![03-34694233905_6f774ba164_o image](thumbnails/images/v1.0/level2/03-34694233905_6f774ba164_o.png) ![03-34694233905_6f774ba164_o segmentation](thumbnails/segmentations/v1.0/level2/03-34694233905_6f774ba164_o.png) ![04-33916867564_c6af07fd52_o image](thumbnails/images/v1.0/level2/04-33916867564_c6af07fd52_o.png) ![04-33916867564_c6af07fd52_o segmentation](thumbnails/segmentations/v1.0/level2/04-33916867564_c6af07fd52_o.png)

![05-Tom_Selleck_at_PaleyFest_2014 image](thumbnails/images/v1.0/level2/05-Tom_Selleck_at_PaleyFest_2014.png) ![05-Tom_Selleck_at_PaleyFest_2014 segmentation](thumbnails/segmentations/v1.0/level2/05-Tom_Selleck_at_PaleyFest_2014.png) ![06-15158628486_c93546d21d_o image](thumbnails/images/v1.0/level2/06-15158628486_c93546d21d_o.png) ![06-15158628486_c93546d21d_o segmentation](thumbnails/segmentations/v1.0/level2/06-15158628486_c93546d21d_o.png) ![07-9467963321_63d0375465_o image](thumbnails/images/v1.0/level2/07-9467963321_63d0375465_o.png) ![07-9467963321_63d0375465_o segmentation](thumbnails/segmentations/v1.0/level2/07-9467963321_63d0375465_o.png) ![08-16022313531_5aa50d89d3_o image](thumbnails/images/v1.0/level2/08-16022313531_5aa50d89d3_o.png) ![08-16022313531_5aa50d89d3_o segmentation](thumbnails/segmentations/v1.0/level2/08-16022313531_5aa50d89d3_o.png)

![09-306039906_24c5e9600c_o image](thumbnails/images/v1.0/level2/09-306039906_24c5e9600c_o.png) ![09-306039906_24c5e9600c_o segmentation](thumbnails/segmentations/v1.0/level2/09-306039906_24c5e9600c_o.png) ![10-3761108471_08e3f9f80d_o image](thumbnails/images/v1.0/level2/10-3761108471_08e3f9f80d_o.png) ![10-3761108471_08e3f9f80d_o segmentation](thumbnails/segmentations/v1.0/level2/10-3761108471_08e3f9f80d_o.png) ![11-2389874253_759d8164ab_o image](thumbnails/images/v1.0/level2/11-2389874253_759d8164ab_o.png) ![11-2389874253_759d8164ab_o segmentation](thumbnails/segmentations/v1.0/level2/11-2389874253_759d8164ab_o.png) ![12-14452459445_1bb06c6302_o image](thumbnails/images/v1.0/level2/12-14452459445_1bb06c6302_o.png) ![12-14452459445_1bb06c6302_o segmentation](thumbnails/segmentations/v1.0/level2/12-14452459445_1bb06c6302_o.png)

![13-noah-buscher-_E-ogRrpM0s-unsplash image](thumbnails/images/v1.0/level2/13-noah-buscher-_E-ogRrpM0s-unsplash.png) ![13-noah-buscher-_E-ogRrpM0s-unsplash segmentation](thumbnails/segmentations/v1.0/level2/13-noah-buscher-_E-ogRrpM0s-unsplash.png) ![14-230501453_85963e7ee3_o image](thumbnails/images/v1.0/level2/14-230501453_85963e7ee3_o.png) ![14-230501453_85963e7ee3_o segmentation](thumbnails/segmentations/v1.0/level2/14-230501453_85963e7ee3_o.png) ![15-pexels-355020 image](thumbnails/images/v1.0/level2/15-pexels-355020.png) ![15-pexels-355020 segmentation](thumbnails/segmentations/v1.0/level2/15-pexels-355020.png) ![16-14610754861_8fd4939744_k image](thumbnails/images/v1.0/level2/16-14610754861_8fd4939744_k.png) ![16-14610754861_8fd4939744_k segmentation](thumbnails/segmentations/v1.0/level2/16-14610754861_8fd4939744_k.png)

![17-wikimedia image](thumbnails/images/v1.0/level2/17-wikimedia.png) ![17-wikimedia segmentation](thumbnails/segmentations/v1.0/level2/17-wikimedia.png) ![18-Bjornar_Moxnes image](thumbnails/images/v1.0/level2/18-Bjornar_Moxnes.png) ![18-Bjornar_Moxnes segmentation](thumbnails/segmentations/v1.0/level2/18-Bjornar_Moxnes.png) ![19-7741742246_502b485404_h image](thumbnails/images/v1.0/level2/19-7741742246_502b485404_h.png) ![19-7741742246_502b485404_h segmentation](thumbnails/segmentations/v1.0/level2/19-7741742246_502b485404_h.png) ![20-3900823607_9f9d376bb8_o image](thumbnails/images/v1.0/level2/20-3900823607_9f9d376bb8_o.png) ![20-3900823607_9f9d376bb8_o segmentation](thumbnails/segmentations/v1.0/level2/20-3900823607_9f9d376bb8_o.png)


#### Level 3

![01-johanna-buguet-9GOAzu0G4oM-unsplash image](thumbnails/images/v1.0/level3/01-johanna-buguet-9GOAzu0G4oM-unsplash.png) ![01-johanna-buguet-9GOAzu0G4oM-unsplash segmentation](thumbnails/segmentations/v1.0/level3/01-johanna-buguet-9GOAzu0G4oM-unsplash.png) ![02-29881657997_24106d0716_o image](thumbnails/images/v1.0/level3/02-29881657997_24106d0716_o.png) ![02-29881657997_24106d0716_o segmentation](thumbnails/segmentations/v1.0/level3/02-29881657997_24106d0716_o.png) ![03-felipe-sagn-2xd0_6wEj6k-unsplash image](thumbnails/images/v1.0/level3/03-felipe-sagn-2xd0_6wEj6k-unsplash.png) ![03-felipe-sagn-2xd0_6wEj6k-unsplash segmentation](thumbnails/segmentations/v1.0/level3/03-felipe-sagn-2xd0_6wEj6k-unsplash.png) ![04-nathan-dumlao-cibBnDQ9hcQ-unsplash image](thumbnails/images/v1.0/level3/04-nathan-dumlao-cibBnDQ9hcQ-unsplash.png) ![04-nathan-dumlao-cibBnDQ9hcQ-unsplash segmentation](thumbnails/segmentations/v1.0/level3/04-nathan-dumlao-cibBnDQ9hcQ-unsplash.png)

![05-old-youth-tAJog0uJkT0-unsplash image](thumbnails/images/v1.0/level3/05-old-youth-tAJog0uJkT0-unsplash.png) ![05-old-youth-tAJog0uJkT0-unsplash segmentation](thumbnails/segmentations/v1.0/level3/05-old-youth-tAJog0uJkT0-unsplash.png) ![06-olesya-yemets-AjilVpkggN8-unsplash image](thumbnails/images/v1.0/level3/06-olesya-yemets-AjilVpkggN8-unsplash.png) ![06-olesya-yemets-AjilVpkggN8-unsplash segmentation](thumbnails/segmentations/v1.0/level3/06-olesya-yemets-AjilVpkggN8-unsplash.png) ![07-azamat-zhanisov-h9Oo45soK_0-unsplash image](thumbnails/images/v1.0/level3/07-azamat-zhanisov-h9Oo45soK_0-unsplash.png) ![07-azamat-zhanisov-h9Oo45soK_0-unsplash segmentation](thumbnails/segmentations/v1.0/level3/07-azamat-zhanisov-h9Oo45soK_0-unsplash.png) ![08-claudia-owBcefxgrIE-unsplash image](thumbnails/images/v1.0/level3/08-claudia-owBcefxgrIE-unsplash.png) ![08-claudia-owBcefxgrIE-unsplash segmentation](thumbnails/segmentations/v1.0/level3/08-claudia-owBcefxgrIE-unsplash.png)

![09-8079036040_6e5d7798f5_o image](thumbnails/images/v1.0/level3/09-8079036040_6e5d7798f5_o.png) ![09-8079036040_6e5d7798f5_o segmentation](thumbnails/segmentations/v1.0/level3/09-8079036040_6e5d7798f5_o.png) ![10-calvin-lupiya-Mx4auh5zO4w-unsplash image](thumbnails/images/v1.0/level3/10-calvin-lupiya-Mx4auh5zO4w-unsplash.png) ![10-calvin-lupiya-Mx4auh5zO4w-unsplash segmentation](thumbnails/segmentations/v1.0/level3/10-calvin-lupiya-Mx4auh5zO4w-unsplash.png) ![11-artyom-kim-zEa75CRX88M-unsplash image](thumbnails/images/v1.0/level3/11-artyom-kim-zEa75CRX88M-unsplash.png) ![11-artyom-kim-zEa75CRX88M-unsplash segmentation](thumbnails/segmentations/v1.0/level3/11-artyom-kim-zEa75CRX88M-unsplash.png) ![12-jordan-bauer-Is3VRzUaXVk-unsplash image](thumbnails/images/v1.0/level3/12-jordan-bauer-Is3VRzUaXVk-unsplash.png) ![12-jordan-bauer-Is3VRzUaXVk-unsplash segmentation](thumbnails/segmentations/v1.0/level3/12-jordan-bauer-Is3VRzUaXVk-unsplash.png)

![13-alex-iby-470eBDOc8bk-unsplash image](thumbnails/images/v1.0/level3/13-alex-iby-470eBDOc8bk-unsplash.png) ![13-alex-iby-470eBDOc8bk-unsplash segmentation](thumbnails/segmentations/v1.0/level3/13-alex-iby-470eBDOc8bk-unsplash.png) ![14-andrew-robinson-4ar-CSxLcMg-unsplash image](thumbnails/images/v1.0/level3/14-andrew-robinson-4ar-CSxLcMg-unsplash.png) ![14-andrew-robinson-4ar-CSxLcMg-unsplash segmentation](thumbnails/segmentations/v1.0/level3/14-andrew-robinson-4ar-CSxLcMg-unsplash.png) ![15-8717570008_edc9120e59_o image](thumbnails/images/v1.0/level3/15-8717570008_edc9120e59_o.png) ![15-8717570008_edc9120e59_o segmentation](thumbnails/segmentations/v1.0/level3/15-8717570008_edc9120e59_o.png) ![16-gabriel-silverio-u3WmDyKGsrY-unsplash image](thumbnails/images/v1.0/level3/16-gabriel-silverio-u3WmDyKGsrY-unsplash.png) ![16-gabriel-silverio-u3WmDyKGsrY-unsplash segmentation](thumbnails/segmentations/v1.0/level3/16-gabriel-silverio-u3WmDyKGsrY-unsplash.png)

![17-6262243021_47792d9ca0_o image](thumbnails/images/v1.0/level3/17-6262243021_47792d9ca0_o.png) ![17-6262243021_47792d9ca0_o segmentation](thumbnails/segmentations/v1.0/level3/17-6262243021_47792d9ca0_o.png) ![18-16585637733_67b0e18bcf_o image](thumbnails/images/v1.0/level3/18-16585637733_67b0e18bcf_o.png) ![18-16585637733_67b0e18bcf_o segmentation](thumbnails/segmentations/v1.0/level3/18-16585637733_67b0e18bcf_o.png) ![19-1824233430_59f1a20f0d_o image](thumbnails/images/v1.0/level3/19-1824233430_59f1a20f0d_o.png) ![19-1824233430_59f1a20f0d_o segmentation](thumbnails/segmentations/v1.0/level3/19-1824233430_59f1a20f0d_o.png) ![20-3683799501_052eb48752_o image](thumbnails/images/v1.0/level3/20-3683799501_052eb48752_o.png) ![20-3683799501_052eb48752_o segmentation](thumbnails/segmentations/v1.0/level3/20-3683799501_052eb48752_o.png)

## License
The Creative Commons Attribution 4.0 International License applies solely to the segmentation images that we have created. It does not apply to any third-party data or information that we may have used in the creation of our segmentation. We make no claims or guarantees regarding the accuracy, completeness, or legality of any third-party data or information that may have been used in our data, and we disclaim any liability for any damages or losses that may result from the use or reliance on such third-party data or information.

## Citation

If you use the _NPRportrait-segmentation_ dataset provided in this repository, please cite it as below:

```bibtex
@misc{Bultemeier_NPRportrait-segmentation,
  author = {Bültemeier, Julian and Meier, Philip and Lohweg, Volker},
  doi    = {10.5281/zenodo.7852139},
  title  = {{NPRportrait-segmentation}},
  url    = {https://github.com/pystiche/NPRportrait-segmentation}
}
```

Please don't forget to cite the original work by Rosin et al. as well:

### [_NPRportrait 0.1_](https://dl.acm.org/doi/10.1145/3092919.3092921)

```bibtex
@inproceedings{10.1145/3092919.3092921,
  author     = {Rosin, Paul L. and Mould, David and Berger, Itamar and Collomosse, John and Lai, Yu-Kun and Li, Chuan and Li, Hua and Shamir, Ariel and Wand, Michael and Wang, Tinghuai and Winnem\"{o}ller, Holger},
  title      = {Benchmarking Non-Photorealistic Rendering of Portraits},
  year       = {2017},
  isbn       = {9781450350815},
  publisher  = {Association for Computing Machinery},
  address    = {New York, NY, USA},
  url        = {https://doi.org/10.1145/3092919.3092921},
  doi        = {10.1145/3092919.3092921},
  abstract   = {We present a set of images for helping NPR practitioners evaluate their image-based portrait stylisation algorithms. Using a standard set both facilitates comparisons with other methods and helps ensure that presented results are representative. We give two levels of difficulty, each consisting of 20 images selected systematically so as to provide good coverage of several possible portrait characteristics. We applied three existing portrait-specific stylisation algorithms, two general-purpose stylisation algorithms, and one general learning based stylisation algorithm to the first level of the benchmark, corresponding to the type of constrained images that have often been used in portrait-specific work. We found that the existing methods are generally effective on this new image set, demonstrating that level one of the benchmark is tractable; challenges remain at level two. Results revealed several advantages conferred by portrait-specific algorithms over general-purpose algorithms: portrait-specific algorithms can use domain-specific information to preserve key details such as eyes and to eliminate extraneous details, and they have more scope for semantically meaningful abstraction due to the underlying face model. Finally, we provide some thoughts on systematically extending the benchmark to higher levels of difficulty.},
  booktitle  = {Proceedings of the Symposium on Non-Photorealistic Animation and Rendering},
  articleno  = {11},
  numpages   = {12},
  keywords   = {image stylisation, evaluation, portraits, non-photorealistic rendering},
  location   = {Los Angeles, California},
  series     = {NPAR '17},
}
```

### [_NPRportrait 1.0_](https://doi.org/10.1007/s41095-021-0255-3)

```bibtex
@article{Rosin2022,
  title    = {NPRportrait 1.0: A three-level benchmark for non-photorealistic rendering of portraits},
  author   = {Rosin, Paul L and Lai, Yu-Kun and Mould, David and Yi, Ran and Berger, Itamar and Doyle, Lars and Lee, Seungyong and Li, Chuan and Liu, Yong-Jin and Semmo, Amir and others},
  journal  = {Computational Visual Media},
  volume   = {8},
  number   = {3},
  pages    = {445--465},
  year     = {2022},
  abstract = {Recently, there has been an upsurge of activity in image-based non-photorealistic rendering (NPR), and in particular portrait image stylisation, due to the advent of neural style transfer (NST). However, the state of performance evaluation in this field is poor, especially compared to the norms in the computer vision and machine learning communities. Unfortunately, the task of evaluating image stylisation is thus far not well defined, since it involves subjective, perceptual, and aesthetic aspects. To make progress towards a solution, this paper proposes a new structured, three-level, benchmark dataset for the evaluation of stylised portrait images. Rigorous criteria were used for its construction, and its consistency was validated by user studies. Moreover, a new methodology has been developed for evaluating portrait stylisation algorithms, which makes use of the different benchmark levels as well as annotations provided by user studies regarding the characteristics of the faces. We perform evaluation for a wide variety of image stylisation methods (both portrait-specific and general purpose, and also both traditional NPR approaches and NST) using the new benchmark dataset.},
  url      = {https://doi.org/10.1007/s41095-021-0255-3},
  doi      = {10.1007/s41095-021-0255-3},
}
```
