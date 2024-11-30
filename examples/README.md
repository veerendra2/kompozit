# Example

[Docs](https://veerendra2.gitbook.io/kompozit)

```bash
python3 -m pip install kompozit

kompozit -b examples/overlay/homeserver/
---
networks:
  public:
    attachable: true
    internal: false
  private:
    attachable: true
    internal: true
volumes:
  acme: null
services:
  dev-traefik-test:
    image: traefik:v2
    hostname: traefik
    container_name: traefik
    restart: unless-stopped
    environment:
      DUCKDNS_TOKEN: ${DUCKDNS_TOKEN}
      CLOUDFLARE_DNS_API_TOKEN: ${CLOUDFLARE_DNS_API_TOKEN}
    ports:
    - 80:80/tcp
    - 443:443/tcp
    networks:
    - public
    - private
    volumes:
    - /var/run/docker.sock:/var/run/docker.sock
    - acme:/letsencrypt
    command:
    - --log.level=INFO
    - --api.insecure=false
    - --api.dashboard=false
    - --providers.docker=true
    - --providers.docker.exposedByDefault=false
    - --global.sendAnonymousUsage=false
    - --global.checkNewVersion=false
    labels:
    - com.centurylinklabs.watchtower.enable=true
```
