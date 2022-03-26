FROM python:3.9.12
ENV PIP_NO_CACHE_DIR=1

# get the latest pip
RUN python -m pip install --upgrade pip

# copy the source code
COPY . ./

# install the package
RUN pip install .

# expose utility
ENTRYPOINT ["npxcompress"]
