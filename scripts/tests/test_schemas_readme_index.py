"""docs/schemas 下每个 *.schema.json 须在 docs/schemas/README.md 索引表中登记。"""
from __future__ import annotations

import unittest
from pathlib import Path


class TestSchemasReadmeIndex(unittest.TestCase):
    def test_each_schema_file_mentioned_in_readme(self) -> None:
        root = Path(__file__).resolve().parents[2]
        schema_dir = root / "docs" / "schemas"
        readme = schema_dir / "README.md"
        self.assertTrue(readme.is_file(), msg="缺少 docs/schemas/README.md")
        text = readme.read_text(encoding="utf-8")
        schema_files = sorted(schema_dir.glob("*.schema.json"))
        self.assertTrue(schema_files, msg="docs/schemas 下应至少有一个 .schema.json")
        for path in schema_files:
            self.assertIn(
                path.name,
                text,
                msg=f"{path.name} 须在 docs/schemas/README.md 的索引表或正文中登记",
            )


if __name__ == "__main__":
    unittest.main()
