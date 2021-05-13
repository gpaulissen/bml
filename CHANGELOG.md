# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.6.1] - 2021-05-13

### Changed

  - A bidding table where a bid has more than one description line and
    the last description line is just a point, will convert that last
    description line into an empty line, see issue [Blank & Comment Line](https://github.com/gpaulissen/bml/issues/7)

## [2.6.0] - 2021-05-10

### Added

  - Added string representation of class Args so the default arguments can be tested
  - The output file may also be a directory
  - A bidding table line with a single point is ignored, see issue [Blank & Comment Line](https://github.com/gpaulissen/bml/issues/7)
  - Extra logging will help in detecting this [Puzzling indentation error](https://github.com/gpaulissen/bml/issues/12)

## [2.5.1] - 2021-05-06

### Changed

  - Moved module about.py to the src/bml directory because it was missing in the distribution.

### Changed

  - Issue [Bold description #4](https://github.com/gpaulissen/bml/issues/4)   
  - Issue [Printing a bidding table in HTML loses the tree
  - decoration.](https://github.com/gpaulissen/bml/issues/10

## [2.5.0] - 2021-05-05

### Added

  - Added --version option to command line.
  - Added pretty printing HTML.

### Changed

  - Issue [Bold description #4](https://github.com/gpaulissen/bml/issues/4)   
  - Issue [Printing a bidding table in HTML loses the tree decoration.](https://github.com/gpaulissen/bml/issues/10)

## [2.4.0] - 2021-04-30

### Added

  - Added latexmk to README.
  - Added bml_makedepend utility.
  - Added tests for bml_makedepend utility.
  - Added Make file bml.mk.
  - Added Docker files.
  - BML utility modules (bml2bss, bml2html, bml2latex, bss2bml, bml_makedepend) can now be run from Python as a script.
  - Indentation option is suppressed for bml2bss, bss2bml and bml_makedepend.

### Changed

  - Installation moved from README to my blog site.
  - Testing tree generation for HTML and LaTeX.
  - Handling of command line arguments enhanced.
  
## [2.3.0] - 2021-04-20

### Changed
  - Added BSS syntax to README.
  - README enhanced for non-HTML tags like <bid> <description>.
  - Variable suits also correctly translated for their bids.
  - bss2bml utility added.
  
## [2.2.1] - 2021-04-15

### Changed
  - README enhanced for variable suits.

## [2.2.0] - 2021-04-15

### Changed
  - Two More Variable Colours (issue #1)
  - Things for newbies to do (issue #3)
  - Some characters have a special meaning for LaTeX (issue #8)

## [2.0.3] - 2021-03-21

### Changed

  - Updated the README with respect to the command line options.

## [2.0.2] - 2021-03-19

### Changed

  - README.md and README.org merged to README.md.

## [2.0.1] - 2021-03-19

### Added

  - Python package now correctly includes external files bml.css and bml.tex.

### Changed

  - README.md now links correctly to README.org for a Python package.
  - Replaced test package pytest-cover by pytest-cov (pytest-cover has been merged back into pytest-cov 2.0).

## [2.0.0] - 2021-03-18

### Added

  - Applied Python best practices.
  - Uploading to PyPi as package bridge-markup.
