FROM debian:stretch-slim

RUN apt-get update && \
    apt-get install -y build-essential cmake git wget libatlas-base-dev \
    libboost-all-dev libgflags-dev libgoogle-glog-dev libhdf5-serial-dev \
    libleveldb-dev liblmdb-dev libopencv-dev libprotobuf-dev libsnappy-dev \
    protobuf-compiler python-dev python-numpy python-pip python-setuptools \
    python-scipy

ENV CAFFE_ROOT=/opt/caffe
WORKDIR $CAFFE_ROOT

ENV CLONE_TAG=1.0

RUN git clone -b ${CLONE_TAG} --depth 1 https://github.com/BVLC/caffe.git .
RUN pip install --upgrade pip
WORKDIR $CAFFE_ROOT/python
RUN pip install -r requirements.txt
RUN pip install pydot
WORKDIR $CAFFE_ROOT
RUN mkdir build
WORKDIR $CAFFE_ROOT/build
RUN cmake -DCPU_ONLY=1 ..
RUN make -j"$(nproc)"

ENV PYCAFFE_ROOT $CAFFE_ROOT/python
ENV PYTHONPATH $PYCAFFE_ROOT:$PYTHONPATH
ENV PATH $CAFFE_ROOT/build/tools:$PYCAFFE_ROOT:$PATH
RUN echo "$CAFFE_ROOT/build/lib" >> /etc/ld.so.conf.d/caffe.conf && ldconfig

RUN wget http://dl.caffe.berkeleyvision.org/bvlc_reference_caffenet.caffemodel \
    -O $CAFFE_ROOT/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel

RUN wget http://dl.caffe.berkeleyvision.org/caffe_ilsvrc12.tar.gz \
    -O $CAFFE_ROOT/data/ilsvrc12/caffe_ilsvrc12.tar.gz
RUN tar xf $CAFFE_ROOT/data/ilsvrc12/caffe_ilsvrc12.tar.gz \
    -C $CAFFE_ROOT/data/ilsvrc12/
RUN rm $CAFFE_ROOT/data/ilsvrc12/caffe_ilsvrc12.tar.gz

WORKDIR /workspace
COPY . /workspace
RUN pip install -r requirements.txt

CMD python app.py
