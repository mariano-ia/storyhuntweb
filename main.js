document.addEventListener('DOMContentLoaded', () => {
    // Typewriter Effect
    const typewriterElement = document.getElementById('typewriter-text');
    const textToType = "An interactive city adventure is about to begin";
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
        document.querySelector('.glitch').classList.add('visible'); // Reveal title
        typeWriter();
    }, 1500);

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

    // Handle Form Submission handled by FormSubmit (commented out for native post)
    /*
    const form = document.querySelector('.recruitment-form');
    const submitBtn = form.querySelector('.submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;

        // Disable form during "processing"
        form.style.opacity = '0.5';
        form.style.pointerEvents = 'none';
        btnText.innerText = 'PROCESSING_REQUEST...';

        // Simulate recruitment phase processing
        setTimeout(() => {
            form.innerHTML = `
                <div class="reveal-text visible" style="margin-top: 2rem; border: 1px solid var(--accent); padding: 2rem;">
                    <p class="mono accent">APPLICATION_RECEIVED // [200]</p>
                    <p class="mono" style="font-size: 0.8rem; margin-top: 1rem;">YOUR_CREDENTIALS_ARE_UNDER_REVIEW. WE_WILL_CONTACT_YOU_IF_YOU_ARE_CHOSEN_FOR_PHASE_01.</p>
                </div>
            `;
        }, 2000);
    });
    */

    // Subtle parallax for the background grain
    window.addEventListener('scroll', () => {
        const offset = window.pageYOffset;
        const main = document.getElementById('main-content');
        // Slight parallax for the noise layer if needed, but keeping it minimal for "serious" vibe
    });
});
