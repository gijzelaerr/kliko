FROM python:3.5
MAINTAINER gijsmolenaar@gmail.com
RUN pip install kliko
ADD kliko.yml /
ADD kliko /
RUN chmod 755 /kliko
CMD /kliko
