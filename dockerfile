FROM ubuntu:22.04
ARG TOK

RUN apt-get update && apt install -y vim git net-tools g++ make python
RUN cd /root/ && git clone https://$TOK@github.com/carsonhwright/cdubz_fuzzer.git