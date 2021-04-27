# BML Makefile

# Just a snippet to stop executing under other make(1) commands
# that won't understand these lines
ifneq (,)
This makefile requires GNU Make.
endif

# OS specific section
ifeq '$(findstring WINDOWS,$(ComSpec))' 'WINDOWS'
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

# BML executables
BML2BSS := bml2bss
BML2HTML := bml2html
BML2LATEX := bml2latex
BML_MAKEDEPEND := bml_makedepend

# BML flags
BML_FLAGS =

BML2BSS_FLAGS = $(BML_FLAGS)
BML2HTML_FLAGS = $(BML_FLAGS)
BML2LATEX_FLAGS = $(BML_FLAGS)
BML_MAKEDEPEND_FLAGS = $(BML_FLAGS)

# LaTeX executable/flags
LATEXMK := latexmk
LATEXMK_FLAGS := -pdf

# Input files
INPUT_FILES := $(wildcard *.bml)

# Output files
BSS_FILES    := $(patsubst %.bml, %.bss, $(INPUT_FILES))
HTM_FILES 	 := $(patsubst %.bml, %.htm, $(INPUT_FILES))
LATEX_FILES  := $(patsubst %.bml, %.tex, $(INPUT_FILES))
PDF_FILES  := $(patsubst %.tex, %.pdf, $(LATEX_FILES))
OUTPUT_FILES := $(BSS_FILES) $(HTM_FILES) $(LATEX_FILES) $(PDF_FILES)

# Dependency files
MK_FILES  := $(patsubst %.bml, %.mk, $(INPUT_FILES))

# target: all - Build all output files.
all: .depend $(OUTPUT_FILES)

# target: help - Display callable targets.
help:
	@perl -ne "foreach (m/^# target: (.+)/) { print; print qq(\n) }" $(MAKEFILE_LIST)

# target: depend - Generate dependency include file.
depend: .depend

.depend:  $(MK_FILES)
	@$(CAT) $? 1>$@ 2>$(NOWHERE)

-include .depend

# These are the pattern matching rules. In addition to the automatic
# variables used here, the variable $* that matches whatever % stands for
# can be useful in special cases.
%.bss: %.bml
	$(BML2BSS) $(BML2BSS_FLAGS) -o $@ $< 

%.htm: %.bml
	$(BML2HTML) $(BML2HTML_FLAGS) -o $@ $< 

%.tex: %.bml
	$(BML2LATEX) $(BML2LATEX_FLAGS) -o $@ $< 

%.pdf: %.tex
	$(LATEXMK) $(LATEXMK_FLAGS) $< 

%.mk: %.bml
	@$(BML_MAKEDEPEND) $(BML_MAKEDEPEND_FLAGS) -o $@ $< 

# target: clean - Cleanup output files and dependency include file.
clean:
	@$(RM_F) .depend $(OUTPUT_FILES) $(MK_FILES)
	@-$(LATEXMK) -C -f $(LATEX_FILES) 2>$(NOWHERE)

.PHONY: all help depend clean
