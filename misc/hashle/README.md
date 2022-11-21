# Hashle

I have made a password checker based on the popular Wordle game.
Check it out at `nc 0.0.0.0 1337` and see if you can guess my password.

Note: run the Dockerfile before connecting:

```bash
docker build -t hashle .
docker run --rm -p 1337:1337 hashle
```
