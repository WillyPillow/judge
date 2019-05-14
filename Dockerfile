FROM debian:stable-slim
MAINTAINER Quantum <quantum@dmoj.ca>

RUN groupadd -r judge && useradd -u 7122 -r -m -g judge judge
RUN mkdir -p /usr/share/man/man1/
RUN apt-get -y update && \
    apt-get install -y --no-install-recommends python python2.7-dev python3-dev gcc g++ wget file python3-pip python3-setuptools python3-wheel libseccomp-dev && \
    apt-get clean
RUN pip3 install pyyaml watchdog cython ansi2html termcolor && \
    rm -rf ~/.cache
RUN mkdir -p /dmoj/problems

COPY . /judge
WORKDIR /judge

RUN env DMOJ_REDIST=1 python3 setup.py develop && rm -rf build/

COPY judge.yml /judge/
RUN chmod a+rwx -R /judge/
USER judge

ENTRYPOINT ["/judge/docker-entry"]
