"""GPT prompt templates for programmatic SEO content generation."""

SYSTEM_PROMPT = """You write SEO content for StoryHunt, an interactive mystery walk company in NYC.

About StoryHunt:
- Players receive clues via chat on their phone (no app download needed)
- 2-3 hours of self-guided walking adventure through real NYC neighborhoods
- No tour guide, no group — just you (or your group) and the city
- Clues lead to hidden spots, secret doors, forgotten history
- An AI narrator tells a story and reacts to your answers
- Price: from $14.99 per person

Your writing style:
- Factual, dense with real NYC history and geography
- Mention real street names, real buildings, real historical events
- No marketing fluff, no filler words, no generic tourism copy
- Write like a knowledgeable local, not a brochure
- Third paragraph always naturally connects the topic to StoryHunt's mystery walk experience

Return ONLY valid JSON, no markdown fences."""


def prompt_template_a(activity_display, neighborhood_display):
    """Template A: {activity} in {neighborhood}"""
    return f"""Write content for a programmatic SEO page about "{activity_display} in {neighborhood_display}, NYC".

Return this exact JSON structure:
{{
  "content_title": "...",
  "subtitle": "One evocative line about this activity in this neighborhood (max 15 words)",
  "paragraphs": [
    "Paragraph 1 (150-200 words): History and character of {neighborhood_display} relevant to this activity. Real street names, real buildings, specific details.",
    "Paragraph 2 (150-200 words): What makes {neighborhood_display} uniquely suited for a {activity_display.lower()}. Specific landmarks, hidden spots, atmosphere.",
    "Paragraph 3 (150-200 words): How StoryHunt's interactive mystery walk transforms a {activity_display.lower()} in {neighborhood_display} into something different. Clues, narrative, phone-guided exploration."
  ],
  "faq": [
    {{"q": "How long does the {activity_display.lower()} in {neighborhood_display} take?", "a": "..."}},
    {{"q": "Do I need to download an app?", "a": "..."}},
    {{"q": "What's the best time to do a {activity_display.lower()} in {neighborhood_display}?", "a": "..."}},
    {{"q": "How much does it cost?", "a": "..."}}
  ]
}}"""


def prompt_template_b(activity_display, audience_display):
    """Template B: {activity} for {audience}"""
    return f"""Write content for a programmatic SEO page about "{activity_display} for {audience_display} in NYC".

Return this exact JSON structure:
{{
  "content_title": "...",
  "subtitle": "One evocative line about this activity for {audience_display.lower()} (max 15 words)",
  "paragraphs": [
    "Paragraph 1 (150-200 words): Why a {activity_display.lower()} is perfect for {audience_display.lower()} visiting or living in NYC. Address their specific needs and interests.",
    "Paragraph 2 (150-200 words): Best NYC neighborhoods for {audience_display.lower()} to explore on a {activity_display.lower()}. Mention 3-4 specific neighborhoods with reasons.",
    "Paragraph 3 (150-200 words): How StoryHunt works for {audience_display.lower()} — the phone-guided experience, self-paced, flexible timing, narrative story. Why it's better than traditional options."
  ],
  "faq": [
    {{"q": "Is a {activity_display.lower()} good for {audience_display.lower()}?", "a": "..."}},
    {{"q": "How many people can participate?", "a": "..."}},
    {{"q": "What neighborhoods are available?", "a": "..."}},
    {{"q": "How much does it cost?", "a": "..."}}
  ]
}}"""


def prompt_template_c(activity_display, slug):
    """Template C: broad {activity}-nyc pages"""
    return f"""Write content for a broad SEO page about "{activity_display} in NYC" targeting the keyword "{slug.replace('-', ' ')}".

Return this exact JSON structure:
{{
  "content_title": "...",
  "subtitle": "One evocative line about this activity in New York City (max 15 words)",
  "paragraphs": [
    "Paragraph 1 (150-200 words): Overview of {activity_display.lower()} options in NYC. What makes New York the perfect city for this. Real neighborhoods and landmarks.",
    "Paragraph 2 (200-250 words): The best NYC neighborhoods for a {activity_display.lower()}, covering 4-5 areas with specific details about what makes each one special.",
    "Paragraph 3 (150-200 words): How StoryHunt reinvents the {activity_display.lower()} with interactive storytelling, phone-guided clues, and no tour guide needed. Position against traditional alternatives."
  ],
  "faq": [
    {{"q": "What is the best {activity_display.lower()} in NYC?", "a": "..."}},
    {{"q": "How long does it take?", "a": "..."}},
    {{"q": "Do I need to book in advance?", "a": "..."}},
    {{"q": "Is it available at night?", "a": "..."}},
    {{"q": "How much does a {activity_display.lower()} cost in NYC?", "a": "..."}}
  ]
}}"""


def prompt_template_d(activity_display, temporal_display):
    """Template D: {activity}-nyc-{temporal} (seasonal/moment)"""
    return f"""Write content for a programmatic SEO page about "{activity_display} in NYC {temporal_display}".
This targets people searching right now for something to do {temporal_display.lower()} in New York City.

Return this exact JSON structure:
{{
  "content_title": "...",
  "subtitle": "One evocative line (max 15 words)",
  "paragraphs": [
    "Paragraph 1 (150-200 words): What makes NYC special for a {activity_display.lower()} {temporal_display.lower()}. Atmosphere, weather, seasonal events, time-specific details.",
    "Paragraph 2 (150-200 words): Best neighborhoods and specific spots for this activity {temporal_display.lower()}. Real locations, practical tips.",
    "Paragraph 3 (150-200 words): How StoryHunt works {temporal_display.lower()} — phone-guided clues, self-paced, 2-3 hours, works in any weather/time. Connect to the seasonal angle."
  ],
  "faq": [
    {{"q": "Can I do a {activity_display.lower()} in NYC {temporal_display.lower()}?", "a": "..."}},
    {{"q": "How long does it take?", "a": "..."}},
    {{"q": "What should I wear/bring?", "a": "..."}},
    {{"q": "How much does it cost?", "a": "..."}}
  ]
}}"""


def prompt_template_e(theme_display, activity_display):
    """Template E: {theme}-{activity}-nyc"""
    return f"""Write content for a programmatic SEO page about "{theme_display} {activity_display} in NYC".
This targets people interested in the {theme_display.lower()} side of New York City.

Return this exact JSON structure:
{{
  "content_title": "...",
  "subtitle": "One evocative line (max 15 words)",
  "paragraphs": [
    "Paragraph 1 (150-200 words): NYC's {theme_display.lower()} history and why it matters. Real events, real locations, specific details that make NYC the capital of {theme_display.lower()} stories.",
    "Paragraph 2 (200-250 words): The best spots and neighborhoods for a {theme_display.lower()} {activity_display.lower()} in NYC. Cover 3-4 specific locations with real street addresses or landmarks.",
    "Paragraph 3 (150-200 words): How StoryHunt's interactive mystery walk brings the {theme_display.lower()} theme to life — clues based on real {theme_display.lower()} history, phone-guided, no tour guide, 2-3 hours."
  ],
  "faq": [
    {{"q": "What is a {theme_display.lower()} {activity_display.lower()}?", "a": "..."}},
    {{"q": "Is it scary/intense?", "a": "..."}},
    {{"q": "What neighborhoods does it cover?", "a": "..."}},
    {{"q": "How much does it cost?", "a": "..."}}
  ]
}}"""


def prompt_template_f(display_title):
    """Template F: comparison/vs pages"""
    return f"""Write content for an SEO comparison page: "{display_title} in NYC".
This is an honest comparison that helps people decide between two activity types, while positioning StoryHunt as the superior option.

Return this exact JSON structure:
{{
  "content_title": "...",
  "subtitle": "One evocative comparison line (max 15 words)",
  "paragraphs": [
    "Paragraph 1 (200-250 words): Honest comparison of both options. What each offers, typical price range, duration, group size, pros and cons. Be fair to both sides.",
    "Paragraph 2 (200-250 words): Key differences — flexibility, interactivity, cost, uniqueness, repeatability. Use a comparison framework (not a table, just flowing prose).",
    "Paragraph 3 (150-200 words): Why StoryHunt combines the best of both — interactive like an escape room, exploratory like a walking tour, narrative-driven, phone-guided, no booking hassle, self-paced."
  ],
  "faq": [
    {{"q": "Which is better for couples?", "a": "..."}},
    {{"q": "Which is cheaper?", "a": "..."}},
    {{"q": "Which takes longer?", "a": "..."}},
    {{"q": "Can I do both in one day?", "a": "..."}}
  ]
}}"""


def prompt_template_g(page_title):
    """Template G: best-of / insider guide pages"""
    return f"""Write content for an insider guide page: "{page_title}".
This is a curated guide that positions StoryHunt as the local expert. Dense with real locations and insider knowledge.

Return this exact JSON structure:
{{
  "content_title": "...",
  "subtitle": "One evocative insider-knowledge line (max 15 words)",
  "paragraphs": [
    "Paragraph 1 (200-250 words): Overview — why this topic matters, what most people miss. Set up the insider angle. Mention 2-3 specific spots with real addresses or cross streets.",
    "Paragraph 2 (250-300 words): The actual list/guide — 5-7 specific recommendations with real details. Street names, what to look for, best times to visit. This should be genuinely useful content.",
    "Paragraph 3 (150-200 words): How StoryHunt lets you discover these spots through an interactive mystery walk. Clues lead to the real locations, narrative connects them, phone-guided, 2-3 hours."
  ],
  "faq": [
    {{"q": "How many {page_title.split(' in ')[0].lower().replace('best ', '')} are there?", "a": "..."}},
    {{"q": "Do I need to book in advance?", "a": "..."}},
    {{"q": "Is this a guided tour?", "a": "..."}},
    {{"q": "How much does StoryHunt cost?", "a": "..."}}
  ]
}}"""


def get_prompt(template, **kwargs):
    """Get the appropriate prompt for a page template type."""
    if template == "A":
        return SYSTEM_PROMPT, prompt_template_a(kwargs["activity_display"], kwargs["neighborhood_display"])
    elif template == "B":
        return SYSTEM_PROMPT, prompt_template_b(kwargs["activity_display"], kwargs["audience_display"])
    elif template == "C":
        return SYSTEM_PROMPT, prompt_template_c(kwargs["activity_display"], kwargs["slug"])
    elif template == "D":
        return SYSTEM_PROMPT, prompt_template_d(kwargs["activity_display"], kwargs.get("temporal_display", ""))
    elif template == "E":
        return SYSTEM_PROMPT, prompt_template_e(kwargs.get("theme_display", ""), kwargs["activity_display"])
    elif template == "F":
        return SYSTEM_PROMPT, prompt_template_f(kwargs.get("display_title", kwargs.get("slug", "").replace("-", " ").title()))
    elif template == "G":
        return SYSTEM_PROMPT, prompt_template_g(kwargs.get("page_title", kwargs.get("slug", "").replace("-", " ").title()))
    raise ValueError(f"Unknown template: {template}")
