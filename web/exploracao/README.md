# Exploração

## De Danske Cybermesterskaber 2023 - Qualifiers

![Budget GeoGuessr](geo.jpg)

[http://exploracao.hkn](http://exploracao.hkn)

## Local Setup

To play this challenge as if it ran remotely, use the local Dockerfile:

```bash
docker build -t exploracao .
docker run --rm -it -p 80:80 exploracao
```

and add the following line to your hosts file (`/etc/hosts` on Linux, `C:\Windows\System32\drivers\etc\hosts` on Windows):

```
127.0.0.1 exploracao.hkn
```
