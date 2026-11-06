const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {create} = require('../src/assets/assistant-engine.js');
const data = JSON.parse(fs.readFileSync(path.join(__dirname,'../dist/assets/assistant-index.json')));
const engine=create(data);
const cases=[
 ['À quelle heure puis-je venir voir ma maman ?',/13 h à 20 h/,'parcours/visites.html'],
 ['Horaires des visites en EHPAD',/9 h à 18 h/,'parcours/visites.html'],
 ['horraires des visites',/13 h à 20 h/,'parcours/visites.html'],
 ['Quel est le numéro du standard ?',/02 54 03 54 03/,'contact.html'],
 ['Comment prendre rendez-vous pour un scanner ?',/02 54 03 63 99/,'services/imagerie.html'],
 ['Quel est le numéro de la radiologie ?',/02 54 03 63 99/,'services/imagerie.html'],
 ['RDV Dr Molcard',/02 54 03 54 53/,'services/consultations.html'],
 ['Rendez-vous diététique',/02 54 03 63 18/,'services/consultations.html'],
 ['numéro dermathologie',/02 54 03 55 06/,'services/consultations.html'],
 ['Quel jour consulte le docteur Ferrandiz ?',/Mardi/,'services/consultations.html'],
 ['Quelle est l’adresse de l’hôpital ?',/Jean Bonnefont/,'acces.html'],
 ['Combien coûte une chambre seule ?',/45 €/,'parcours/frais.html'],
 ['La chambre seule est-elle remboursée ?',/mutuelle|remboursé/i,'parcours/frais.html'],
 ['Quels documents dois-je apporter ?',/Carte Vitale/,'parcours/preparer-venue.html'],
 ['Que dois-je mettre dans ma valise ?',/toilette/,'parcours/preparer-venue.html'],
 ['Comment récupérer mon dossier médical ?',/Écrivez à la direction/,'parcours/dossier-medical.html'],
 ['Y a-t-il du wifi ?',/code Wi-Fi/,'parcours/sejour.html'],
 ['Puis-je manger avec mon père hospitalisé ?',/72 h/,'parcours/visites.html'],
 ['Qui est le directeur ?',/Marc Kugelstadt/,'hopital/organisation.html'],
 ['Je cherche un emploi d’infirmier',/Infirmier diplômé/,'carrieres/index.html'],
 ['Quelles communes sont couvertes par le SSIAD ?',/Reuilly/,'services/ssiad.html'],
 ['Puis-je venir aux urgences après 19h ?',/régulation du 15/,'urgences.html']
];
for(const [q,match,page] of cases){const r=engine.answer(q);assert.equal(r.kind,'answer',q);assert.match(r.text,match,q);assert.ok(r.sources.some(s=>s.url.split('#')[0]===page),q);}
for(const q of ['Est-ce qu’on peut faire une IRM ?','Le parking est-il gratuit ?','Combien coûte une licorne ?','Quel temps fera-t-il demain ?','Qui est le président des États-Unis ?'])assert.equal(engine.answer(q).kind,'unknown',q);
for(const q of ['Quels sont vos horaires ?','Quels sont vos tarifs ?'])assert.equal(engine.answer(q).kind,'clarify',q);
assert.equal(engine.answer('J’ai mal dans la poitrine').kind,'urgent');
assert.equal(engine.answer('Quel médicament prendre pour la fièvre ?').kind,'unknown');
assert.equal(engine.answer('Quelle est la différence entre l’ESA et La Parenthèse ?').sources.length,2);
const previous=engine.answer('Comment joindre le Dr Molcard ?');
assert.match(engine.answer('Et les horaires ?',previous.context).text,/Mardi/);
const imaging=engine.answer('Quel est le numéro de l’imagerie ?');
assert.match(engine.answer('Et les horaires ?',imaging.context).text,/9 h 30/);
for(const p of data.passages){const [file,id]=p.url.split('#');const html=fs.readFileSync(path.join(__dirname,'../dist',file),'utf8');assert.ok(html.includes('id="'+id+'"'),p.url);}
// Updating source data changes the answer without editing a response template.
const changed=JSON.parse(JSON.stringify(data));
changed.passages.filter(p=>p.page==='services/imagerie.html').forEach(p=>{p.text=p.text.replaceAll('02 54 03 63 99','02 54 00 00 00');});
assert.match(create(changed).answer('Quel est le numéro de l’imagerie ?').text,/02 54 00 00 00/);
console.log(`Assistant: ${cases.length+13} checks passed, ${data.passages.length} source anchors verified.`);
