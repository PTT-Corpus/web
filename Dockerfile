FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install mercurial bison flex libwww-perl subversion libpcre3 libpcre3-dev libgtk2.0-dev -y
# RUN pip install --upgrade pip
# ADD requirements.txt /tmp
# ADD Pipfile /tmp
# ADD Pipfile.lock /tmp


# WORKDIR /tmp
# RUN pip3 install --no-cache-dir -r requirements.txt
# RUN pip3 install pipenv && pipenv install

# Download CWB & CWB-PERL from SVN
RUN svn co http://svn.code.sf.net/p/cwb/code/cwb/trunk /cwb
RUN svn co http://svn.code.sf.net/p/cwb/code/perl/trunk /cwb-perl

# Install CWB
WORKDIR /cwb/
RUN ./install-scripts/config-basic
RUN ./install-scripts/install-linux
RUN mv /usr/local/cwb-* /usr/local/cwb
ENV PATH="/usr/local/cwb/bin:${PATH}"

# Install CWB-PERL
WORKDIR /cwb-perl/CWB
RUN perl Makefile.PL
RUN make
RUN make test; exit 0
RUN make install

WORKDIR /app
ADD ./cwb-python-0.2.2 /app/cwb-python-0.2.2

RUN pip install Cython
WORKDIR /app/cwb-python-0.2.2
ENV CWB_DIR=/usr/local/cwb
RUN python setup.py build
RUN python setup.py install

WORKDIR /app
ADD ./requirements.txt /app
RUN mkdir -p cwb/vrt cwb/registry cwb/data cwb/results
RUN pip install -r requirements.txt

ADD . /app

# CMD ["./start.sh"]
