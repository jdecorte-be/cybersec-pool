FROM nginx:latest

EXPOSE 4242

# Install Dependencies
RUN apt-get update && \ 
    apt-get install -y openssh-server

# Setup SSH Service
RUN echo "root:root" | chpasswd
COPY "./sshd_config" "/etc/ssh/sshd_config"

CMD service ssh start
