# BML Makefile

# Just a snippet to stop executing under other make(1) commands
# that won't understand these lines
ifneq (,)
This makefile requires GNU Make.
endif

# Disable built-in rules and variables plus clean the suffix rules
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables

.SUFFIXES:

# OS specific section (see https://stackoverflow.com/questions/714100/os-detecting-makefile/52062069#52062069)
ifeq '$(findstring ;,$(PATH))' ';'
    detected_OS := Windows
else
    detected_OS := $(shell uname 2>/dev/null || echo Unknown)
    detected_OS := $(patsubst CYGWIN%,Cygwin,$(detected_OS))
    detected_OS := $(patsubst MSYS%,MSYS,$(detected_OS))
    detected_OS := $(patsubst MINGW%,MSYS,$(detected_OS))
endif

ifeq ($(detected_OS),Windows)
    CAT := type
    RM_F := del /q
    NOWHERE := nul
else
    CAT := cat
    RM_F := rm -f
    NOWHERE := /dev/null
endif

BML_HOME := /bml

# BML executables
BML2BSS := bml2bss
BML2HTML := bml2html
BML2LATEX := bml2latex
BML_MAKEDEPEND := bml_makedepend

# BML flags
BML_OPTIONS :=

BML2BSS_OPTIONS := $(BML_OPTIONS)
BML2HTML_OPTIONS := $(BML_OPTIONS)
BML2LATEX_OPTIONS := $(BML_OPTIONS)
BML_MAKEDEPEND_OPTIONS := $(BML_OPTIONS)

# LaTeX executable/flags
LATEXMK := latexmk
LATEXMK_OPTIONS := -pdf -verbose -latexoption=-verbose
#LATEXMK_OPTIONS := -pdf

# Input files
INPUT_FILES := $(wildcard *.bml)

# Output files
BSS_FILES    := $(patsubst %.bml, %.bss, $(INPUT_FILES))
HTM_FILES 	 := $(patsubst %.bml, %.htm, $(INPUT_FILES))
LATEX_FILES  := $(patsubst %.bml, %.tex, $(INPUT_FILES))
PDF_FILES    := $(patsubst %.tex, %.pdf, $(LATEX_FILES))
OUTPUT_FILES := $(BSS_FILES) $(HTM_FILES) $(LATEX_FILES) $(PDF_FILES)

# Dependency files
MK_FILES     := $(patsubst %.bml, %.mk, $(INPUT_FILES))

-include $(MK_FILES)

all: $(OUTPUT_FILES) ## Build all output files.

help: ## This help.
	@perl -ne 'printf(qq(%-30s  %s\n), $$1, $$2) if (m/^([a-zA-Z_-]+):.*##\s*(.*)$$/)' $(MAKEFILE_LIST)

docker-info: ## Show various Docker container information like current directory, contents of /bml, environment variables.
	@echo "=== Docker info ==="
	@echo "=== Current directory ==="; pwd
	@echo "=== Contents of /bml ==="; find $(BML_HOME) -print
	@for e in latexmk; do echo "=== Executable $$e ==="; which $$e; done
	@echo "=== set ==="; set
	@echo "=== The END ==="

# These are the pattern matching rules. In addition to the automatic
# variables used here, the variable $* that matches whatever % stands for
# can be useful in special cases.
%.bss: %.bml
	$(BML2BSS) $(BML2BSS_OPTIONS) -o $@ $< 

%.htm: %.bml
	$(BML2HTML) $(BML2HTML_OPTIONS) -o $@ $< 

%.tex: %.bml
	$(BML2LATEX) $(BML2LATEX_OPTIONS) -o $@ $< 

%.pdf: %.tex
	$(LATEXMK) $(LATEXMK_OPTIONS) $< 

%.mk: %.bml
	$(BML_MAKEDEPEND) $(BML_MAKEDEPEND_OPTIONS) -o $@ $< 

clean: ## Cleanup output files.
	-$(LATEXMK) -C -f $(wildcard *.tex) 2>$(NOWHERE)
	$(RM_F) $(wildcard *.bss *.htm *.tex *.pdf)

distclean: clean ## Runs clean first and then cleans up dependency include files. 
	$(RM_F) $(wildcard *.mk)

.PHONY: all help docker-info clean distclean

