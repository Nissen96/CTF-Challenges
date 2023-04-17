with open("source.c") as f:
    code = f.read()

lines = code.split("\n")

for offset, line in enumerate(lines):
    if line.startswith("//"):
        continue
    if line.startswith("#include"):
        print(line)
        continue
    break

print()

tokenized = [w.replace("§", " ") for w in " ".join(code.split("\n")[offset:]).split()]
tokens = {t for t in tokenized if len(t) > 1}
alphabet = "psyduckPSYDUCK_abefghjmoqrtvwxzABEFGHIJLMNOQRTVWXZiln"

assert len(alphabet) > len(tokens)

mapping = {t: c for t, c in zip(tokens, alphabet)}

for t, c in sorted(mapping.items(), key=lambda x: alphabet.index(x[1])):
    print(f"#define {c} {t}")
print()

with open("psyduck.txt") as f:
    psyduck = f.read()

token = 0
for c in psyduck:
    if c == " " or c == "\n":
        print(c, end="")
    else:
        print(mapping.get(tokenized[token], tokenized[token]), end="")
        token += 1
        if token >= len(tokenized):
            break

print()