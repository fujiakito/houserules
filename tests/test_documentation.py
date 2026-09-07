"""Prevent an inventory addition from leaving the user-facing stage guide incomplete."""
from pathlib import Path
import re
import sys
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


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

    def test_scaffold_marker_still_identifies_an_unfilled_agents_file(self):
        """The installer reads this marker to pick the first action it prints on the entry page.

        Editing the scaffold's comment without it would silently turn every fresh install into
        the "onboarding is done" branch, and nothing else would fail.
        """
        import install
        template = (ROOT / 'templates/AGENTS.md').read_text(encoding='utf-8')
        self.assertIn(install.SCAFFOLD_MARKER, template)
        self.assertNotIn(install.SCAFFOLD_MARKER, (ROOT / 'AGENTS.md').read_text(encoding='utf-8'))

    def test_agent_read_files_state_a_stop_condition(self):
        """An ambiguity guard, not a behavioral one: it cannot establish what a weak model does."""
        for rel, marker in [('templates/START.md', 'Stop when'),
                            ('templates/work/README.md', 'Stop at step')]:
            with self.subTest(file=rel):
                self.assertIn(marker, (ROOT / rel).read_text(encoding='utf-8'))

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
