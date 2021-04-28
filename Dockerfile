FROM miktex/miktex:latest
#FROM ubuntu:latest
#FROM node:alpine

LABEL Description="Dockerized BML" Vendor="Gert-Jan Paulissen"

#RUN    apt-get update \ 
#    && apt-get install -y --no-install-recommends \ 
#           apt-transport-https \ 
#           ca-certificates \ 
#           dirmngr \ 
#           ghostscript \ 
#           gnupg \ 
#           make \ 
#           perl \ 
#						python \ 
#						miktex 
# 
# 
# RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys D6BC243565B2087BC3F897C9277A7293F59E4889
# RUN echo "deb http://miktex.org/download/ubuntu focal universe" | tee /etc/apt/sources.list.d/miktex.list
#
# RUN    apt-get update \
#    && apt-get install -y --no-install-recommends \
#           miktex
# 
# RUN    miktexsetup finish \ 
#    && initexmf --admin --set-config-value=[MPM]AutoInstall=1 \ 
#    && mpm --admin --update-db \ 
#    && mpm --admin \ 
#           --install amsfonts \ 
#           --install biber-linux-x86_64 \ 
#    && initexmf --admin --update-fndb 

RUN    apt-get update \ 
    && apt-get install -y --no-install-recommends \ 
							 python3 \
							 python3-pip \
  		 # smoke tests
  		 && make --version \
  		 && perl --version \
  		 && python3 --version \
  		 && pip3 --version \
  		 && mpm --version

WORKDIR /bml

COPY . .

# 1) install BML and test that the executables are there
# 2) Let latexmk do its work.
# 3) Unset AutoInstall for MiKTeX
RUN pip3 install -e . && which bml2bss bml2html bml2latex bss2bml bml_makedepend && \
    make -f bml.mk BML2LATEX_FILES="`ls -1 test/expected/*.tex`" all && \
		initexmf --admin --set-config-value=[MPM]AutoInstall=0

ENTRYPOINT ["entrypoint.sh", "echo", "make", "-f", "/bml/bml.mk"]

WORKDIR /bml/files

RUN groupadd bml && useradd bml -g bml && chown -R bml:bml /bml && chmod -R 755 /bml

USER bml:bml

# Default target
CMD ["help"]
