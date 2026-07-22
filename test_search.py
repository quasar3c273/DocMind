from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from docmind.documents import read_sections
from docmind.search import search


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.sections = list(read_sections(Path(__file__).parent / "examples"))

    def test_first_result(self):
        cases = [
            ("Где посмотреть изменения статуса?", "История статусов"),
            ("Как создать заявку?", "Создание заявки"),
            ("Почему нужна причина повторного открытия?", "Повторное открытие"),
        ]
        for question, title in cases:
            with self.subTest(question=question):
                self.assertEqual(search(self.sections, question)[0].title, title)

    def test_missing_answer(self):
        self.assertEqual(search(self.sections, "пароль VPN"), [])

    def test_empty_folder(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(list(read_sections(Path(folder))), [])

    def test_source_location(self):
        section = search(self.sections, "история статусов")[0]
        self.assertEqual((section.file, section.line), ("support.md", 9))
