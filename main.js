document.addEventListener('DOMContentLoaded', () => {
    // Typewriter Effect
    const typewriterElement = document.getElementById('typewriter-text');
    const textToType = "An interactive city adventure is about to begin in New York City.";
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

    // System Launch & Spots counter logic
    const launchDate = new Date('2026-04-03T00:00:00-05:00'); // Fixed 30 days from March 3rd
    const maxSpots = 100;

    function updateSystemStatus() {
        const now = new Date();
        const diffTime = Math.max(0, launchDate - now);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        const countdownEl = document.getElementById('countdown-days');
        if (countdownEl) {
            countdownEl.innerText = `T-MINUS ${diffDays} DAYS`;
        }

        // Simulate scarcity dynamically using time logic so it naturally decays globally
        const totalCampaignDays = 30;
        const daysPassed = Math.max(0, totalCampaignDays - diffDays);
        // Decrease roughly 2-3 spots per day, capping at 0.
        let simulatedSpots = maxSpots - Math.floor(daysPassed * 2.8);

        // If the user has already registered on this browser, guarantee it drops by 1 to show instant effect
        if (localStorage.getItem('storyhunt_access_requested') === 'true') {
            simulatedSpots = simulatedSpots - 1;
        }

        simulatedSpots = Math.max(0, simulatedSpots); // Never go below 0

        const spotsEl = document.getElementById('spots-counter');
        if (spotsEl) {
            spotsEl.innerText = `${simulatedSpots} / 100`;
            if (simulatedSpots < 20) {
                spotsEl.classList.remove('electric-blue');
                spotsEl.classList.add('accent'); // Turn red if scarcity is high
            }
        }
    }

    // Initialize counters
    updateSystemStatus();

    // Intersection Observer for sections
    const observerOptions = {
        threshold: 0.2
    };

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Optional: stop observing once revealed
                // revealObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.reveal-text').forEach(el => {
        revealObserver.observe(el);
    });

    // Handle Form Submission handled by FormSubmit via AJAX
    const form = document.querySelector('.recruitment-form');
    if (form) {
        const submitBtn = form.querySelector('.submit-btn');
        const btnText = submitBtn.querySelector('.btn-text');

        form.addEventListener('submit', (e) => {
            e.preventDefault();

            // Disable form during "processing"
            form.style.opacity = '0.5';
            form.style.pointerEvents = 'none';
            btnText.innerText = 'PROCESSING_REQUEST...';

            const formData = new FormData(form);

            fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    'Accept': 'application/json'
                }
            })
                .then(response => {
                    if (response.ok) {
                        // Notify system that user requested access
                        localStorage.setItem('storyhunt_access_requested', 'true');
                        updateSystemStatus(); // Decrement counter immediately

                        form.style.opacity = '1';
                        form.style.pointerEvents = 'auto';
                        form.innerHTML = `
                        <div class="reveal-text visible" style="margin-top: 2rem; border: 1px solid var(--electric-blue); padding: 2rem; opacity: 1; transform: translateY(0);">
                            <p class="mono" style="color: var(--electric-blue); font-size: 1.2rem; margin-bottom: 1rem;">APPLICATION_RECEIVED // [200]</p>
                            <p class="mono" style="font-size: 0.8rem; line-height: 1.6; margin-bottom: 1.5rem;">YOUR_CREDENTIALS_HAVE_BEEN_LOGGED. SPOT SECURED.<br>WE_WILL_CONTACT_YOU_SHORTLY.</p>
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

    // Subtle parallax for the background grain
    window.addEventListener('scroll', () => {
        const offset = window.pageYOffset;
        const main = document.getElementById('main-content');
        // Slight parallax for the noise layer if needed, but keeping it minimal for "serious" vibe
    });
});
