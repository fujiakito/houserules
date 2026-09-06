"""Prevent an inventory addition from leaving the user-facing stage guide incomplete."""
from pathlib import Path
import re
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


class DocumentationTests(unittest.TestCase):
    def test_each_stage_maps_every_inventory(self):
        inventories = {p.name for p in (ROOT / 'docs/agents').glob('*.md')
                       if p.name not in {'README.md', '_TEMPLATE.md'}}
        guide = (ROOT / 'docs/GUIDE.md').read_text(encoding='utf-8')
        tables = re.findall(r'\| Agent / inventory \|[^\n]*\n((?:\|[^\n]*\n)+)', guide)
        self.assertEqual(len(tables), 15, '12 stages and 3 cross-cutting concerns require mappings')
        for index, table in enumerate(tables, 1):
            with self.subTest(table=index):
                mapped = re.findall(r'\]\(agents/([^/#)]+\.md)\)', table)
                self.assertEqual(set(mapped), inventories)
                self.assertEqual(len(mapped), len(inventories), 'One row per agent')
                for row in table.splitlines()[1:]:
                    cells = row.strip('|').split('|')
                    self.assertEqual(len(cells), 4, 'Keep the human guide narrow')
                    self.assertTrue(all(cell.strip() for cell in cells))

    def test_first_party_skill_notice_matches_the_project_license(self):
        """hr-onboard is copied on its own, so its notice must not drift from the root one."""
        self.assertEqual((ROOT / 'templates/skills/hr-onboard/LICENSE').read_bytes(),
                         (ROOT / 'LICENSE').read_bytes())

    def test_short_agent_entry_does_not_expand_the_research_bundle(self):
        entry = (ROOT / 'templates/START.md').read_text(encoding='utf-8')
        self.assertLess(len(entry.split()), 400, 'Keep the routine execution entry small')
        self.assertIn('workflow.py status', entry)
        self.assertNotRegex(entry, r'\]\([^)]*(?:research/|docs/GUIDE)')

    def test_human_navigation_and_template_links_resolve(self):
        files = [ROOT / 'README.md', ROOT / 'HOUSERULES.md',
                 *(ROOT / 'docs').rglob('*.md'), ROOT / 'templates/work/README.md']
        for file in files:
            for destination in re.findall(r'\]\(([^)\s]+)(?:\s+"[^"]*")?\)',
                                          file.read_text(encoding='utf-8')):
                if '://' in destination or destination.startswith(('mailto:', 'app:')):
                    continue
                with self.subTest(file=file.relative_to(ROOT), link=destination):
                    name, _, fragment = destination.partition('#')
                    target = (file.parent / unquote(name)).resolve() if name else file
                    self.assertTrue(target.exists())
                    if fragment and target.suffix == '.md':
                        headings = re.findall(r'^#{1,6}\s+(.+)', target.read_text(encoding='utf-8'), re.M)
                        slugs = [re.sub(r'[^\w\- ]', '', h.lower()).replace(' ', '-') for h in headings]
                        self.assertIn(unquote(fragment), slugs)
