@echo off
set proj_dir=%cd%

docker build -t ubuntu2204:fuzzer-dev-latest %proj_dir%