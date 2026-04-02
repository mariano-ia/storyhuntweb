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

    // Card Flip Interaction
    document.querySelectorAll('.experience-card').forEach(card => {
        card.addEventListener('click', (e) => {
            if (e.target.closest('a') || e.target.closest('button')) return;
            card.classList.toggle('flipped');
        });
    });

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
