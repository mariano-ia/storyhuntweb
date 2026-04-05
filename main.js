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

    if (grid) {
        fetch(`${API_BASE}/api/public/experiences`)
            .then(res => res.json())
            .then(experiences => {
                if (!Array.isArray(experiences) || experiences.length === 0) {
                    subtitle.textContent = 'NO_ACTIVE_MISSIONS';
                    grid.innerHTML = '<p class="mono" style="text-align:center;color:var(--text-muted);grid-column:1/-1;">STANDBY_MODE // NO_MISSIONS_AVAILABLE</p>';
                    return;
                }

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
                    const priceLabel = exp.price > 0 ? `$${exp.price}` : 'FREE';
                    const ctaLabel = exp.price > 0 ? 'BUY_ACCESS' : 'GET_FREE_ACCESS';

                    const backContent = isLive ? `
                        <h3>${(exp.name || '').toUpperCase()}</h3>
                        <p class="card-description">${exp.web_description || ''}</p>
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
                                    ${exp.web_image ? `<img class="card-image" src="${exp.web_image}" alt="${exp.name}" loading="lazy">` : '<div class="card-image" style="background:#111;"></div>'}
                                    <div class="card-content">
                                        ${exp.location ? `<span class="card-location-badge mono">${exp.location.toUpperCase()}</span>` : ''}
                                        <h3>${(exp.name || '').toUpperCase()}</h3>
                                        <p class="card-tagline">${exp.web_tagline || ''}</p>
                                        ${isLive ? '<span class="card-langs mono">EN | ES</span>' : ''}
                                        <div class="card-front-footer">
                                            <span class="card-price mono">${isLive ? (exp.price > 0 ? `$${exp.price} USD` : 'FREE') : 'COMING_SOON'}</span>
                                            ${frontCTA}
                                        </div>
                                        <span class="card-flip-hint mono always-visible">TAP_FOR_DETAILS &gt;</span>
                                    </div>
                                </div>
                                <div class="card-back">
                                    ${backContent}
                                    ${backCTA}
                                    <span class="card-flip-hint">&lt; FLIP_BACK</span>
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

    // ─── Language Picker (pre-checkout) ─────────────────────────────────────────
    window.showLangPicker = function(experienceId) {
        // Remove any existing picker
        const existing = document.getElementById('lang-picker-overlay');
        if (existing) existing.remove();

        const overlay = document.createElement('div');
        overlay.id = 'lang-picker-overlay';
        overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.85);z-index:9999;display:flex;align-items:center;justify-content:center;animation:fadeIn 0.2s ease';
        overlay.innerHTML = `
            <div style="background:#0a0a0a;border:1px solid rgba(124,58,237,0.4);border-radius:12px;padding:2.5rem;max-width:360px;width:90%;text-align:center;">
                <p class="mono" style="color:#7C3AED;font-size:0.75rem;margin-bottom:0.5rem;letter-spacing:2px;">SELECT_LANGUAGE</p>
                <p class="mono" style="color:rgba(255,255,255,0.5);font-size:0.7rem;margin-bottom:1.5rem;">CHOOSE_YOUR_PREFERRED_LANGUAGE</p>
                <div style="display:flex;flex-direction:column;gap:0.75rem;">
                    <button class="mono" onclick="startCheckout('${experienceId}', 'en')" style="display:block;width:100%;padding:0.9rem;font-size:0.8rem;font-weight:700;letter-spacing:2px;background:var(--accent);color:#fff;border:none;border-radius:6px;cursor:pointer;">ENGLISH</button>
                    <button class="mono" onclick="startCheckout('${experienceId}', 'es')" style="display:block;width:100%;padding:0.9rem;font-size:0.8rem;font-weight:700;letter-spacing:2px;background:transparent;color:#fff;border:1px solid rgba(255,255,255,0.3);border-radius:6px;cursor:pointer;">ESPANOL</button>
                </div>
                <button class="mono" onclick="document.getElementById('lang-picker-overlay').remove()" style="background:none;border:none;color:rgba(255,255,255,0.3);margin-top:1rem;cursor:pointer;font-size:0.7rem;">CANCEL</button>
            </div>
        `;
        overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });
        document.body.appendChild(overlay);
    };

    // ─── Stripe Checkout ──────────────────────────────────────────────────────
    window.startCheckout = async function(experienceId, lang) {
        // Close lang picker if open
        const picker = document.getElementById('lang-picker-overlay');
        if (picker) picker.remove();
        try {
            const res = await fetch(`${API_BASE}/api/checkout`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ experience_id: experienceId, lang: lang }),
            });
            const data = await res.json();
            if (data.url) {
                window.location.href = data.url;
            } else {
                alert(data.error || 'Error creating checkout session');
            }
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
