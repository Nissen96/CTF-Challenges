# Hashle

## De Danske Cybermesterskaber 2022 - Regionals

I have made a password checker based on the popular Wordle game.
Check it out at `nc 0.0.0.0 1337` and see if you can guess my password.

Note: run the Dockerfile before connecting:

```bash
docker build -t hashle .
docker run --rm -p 1337:1337 hashle
```

## Original (Danish)

Jeg har lavet en password checker baseret på det populære spil Wordle. Tjek den ud på `nc 0.0.0.0 1337` og se, om du kan gætte mit password.
