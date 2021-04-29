#FROM miktex/miktex:latest
#FROM ubuntu:latest
FROM node:alpine

LABEL Description="Dockerized BML" Vendor="Gert-Jan Paulissen"

# Install perl, wget and libraries needed for TinyTeX (https://yihui.org/tinytex/)
# Install python3
RUN apk update &&\
    apk upgrade &&\
    apk add --no-cache perl wget fontconfig freetype gnupg make python3 py3-pip py3-setuptools su-exec

# Install TinyTex in a separate RUN due to the 'wget ... | sh' construction
RUN wget -qO- "https://yihui.org/tinytex/install-bin-unix.sh" | sh

ENV PATH="${PATH}:/root/bin"

# This is bml root directory
WORKDIR /bml

COPY . .
    
# 1) install missing LaTeX packages
# 2) generate some PDFs to test a complete LaTeX installation
# 3) install BML and test that the executables are there
# 4) test that they are there
# 5) create user bml and modify permissions for /bml
RUN tlmgr install dirtree listliketab parskip pbox txfonts &&\
    latexmk -pdf -output-directory=/tmp /bml/test/expected/*.tex &&\
    pip3 install -e . &&\
    which bml2bss bml2html bml2latex bss2bml bml_makedepend &&\
    addgroup -S bml && adduser -S -G bml bml && chown -R bml:bml /bml && chmod -R 755 /bml

ENTRYPOINT ["/bml/entrypoint.sh"]

# This is the place where input files are expected and where we run make from
WORKDIR /bml/files

USER bml:bml

# Default command
CMD ["make", "-f", "/bml/bml.mk", "help"]
