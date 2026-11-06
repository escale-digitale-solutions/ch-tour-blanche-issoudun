import re
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from assistant_index import build_assistant_index, split_text, Tree

class PassageIndexTests(unittest.TestCase):
    def build(self, html):
        return build_assistant_index([('services/demo.html', html)], [{'u': 'services/demo.html', 't': 'Service test', 'k': 'soins rendez vous'}])

    def test_excludes_chrome_and_preserves_negation(self):
        html = '<header>Faux numéro global</header><main><h1>Test</h1><nav>Navigation</nav><h2>Accueil</h2><p>Le service ne reçoit pas sans rendez-vous.</p></main><footer>Pied</footer>'
        docs, index = self.build(html)
        self.assertEqual([p['text'] for p in index['passages']], ['Le service ne reçoit pas sans rendez-vous.'])
        self.assertEqual(index['passages'][0]['keywords'], 'soins rendez vous')
        anchor = index['passages'][0]['url'].split('#')[1]
        self.assertIn(f'id="{anchor}"', docs[0][1])

    def test_definition_and_table_remain_associated(self):
        html = '<main><h1>Test</h1><dl><dt>Rendez-vous</dt><dd><a href="tel:0254035506">02 54 03 55 06</a></dd></dl><table><thead><tr><th scope="col">Spécialité</th><th scope="col">Médecin</th><th scope="col">Horaires</th></tr></thead><tbody><tr><th>Dermatologie</th><td>Dr Ferrandiz</td><td>Mardi 11 h</td></tr></tbody></table></main>'
        _, index = self.build(html)
        self.assertEqual(index['passages'][0]['text'], 'Rendez-vous : 02 54 03 55 06')
        self.assertEqual(index['passages'][1]['text'], 'Spécialité : Dermatologie ; Médecin : Dr Ferrandiz ; Horaires : Mardi 11 h')

    def test_docs_are_not_assertions(self):
        html = '<main><h1>Test</h1><ul class="docs"><li><a href="https://example.com/livret.pdf">Livret <small>Édition 2019</small></a></li></ul><ul class="stations"><li><a href="autre.html">Autre service</a></li></ul></main>'
        _, index = self.build(html)
        self.assertEqual([p['kind'] for p in index['passages']], ['document', 'navigation'])

    def test_existing_anchor_and_stable_new_anchors(self):
        html = '<main><h1>Test</h1><p id="existant">Texte déjà ancré.</p><p>Second texte.</p></main>'
        docs, one = self.build(html)
        _, two = self.build(html)
        self.assertEqual(one['passages'], two['passages'])
        self.assertTrue(one['passages'][0]['url'].endswith('#existant'))
        ids = re.findall(r'\bid="([^"]+)"', docs[0][1])
        self.assertEqual(len(ids),len(set(ids)))

    def test_short_lists_group_and_404_excluded(self):
        docs, index = build_assistant_index([('index.html','<main><h1>Test</h1><h2>Documents</h2><ul><li>Carte Vitale</li><li>Pièce d’identité</li></ul></main>'), ('404.html','<main><p>Introuvable</p></main>')], [])
        self.assertEqual(index['pages'],1)
        self.assertEqual(index['passages'][0]['text'],'Carte Vitale ; Pièce d’identité')
        self.assertEqual(len(docs),2)

    def test_split_stays_bounded_and_keeps_text(self):
        text = 'Le service ne reçoit pas sans rendez-vous. ' * 30
        chunks=split_text(text)
        self.assertTrue(all(len(t)<=500 for t in chunks))
        self.assertEqual(' '.join(chunks),text.strip())

    def test_real_site_anchors_resolve(self):
        root = Path(__file__).resolve().parents[1]/'dist'
        docs = [(str(p.relative_to(root)),p.read_text()) for p in root.rglob('*.html') if p.name!='qa-responsive.html']
        if not docs:
            self.skipTest('Site build unavailable')
        updated,index = build_assistant_index(docs,[])
        anchor_sets={p:{n.attrs['id'] for n in Tree(s).root.nodes() if n.attrs.get('id')} for p,s in updated}
        for passage in index['passages']:
            self.assertIn(passage['url'].split('#')[1], anchor_sets[passage['page']])
            self.assertLessEqual(len(passage['text']),500)
        self.assertEqual(len({p['id'] for p in index['passages']}), len(index['passages']))

if __name__ == '__main__':
    unittest.main()
