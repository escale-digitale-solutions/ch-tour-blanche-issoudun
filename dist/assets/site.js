/* Centre Hospitalier de la Tour Blanche : interactions.
   Aucune dépendance, aucun traceur. Le site reste lisible sans JavaScript. */
(function () {
  'use strict';
  var d = document, root = d.documentElement;
  var $ = function (s, c) { return (c || d).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); };
  var store = {
    get: function (k) { try { return localStorage.getItem('chtb:' + k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem('chtb:' + k, v); } catch (e) {} }
  };
  var norm = function (s) {
    return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[’'\-]/g, ' ').replace(/\s+/g, ' ').trim();
  };

  /* Menu principal */
  var navBtns = $$('.nav-btn[aria-controls]');
  function closeMenus(except) {
    navBtns.forEach(function (b) {
      if (b === except) return;
      b.setAttribute('aria-expanded', 'false');
      var m = d.getElementById(b.getAttribute('aria-controls'));
      if (m) m.classList.remove('open');
    });
  }
  navBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      var open = b.getAttribute('aria-expanded') === 'true';
      closeMenus(b);
      b.setAttribute('aria-expanded', String(!open));
      d.getElementById(b.getAttribute('aria-controls')).classList.toggle('open', !open);
      togglePrefs(false);
    });
  });
  var menuBtn = $('.menu-btn'), nav = $('.nav');
  function toggleNav(force) {
    var open = typeof force === 'boolean' ? force : !nav.classList.contains('open');
    nav.classList.toggle('open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    if (open) window.scrollTo(0, 0);
  }
  if (menuBtn) menuBtn.addEventListener('click', function () { toggleNav(); });
  $$('[data-open-menu]').forEach(function (b) { b.addEventListener('click', function () { toggleNav(); }); });
  d.addEventListener('click', function (e) {
    if (!e.target.closest('.head')) { closeMenus(); togglePrefs(false); }
  });

  /* Confort de lecture */
  var prefs = $('.prefs'), prefBtn = $('[data-prefs]');
  function togglePrefs(force) {
    if (!prefs) return;
    var open = typeof force === 'boolean' ? force : !prefs.classList.contains('open');
    prefs.classList.toggle('open', open);
    prefBtn.setAttribute('aria-expanded', String(open));
  }
  if (prefBtn) prefBtn.addEventListener('click', function (e) { e.stopPropagation(); closeMenus(); togglePrefs(); });
  function applyPref(name, val) {
    if (val && val !== 'normal') root.setAttribute('data-' + name, val); else root.removeAttribute('data-' + name);
    $$('[data-' + name + '-set]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-' + name + '-set') === (val || 'normal')));
    });
  }
  ['size', 'contrast'].forEach(function (name) {
    applyPref(name, store.get(name));
    $$('[data-' + name + '-set]').forEach(function (b) {
      b.addEventListener('click', function () {
        var v = b.getAttribute('data-' + name + '-set');
        store.set(name, v); applyPref(name, v);
      });
    });
  });

  /* Recherche */
  var dlg = $('dialog.search'), input = dlg && $('input', dlg), list = dlg && $('.s-res', dlg), empty = dlg && $('.s-empty', dlg);
  var base = root.getAttribute('data-base') || '';
  var phoneDigits = function (s) {
    var n = (s || '').replace(/\D/g, '');
    if (/^\+33/.test(s)) return '0' + n.slice(2).replace(/^0/, '');
    if (/^0033/.test(n)) return '0' + n.slice(4).replace(/^0/, '');
    return n;
  };
  var idx = (window.SEARCH_INDEX || []).map(function (p) {
    p.nt = norm(p.t);
    p.nh = norm(p.t + ' ' + p.d + ' ' + (p.k || '') + ' ' + (p.b || ''));
    p.numbers = (p.p || []).map(phoneDigits);
    return p;
  });
  var sel = -1;
  var syn = { rdv: 'rendez vous', irm: 'imagerie', radio: 'imagerie', radiologie: 'imagerie', scanner: 'imagerie', kine: 'readaptation', maternite: 'perinatal', grossesse: 'perinatal', sage: 'perinatal', ivg: 'sante sexuelle', planning: 'sante sexuelle', alzheimer: 'parenthese', vieux: 'ehpad', retraite: 'ehpad', maison: 'ehpad', job: 'emploi', travail: 'emploi', telephone: 'annuaire', numero: 'annuaire', parking: 'acces', venir: 'acces' };
  function hasTerm(text, term) {
    // Les sigles doivent former un mot : « IRM » ne doit pas retrouver « infirmier ».
    return term.length <= 3 ? text.split(/[^a-z0-9]+/).indexOf(term) > -1 : text.indexOf(term) > -1;
  }
  function searchResults(q) {
    var query = (q || '').trim();
    var numeric = /^[+\d\s().-]+$/.test(query) && query.replace(/\D/g, '').length >= 3;
    var number = numeric ? phoneDigits(query) : '';
    var words = norm(query).split(' ').filter(Boolean);
    if (!words.length) return [];
    return idx.map(function (p) {
      if (numeric) {
        var phoneScore = 0;
        p.numbers.forEach(function (n) {
          if (n === number) phoneScore = Math.max(phoneScore, 30);
          else if (n.indexOf(number) > -1) phoneScore = Math.max(phoneScore, 15);
        });
        // Les lignes de l’annuaire et les consultations précises précèdent les pages générales.
        if (phoneScore && !p.b) phoneScore += 5;
        return { p: p, s: phoneScore };
      }
      var s = 0;
      for (var i = 0; i < words.length; i++) {
        var w = words[i];
        var alternatives = syn[w] ? [w, syn[w]] : [w];
        var best = 0;
        alternatives.forEach(function (term, j) {
          var score = hasTerm(p.nt, term) ? (p.nt.indexOf(term) === 0 ? 8 : 5) : hasTerm(p.nh, term) ? 2 : 0;
          if (score) best = Math.max(best, score - (j ? 0.5 : 0));
        });
        if (!best) return { p: p, s: 0 };
        s += best;
      }
      return { p: p, s: s };
    }).filter(function (r) { return r.s > 0; }).sort(function (a, b) { return b.s - a.s; }).slice(0, 9);
  }
  function run(q) {
    list.innerHTML = ''; sel = -1;
    if (!norm(q)) { empty.hidden = true; return; }
    var res = searchResults(q);
    empty.hidden = res.length > 0;
    res.forEach(function (r) {
      var li = d.createElement('li'), a = d.createElement('a'), b = d.createElement('b'), s = d.createElement('span');
      a.href = base + r.p.u; a.className = 'l-' + (r.p.l || 'inst');
      b.textContent = r.p.t; s.textContent = r.p.d; a.appendChild(b); a.appendChild(s);
      li.appendChild(a); list.appendChild(li);
    });
  }
  function openSearch(q) {
    if (!dlg) return;
    closeMenus();
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
    input.value = q || ''; run(input.value); input.focus();
  }
  if (dlg) {
    input.addEventListener('input', function () { run(input.value); });
    input.addEventListener('keydown', function (e) {
      var as = $$('a', list);
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault(); if (!as.length) return;
        sel = (sel + (e.key === 'ArrowDown' ? 1 : -1) + as.length) % as.length;
        as.forEach(function (a, i) { a.classList.toggle('sel', i === sel); });
        as[sel].scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'Enter') {
        var t = as[sel] || as[0]; if (t) { e.preventDefault(); location.href = t.href; }
      }
    });
    $('[data-close-search]', dlg).addEventListener('click', function () { dlg.close(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  }
  $$('[data-search]').forEach(function (b) { b.addEventListener('click', function (e) { e.preventDefault(); openSearch(); }); });
  var hs = $('[data-hero-search]');
  if (hs) hs.addEventListener('submit', function (e) { e.preventDefault(); openSearch($('input', hs).value); });
  d.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); openSearch(); }
    if (e.key === 'Escape') { closeMenus(); togglePrefs(false); if (nav && nav.classList.contains('open')) toggleNav(false); }
  });

  /* Filtres de listes et tableaux */
  $$('[data-filter-for]').forEach(function (box) {
    var target = d.getElementById(box.getAttribute('data-filter-for'));
    var rows = $$('[data-row]', target), inp = $('input[type=search]', box), chips = $$('.chip', box);
    var count = $('.count', box), none = target.parentNode.querySelector('.empty') || $('.empty', target);
    var today = new Date().getDay() || 7;
    rows.forEach(function (r) {
      var days = (r.getAttribute('data-days') || '').split(',');
      r._today = days.indexOf(String(today)) > -1;
      if (r._today) r.classList.add('today');
    });
    function apply() {
      var q = inp ? norm(inp.value) : '';
      var active = chips.filter(function (c) { return c.getAttribute('aria-pressed') === 'true'; })[0];
      var f = active ? active.getAttribute('data-f') : '';
      var n = 0;
      rows.forEach(function (r) {
        var ok = (!q || norm(r.textContent).indexOf(q) > -1) &&
          (!f || (f === 'today' ? r._today : (r.getAttribute('data-cat') || '').split(' ').indexOf(f) > -1));
        r.hidden = !ok; if (ok) n++;
      });
      $$('[data-group]', target).forEach(function (g) {
        g.hidden = !$$('[data-row]', g).some(function (r) { return !r.hidden; });
      });
      if (count) count.textContent = n + (n > 1 ? ' résultats' : ' résultat');
      if (none) none.hidden = n > 0;
    }
    if (inp) inp.addEventListener('input', apply);
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        var was = c.getAttribute('aria-pressed') === 'true';
        chips.forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        if (!was) c.setAttribute('aria-pressed', 'true');
        apply();
      });
    });
    apply();
  });

  /* Liste de préparation */
  $$('[data-checklist]').forEach(function (form) {
    var key = 'check:' + form.getAttribute('data-checklist');
    var boxes = $$('input[type=checkbox]', form), prog = $('.prog', form);
    var saved = {};
    try { saved = JSON.parse(store.get(key) || '{}'); } catch (e) {}
    function upd() {
      var n = boxes.filter(function (b) { return b.checked; }).length;
      if (prog) prog.textContent = n + ' sur ' + boxes.length + ' prêts';
      var o = {}; boxes.forEach(function (b, i) { if (b.checked) o[i] = 1; });
      store.set(key, JSON.stringify(o));
    }
    boxes.forEach(function (b, i) { b.checked = !!saved[i]; b.addEventListener('change', upd); });
    var clear = $('[data-clear]', form);
    if (clear) clear.addEventListener('click', function () { boxes.forEach(function (b) { b.checked = false; }); upd(); });
    upd();
  });
  $$('[data-print]').forEach(function (b) { b.addEventListener('click', function () { window.print(); }); });

  /* Vérificateur de commune */
  $$('[data-communes]').forEach(function (form) {
    var list = form.getAttribute('data-communes').split('|');
    var inp = $('input', form), out = $('.result', form), nlist = list.map(norm);
    function check() {
      var q = norm(inp.value);
      if (!q) { out.hidden = true; return; }
      var i = nlist.indexOf(q), part = nlist.filter(function (c) { return c.indexOf(q) === 0; });
      out.hidden = false;
      if (i > -1) out.textContent = list[i] + ' fait partie du secteur d’intervention du SSIAD.';
      else if (part.length === 1) out.textContent = list[nlist.indexOf(part[0])] + ' fait partie du secteur d’intervention du SSIAD.';
      else if (part.length > 1) out.textContent = 'Précisez : ' + part.map(function (c) { return list[nlist.indexOf(c)]; }).join(', ') + '.';
      else out.textContent = 'Cette commune ne figure pas dans la liste du SSIAD. Appelez le 02 54 03 17 76 pour connaître la solution adaptée.';
    }
    inp.addEventListener('input', check);
    form.addEventListener('submit', function (e) { e.preventDefault(); check(); });
  });

  /* Contact : aiguillage et démonstration */
  var motif = $('[data-motif]');
  if (motif) {
    var panels = $$('[data-motif-panel]');
    var show = function () {
      panels.forEach(function (p) { p.hidden = p.getAttribute('data-motif-panel') !== motif.value; });
    };
    motif.addEventListener('change', show); show();
  }
  $$('[data-demo-form]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var r = $('.result', f); r.hidden = false; r.focus();
    });
  });
})();
