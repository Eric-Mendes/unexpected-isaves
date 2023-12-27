# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2023-12-27
### Refactored
- `to_excel` and `to_rubiks` were refactored amounting in a 1.31x and a 1.37x speedup, respectively.

## [2.1.4] - 2023-10-25
### Added
- Now we support Minecraft versions `1.20.1` and `1.20.2`

## [2.1.3] - 2023-07-25
### Added
- Now we support Minecraft version `1.20.0`

## [2.1.2] - 2023-04-17
### Added
- Now we support Minecraft version `1.19.4`

### Fixed
- `blocks.json` file

## [2.1.1] - 2023-04-04
### Fixed
- `__to_minecraft_save()` res type

## [2.1.0] - 2023-03-01
### Added
- `to_rubiks()` function.

## [2.0.3] - 2023-02-26
### Added
- ascii tag on pypi. 

## [2.0.2] - 2023-02-05
### Changed
- docs: used Google's guidelines for docstrings. See: https://google.github.io/styleguide/pyguide.html#383-functions-and-methods.

## [2.0.1] - 2023-02-05
### Fixed
- docs: updated package's short description.

## [2.0.0] - 2023-02-05
### Added
- `to_ascii()` function.

## [1.5.1] - 2023-02-02
### Changed
- Refactored `README.md`.

## [1.5.0] - 2023-01-31
### Changed
- `image` arg now accepts `str`.

## [1.4.0] - 2023-01-04
### Added
- `to_excel()`: added `image_position` parameter. 

## [1.3.0] - 2023-01-03
### Added
- Added support for different minecraft versions.

### Changed
- Moved metadata to `pyproject.toml`. See https://github.com/pypa/sampleproject/pull/166.

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
