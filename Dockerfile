#FROM miktex/miktex:latest
#FROM ubuntu:latest
FROM node:alpine

LABEL Description="Dockerized BML" Vendor="Gert-Jan Paulissen"

# 1) Install:
#	   - perl, wget and libraries needed for TinyTeX (https://yihui.org/tinytex/)
#		 - make
#    - python3
#		 - su-exec
# 2) Create user bml and show its details
RUN apk update && apk upgrade && apk add --no-cache perl wget fontconfig freetype gnupg make python3 py3-pip py3-setuptools su-exec &&\
    addgroup -S bml && adduser -S -G bml bml && getent passwd bml

# This is bml root directory
WORKDIR /bml
	
COPY . .

# Install TinyTeX as bml
USER bml

# Prepare to install TinyTeX system wide (see https://yihui.org/tinytex/faq/)
RUN wget -qO- "https://yihui.org/tinytex/install-unx.sh" | sh -s - --admin --no-path

# Back to root to continue with some tasks
USER root

# 1) install TinyTeX in /usr/local/bin
# 2) install BML and test that the executables are there
# 3) modify permissions for /bml
RUN ~bml/.TinyTeX/bin/*/tlmgr path add &&\
    pip3 install -e . && which bml2bss bml2html bml2latex bss2bml bml_makedepend &&\
    chown -R bml:bml . && chmod -R 755 .
		
USER bml

# 1) Install missing LaTeX packages (by looking at errors from next statement)
# 2) Generate some PDFs to test a complete LaTeX installation
RUN tlmgr install dirtree listliketab parskip pbox txfonts &&\
    latexmk -pdf -output-directory=/tmp /bml/test/expected/example.tex /bml/test/expected/example-tree.tex

ENTRYPOINT ["/bml/entrypoint.sh"]

# This is the place where input files are expected and where we run make from
WORKDIR /bml/files

# Default command
CMD ["make", "-f", "/bml/bml.mk", "help"]
