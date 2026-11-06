/* Assistant documentaire local : l’interface n’envoie aucune question à un serveur. */
(function () {
  'use strict';
  if (document.getElementById('ha-launch')) return;
  var d = document, base = d.documentElement.getAttribute('data-base') || '';
  var rootURL = new URL(base || './', location.href);
  var icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 11.5a8 8 0 0 1-8 8H5l-3 2v-10a8 8 0 0 1 8-8h2a8 8 0 0 1 8 8Z"/><path d="M7 10h8m-8 4h5"/></svg>';
  var host = d.createElement('div');
  host.className = 'ha-widget';
  // Markup below is constant. Questions, answers and links are inserted as text nodes.
  host.innerHTML = '<button type="button" id="ha-launch" class="ha-launch" aria-haspopup="dialog" aria-controls="ha-dialog" aria-expanded="false">' + icon + '<span>Une question ?</span></button>' +
    '<dialog id="ha-dialog" class="ha-dialog" aria-labelledby="ha-title" aria-describedby="ha-intro">' +
      '<div class="ha-shell"><header class="ha-head"><div class="ha-head-icon">' + icon + '</div><div class="ha-heading"><span>À votre écoute</span><h2 id="ha-title">L’assistant du site</h2></div><button type="button" class="ha-close" aria-label="Fermer l’assistant"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg></button></header>' +
      '<div class="ha-toolbar"><span>Informations du site · aucune donnée envoyée</span><button type="button" class="ha-reset" aria-label="Recommencer la conversation">Recommencer</button></div>' +
      '<div class="ha-scroll"><p id="ha-intro" class="ha-intro">Je vous aide à trouver une information sur l’hôpital. Posez votre question, je vous indique la page utile.</p><div class="ha-start" aria-label="Exemples de questions"></div><div class="ha-messages" role="log" aria-label="Conversation avec l’assistant" aria-live="polite" aria-relevant="additions" aria-atomic="false"></div></div>' +
      '<div class="ha-load" role="status"><span></span><button type="button" hidden>Réessayer</button></div>' +
      '<form class="ha-form"><label for="ha-question">Votre question</label><div class="ha-compose"><textarea id="ha-question" name="question" rows="2" maxlength="400" required placeholder="À quelle heure puis-je rendre visite ?" aria-describedby="ha-input-help" enterkeyhint="send"></textarea><button type="submit" class="ha-send" aria-label="Envoyer ma question" disabled><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m4 12 16-8-6 16-3-6-7-2Z"/><path d="m11 14 9-10"/></svg></button></div><span id="ha-input-help" class="ha-help">N’indiquez pas d’information médicale personnelle.</span></form>' +
      '<div class="ha-emergency">Pour une urgence : <a href="tel:15">15</a> ou <a href="tel:112">112</a>.</div></div>' +
    '</dialog>';
  d.body.appendChild(host);
  var launch = host.querySelector('.ha-launch'), dialog = host.querySelector('dialog');
  var form = host.querySelector('.ha-form'), input = host.querySelector('textarea'), submit = host.querySelector('.ha-send');
  var transcript = host.querySelector('.ha-messages'), scroll = host.querySelector('.ha-scroll');
  var load = host.querySelector('.ha-load'), loadText = load.querySelector('span'), retry = load.querySelector('button');
  var starters = host.querySelector('.ha-start'), reset = host.querySelector('.ha-reset');
  var engine = null, context = {}, loading = false, answering = false, previousFocus = null, request = 0;
  var initialQuestions = ['Horaires de visite', 'Prendre rendez-vous', 'Préparer mon séjour', 'Venir à l’hôpital'];

  function setStatus(message, error) {
    loadText.textContent = message;
    load.hidden = !message;
    load.classList.toggle('ha-load-error', !!error);
    retry.hidden = !error;
  }
  function updateControls() {
    submit.disabled = loading || answering || !engine || !input.value.trim();
    starters.querySelectorAll('button').forEach(function (b) { b.disabled = loading || answering || !engine; });
    form.setAttribute('aria-busy', String(loading || answering));
  }
  function scrollToLatest() { scroll.scrollTop = scroll.scrollHeight; }
  function sourceURL(value) {
    if (typeof value !== 'string' || !value) return null;
    try {
      var url = new URL(value, rootURL);
      if (url.origin !== location.origin || !/^(https?:|file:)$/.test(url.protocol)) return null;
      return url.href;
    } catch (e) { return null; }
  }
  function addMessage(text, isUser, result) {
    var message = d.createElement('div');
    message.className = 'ha-message ' + (isUser ? 'ha-user' : 'ha-answer');
    if (result && result.kind === 'urgent') message.classList.add('ha-urgent');
    var label = d.createElement('span');
    label.className = 'ha-speaker'; label.textContent = isUser ? 'Vous' : 'L’assistant du site';
    var paragraph = d.createElement('p'); paragraph.textContent = text;
    message.appendChild(label); message.appendChild(paragraph);
    if (result && Array.isArray(result.sources)) {
      var links = d.createElement('ul'); links.className = 'ha-sources';
      result.sources.forEach(function (source) {
        var url = sourceURL(source.url);
        if (!url) return;
        var li = d.createElement('li'), a = d.createElement('a');
        a.href = url; a.textContent = source.title || 'Voir la page concernée';
        li.appendChild(a); links.appendChild(li);
      });
      if (links.childNodes.length) message.appendChild(links);
    }
    if (result && Array.isArray(result.suggestions) && result.suggestions.length) {
      var choices = d.createElement('div'); choices.className = 'ha-choices';
      result.suggestions.slice(0, 4).forEach(function (choice) {
        if (!choice || typeof choice.question !== 'string') return;
        var b = d.createElement('button'); b.type = 'button'; b.textContent = choice.label || choice.question;
        b.addEventListener('click', function () { ask(choice.question); }); choices.appendChild(b);
      });
      message.appendChild(choices);
    }
    transcript.appendChild(message);
    scrollToLatest();
  }
  function freshConversation() {
    context = {}; transcript.replaceChildren(); input.value = '';
    starters.hidden = false; host.querySelector('.ha-intro').hidden = false;
    scroll.scrollTop = 0; updateControls(); input.focus({preventScroll: true});
  }
  function loadIndex() {
    var id = ++request;
    loading = true; engine = null; setStatus('Chargement des informations du site…', false); updateControls();
    return fetch(new URL('assets/assistant-index.json', rootURL).href, {cache: 'no-store', credentials: 'same-origin'})
      .then(function (response) {
        if (!response.ok) throw new Error('index');
        return response.json();
      }).then(function (data) {
        if (id !== request) return;
        if (!window.HospitalAssistant || typeof window.HospitalAssistant.create !== 'function') throw new Error('engine');
        engine = window.HospitalAssistant.create(data);
        if (!engine || typeof engine.answer !== 'function') throw new Error('engine');
        setStatus('', false);
      }).catch(function () {
        if (id !== request) return;
        engine = null;
        setStatus('Les informations ne sont pas accessibles pour le moment. Réessayez ou utilisez l’annuaire du site.', true);
      }).finally(function () {
        if (id !== request) return;
        loading = false; updateControls();
      });
  }
  function ask(question) {
    var q = String(question || '').trim();
    if (!q || q.length > 400 || !engine || loading || answering) return;
    answering = true; starters.hidden = true; host.querySelector('.ha-intro').hidden = true;
    addMessage(q, true); input.value = ''; updateControls();
    Promise.resolve().then(function () { return engine.answer(q, context); }).then(function (result) {
      if (!result || typeof result.text !== 'string' || !result.text.trim()) throw new Error('answer');
      if (result.context) context = result.context;
      addMessage(result.text, false, result);
    }).catch(function () {
      addMessage('Je n’ai pas pu trouver une réponse. Vous pouvez reformuler votre question ou consulter l’annuaire.', false, {sources:[{title:'Consulter l’annuaire', url:'annuaire.html'}]});
    }).finally(function () {
      answering = false; updateControls();
      if (dialog.open) input.focus({preventScroll: true});
    });
  }
  function openAssistant() {
    if (dialog.open) return;
    previousFocus = d.activeElement;
    if (typeof dialog.showModal === 'function') dialog.showModal();
    else { dialog.setAttribute('open', ''); dialog.setAttribute('aria-modal', 'true'); }
    launch.setAttribute('aria-expanded', 'true');
    input.focus({preventScroll: true});
    loadIndex();
  }
  function closeAssistant() {
    if (typeof dialog.close === 'function') dialog.close();
    else { dialog.removeAttribute('open'); onClosed(); }
  }
  function onClosed() {
    launch.setAttribute('aria-expanded', 'false');
    if (previousFocus && previousFocus.isConnected) previousFocus.focus({preventScroll: true});
    else launch.focus({preventScroll: true});
  }
  initialQuestions.forEach(function (q) {
    var b = d.createElement('button'); b.type = 'button'; b.textContent = q; b.disabled = true;
    b.addEventListener('click', function () { ask(q); }); starters.appendChild(b);
  });
  launch.addEventListener('click', openAssistant);
  host.querySelector('.ha-close').addEventListener('click', closeAssistant);
  dialog.addEventListener('close', onClosed);
  dialog.addEventListener('cancel', function (event) { event.preventDefault(); closeAssistant(); });
  dialog.addEventListener('click', function (event) {
    if (event.target !== dialog) return;
    var rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) closeAssistant();
  });
  dialog.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') { event.preventDefault(); closeAssistant(); return; }
    if (event.key !== 'Tab') return;
    var focusable = Array.from(dialog.querySelectorAll('button:not([disabled]),a[href],textarea:not([disabled])')).filter(function (el) { return el.getClientRects().length; });
    var first = focusable[0], last = focusable[focusable.length-1];
    if (event.shiftKey && d.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && d.activeElement === last) { event.preventDefault(); first.focus(); }
  });
  input.addEventListener('input', updateControls);
  input.addEventListener('keydown', function (event) {
    if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) { event.preventDefault(); ask(input.value); }
  });
  form.addEventListener('submit', function (event) { event.preventDefault(); ask(input.value); });
  reset.addEventListener('click', freshConversation);
  retry.addEventListener('click', loadIndex);
})();
