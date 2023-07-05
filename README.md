<h1 align="center">KelPy</h1>
<p align="center">
<a href="https://img.shields.io/github/last-commit/Barnacle-Foods/barnacle-imagery"><img alt="Last Commit" src="https://img.shields.io/github/last-commit/Barnacle-Foods/barnacle-imagery"></a>
<a href="https://img.shields.io/github/languages/top/Barnacle-Foods/barnacle-imagery"><img alt="Action Status" src="https://img.shields.io/github/languages/top/Barnacle-Foods/barnacle-imagery"></a>
<a href="https://img.shields.io/github/issues/Barnacle-Foods/barnacle-imagery"><img alt="Issues" src="https://img.shields.io/github/issues/Barnacle-Foods/barnacle-imagery"></a>
<a href="https://img.shields.io/github/v/release/Barnacle-Foods/barnacle-imagery"><img alt="GitHub Release" src="https://img.shields.io/github/v/release/Barnacle-Foods/barnacle-imagery">
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://img.shields.io/github/license/Barnacle-Foods/barnacle-imagery"><img alt="License" src="https://img.shields.io/github/license/Barnacle-Foods/barnacle-imagery"></a>
</p>

<p align="center">A tool that streamlines orthorectification and kelp identification in a simple to use interface.</p>

## Installation

You must have [OpenDroneMap](https://github.com/OpenDroneMap/ODM) installed locally on Windows to run KelPy.
  

### Flags and variables

  Image Folder - Directory where your drone images are stored.

  Results Folder - Directory where you want to store the results.

  Pixel Buffer - [A glint-mask-generator flag](https://github.com/HakaiInstitute/GlintMaskGenerator). Default is 5. Higher values take more processing time. 
  
  Quality - [ODM option](https://docs.opendronemap.org/arguments/pc-quality/) to determine quality of the orthomosaic generated. Default is high. Higher values take more processing power.

  Crop -  [ODM option](https://docs.opendronemap.org/arguments/crop/) to crop dataset boundaries. Default is 0.

  Feature-type algorithm - [ODM option](https://docs.opendronemap.org/arguments/feature-type/) to determine feature types. Default is sift. 

  Species classification - [Kelp-o-matic](https://hakai-segmentation.readthedocs.io/en/latest/lib.html#module-hakai_segmentation) option to determine whether or not to differentiate between bullkelp and giantkelp.


### Flags for independent identification

  Orthomosaic File - The orthomosaic image you want to process.

  Results Folder - The folder you want to save your results to.

  GSD (Ground Sampling Distance) - Sampling distance calculated in the orthorectification step. Should be located in the ODM report.



## Acknowledgement

  This application uses code from the following repositories:

  https://github.com/HakaiInstitute/GlintMaskGenerator

  https://github.com/HakaiInstitute/kelp-o-matic

  https://github.com/OpenDroneMap/NodeODM
