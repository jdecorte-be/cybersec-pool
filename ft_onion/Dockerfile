FROM nginx:latest
EXPOSE 80
EXPOSE 4242

# Install Dependencies
RUN apt-get update && \ 
    apt-get install -y tor nginx openssh-server curl

# Check if tor is up
HEALTHCHECK CMD ["/usr/bin/curl", "--socks5", "localhost:9050", "--socks5-hostname", "localhost:9050", "https://check.torproject.org/api/ip"]

# Setup Nginx Service
COPY "./nginx.conf" "/etc/nginx/conf.d/default.conf"
COPY "./index.html" "/var/www/html/index.html"

# Setup SSH Service
RUN echo "root:root" | chpasswd
COPY "./sshd_config" "/etc/ssh/sshd_config"

# Setup Tor Service
COPY "./torrc" "/etc/tor/torrc"

CMD service ssh start && service tor start && nginx -g "daemon off;"

# /var/lib/tor/my_website/hostname