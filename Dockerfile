FROM miktex/miktex:latest
#FROM ubuntu:latest
#FROM node:alpine

LABEL Description="Dockerized BML" Vendor="Gert-Jan Paulissen"

RUN    apt-get update &&\ 
    	 apt-get install -y --no-install-recommends \ 
							 python3 \
							 python3-pip \
							 python3-setuptools \
			 # smoke tests
  		 && make --version \
  		 && perl --version \
  		 && python3 --version \
  		 && pip3 --version \
  		 && mpm --version

# This is bml root directory
WORKDIR /bml

COPY . .

# install BML and test that the executables are there
RUN pip3 install -e . && \
		which bml2bss bml2html bml2latex bss2bml bml_makedepend

RUN    miktexsetup finish \
    && initexmf --admin --set-config-value=[MPM]AutoInstall=1

RUN    mpm --admin --install=expl3 || true

RUN    mpm --admin --update-db \
    && initexmf --admin --update-fndb
		
# generate some PDFs to have a complete MiKTeX installation
RUN cd /bml/test/expected && \
		make -i -f /bml/bml.mk example.pdf example-tree.pdf && \
		make -f /bml/bml.mk clean && \
		find / \( -name dirtree.sty -o -name pdflatex.log \) -ls

ENTRYPOINT ["/entrypoint.sh"]

# This is the place where input files are expected and where we run make from
WORKDIR /miktex/work

# Default target
CMD ["help"]
