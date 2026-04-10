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


def get_prompt(template, **kwargs):
    """Get the appropriate prompt for a page template type."""
    if template == "A":
        return SYSTEM_PROMPT, prompt_template_a(kwargs["activity_display"], kwargs["neighborhood_display"])
    elif template == "B":
        return SYSTEM_PROMPT, prompt_template_b(kwargs["activity_display"], kwargs["audience_display"])
    elif template == "C":
        return SYSTEM_PROMPT, prompt_template_c(kwargs["activity_display"], kwargs["slug"])
    raise ValueError(f"Unknown template: {template}")
