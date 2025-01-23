FROM debian:latest

# check if tor is up
HEALTHCHECK CMD ["/usr/bin/curl", "--socks5", "localhost:9050", "--socks5-hostname", "localhost:9050", "https://check.torproject.org/api/ip"]

RUN apt-get install tor && chmod o+rwx /etc/tor

USER ¨tor¨
