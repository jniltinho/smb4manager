FROM ubuntu:22.04

# docker build --no-cache -t jniltinho/smb4manager .
# docker run -d --name smb4manager -p 8010:8010 jniltinho/smb4manager

RUN apt-get update && gcc make git python3-dev python3-pip python3-virtualenv samba \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN git clone http://github.com/jniltinho/smb4manager.git /opt/smb4manager
RUN cd /opt/smb4manager && bash create_env.sh

EXPOSE 8010
