# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
