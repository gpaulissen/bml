## -*- mode: make -*-

GIT = git
PYTHON = python
MYPY = mypy
PIP = pip
PROJECT = bridge-markup

# OS specific section
ifeq '$(findstring ;,$(PATH))' ';'
    detected_OS := Windows
    HOME = $(USERPROFILE)
else
    detected_OS := $(shell uname 2>/dev/null || echo Unknown)
    detected_OS := $(patsubst CYGWIN%,Cygwin,$(detected_OS))
    detected_OS := $(patsubst MSYS%,MSYS,$(detected_OS))
    detected_OS := $(patsubst MINGW%,MSYS,$(detected_OS))
endif

ifdef CONDA_PREFIX
    home = $(CONDA_PREFIX)
else
    home = $(HOME)
endif

ifeq ($(detected_OS),Windows)
    RM_EGGS = pushd $(home) && del /s/q $(PROJECT).egg-link $(PROJECT)-nspkg.pth
else
    RM_EGGS = { cd $(home) && find . \( -name $(PROJECT).egg-link -o -name $(PROJECT)-nspkg.pth \) -print -exec rm -i "{}" \; ; } 2>/dev/null
endif

.PHONY: clean install test dist distclean upload

clean:
	$(PYTHON) setup.py clean --all
	-$(RM_EGGS)
	$(PYTHON) -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
	$(PYTHON) -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"
	$(PYTHON) -Bc "import shutil; import os; [shutil.rmtree(d) for d in ['.pytest_cache', '.mypy_cache', 'dist', 'htmlcov', '.coverage'] if os.path.isdir(d)]"
	cd test/data && $(MAKE) -f ../../bml.mk clean
	cd test/expected && $(MAKE) -f ../../bml.mk clean

install: clean
	$(PIP) install -e .
	$(PIP) install -r test_requirements.txt

test:
	$(MYPY) --show-error-codes src
	$(PYTHON) -m pytest --exitfirst

dist: install test
	$(PYTHON) -m build
	$(PYTHON) -m twine check dist/*

upload_test: dist
	$(PYTHON) -m twine upload --repository testpypi dist/*

upload: dist
	$(PYTHON) -m twine upload dist/*

# This is GNU specific I guess
VERSION = $(shell $(PYTHON) __about__.py)

TAG = v$(VERSION)

tag:
	git tag -a $(TAG) -m "$(TAG)"
	git push origin $(TAG)
