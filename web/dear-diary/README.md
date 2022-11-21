# Dear Diary

## De Danske Cybermesterskaber 2022 - Regionals

Dear Diary,

Jens claims to have found a vulnerability on my new [diary website](http://dear-diary.hkn).

He says he read all my private entries! 😲

He's so mean, but I don't believe him at all - he's just jealous of my web skills 💻

❤️ XOXO ❤️

Challenge source with local setup: [deardiary.zip](deardiary.zip)

## Note

To play this challenge as if it ran remotely, use the local Dockerfile:

```bash
docker build -t deardiary .
docker run --rm -p 80:80 deardiary
```

And add the following line to your hosts file (`/etc/hosts` on Linux, `C:\Windows\System32\drivers\etc\hosts` on Windows):

```
127.0.0.1 dear-diary.hkn
```

Now navigate to http://dear-diary.hkn to play.

Running the local setup at the same time is not recommended.
Instead, develop your exploit on the local instance, and run the "remote" instance locally afterwards.
