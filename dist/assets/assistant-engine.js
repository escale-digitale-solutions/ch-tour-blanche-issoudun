/* Assistant documentaire local : classe des extraits du site, sans inventer de réponse. */
(function (root) {
  'use strict';
  var normalize = function (s) { return String(s || '').replace(/wi[ -]?fi/gi,'wifi').replace(/(\d+)\s*h\b/gi,'$1 heures').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[’']/g, ' ').replace(/[^a-z0-9]+/g, ' ').trim(); };
  var stop = new Set(('a au aux avec ce ces cet cette dans de des du elle en et eux il ils je la le les leur lui ma mes me mon ne nos notre nous on ou par pas pour que quel quelle quelles quels qui sa sans se ses si son sur ta te tes toi ton tu un une vos votre vous y est sont etre avoir ai as avez avons suis peut peux puis faire fait faut voudrais souhaite savoir connaitre trouve trouver information informations merci bonjour salut svp please comment combien quand pourquoi quoi aller dit dire donc encore vraiment possible prendre rendre recuperer obtenir mettre dois doit cherchez cherche aimerais voudrais souhaiterais besoin faites fait existe existez pouvez pourrait puis pouvez recevoir merci hopital hospitalier centre tour blanche issoudun').split(' '));
  function tokens(s) { return normalize(s).split(' ').filter(function(w){return w && !stop.has(w) && (w.length > 1 || /^\d$/.test(w));}); }
  var groups = [
    ['visite','visites','visiter','voir','proche','proches'], ['horaire','horaires','heure','heures','ouverture','ouvert','accueil'],
    ['telephone','telephoner','appeler','appel','numero','joindre','contact','standard'], ['rendez','rdv','consultation','consultations'],
    ['imagerie','radiologie','radio','radiographie','radiographies'], ['echo','echographie'],
    ['kine','kinesitherapie','reeducation','readaptation','mpr'], ['ehpad','residence','resident','residents','retraite'],
    ['grossesse','enceinte','perinatal','prenatal','maternite','sage','femme','naissance'], ['gyneco','gynecologie','gynecologique','gynecologue'],
    ['emploi','emplois','recrutement','recruter','recrute','travail','travailler','poste','postes','candidature','job','embauche'],
    ['prix','tarif','tarifs','cout','coute','payer','paiement','frais','facture','facturation','combien'],
    ['chambre','chambres'], ['individuelle','individuel','particuliere','seule','seul'],
    ['preparer','preparation','apporter','amener','emmener','valise','affaires','papiers','documents','justificatifs'],
    ['hospitalisation','hospitalise','hospitalisee','sejour','admission'], ['adresse','acces','localisation','situe','situee','venir','plan','itineraire'],
    ['dormir','nuit','accompagnant','accompagner','coucher'], ['repas','manger','dejeuner','diner','petit','restaurant','restauration'],
    ['wifi','internet','connexion'], ['tele','television'], ['stage','stages','stagiaire'],
    ['formation','former','ifas','ecole','etudes'], ['dossier','copie'], ['medical','medicaux'],
    ['alzheimer','parenthese','esa'], ['domicile','ssiad'], ['handicap','handicape','mobilite','fauteuil'],
    ['visiteur','visiteurs','famille','entourage'], ['enfant','enfants','mineur','mineurs'],
    ['securite','qualite','certification','certifie','has'], ['medecin','medecins','docteur','dr'],
    ['infirmier','infirmiere','infirmiers','infirmieres'], ['chirurgie','chirurgical','operation','operer'],
    ['regime','regimes','allergie','allergies'], ['fumer','tabac','vapoter','cigarette'], ['interprete','traduction','langue'],
    ['sortie','sortir','depart'], ['mutuelle','assurance','remboursement','rembourse','remboursee'],
    ['transport','taxi','ambulance','vsl'], ['direction','directeur','dirige','responsable'], ['gratuit','gratuite','gratuits'], ['commune','communes','secteur','couverte','couvertes','couvert','intervient','desservie']
  ];
  var synonyms = new Map(); groups.forEach(function(g){g.forEach(function(w){synonyms.set(w,g);});});
  function alternatives(w) { var a = (synonyms.get(w) || [w]).slice(); if(w.length>4){if(w.endsWith('s'))a.push(w.slice(0,-1));else a.push(w+'s');} return a; }
  function edit(a,b) { if(Math.abs(a.length-b.length)>1)return 3; var row=Array.from({length:b.length+1},function(_,i){return i;}); for(var i=1;i<=a.length;i++){var last=row[0];row[0]=i;for(var j=1;j<=b.length;j++){var old=row[j];row[j]=Math.min(row[j]+1,row[j-1]+1,last+(a[i-1]===b[j-1]?0:1));last=old;}}return row[b.length]; }
  function sentences(s) { return String(s).replace(/\b(Dr|Mme|M)\./g,'$1∯').split(/(?<=[.!?])\s+(?:;\s*)?/).map(function(x){return x.replace(/∯/g,'.').replace(/^[;\s]+/,'').trim();}).filter(Boolean); }
  function excerpt(p, query) {
    var text=p.text.replace(/\s+/g,' ').trim();
    var ss=sentences(text).map(function(s){return s.trim();}).filter(Boolean);
    var best=0, score=-1;
    ss.forEach(function(s,i){var ts=new Set(tokens(s));var v=query.reduce(function(n,w){return n+(alternatives(w).some(function(a){return ts.has(a);})?1:0);},0);if(v>score){score=v;best=i;}});
    var result=ss.slice(best,best+2).join(' ');
    if(query.some(function(w){return /prix|cout|coute|tarif/.test(w);})) { var pi=ss.findIndex(function(t){return /€|euros/.test(t);}); if(pi>=0)result=ss.slice(pi,pi+2).join(' '); }
    if(result.length>520) return result.slice(0,500).replace(/\s+\S*$/,'')+'…';
    return result;
  }
  var domains = [
    [/\b(imagerie|radiologie|radio|scanner|echographie|irm)\b/,['services/imagerie.html']],
    [/\b(dermatologie|dermatologue|ferrandiz|molcard|ophtalmo|ophtalmologie|orl|rhumatologie|gastro|urologie|diabetologie|pneumologie)\b/,['services/consultations.html']],
    [/\b(reeducation|readaptation|mpr|kine)\b/,['services/mpr.html','services/hopital-de-jour-mpr.html']],
    [/\b(ssiad|soins a domicile)\b/,['services/ssiad.html']],
    [/\b(bel air|mesanges)\b/,['services/ehpad-bel-air.html']],
    [/\b(reflets|argent)\b/,['services/ehpad-reflets-argent.html']],
    [/\b(parenthese)\b/,['services/la-parenthese.html']],
    [/\b(esa|equipe specialisee alzheimer)\b/,['services/esa.html']],
    [/\b(ifas|ecole aide|formation aide)\b/,['carrieres/ifas.html']],
    [/\b(grossesse|enceinte|perinatal|sage femme|maternite)\b/,['services/centre-perinatal.html']],
    [/\b(ivg|contraception|sexuelle)\b/,['services/sante-sexuelle.html']],
    [/\b(pharmacie|pharmacien)\b/,['services/pharmacie.html']],
    [/\b(pass|sans couverture)\b/,['services/pass.html']],
    [/\b(urgence|urgences|smur)\b/,['urgences.html']],
    [/\b(centre de sante)\b/,['services/centre-de-sante.html']]
  ];
  function create(data) {
    var df=new Map(), vocab=new Set();
    var passages=(data.passages||[]).map(function(p){
      var doc=Object.assign({},p);doc.bt=new Set(tokens(p.text));doc.ht=new Set(tokens(p.title+' '+p.section));doc.all=new Set([...doc.bt,...doc.ht]);
      doc.all.forEach(function(w){vocab.add(w);df.set(w,(df.get(w)||0)+1);});return doc;
    });
    function weight(w){return Math.max(1,Math.log(1+passages.length/(1+(df.get(w)||0))));}
    function answer(question, context) {
      var raw=normalize(question).slice(0,600);
      var unknown={kind:'unknown',text:'Je ne trouve pas de réponse assez précise dans les pages du site. Pouvez-vous préciser le service ou reformuler votre question ?',sources:[],suggestions:[{label:'Contacter l’hôpital',question:'Quel est le numéro du standard ?'}]};
      if(!raw||!/[a-z]/.test(raw))return unknown;
      if(/^(bonjour|salut|bonsoir|merci|merci beaucoup|coucou)$/.test(raw))return {kind:'clarify',text:'Bonjour ! Quelle information cherchez-vous sur l’hôpital ?',sources:[],suggestions:[{label:'Les visites',question:'Quels sont les horaires des visites ?'},{label:'Un rendez-vous',question:'Comment prendre rendez-vous ?'}]};
      if(/\b(douleur (thoracique|poitrine)|mal (a|dans) la poitrine|respire (mal|plus)|du mal a respirer|ne respire|suicid|me tuer|overdose|perte de connaissance|inconscient)\b/.test(raw))return {kind:'urgent',text:'Si une personne est en danger ou présente une urgence médicale, appelez le 15 ou le 112. Cet assistant ne peut pas évaluer un état de santé.',sources:[{title:'Urgences : les numéros et consignes',url:'urgences.html'}]};
      if(/\b(diagnostic|symptomes?|dose|dosage|posologie|quel medicament|quel traitement|dois je prendre|j ai mal|me soigner)\b/.test(raw))return {kind:'unknown',text:'Je peux vous orienter dans les informations de l’hôpital, mais pas donner un avis médical. Pour une question sur votre santé, contactez un professionnel de santé.',sources:[{title:'Contacter l’hôpital',url:'contact.html'}]};
      var words=tokens(raw).filter(function(w){return !['veux','besoin','pourrais','pourrait','peut','petite','petit','possible','svp','demande','question','rendre','prendre','mettre','dois','doit','recuperer','obtenir','cherche','existe','consulte','maman','papa','mere','pere','mamie','19h','soir','maintenant','aujourd','hui','service','services','jours','jour','personne','atteinte','difference','entre'].includes(w);});
      if(!words.length)return unknown;
      var corrected=words.map(function(w){if(vocab.has(w)||synonyms.has(w)||w.length<5)return w;if(w.endsWith('s')&&vocab.has(w.slice(0,-1)))return w.slice(0,-1);var found=Array.from(vocab).filter(function(v){return v[0]===w[0]&&edit(w,v)<=1;});return found.length===1?found[0]:w;});
      words.forEach(function(w,i){if(w!==corrected[i])raw=raw.replace(new RegExp('\\b'+w+'\\b','g'),corrected[i]);});
      words=Array.from(new Set(corrected));
      var specificRow=passages.find(function(p){if(p.page!=='services/consultations.html'||p.kind!=='table')return false;var label=normalize(p.text.split(/Jours et horaires|Rendez-vous/)[0]);return words.some(function(w){return w.length>=4&&!synonyms.has(w)&&new Set(tokens(label)).has(w);});});
      var target=[];domains.forEach(function(d){if(d[0].test(raw))target.push.apply(target,d[1]);});
      if(specificRow&&!target.length)target=['services/consultations.html'];
      var follow=/^(et|sinon|aussi|pour ce|pour les|leurs|ses)\b/.test(raw)&&context&&context.page&&!target.length;
      if(follow)target=[context.page];
      var intent={
        visit:/\b(visite|visites|visiter|voir (un|une|mon|ma|mes)|rendre visite)\b/.test(raw),
        phone:/\b(telephone|numero|appeler|joindre|contacter|standard|tel)\b/.test(raw),
        appointment:/\b(rdv|rendez vous|prendre rendez)\b/.test(raw),
        hours:/\b(horaire|horaires|heure|heures|ouvert|ouverture|ferme)\b/.test(raw),
        address:/\b(adresse|situe|situee|venir|itineraire|acces|etage|niveau|ou se trouve)\b/.test(raw),
        price:/\b(prix|tarif|tarifs|combien|coute|cout|payer|frais)\b/.test(raw),
        prepare:/\b(apporter|amener|emmener|valise|preparer|papiers)\b/.test(raw),
        record:/\b(dossier medical|dossier de sante|copie (de|du|mon) dossier)\b/.test(raw)
      };
      function reply(p, focus) {
        if(!p)return unknown;
        var text=excerpt(p,words);
        if(focus){var ss=sentences(p.text),at=ss.findIndex(function(x){return focus.test(normalize(x));});if(at>=0)text=ss.slice(at,at+2).join(' ');}
        return {kind:'answer',text:text,sources:[{title:p.title+(p.section?' — '+p.section:''),url:p.url}],context:{page:p.page,passage:p.id}};
      }
      function select(page, sec, kind, text) { return passages.find(function(p){return p.page===page&&(!sec||sec.test(normalize(p.section)))&&(!kind||kind===p.kind)&&(!text||text.test(normalize(p.text)));}); }
      var elder=/ehpad|resident|retraite|bel air|reflets|mesanges/.test(raw);
      var broadPage = target[0] || (follow&&context.page);
      var isPhone=function(p){return /(?:0[1-9](?:[ \u00a0]?\d{2}){4})/.test(p.text);};
      var queryUnknown=words.filter(function(w){return w.length>3&&!synonyms.has(w)&&!vocab.has(w)&&!/^\d+$/.test(w);});
      var rulesAllowed=queryUnknown.length===0;
      // Réponses ciblées : les textes et valeurs sont toujours lus dans l’index courant.
      if(rulesAllowed){
        if(follow&&context.passage&&/horaire|rendez|numero|telephone/.test(raw)){var prior=passages.find(function(p){return p.id===context.passage&&p.kind==='table'&&p.page==='services/consultations.html';});if(prior)return reply(prior);}
        if(specificRow&&!/prix|tarif|cout|payer/.test(raw))return reply(specificRow);
        if((/alzheimer/.test(raw)||(/esa/.test(raw)&&/parenthese/.test(raw)))&&!intent.phone&&!intent.price&&!intent.hours&&!intent.address){var ea=select('services/esa.html',/^$/,'paragraph'),pa=select('services/la-parenthese.html',/^$/,'paragraph');if(ea&&pa)return {kind:'answer',text:'ESA : '+sentences(ea.text)[0]+' La Parenthèse : '+sentences(pa.text)[0],sources:[{title:ea.title,url:ea.url},{title:pa.title,url:pa.url}]};}
        if(/ssiad/.test(raw)&&/commune|couverte|secteur/.test(raw))return reply(select('services/ssiad.html',/commune/,'paragraph'));

        if(!broadPage && ((intent.hours&&!intent.visit&&!intent.appointment)||(/^quels? sont (vos|les) tarifs/.test(raw))))return {kind:'clarify',text:'Pour quel service souhaitez-vous cette information ?',sources:[],suggestions:[{label:'Les visites',question:'Quels sont les horaires de visite ?'},{label:'L’imagerie',question:'Quels sont les horaires de l’imagerie ?'},{label:'Les EHPAD',question:'Quels sont les tarifs en EHPAD ?'}]};
        if(/emploi|recrut|travaill|job|embauche|poste|candidature/.test(raw)){
          var profession=words.filter(function(w){return /infirm|soignant|medecin|secretaire|cuisin|radiologue|orthophon|ergo|psycho|pharmac/.test(w);});
          var job=passages.find(function(p){return p.page==='carrieres/index.html'&&p.kind==='navigation'&&profession.length&&profession.some(function(w){return alternatives(w).some(function(x){return normalize(p.text).includes(x);});});});
          if(job){var jr=reply(job);jr.text=job.text.replace(/Publiée/g,' — Publiée').replace(/Lire l’annonce/g,'').trim()+'.';return jr;}
          if(profession.length)return unknown;
          return reply(select('carrieres/index.html',null,'paragraph'));
        }
        if(intent.phone&&/admissions/.test(raw))return reply(select('hebergement/tarifs-aides.html',/bureau des admissions/,'definition'));
        if(broadPage==='services/consultations.html'){
          var named=words.filter(function(w){return !synonyms.has(w)&&w.length>=4&&vocab.has(w);});
          var row=passages.find(function(p){return p.page===broadPage&&p.kind==='table'&&named.some(function(w){return p.bt.has(w);});});
          if(row)return reply(row);
        }

        if(intent.visit && !/repas|manger|dormir|nuit/.test(raw))return reply(select('parcours/visites.html',elder?/visiter un resident/:/heures de visite/,'paragraph'),/visites|rendre visite/);
        if(/(?:manger|repas|dejeuner).*(?:proche|pere|mere|famille|hospitalise|accompagn)|(?:proche|pere|mere).*(?:manger|repas|dejeuner)/.test(raw))return reply(select('parcours/visites.html',/partager un repas/,'paragraph'));
        if(/dormir|passer la nuit|rester la nuit/.test(raw))return reply(select('parcours/visites.html',/dormir sur place/,'paragraph'));
        if(/wifi|internet|television|\btele\b/.test(raw)&&!elder){var wp=select('parcours/sejour.html',/telephone television/,'paragraph'); if(wp&&/wifi|internet/.test(raw)){var ws=sentences(wp.text);var wr=reply(wp);wr.text=ws.filter(function(t){return /mise en service|code wi.fi/i.test(t);}).slice(0,2).join(' ');return wr;}return reply(wp);}
        if(intent.price&&elder)return reply(select('hebergement/tarifs-aides.html',/prix de sejour/,'paragraph',/tarifs sont fixes/));
        if(/chambre/.test(raw)&&/prix|cout|combien|tarif|rembours|mutuelle|payer/.test(raw))return reply(select('parcours/frais.html',/chambre particuliere/,'paragraph'),/rembours|mutuelle/.test(raw)?/rembourse/:/supplement/);
        if(/directeur|dirige/.test(raw)&&!/ecrire|reclamation|contacter|telephone|numero/.test(raw))return reply(select('hopital/organisation.html',/gouvernance.*directeur/,'definition'));
        if(intent.prepare)return reply(select('parcours/preparer-venue.html',/affaires|valise|vetement/.test(raw)?/affaires/:/documents/,'list'));
        if(intent.record&&!/delai|temps|conserve|ans/.test(raw))return reply(select('parcours/dossier-medical.html',/comment le demander/,'list'),/ecrivez/);
        if(/interprete|traduction/.test(raw))return reply(select('parcours/sejour.html',/interprete/,'paragraph'));
        if(/fumer|vapoter|tabac/.test(raw))return reply(select('parcours/sejour.html',/tabac/,'definition'));
        if(intent.address&&!broadPage)return reply(select('acces.html',/adresse/,'definition'));
        if(/urgence/.test(raw)&&/soir|nuit|19|avant|apres|venir|acces/.test(raw))return reply(select('urgences.html',/19/,'paragraph'));
        if((intent.phone||intent.appointment)&&!intent.hours){
          if(!broadPage&&/standard/.test(raw))return reply(select('contact.html',/standard/,'definition'));
          if(!broadPage&&intent.appointment)broadPage='services/consultations.html';
          if(broadPage){
            var pageTerms=new Set(tokens(passages.filter(function(p){return p.page===broadPage;}).map(function(p){return p.text;}).join(' ')));
            if(words.some(function(w){return ['irm','cardiologie','cardiologue'].includes(w)&&!pageTerms.has(w);}))return unknown;
            var ph=passages.filter(function(p){return p.page===broadPage&&p.kind==='definition'&&isPhone(p);}).sort(function(a,b){var v=function(p){return /rendez|secretariat/.test(normalize(p.section))?2:/standard/.test(normalize(p.section))?0:1;};return v(b)-v(a);})[0];
            if(ph)return reply(ph);
          }
          if(!broadPage&&intent.phone)return unknown;
        }
        if(intent.hours&&broadPage){var hr=select(broadPage,/secretariat/.test(raw)?/secretariat/:/accueil telephonique|horaire|interventions/,'definition');if(hr)return reply(hr);}
        if(intent.address&&broadPage){var ad=select(broadPage,/adresse|\bou\b/,'definition');if(ad)return reply(ad);}
      }
      if(intent.visit&&!target.length)target=['parcours/visites.html','hebergement/vie-quotidienne.html'];
      if(intent.prepare&&!target.length)target=['parcours/preparer-venue.html'];
      if(intent.record)target=['parcours/dossier-medical.html'];
      if(intent.address&&!target.length)target=['acces.html'];
      if(intent.price&&/chambre/.test(raw))target=['parcours/frais.html'];
      if(intent.appointment&&!target.length)target=['services/consultations.html'];
      if(intent.phone&&/standard/.test(raw))target=['contact.html','annuaire.html'];
      var substantive=words.filter(function(w){return !synonyms.has(w)&&!/^\d+$/.test(w)&&!['rendez','vous','hospitalise','mere','pere','mamie','papa','maman'].includes(w);});
      // Un sujet absent (IRM, parking, cardiologie…) ne devient jamais une réponse voisine.
      if(substantive.some(function(w){return !vocab.has(w)&&!vocab.has(w.replace(/s$/,''));}))return unknown;
      var candidates=passages.map(function(p){
        var score=0,matched=0,exact=0,total=0,bodyMatch=0;
        words.forEach(function(w){var wt=weight(w);total+=wt;var b=p.bt.has(w),h=p.ht.has(w),alt=alternatives(w);var sb=alt.some(function(x){return p.bt.has(x);}),sh=alt.some(function(x){return p.ht.has(x);});
          if(b||h){matched+=wt;exact++;score+=wt*(b?2.4:1.7);if(b)bodyMatch++;}else if(sb||sh){matched+=wt*.7;score+=wt*(sb?1.1:.7);if(sb)bodyMatch+=.4;}
        });
        var coverage=matched/(total||1), sec=normalize(p.section),txt=normalize(p.text);
        if(target.length){if(target.includes(p.page))score+=10;else score-=10;}
        if(follow&&target.includes(p.page))score+=7;
        if(intent.phone&&/\d[\s\u00a0]*\d/.test(p.text)&&/telephone|standard|contact|rendez/.test(sec+' '+txt))score+=8;
        if(intent.appointment&&/rendez|secretariat|telephone/.test(sec+' '+txt))score+=6;
        if(intent.hours&&/horaire|ouverture|accueil telephonique|secretariat|heures de visite/.test(sec))score+=8;
        if(intent.address&&/adresse|ou|etage|niveau/.test(sec))score+=8;
        if(intent.price&&/[€%]|euros/.test(p.text))score+=8;
        if(intent.visit){if(/visite/.test(sec))score+=8;if(!/ehpad|resident|retraite|bel air|reflets/.test(raw)&&/ehpad/.test(sec+' '+txt))score-=12;}
        if(intent.prepare&&/documents|affaires|preparation/.test(sec))score+=8;
        if(intent.record&&/comment le demander/.test(sec))score+=6;
        if(/^(navigation|document)$/.test(p.kind))score-=7;
        if(/actualites\//.test(p.page)&&!/actualite|concert|chorale|velo|bilan|photobiomodulation/.test(raw))score-=7;
        if(p.page==='plan-du-site.html'||p.page==='index.html')score-=5;
        return {p:p,score:score,coverage:coverage,bodyMatch:bodyMatch,exact:exact};
      }).filter(function(r){return r.coverage>=.44&&r.exact>=1&&r.bodyMatch>0&&r.score>=5;}).sort(function(a,b){return b.score-a.score;});
      if(!candidates.length)return unknown;
      var best=candidates[0],p=best.p;
      // Les sigles/spécialités explicitement demandés doivent figurer dans le passage ou son titre.
      if(substantive.length&&substantive.some(function(w){return !p.all.has(w)&&!p.all.has(w.replace(/s$/,''));}))return unknown;
      if(target.length&&!target.includes(p.page))return unknown;
      if(intent.phone&&!isPhone(p))return unknown;
      if(intent.hours&&!/\d|lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche/.test(p.text))return unknown;
      if(intent.price&&!/[€%]|euros|gratuit|tarif|charge|factur|paiement/.test(normalize(p.text))&&!/[€%]/.test(p.text))return unknown;
      if(/^(navigation|document)$/.test(p.kind))return {kind:'answer',text:'Cette information est à consulter dans la page ou le document indiqué ci-dessous.',sources:[{title:p.title+' — '+p.section,url:p.url}],context:{page:p.page,passage:p.id}};
      return {kind:'answer',text:excerpt(p,words),sources:[{title:p.title+(p.section&&p.section!==p.title?' — '+p.section:''),url:p.url}],context:{page:p.page,passage:p.id}};
    }
    return {answer:answer};
  }
  var api={create:create,normalize:normalize};
  if(typeof module==='object'&&module.exports)module.exports=api;else root.HospitalAssistant=api;
})(typeof window!=='undefined'?window:this);
