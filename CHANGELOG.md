# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.4] - 2022-02-09
### Changed
- Deleted readme's mention to the function `image_utilities.fit_to_palette(image: Image, palette: List[RGBColor]) -> Image`.

### Deprecated
- `image_utilities.fit_to_palette(image: Image, palette: List[RGBColor]) -> Image` function because it is too slow and `PIL` already has the [`Image.quantize()`](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.quantize) function, which I'm sure that it does the job way better than our simple `fit_to_palette`.
    - Note: the function is still usable, but now it prints a warning letting the user know that it shouldn't be used.

## [1.1.3] - 2022-02-09
### Added
- Github Actions workflows for automated building & distribution of the package.

### Changed
- [@Eric-Mendes](https://github.com/Eric-Mendes) finally settled for a versioning style: it should be `n1.n2.n3` where `n1` is for new feature added; `n2` is for enhacements on pre-existing code & documentation; and `n3` is for fixes, style changes & refactors.
