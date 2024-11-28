# Example

```bash
$ python3 -m pip install kompozit
$ kompozit -b examples/overlay/
---
networks:
  db:
    attachable: true
services:
  postgres:
    container_name: postgres
    hostname: postgres
    image: postgres:14-alpine
    labels:
    - com.centurylinklabs.watchtower.enable=false
    - traefik.enable=false
    networks:
    - db
    restart: always
    volumes:
    - acme:/var/lib/postgresql/data:rw
volumes:
  acme: null
---
networks:
  private:
    attachable: true
    internal: true
  public:
    attachable: true
    internal: false
services:
  traefik:
    command:
    - NO_COMMAND_TEST
    container_name: traefik
    environment:
      CLOUDFLARE_DNS_API_TOKEN: ${CLOUDFLARE_DNS_API_TOKEN}
      DUCKDNS_TOKEN: ${DUCKDNS_TOKEN}
    hostname: traefik
    image: traefik:v2
    labels:
    - com.centurylinklabs.watchtower.enable=true
    - traefik.enable=true
    - traefik.docker.network=traefik_public
    - traefik.http.routers.api.tls=true
    - traefik.http.routers.api.entryPoints=websecure
    - traefik.http.routers.api.service=api@internal
    - traefik.http.routers.api.tls.certresolver=letsencrypt
    - traefik.http.routers.api.rule=Host(`${MY_DOMAIN}`)
    networks:
    - public
    - private
    ports:
    - 80:80/tcp
    - 443:443/tcp
    restart: unless-stopped
    volumes:
    - /var/run/docker.sock:/var/run/docker.sock
    - acme:/letsencrypt
volumes:
  acme: null
```
