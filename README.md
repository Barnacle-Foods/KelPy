# barnacle-imagery
An application that streamlines orthorectification and kelp area calculation in a simple to use application.

---

### Installation

Before installing, you must have a NodeODM node running locally via:

```sh
  $ docker run -ti -p 3000:3000 opendronemap/nodeodm
```
After this, you are ready to go!

### Flags and variables

Image Folder - Directory where your drone images are stored.
Results Folder - Directory where you want to store the results.
Pixel Buffer - A glint-mask-generator flag. Default is 5. [Link](https://github.com/HakaiInstitute/GlintMaskGenerator)
Quality - ODM option to determine quality of the orthomosaic generated. Default is high. [Link](https://docs.opendronemap.org/arguments/pc-quality/)
Crop - ODM option to crop dataset boundaries. Default is 0. [Link](https://docs.opendronemap.org/arguments/crop/)
Feature-type algorithm - ODM option to determine feature types. Default is sift. [Link](https://docs.opendronemap.org/arguments/feature-type/)
Species classification - Use species classification. [Link](https://hakai-segmentation.readthedocs.io/en/latest/lib.html#module-hakai_segmentation)

## Flags for independent identification
Orthomosaic File - The orthomosaic image you want to process.
Results Folder - The folder you want to save your results to.
GSD (Ground Sampling Distance) - Sampling distance calculated in the orthorectification step. Should be located in the ODM report.

### Acknowledgment

This application uses the following repositories:
https://github.com/HakaiInstitute/GlintMaskGenerator
https://github.com/HakaiInstitute/hakai-segmentation
https://github.com/OpenDroneMap/NodeODM
