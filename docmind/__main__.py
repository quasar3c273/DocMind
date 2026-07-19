import argparse
from pathlib import Path

from .documents import read_sections
from .ollama import answer
from .search import search


def main():
    parser = argparse.ArgumentParser(description="Поиск по документам Markdown")
    parser.add_argument("folder", type=Path)
    parser.add_argument("question")
    parser.add_argument("--model", help="Имя локальной модели Ollama")
    args = parser.parse_args()
    try:
        sections = search(list(read_sections(args.folder)), args.question)
        if not sections:
            print("Подходящих разделов не найдено.")
            return
        if args.model:
            print(answer(args.question, sections, args.model))
        for number, section in enumerate(sections, 1):
            print(f"[{number}] {section.file}:{section.line} — {section.title}")
            print(section.text)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Ошибка: {exc}\n")


if __name__ == "__main__":
    main()
