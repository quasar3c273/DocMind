from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class Section:
    file: str
    line: int
    title: str
    text: str


def read_sections(folder: Path):
    if not folder.is_dir():
        raise ValueError("Папка с документами не найдена")
    for path in sorted(folder.rglob("*.md")):
        name = path.relative_to(folder).as_posix()
        title = path.stem
        start = 1
        lines = []
        for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            heading = re.match(r"^#{1,6}\s+(.+)$", line)
            if heading:
                if content := "\n".join(lines).strip():
                    yield Section(name, start, title, content)
                title = heading[1].strip()
                start = number
                lines = []
            else:
                lines.append(line)
        if content := "\n".join(lines).strip():
            yield Section(name, start, title, content)
