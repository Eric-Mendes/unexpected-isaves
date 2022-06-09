# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
### Added
- Simple Docker app for local use without installing the package.
- Read The Docs page.

## [1.2.2] - 2022-03-22
### Changed
- Now accepting Python 3.8 as this works just fine with it as well.

## [1.2.1] - 2022-03-22
### Changed
- `README.md` now's got examples and a logo on it.

## [1.2.0] - 2022-03-02
### Added
- Project's goal on `README.md`.

### Changed
- [@radarhere](https://github.com/radarhere) refactored code, mainly the `to_minecraft` function.
- Package's short description for SEO optimization (again).

## [1.1.5] - 2022-02-10
### Changed
- Package description for SEO optimization.

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
- [@Eric-Mendes](https://github.com/Eric-Mendes) finally "learned" semver.
