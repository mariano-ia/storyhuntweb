document.addEventListener('DOMContentLoaded', () => {
    // Typewriter Effect
    const typewriterElement = document.getElementById('typewriter-text');
    if (typewriterElement) {
        const textToType = "An immersive mystery walk through NYC's hidden layers. Not a tour. A chat-based adventure you play with your phone, your wits, and the streets.";
        let index = 0;

        function typeWriter() {
            if (index < textToType.length) {
                typewriterElement.innerHTML += textToType.charAt(index);
                index++;
                setTimeout(typeWriter, 50);
            } else {
                typewriterElement.classList.add('visible');
            }
        }

        // Remove loading class
        setTimeout(() => {
            document.body.classList.remove('loading');
            const glitchEl = document.querySelector('.glitch');
            if (glitchEl) glitchEl.classList.add('visible');
            typeWriter();
        }, 1500);
    } else {
        // Explore pages: just remove loading
        setTimeout(() => {
            document.body.classList.remove('loading');
            const glitchEl = document.querySelector('.glitch');
            if (glitchEl) glitchEl.classList.add('visible');
        }, 1500);
    }

    // ─── Chat Demo Animation (Hero + HOW_IT_WORKS) ─────────────────────────────
    const chatConversations = [
        [
            { role: 'narrator', text: "Look up. The ceiling above you holds a secret most people walk right past." },
            { role: 'user', text: "The constellation mural on the ceiling?" },
            { role: 'narrator', text: "Yes. But did you notice? The stars are painted backwards. A deliberate mistake... or a message?" },
            { role: 'user', text: "Wait, backwards? Like a mirror?" },
            { role: 'narrator', text: "Exactly. Now find the one constellation that IS correct. That's your next clue." },
        ],
        [
            { role: 'narrator', text: "You're standing where a man jumped to his death in 1886. Except... he didn't die." },
            { role: 'user', text: "What happened to him?" },
            { role: 'narrator', text: "He survived. And what he built next changed this city forever. Look at the plaque on your left." },
            { role: 'user', text: "I see it! Washington Roebling?" },
            { role: 'narrator', text: "The man who built the bridge from his bedroom window. Now cross it. Your next clue is waiting on the other side." },
        ],
        [
            { role: 'narrator', text: "There's a door behind you. Most people think it's a janitor's closet." },
            { role: 'user', text: "I see a small green door with no sign" },
            { role: 'narrator', text: "That's the one. In 1924, this was the entrance to a speakeasy run by a woman known only as 'The Duchess'." },
            { role: 'user', text: "No way. Can I open it?" },
            { role: 'narrator', text: "Try knocking three times. Slowly." },
        ],
    ];

    const hiwConversation = [
        { role: 'narrator', text: "Find the bronze owl hidden on the facade." },
        { role: 'user', text: "Found it! Above the second window" },
        { role: 'narrator', text: "Correct. The owl marks a secret passage..." },
    ];

    function animateChat(container, conversation, opts = {}) {
        if (!container) return;
        const { loop = true, delayBetween = 2000, pauseAtEnd = 4000 } = opts;
        let convIndex = 0;

        async function playConversation(messages) {
            container.innerHTML = '';
            for (let i = 0; i < messages.length; i++) {
                const msg = messages[i];
                // Show typing indicator
                const typing = document.createElement('div');
                typing.className = 'chat-bubble chat-bubble--typing';
                typing.innerHTML = '<span></span><span></span><span></span>';
                if (msg.role === 'user') typing.style.alignSelf = 'flex-end';
                container.appendChild(typing);
                container.scrollTop = container.scrollHeight;
                await new Promise(r => setTimeout(r, 800 + Math.random() * 600));
                typing.remove();

                // Show message
                const bubble = document.createElement('div');
                bubble.className = `chat-bubble chat-bubble--${msg.role === 'narrator' ? 'narrator' : 'user'}`;
                bubble.textContent = msg.text;
                container.appendChild(bubble);
                container.scrollTop = container.scrollHeight;
                await new Promise(r => setTimeout(r, delayBetween));
            }
            // Pause at end, then fade out
            await new Promise(r => setTimeout(r, pauseAtEnd));
            container.style.opacity = '0';
            container.style.transition = 'opacity 0.6s ease';
            await new Promise(r => setTimeout(r, 600));
            container.style.opacity = '1';
        }

        async function run() {
            const msgs = Array.isArray(conversation[0]) ? conversation[convIndex % conversation.length] : conversation;
            await playConversation(msgs);
            if (loop && Array.isArray(conversation[0])) {
                convIndex++;
                run();
            } else if (loop) {
                run();
            }
        }

        // Start when visible
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                observer.disconnect();
                run();
            }
        }, { threshold: 0.3 });
        observer.observe(container);
    }

    // Hero chat — loops through conversations
    animateChat(document.getElementById('hero-chat'), chatConversations, {
        loop: true, delayBetween: 1800, pauseAtEnd: 3000,
    });

    // HIW mini chat — loops same short conversation
    animateChat(document.getElementById('hiw-chat-demo'), hiwConversation, {
        loop: true, delayBetween: 1500, pauseAtEnd: 2500,
    });

    // Intersection Observer for sections
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.2 });

    document.querySelectorAll('.reveal-text').forEach(el => {
        revealObserver.observe(el);
    });

    // Handle Form Submission via AJAX
    const form = document.querySelector('.recruitment-form');
    if (form) {
        const submitBtn = form.querySelector('.submit-btn');
        const btnText = submitBtn.querySelector('.btn-text');

        form.addEventListener('submit', (e) => {
            e.preventDefault();

            form.style.opacity = '0.5';
            form.style.pointerEvents = 'none';
            btnText.innerText = 'PROCESSING_REQUEST...';

            const formData = new FormData(form);
            const data = Object.fromEntries(formData);

            fetch(form.action, {
                method: "POST",
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            })
                .then(response => {
                    if (response.ok) {
                        form.style.opacity = '1';
                        form.style.pointerEvents = 'auto';
                        form.innerHTML = `
                        <div class="reveal-text visible" style="margin-top: 2rem; border: 1px solid var(--electric-blue); padding: 2rem; opacity: 1; transform: translateY(0);">
                            <p class="mono" style="color: var(--electric-blue); font-size: 1.2rem; margin-bottom: 1rem;">APPLICATION_RECEIVED // [200]</p>
                            <p class="mono" style="font-size: 0.8rem; line-height: 1.6; margin-bottom: 1.5rem;">YOUR_SPOT_IS_SECURED. YOU_GET_FREE_ACCESS_TO_YOUR_FIRST_HUNT.<br>CHECK_YOUR_INBOX_FOR_CONFIRMATION.</p>
                            <a href="/" class="primary-btn mono" style="padding: 0.8rem 2rem; font-size: 0.8rem;">
                                <span class="btn-text">RETURN_TO_BASE</span>
                                <span class="btn-hover">EXECUTE_RETURN</span>
                            </a>
                        </div>
                    `;
                    } else {
                        btnText.innerText = 'ERROR. TRY_AGAIN.';
                        form.style.opacity = '1';
                        form.style.pointerEvents = 'auto';
                    }
                })
                .catch(error => {
                    console.error('Error submitting form', error);
                    btnText.innerText = 'ERROR. TRY_AGAIN.';
                    form.style.opacity = '1';
                    form.style.pointerEvents = 'auto';
                });
        });
    }

    // ─── Load Experiences from API ────────────────────────────────────────────
    const API_BASE = '';
    const grid = document.getElementById('experience-grid');
    const subtitle = document.getElementById('missions-subtitle');

    // Global experience cache — used by showLangPicker to look up name + starting_point
    window.__shExperiences = {};

    if (grid) {
        fetch(`${API_BASE}/api/public/experiences`)
            .then(res => res.json())
            .then(experiences => {
                if (!Array.isArray(experiences) || experiences.length === 0) {
                    subtitle.textContent = 'NO_ACTIVE_MISSIONS';
                    grid.innerHTML = '<p class="mono" style="text-align:center;color:var(--text-muted);grid-column:1/-1;">STANDBY_MODE // NO_MISSIONS_AVAILABLE</p>';
                    return;
                }

                // Cache experiences by id so modal can pull name/start/price
                experiences.forEach(e => { window.__shExperiences[e.id] = e; });

                const published = experiences.filter(e => e.status === 'published').length;
                const coming = experiences.filter(e => e.status === 'coming_soon').length;
                subtitle.textContent = `ACTIVE_OPERATIONS: ${published} / ${experiences.length}  |  COMING_SOON: ${coming}`;

                const difficultyBar = (d) => {
                    if (d === 'easy') return '██░░░';
                    if (d === 'medium') return '███░░';
                    if (d === 'hard') return '█████';
                    return '░░░░░';
                };

                grid.innerHTML = experiences.map((exp, i) => {
                    const isLive = exp.status === 'published';
                    const cardClass = isLive ? 'active' : 'coming-soon';
                    const statusLabel = isLive ? 'LIVE' : 'COMING_SOON';
                    const dotClass = isLive ? '' : 'status-dot--pending';
                    const badgeClass = isLive ? '' : 'coming-soon-badge';
                    const delay = (0.2 + i * 0.08).toFixed(2);
                    const originalPrice = exp.price > 0 ? Math.ceil(exp.price * 1.5) - 0.01 : 0;
                    const priceLabel = exp.price > 0 ? `<span class="price-original">$${originalPrice.toFixed(2)}</span> $${exp.price}` : 'FREE';
                    const ctaLabel = exp.price > 0 ? 'BUY_ACCESS' : 'GET_FREE_ACCESS';

                    const backContent = isLive ? `
                        <h3>${(exp.name || '').toUpperCase()}</h3>
                        <p class="card-description">${exp.web_description || ''}</p>
                        ${exp.starting_point ? `
                        <div class="starting-point-badge">
                            <div class="starting-point-label">START_POINT</div>
                            <div class="starting-point-value">${exp.starting_point}</div>
                        </div>` : ''}
                        <div class="card-meta">
                            ${exp.duration ? `<div><span class="label">DURATION:</span> ${exp.duration.toUpperCase()}</div>` : ''}
                            ${exp.distance ? `<div><span class="label">DISTANCE:</span> ${exp.distance.toUpperCase()}</div>` : ''}
                            ${exp.difficulty ? `<div><span class="label">DIFFICULTY:</span> ${difficultyBar(exp.difficulty)}</div>` : ''}
                            <div><span class="label">PRICE:</span> ${priceLabel}</div>
                        </div>
                    ` : `
                        <h3>${(exp.name || '').toUpperCase()}</h3>
                        <p class="card-description">${exp.web_description || ''}</p>
                        <div class="card-meta">
                            <div><span class="label">STATUS:</span> IN_DEVELOPMENT</div>
                            ${exp.location ? `<div><span class="label">LOCATION:</span> ${exp.location.toUpperCase()}</div>` : ''}
                        </div>
                    `;

                    // CTA button on the front (visible without flip)
                    const frontCTA = isLive
                        ? `<button class="primary-btn mono card-front-cta" onclick="event.stopPropagation(); showLangPicker('${exp.id}');">${ctaLabel}</button>`
                        : `<a href="#cta" class="secondary-btn mono card-front-cta" onclick="event.stopPropagation();">NOTIFY_ME</a>`;

                    // Back CTA — single buy button
                    const backCTA = isLive
                        ? `<button class="primary-btn mono card-buy-btn" onclick="event.stopPropagation(); showLangPicker('${exp.id}');"><span class="btn-text">${ctaLabel}</span></button>`
                        : `<a href="#cta" class="secondary-btn mono card-notify-btn" onclick="event.stopPropagation();">NOTIFY_ME</a>`;

                    return `
                        <div class="experience-card ${cardClass} reveal-text" style="--d: ${delay}s">
                            <div class="card-inner">
                                <div class="card-front">
                                    <div class="card-status mono ${badgeClass}">
                                        <span class="status-dot ${dotClass}"></span> ${statusLabel}
                                    </div>
                                    <span class="card-flip-badge mono">TAP_FOR_MORE_DETAILS</span>
                                    ${exp.web_image ? `<img class="card-image" src="${exp.web_image}" alt="${exp.name}" loading="lazy">` : '<div class="card-image" style="background:#111;"></div>'}
                                    <div class="card-content">
                                        ${exp.location ? `<span class="card-location-badge mono">${exp.location.toUpperCase()}</span>` : ''}
                                        <h3>${(exp.name || '').toUpperCase()}</h3>
                                        <p class="card-tagline">${exp.web_tagline || ''}</p>
                                        ${isLive ? '<span class="card-langs mono">EN | ES</span>' : ''}
                                        <div class="card-front-footer">
                                            <span class="card-price mono">${isLive ? (exp.price > 0 ? `<span class="price-original">$${originalPrice.toFixed(2)}</span> $${exp.price} USD` : 'FREE') : 'COMING_SOON'}</span>
                                            ${frontCTA}
                                        </div>
                                    </div>
                                </div>
                                <div class="card-back">
                                    <span class="card-flip-badge">FLIP_BACK</span>
                                    ${backContent}
                                    ${backCTA}
                                </div>
                            </div>
                        </div>
                    `;
                }).join('');

                // Re-attach flip handlers and observers
                grid.querySelectorAll('.experience-card').forEach(card => {
                    card.addEventListener('click', (e) => {
                        if (e.target.closest('a') || e.target.closest('button')) return;
                        card.classList.toggle('flipped');
                    });
                });
                grid.querySelectorAll('.reveal-text').forEach(el => revealObserver.observe(el));
            })
            .catch(err => {
                console.error('Error loading experiences:', err);
                subtitle.textContent = 'CONNECTION_ERROR // RETRY_LATER';
            });
    }

    // ─── Language detection (URL > localStorage > navigator) ────────────────
    function detectLang() {
        const params = new URLSearchParams(window.location.search);
        const urlLang = params.get('lang');
        if (urlLang === 'es' || urlLang === 'en') return urlLang;
        try {
            const stored = window.localStorage.getItem('storyhunt_lang');
            if (stored === 'es' || stored === 'en') return stored;
        } catch {}
        const browserLang = (navigator.language || '').toLowerCase();
        return browserLang.startsWith('es') ? 'es' : 'en';
    }

    function detectPromoFromUrl() {
        const params = new URLSearchParams(window.location.search);
        return (params.get('promo') || '').trim().toUpperCase();
    }

    // ─── Language Picker / Checkout Modal (mirrors /start React modal) ─────
    window.showLangPicker = function(experienceId, experienceData) {
        const existing = document.getElementById('lang-picker-overlay');
        if (existing) existing.remove();

        // Fall back to global cache if no explicit data passed (existing onclick handlers
        // call showLangPicker('${exp.id}') without the data object).
        const exp = experienceData || (window.__shExperiences && window.__shExperiences[experienceId]) || {};

        let currentLang = detectLang();
        let showPromo = detectPromoFromUrl() !== '';
        const initialPromo = detectPromoFromUrl();
        const expName = exp.name || '';
        const startingPoint = exp.starting_point || '';
        const price = exp.price || 0;

        const overlay = document.createElement('div');
        overlay.id = 'lang-picker-overlay';
        overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.85);backdrop-filter:blur(8px);z-index:9999;display:flex;align-items:center;justify-content:center;padding:20px;animation:fadeIn 0.2s ease';

        function copyFor(lang) {
            return lang === 'es'
                ? {
                    eyebrow: 'ESTÁS POR DESBLOQUEAR',
                    intro: 'Una vez que pagues, podés <strong style="color:#fff;">jugar ahora o guardar el link para tu viaje</strong>. Tu reloj de 30 días arranca cuando toques “Start hunt” en el punto de partida — no cuando pagás.',
                    startPointLabel: 'PUNTO_DE_INICIO',
                    cta: 'Continuar al pago',
                    ctaHint: '→ Pago seguro vía Stripe',
                    emailLabel: 'Email (opcional)',
                    emailHint: 'Para enviarte el link de acceso',
                    emailPlaceholder: 'tu@email.com',
                    promoToggle: '¿Tenés un código promo?',
                    promoPlaceholder: 'CODIGO',
                    priceFooter: 'por grupo · paga 1 vez, jugás cuando quieras',
                    loading: 'PROCESANDO...',
                  }
                : {
                    eyebrow: "YOU'RE ABOUT TO UNLOCK",
                    intro: 'After payment, you can <strong style="color:#fff;">play now or save the link for your trip</strong>. Your 30-day clock starts when you tap “Start hunt” at the meeting point — not when you pay.',
                    startPointLabel: 'MEET_POINT',
                    cta: 'Continue to checkout',
                    ctaHint: '→ Secure payment via Stripe',
                    emailLabel: 'Email (optional)',
                    emailHint: 'To send you your access link',
                    emailPlaceholder: 'you@email.com',
                    promoToggle: 'Have a promo code?',
                    promoPlaceholder: 'CODE',
                    priceFooter: 'per group · pay once, play whenever',
                    loading: 'PROCESSING...',
                  };
        }

        function render() {
            const t = copyFor(currentLang);
            overlay.innerHTML = `
                <div style="position:relative;width:100%;max-width:420px;background:#0A0A0A;border:1px solid rgba(255,0,51,0.3);border-radius:16px;padding:24px 24px 20px;max-height:92vh;overflow-y:auto;font-family:'Space Mono',monospace;box-sizing:border-box;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
                        <div style="display:inline-flex;background:rgba(255,255,255,0.05);border-radius:999px;padding:3px;border:1px solid rgba(255,255,255,0.08);">
                            <button data-lang="en" style="padding:5px 14px;background:${currentLang==='en'?'#ff0033':'transparent'};border:none;border-radius:999px;color:${currentLang==='en'?'#fff':'#94A3B8'};font-family:inherit;font-size:11px;font-weight:700;letter-spacing:0.08em;cursor:pointer;">EN</button>
                            <button data-lang="es" style="padding:5px 14px;background:${currentLang==='es'?'#ff0033':'transparent'};border:none;border-radius:999px;color:${currentLang==='es'?'#fff':'#94A3B8'};font-family:inherit;font-size:11px;font-weight:700;letter-spacing:0.08em;cursor:pointer;">ES</button>
                        </div>
                        <button id="lp-close" style="background:none;border:none;color:#4B5563;cursor:pointer;padding:4px;font-size:20px;line-height:1;">×</button>
                    </div>

                    <p style="font-family:inherit;font-size:10px;color:#00d2ff;letter-spacing:0.15em;margin:0 0 6px;">${t.eyebrow}</p>
                    <h2 style="font-family:inherit;font-size:18px;color:#fff;margin:0 0 14px;text-transform:uppercase;letter-spacing:0.01em;line-height:1.25;">${expName}</h2>

                    <p style="font-family:'Inter',sans-serif;font-size:13px;color:#94A3B8;line-height:1.6;margin:0 0 14px;">${t.intro}</p>

                    ${startingPoint ? `
                    <div style="padding:10px 12px;background:rgba(255,0,51,0.06);border:1px solid rgba(255,0,51,0.2);border-radius:8px;margin-bottom:16px;">
                        <div style="font-family:inherit;font-size:9px;color:#ff0033;letter-spacing:0.12em;margin-bottom:3px;">${t.startPointLabel}</div>
                        <div style="font-family:'Inter',sans-serif;font-size:13px;color:#fff;font-weight:500;">${startingPoint}</div>
                    </div>
                    ` : ''}

                    <label style="display:block;font-family:inherit;font-size:11px;color:#94A3B8;letter-spacing:0.05em;margin-bottom:4px;">${t.emailLabel} <span style="color:#4B5563;font-weight:400;">— ${t.emailHint}</span></label>
                    <input id="lp-email" type="email" inputmode="email" autocomplete="email" placeholder="${t.emailPlaceholder}" style="width:100%;padding:11px 14px;background:rgba(255,255,255,0.04);border:1px solid rgba(0,210,255,0.2);border-radius:8px;color:#fff;font-family:'Inter',sans-serif;font-size:14px;outline:none;margin-bottom:14px;box-sizing:border-box;" />

                    <button id="lp-cta" style="width:100%;padding:14px 24px;background:#ff0033;border:none;border-radius:10px;color:#fff;font-family:inherit;font-size:14px;font-weight:700;letter-spacing:0.05em;cursor:pointer;min-height:50px;margin-bottom:6px;">${t.cta} →</button>
                    <p style="font-family:inherit;font-size:10px;color:#4B5563;text-align:center;margin:0 0 12px;letter-spacing:0.05em;">${t.ctaHint}</p>

                    <div style="margin-bottom:14px;">
                        ${showPromo
                            ? `<input id="lp-promo" type="text" placeholder="${t.promoPlaceholder}" value="${initialPromo}" style="width:100%;padding:10px 14px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);border-radius:8px;color:#fff;font-family:inherit;font-size:13px;text-align:center;text-transform:uppercase;letter-spacing:0.1em;outline:none;box-sizing:border-box;" />`
                            : `<button id="lp-promo-toggle" style="background:transparent;border:none;color:#94A3B8;font-family:inherit;font-size:11px;letter-spacing:0.05em;cursor:pointer;padding:0;">▸ ${t.promoToggle}</button>`
                        }
                    </div>

                    <div style="padding-top:12px;border-top:1px solid rgba(255,255,255,0.06);text-align:center;font-family:inherit;font-size:11px;color:#64748B;letter-spacing:0.04em;">
                        <span style="color:#ff0033;font-size:16px;font-weight:700;margin-right:6px;">$${price.toFixed(2)}</span>${t.priceFooter}
                    </div>
                    <p id="lp-error" style="display:none;margin-top:12px;font-family:inherit;font-size:12px;color:#ff0033;text-align:center;"></p>
                </div>
            `;

            // Wire interactions
            overlay.querySelector('#lp-close').addEventListener('click', () => overlay.remove());
            overlay.querySelectorAll('[data-lang]').forEach(btn => {
                btn.addEventListener('click', () => {
                    currentLang = btn.getAttribute('data-lang');
                    render();
                });
            });
            const promoToggle = overlay.querySelector('#lp-promo-toggle');
            if (promoToggle) {
                promoToggle.addEventListener('click', () => { showPromo = true; render(); });
            }
            overlay.querySelector('#lp-cta').addEventListener('click', () => doCheckout(experienceId));
        }

        async function doCheckout(expId) {
            const t = copyFor(currentLang);
            const cta = overlay.querySelector('#lp-cta');
            const error = overlay.querySelector('#lp-error');
            const email = (overlay.querySelector('#lp-email') || {}).value || '';
            const promo = (overlay.querySelector('#lp-promo') || {}).value || initialPromo;
            cta.disabled = true;
            cta.textContent = t.loading;
            error.style.display = 'none';
            try { window.localStorage.setItem('storyhunt_lang', currentLang); } catch {}

            try {
                const body = { experience_id: expId, lang: currentLang };
                if (promo.trim()) body.coupon_code = promo.trim().toUpperCase();
                if (email.trim()) body.email = email.trim();

                const res = await fetch(`${API_BASE}/api/checkout`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(body),
                });
                const data = await res.json();
                if (data.url) {
                    // Fire add_payment_info with send_instantly so PostHog flushes before
                    // navigation steals the page. 300ms wait covers fbq/gtag if loaded.
                    if (window.posthog && window.posthog.capture) {
                        window.posthog.capture('add_payment_info', { content_ids: [expId], value: price, currency: 'USD' }, { send_instantly: true });
                    }
                    await new Promise(r => setTimeout(r, 300));
                    window.location.href = data.url;
                } else {
                    error.textContent = data.error || 'Error creating checkout session';
                    error.style.display = 'block';
                    cta.disabled = false;
                    cta.textContent = t.cta + ' →';
                }
            } catch (err) {
                console.error('Checkout error:', err);
                error.textContent = 'Connection error. Please try again.';
                error.style.display = 'block';
                cta.disabled = false;
                cta.textContent = t.cta + ' →';
            }
        }

        render();
        overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });
        document.body.appendChild(overlay);

        // Fire InitiateCheckout
        if (window.posthog && window.posthog.capture) {
            window.posthog.capture('begin_checkout', { content_ids: [experienceId], value: price, currency: 'USD' });
        }
    };

    // Backwards-compat shim — old onclick handlers may still call startCheckout(id, lang)
    window.startCheckout = async function(experienceId, lang) {
        try { window.localStorage.setItem('storyhunt_lang', lang); } catch {}
        try {
            const body = { experience_id: experienceId, lang: lang };
            const res = await fetch(`${API_BASE}/api/checkout`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            const data = await res.json();
            if (data.url) window.location.href = data.url;
            else alert(data.error || 'Error creating checkout session');
        } catch (err) {
            console.error('Checkout error:', err);
            alert('Connection error. Please try again.');
        }
    };

    // Nav Scroll Effect
    const nav = document.querySelector('.nav');
    if (nav) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 100) {
                nav.classList.add('nav--scrolled');
            } else {
                nav.classList.remove('nav--scrolled');
            }
        });
    }

    // Smooth Scroll for Anchor Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            const targetId = anchor.getAttribute('href');
            if (targetId === '#') return;
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});
