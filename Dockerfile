# Copyright 2020 Efabless Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# syntax = docker/dockerfile:1.0-experimental
FROM centos:centos6 as build

# Common development tools and libraries (kitchen sink approach)
RUN yum -y install centos-release-scl && \
    yum -y install devtoolset-8 devtoolset-8-libatomic-devel

# python 3.6
RUN yum install -y https://repo.ius.io/ius-release-el6.rpm
RUN yum install -y python36u python36u-libs python36u-devel python36u-pip python36u-tkinter
RUN alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 60

RUN pip3.6 install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \ 
                pyyaml \
                awscli \
                requests \
                boto3

# magic dependencies
RUN yum install -y csh wget tcl-devel tk-devel libX11-devel cairo-devel ncurses-devel

#General utils
RUN yum install -y tcllib git tcl tk libjpeg libgomp libXext libSM libXft libffi cairo gettext Xvfb  && \
	yum clean all && \
	rm -rf /var/cache/yum

RUN git clone git://opencircuitdesign.com/magic magic_15102020

WORKDIR magic_15102020

RUN git checkout 4bbe4ef74e5eac98c503bf6483ee7a40dbb0547a

# build
RUN ./configure --prefix=/build && \
    make -j4 && \
    make install


ENV PRECHECKER_ROOT=/usr/local/bin/
ENV BUILD_PATH=/build/

ENV PATH=$PRECHECKER_ROOT:$PRECHECKER_ROOT/scripts:$BUILD_PATH/bin:$BUILD_PATH/bin/Linux-x86_64:$BUILD_PATH/pdn/scripts:$PATH
ENV LD_LIBRARY_PATH=$BUILD_PATH/lib:$BUILD_PATH/lib/Linux-x86_64:$LD_LIBRARY_PATH
ENV MANPATH=$BUILD_PATH/share/man:$MANPATH


RUN mkdir -p /build/version/

RUN date +"Build Timestamp: %Y-%m-%d_%H-%M-%S" > /build/version/magic.version
RUN git rev-parse HEAD >> /build/version/magic.version
RUN tar -czf /build.tar.gz /build

WORKDIR $PRECHECKER_ROOT

COPY scripts/ /usr/local/bin/
