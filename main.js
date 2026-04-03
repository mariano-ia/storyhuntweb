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
    const API_BASE = 'https://storyhunt-app.vercel.app';
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

                    const backContent = isLive ? `
                        <h3>${(exp.name || '').toUpperCase()}</h3>
                        <p class="card-description">${exp.web_description || exp.description || ''}</p>
                        <div class="card-meta">
                            ${exp.duration ? `<div><span class="label">DURATION:</span> ${exp.duration.toUpperCase()}</div>` : ''}
                            ${exp.distance ? `<div><span class="label">DISTANCE:</span> ${exp.distance.toUpperCase()}</div>` : ''}
                            ${exp.difficulty ? `<div><span class="label">DIFFICULTY:</span> ${difficultyBar(exp.difficulty)}</div>` : ''}
                            <div><span class="label">PRICE:</span> ${exp.price > 0 ? `$${exp.price}` : '<span class="price-free">FREE</span>'}</div>
                        </div>
                        <a href="${API_BASE}/api/checkout?experience_id=${exp.id}&lang=en" class="primary-btn mono card-buy-btn"
                           onclick="event.preventDefault(); startCheckout('${exp.id}', 'en');">
                            <span class="btn-text">${exp.price > 0 ? 'BUY_ACCESS' : 'GET_FREE_ACCESS'}</span>
                            <span class="btn-hover">SECURE_YOUR_SPOT</span>
                        </a>
                    ` : `
                        <h3>${(exp.name || '').toUpperCase()}</h3>
                        <p class="card-description">${exp.web_description || ''}</p>
                        <div class="card-meta">
                            <div><span class="label">STATUS:</span> IN_DEVELOPMENT</div>
                            ${exp.location ? `<div><span class="label">LOCATION:</span> ${exp.location.toUpperCase()}</div>` : ''}
                        </div>
                        <a href="#cta" class="secondary-btn mono card-notify-btn">NOTIFY_ME</a>
                    `;

                    return `
                        <div class="experience-card ${cardClass} reveal-text" style="--d: ${delay}s">
                            <div class="card-inner">
                                <div class="card-front">
                                    <div class="card-status mono ${badgeClass}">
                                        <span class="status-dot ${dotClass}"></span> ${statusLabel}
                                    </div>
                                    ${exp.web_image ? `<img class="card-image" src="${exp.web_image}" alt="${exp.name}" loading="lazy">` : '<div class="card-image" style="background:#111;"></div>'}
                                    <div class="card-content">
                                        ${exp.location ? `<span class="card-coords mono">${exp.location.toUpperCase()}</span>` : ''}
                                        <h3>${(exp.name || '').toUpperCase()}</h3>
                                        <p class="card-tagline">${exp.web_description ? exp.web_description.slice(0, 60) : ''}</p>
                                        <span class="card-flip-hint">TAP_TO_REVEAL &gt;</span>
                                    </div>
                                </div>
                                <div class="card-back">
                                    ${backContent}
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

    // ─── Stripe Checkout ──────────────────────────────────────────────────────
    window.startCheckout = async function(experienceId, lang) {
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
