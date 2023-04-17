import unicodedata
import re
from pathlib import Path


def slugify(value):
    # From https://github.com/django/django/blob/master/django/utils/text.py
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def confirm(prompt):
    resp = input(f"{prompt} [y/N] ").casefold()
    return resp == "y"


def multiline_input(prompt):
    print(f"{prompt} (press ENTER three times when done)")
    
    resp = ""
    count = 0
    while True:
        line = input()
        resp += line + "\n"
        if line == "":
            count += 1
        else:
            count = 0
        if count >= 2:
            resp = resp[:-3]
            return resp


def gen_description(folder, title):
    if (folder / "README.md").exists() and not confirm("Readme already exists for this challenge - overwrite?"):
            return

    description = multiline_input("Description:")
    event = input("Event: ")
    with open(folder / "README.md", "w") as f:
        f.write(f"# {title}\n\n")
        f.write(f"## {event}\n\n")
        f.write(f"{description}\n")


def gen_solution(folder):
    sol_folder = folder / "solution"
    if (sol_folder / "README.md").exists() and not confirm("Solution readme already exists for this challenge - overwrite?"):
            return
    
    flag = input("Flag: ")
    solution = multiline_input("Solution")
    with open(sol_folder / "README.md", "w") as f:
        f.write(f"# Writeup\n\n")
        f.write(f"{solution}\n\n")
        f.write(f"## Flag\n\n")
        f.write(f"`{flag}`\n")


def gen_challenge():
    print("NEW CHALLENGE")

    category = input("Category: ")
    cat_folder = Path(slugify(category))
    if not cat_folder.exists():
        if confirm("Category folder does not exist, create?"):
            cat_folder.mkdir()
        else:
            exit()

    title = input("Title: ")
    folder = cat_folder / slugify(title)
    folder.mkdir(exist_ok=True)
    (folder / "src").mkdir(exist_ok=True)
    (folder / "solution").mkdir(exist_ok=True)
    gen_description(folder, title)
    gen_solution(folder)


def main():
    while True:
        gen_challenge()
        if not confirm("Generate another challenge?"):
            return


if __name__ == "__main__":
    main()
