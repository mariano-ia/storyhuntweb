#!/usr/bin/env python3
"""
StoryHunt SEO Content Upgrade Script
Adds unique, SEO-rich content to all 42 NYC explore pages.
"""

import os
import re
import sys

EXPLORE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "explore")

# ─── Page data: (filename, subtitle, title, paragraphs[3], related_links[(slug,label)]) ───

PAGES = {
    # ═══════════════════════════════════════
    # NYC NEIGHBORHOODS (17)
    # ═══════════════════════════════════════

    "soho.html": {
        "subtitle": "Where cobblestone streets guard 150 years of secrets beneath cast-iron facades.",
        "title": "The Hidden Layers of SoHo",
        "paragraphs": [
            "SoHo's twenty-six blocks contain the largest concentration of cast-iron architecture anywhere in the world. Walk down Greene Street and you'll pass facades that were designed to mimic Renaissance palaces — but built cheaply from iron molds so 19th-century textile manufacturers could show off without breaking the bank. The building at 112 Prince Street still wears its original cast-iron front, a quiet monument to an era when this neighborhood was the industrial engine of lower Manhattan.",
            "Before the galleries and the boutiques, SoHo was known as \"Hell's Hundred Acres\" — a district of sweatshops and warehouse fires so dangerous that the city nearly demolished the entire neighborhood in the 1960s to build an expressway. Artists moved into the abandoned factory lofts illegally, turning industrial floors into studios. That act of creative defiance saved SoHo and transformed it into the art-world epicenter it became in the 1970s and 80s. Today, traces of that rebellion still hide in plain sight: freight elevators that once hauled bolts of fabric, loading docks converted into gallery entrances, and cobblestone streets that predate the Civil War.",
            "A StoryHunt through SoHo sends you beneath the surface of the shopping district. Your phone guides you past hidden alleyways, asks you to decode symbols carved into iron columns, and leads you to doorways most people walk past without a second glance. Every clue is rooted in real history — the fires, the artists, the narrow escapes. You don't need a guide or a group. Just your curiosity and a willingness to look up, look down, and look twice.",
        ],
        "links": [("hidden-speakeasies-soho.html", "Hidden Speakeasies of SoHo"), ("hidden-places-nyc.html", "Hidden Places in NYC"), ("tribeca.html", "Decode TriBeCa")],
    },

    "chelsea.html": {
        "subtitle": "Art, industry, and reinvention collide in Manhattan's gallery corridor.",
        "title": "Chelsea: From Factory Floors to Gallery Walls",
        "paragraphs": [
            "Chelsea is home to more than 200 art galleries packed into a handful of blocks between Tenth and Eleventh Avenues — the densest concentration of contemporary art in the Western Hemisphere. But long before the white-cube galleries arrived, this neighborhood was defined by heavy industry. The building that now houses Chelsea Market was once the Nabisco factory, where the Oreo cookie was invented in 1912. Workers poured in and out of its brick corridors for decades, fueling a neighborhood that smelled of sugar and diesel.",
            "Walk east along 23rd Street and you'll reach London Terrace, a full-block apartment complex built in 1930 that was so ambitious its developers went bankrupt during construction. The doormen originally wore uniforms modeled after London bobbies. A few blocks south, the loading docks of the Meatpacking District fade into the elevated greenery of the High Line, a rail line that once carried beef carcasses and now carries tourists past public art installations. Chelsea's story is one of constant reinvention — docks to factories to galleries to parks — and each layer left physical evidence behind.",
            "A StoryHunt mystery walk through Chelsea turns gallery-hopping into an investigation. Your phone feeds you clues drawn from the neighborhood's industrial past, sends you searching for hidden details on loading-dock doors, and challenges you to decode the connection between a cookie factory and a contemporary art empire. It's two to three hours of immersive urban exploration — no guide, no group, just you decoding the city block by block.",
        ],
        "links": [("high-line.html", "The High Line"), ("hidden-places-nyc.html", "Hidden Places in NYC"), ("architectural-marvels-nyc.html", "Architectural Marvels")],
    },

    "midtown.html": {
        "subtitle": "Beneath the skyscrapers, a hidden city of tunnels, lobbies, and Art Deco secrets.",
        "title": "Midtown's Secret Architecture",
        "paragraphs": [
            "Midtown Manhattan is the most visited neighborhood in the most visited city in America — and almost nobody sees the real thing. Millions pass through Grand Central Terminal without noticing the astronomical ceiling's dark patch, left unrestored as proof of how much cigarette smoke once filled the hall. The Chrysler Building's lobby, one of the finest Art Deco interiors on the planet, is open to the public but perpetually empty because tourists assume it's off-limits. Beneath the Waldorf Astoria, a private rail platform once carried President Franklin Roosevelt's armored train car directly into the hotel basement.",
            "The Rockefeller Center underground concourse stretches for blocks beneath the plaza, a subterranean city of shops and passages built during the Depression to keep pedestrians moving during winter. Above ground, secret rooftop gardens sit atop skyscrapers most New Yorkers have never entered. The old Grand Hyatt Hotel on 42nd Street — now demolished — concealed an entire secret floor that was never listed on any directory. Midtown rewards those who look beyond the obvious: up at gargoyles, down at subway grates, and through lobbies most people rush past.",
            "StoryHunt's Midtown experience turns the concrete canyon into a puzzle box. Your phone sends you into lobbies, through passages, and past architectural details that hide in plain sight. Each clue connects to real history — Prohibition-era tunnels, Cold War bunkers, and the engineers who built secret infrastructure beneath the world's most famous skyline. No tour bus. No megaphone. Just you, your phone, and a city that's been hiding things for a century.",
        ],
        "links": [("grand-central.html", "Grand Central Secrets"), ("times-square.html", "Decode Times Square"), ("underground-tunnels-nyc.html", "Underground Tunnels of NYC")],
    },

    "central-park.html": {
        "subtitle": "843 acres of engineered wilderness hiding obelisks, secret gardens, and forgotten monuments.",
        "title": "Central Park's Buried Secrets",
        "paragraphs": [
            "Central Park looks natural. It isn't. Every hill, pond, and winding path was designed by Frederick Law Olmsted and Calvert Vaux in the 1850s, sculpted from swampland and rocky outcrops that were home to Seneca Village, a thriving Black community that was demolished through eminent domain to build the park. Beneath the lawns lie buried streams, old reservoir walls, and infrastructure so complex it required its own police force. The park is an illusion of wilderness engineered at industrial scale.",
            "Cleopatra's Needle, the 3,500-year-old Egyptian obelisk behind the Metropolitan Museum, was floated across the Atlantic and dragged through Manhattan on specially built railroad tracks in 1881. The Hallett Nature Sanctuary at the park's southeast corner was closed to the public for decades and remains one of the quietest spots on the island. Shakespeare Garden, planted exclusively with species mentioned in the Bard's plays, sits on a slope near Belvedere Castle — a miniature fortress built as a weather station that now serves as one of the park's most photographed landmarks.",
            "A StoryHunt through Central Park leads you off the main paths and into the park's hidden corners. Your phone sends you searching for forgotten sculptures, coded inscriptions on bridges, and quiet clearings that most visitors never find. Each clue is grounded in the park's layered history — from Seneca Village to the Ramble's role as a birdwatching hotspot. Two to three hours of exploration that will change the way you see the most famous park in the world.",
        ],
        "links": [("secret-gardens-central-park.html", "Secret Gardens of Central Park"), ("hidden-places-nyc.html", "Hidden Places in NYC"), ("upper-east-side.html", "Decode the Upper East Side")],
    },

    "west-village.html": {
        "subtitle": "Jazz, rebellion, and the narrowest house in New York — all on streets that refuse to follow the grid.",
        "title": "The West Village: Where the Grid Breaks Down",
        "paragraphs": [
            "The West Village is the only neighborhood in Manhattan where the streets don't follow the grid. That's because these lanes predate the 1811 Commissioners' Plan — they follow old Dutch farm boundaries and Native American trails. This tangle of streets created a neighborhood that was hard to police and hard to find, which made it the perfect home for bohemians, jazz musicians, and anyone who didn't fit the mainstream. Bob Dylan lived at 161 West 4th Street when he wrote \"The Freewheelin'\" album. Chumley's, at 86 Bedford Street, operated as a speakeasy during Prohibition and famously had no sign — you had to know where the door was.",
            "At 75½ Bedford Street stands the narrowest house in New York City: just 9.5 feet wide, built in 1873 in a former carriage alley. Edna St. Vincent Millay and John Barrymore both lived there. Around the corner, the Cherry Lane Theatre — the oldest continuously running Off-Broadway theater — has operated since 1924 in a building that started as a brewery, became a tobacco warehouse, then a box factory before becoming a stage. The West Village compresses more cultural history per square foot than almost anywhere in America.",
            "StoryHunt's West Village experience sends you down these crooked streets with clues that connect jazz clubs to speakeasies, poetry to architecture, and rebellion to real estate. Your phone guides you to hidden courtyards, asks you to find symbols on doorframes, and challenges you to decode the stories embedded in the neighborhood's winding layout. No guide needed — the streets themselves are the puzzle.",
        ],
        "links": [("literary-secrets-west-village.html", "Literary Secrets of the West Village"), ("speakeasies-nyc.html", "Speakeasies of NYC"), ("greenwich-village.html", "Decode Greenwich Village")],
    },

    "tribeca.html": {
        "subtitle": "Converted warehouses, film legends, and a firehouse you've definitely seen before.",
        "title": "TriBeCa: The Triangle Below Canal",
        "paragraphs": [
            "TriBeCa — the Triangle Below Canal Street — was once Manhattan's primary distribution hub, packed with warehouses that stored everything from eggs to textiles. The neighborhood's wide streets and massive buildings were designed for horse-drawn carts, not pedestrians. By the 1970s, most of the warehouses had been abandoned, and artists began converting them into lofts — following the same pattern that had transformed SoHo a decade earlier. The 19th-century mercantile buildings along Washington Street and Harrison Street remain some of the finest examples of commercial Federal-style architecture in the city.",
            "Hook & Ladder Company 8 at 14 North Moore Street became world-famous as the Ghostbusters firehouse in the 1984 film — and it's still an active firehouse today, complete with a replica Ghostbusters logo painted by fans that the FDNY has quietly tolerated for years. A few blocks away, Robert De Niro co-founded the Tribeca Film Festival in 2002 specifically to revitalize the neighborhood after September 11th — the festival now draws hundreds of thousands of visitors annually and has helped turn TriBeCa into the most expensive residential neighborhood in Manhattan.",
            "A StoryHunt adventure through TriBeCa takes you inside the neighborhood's transformation story. Your phone sends clues tied to real warehouse histories, hidden architectural details, and film connections that go far beyond Ghostbusters. You'll decode inscriptions on loading docks, investigate hidden courtyards, and piece together the puzzle of how a freight district became the most coveted address in New York. Two to three hours, no guide, just the city and your phone.",
        ],
        "links": [("soho.html", "Decode SoHo"), ("movie-locations-nyc.html", "Movie Locations in NYC"), ("hidden-places-nyc.html", "Hidden Places in NYC")],
    },

    "flatiron.html": {
        "subtitle": "Wind gusts, Gilded Age scandals, and the birthplace of American baseball.",
        "title": "Flatiron: The Gilded Age Crossroads",
        "paragraphs": [
            "The Flatiron Building at the intersection of Broadway and Fifth Avenue was not the first skyscraper in New York, but when it opened in 1902 it was the most controversial. Critics called it \"Burnham's Folly\" and predicted it would topple in the wind. They were half right about the wind — the building's triangular shape creates powerful downdrafts at street level that once blew women's skirts up so reliably that the term \"23 Skidoo\" was coined when police had to shoo away men who gathered to watch. The building survived, of course, and the phrase entered the American lexicon.",
            "Madison Square Park, the green triangle at the Flatiron's base, was once the site of the original Madison Square Garden — not the arena on 33rd Street but an open-air venue where the first major boxing matches were held. Before that, the same ground hosted some of the earliest organized baseball games in America. The park's Josephine Shaw Lowell Memorial Fountain was New York's first public monument dedicated to a woman. During the Gilded Age, the blocks around the park were home to the city's most exclusive hotels and restaurants — Delmonico's operated nearby, and Stanford White was murdered in the rooftop theater of the second Madison Square Garden in 1906.",
            "StoryHunt's Flatiron experience turns this crossroads into a crime scene. Your phone sends you searching for Gilded Age clues hidden in the park's monuments, the building's facade, and the surrounding streets. You'll decode the wind patterns, investigate a century-old murder, and uncover why this intersection was once the center of New York's social universe. No tour group — just you and a mystery that spans from baseball diamonds to ballrooms.",
        ],
        "links": [("midtown.html", "Decode Midtown"), ("architectural-marvels-nyc.html", "Architectural Marvels of NYC"), ("mysteries-in-nyc.html", "Mysteries in NYC")],
    },

    "dumbo.html": {
        "subtitle": "Brooklyn's waterfront turned open-air gallery, framed by two iconic bridges.",
        "title": "DUMBO: Down Under the Manhattan Bridge Overpass",
        "paragraphs": [
            "DUMBO — Down Under the Manhattan Bridge Overpass — is a neighborhood defined by its frame. Stand on Washington Street between the old brick warehouses and the Manhattan Bridge arches directly overhead, and you'll see a view of the Empire State Building that has become one of the most photographed compositions in the city. But before the photographers came the merchants. The Empire Stores, a row of Civil War-era coffee and tobacco warehouses on the waterfront, sat empty for decades before being converted into shops, offices, and the Brooklyn Historical Society's satellite gallery. Their thick walls still carry the scent of a century of stored goods.",
            "Jane's Carousel, a 1922 Philadelphia Toboggan Company carousel, was rescued from an amusement park in Youngstown, Ohio, and installed in a Jean Nouvel-designed glass pavilion on the DUMBO waterfront in 2011. It's one of the finest surviving examples of a wooden carousel in the United States. Nearby, the cobblestone streets between the Manhattan and Brooklyn Bridges still follow their original 19th-century grid, and the former industrial buildings now house some of Brooklyn's most influential art studios and tech companies. The transformation from waterfront warehouse district to cultural hub took less than twenty years.",
            "A StoryHunt through DUMBO uses the neighborhood's layered history as a puzzle. Your phone guides you past hidden art installations, asks you to decode markings on warehouse walls, and sends you to viewpoints most visitors walk right past. Each clue connects to the real story of this waterfront — the merchants, the artists, and the bridge builders who shaped it. Two to three hours of immersive exploration along the East River.",
        ],
        "links": [("hidden-art-dumbo.html", "Hidden Art in DUMBO"), ("williamsburg.html", "Decode Williamsburg"), ("brooklyn-bridge.html" if False else "hidden-places-nyc.html", "Hidden Places in NYC")],
    },

    "williamsburg.html": {
        "subtitle": "From sugar refineries to street art — Brooklyn's most radical reinvention.",
        "title": "Williamsburg: A Neighborhood in Permanent Transformation",
        "paragraphs": [
            "Williamsburg's Bedford Avenue is now one of the most recognizable streets in Brooklyn, lined with vintage shops, coffee roasters, and record stores. But a century ago, this same avenue ran through a neighborhood of German beer gardens, Eastern European synagogues, and the massive Domino Sugar Factory, whose refinery processed more than half the sugar consumed in the United States. The factory's smokestack dominated the waterfront skyline for over a hundred years before the complex was finally redeveloped into apartments and a public park in the 2010s. The ghost of industrial sweetness still lingers in the neighborhood's DNA.",
            "McCarren Park, the green heart of Williamsburg, contains a public pool that has its own dramatic history. The massive WPA-era pool opened in 1936, was closed in 1984 due to budget cuts, and spent two decades as an empty concrete bowl that hosted underground concerts and events before being restored and reopened in 2012. The Williamsburg music scene — which produced bands that defined indie rock in the 2000s — grew directly out of the cheap warehouse spaces that surrounded the park. Today those warehouses are luxury condos, but the murals and street art that cover the remaining industrial walls serve as a visual record of the neighborhood's creative peak.",
            "StoryHunt's Williamsburg experience sends you hunting for the layers beneath the brunch spots. Your phone delivers clues connected to brewery history, sugar refinery secrets, and the street art that tells the neighborhood's real story. You'll decode murals, investigate abandoned industrial details, and piece together the puzzle of how a working-class immigrant neighborhood became Brooklyn's cultural engine. No guide, no group — just your phone and the streets.",
        ],
        "links": [("weird-history-williamsburg.html", "Weird History of Williamsburg"), ("bushwick.html", "Decode Bushwick"), ("street-art-nyc.html" if False else "hidden-places-nyc.html", "Hidden Places in NYC")],
    },

    "harlem.html": {
        "subtitle": "The birthplace of the Renaissance that changed American culture forever.",
        "title": "Harlem: Where American Culture Was Reborn",
        "paragraphs": [
            "The Harlem Renaissance didn't happen by accident. In the early 1900s, a Black real estate entrepreneur named Philip Payton Jr. began leasing apartments in Harlem's newly built but under-occupied brownstones to African American families who were being pushed out of other Manhattan neighborhoods. Within two decades, Harlem had become the cultural capital of Black America. The Apollo Theater on 125th Street, which opened to Black audiences in 1934, launched the careers of Ella Fitzgerald, James Brown, and countless others through its legendary Amateur Night. The Cotton Club at 142nd Street and Lenox Avenue presented Duke Ellington and Cab Calloway to whites-only audiences during Prohibition — a painful contradiction that defined the era.",
            "Strivers' Row, the stretch of 138th and 139th Streets between Adam Clayton Powell Jr. Boulevard and Frederick Douglass Boulevard, contains some of the finest rowhouses in Manhattan — designed by Stanford White and originally built for wealthy white families in 1891. When Black professionals moved in during the 1920s, the blocks earned their nickname as the address of Harlem's most ambitious residents. Langston Hughes lived at 20 East 127th Street, where he wrote much of his most celebrated poetry. The Abyssinian Baptist Church, founded in 1808 and one of the oldest Black congregations in the nation, has occupied its current Gothic and Tudor building on 138th Street since 1923.",
            "A StoryHunt through Harlem connects you to the neighborhood's musical and literary history through clues embedded in its streets. Your phone guides you past jazz landmarks, literary addresses, and architectural details that tell the story of a cultural revolution. You'll decode connections between the Cotton Club and the Apollo, investigate hidden courtyards on Strivers' Row, and piece together the puzzle of how one neighborhood changed American art, music, and literature. An immersive walk — no bus, no megaphone, just you and the story.",
        ],
        "links": [("ghost-tours-nyc.html", "Ghost Tours NYC"), ("literary-tours-nyc.html", "Literary Tours NYC"), ("hidden-places-nyc.html", "Hidden Places in NYC")],
    },

    "bushwick.html": {
        "subtitle": "The borough's open-air museum — where every wall tells a story.",
        "title": "Bushwick: Brooklyn's Street Art Capital",
        "paragraphs": [
            "Bushwick was once the beer capital of the Northeastern United States. In the late 1800s, eleven breweries operated within a fourteen-block radius, producing lagers for the neighborhood's large German immigrant population. The brewery buildings — massive brick structures with deep cellars designed to keep beer cool before refrigeration — still stand throughout the neighborhood, repurposed as artist studios, event spaces, and the occasional climbing gym. When the last brewery closed in 1976, the neighborhood entered decades of disinvestment. The 1977 blackout saw widespread looting on Bushwick's commercial corridors, and the area didn't begin its recovery until well into the 2000s.",
            "The Bushwick Collective, founded by local Joe Ficalora in 2011, transformed the neighborhood's warehouse walls into one of the world's most significant outdoor street art galleries. Artists from dozens of countries have painted large-scale murals on the buildings along Troutman Street, Jefferson Street, and surrounding blocks. The works rotate — new murals replace old ones, making each visit different from the last. Beyond the Collective, the underground music scene that grew out of Bushwick's cheap warehouse spaces produced DIY venues like Silent Barn, Shea Stadium, and Market Hotel, which became essential stops on indie touring circuits.",
            "StoryHunt's Bushwick experience turns the street art into a scavenger hunt. Your phone sends you searching for specific murals, hidden details within the artwork, and clues that connect the neighborhood's brewery past to its artistic present. You'll decode visual symbols, investigate warehouse histories, and piece together the puzzle of how a beer district became an open-air museum. Two to three hours of walking, looking, and discovering — no guide needed.",
        ],
        "links": [("williamsburg.html", "Decode Williamsburg"), ("hidden-art-dumbo.html", "Hidden Art in DUMBO"), ("hidden-places-nyc.html", "Hidden Places in NYC")],
    },

    "times-square.html": {
        "subtitle": "Beneath the neon, an underground city that most visitors never suspect.",
        "title": "Times Square: The Hidden City Behind the Lights",
        "paragraphs": [
            "Times Square is the most visited place in America — approximately 50 million people pass through it every year — and almost none of them know what's beneath their feet. The old New York Times building, which gave the square its name in 1904, once operated a system of pneumatic tubes that shot rolled-up newspaper copy through pressurized pipes to the printing presses. Beneath the square itself, an abandoned subway station — the old IRT City Hall loop's connection — sits unused and sealed off from the public. Duffy Square, the triangle at the north end of Times Square named for World War I hero Father Francis Duffy, was once a horse market.",
            "Before the neon and the LED screens, Times Square was the center of New York's legitimate theater industry — and its illegitimate one. The blocks between 40th and 53rd Streets contain more than forty historic theaters, many of which have hidden architectural details above their marquees that most theatergoers never notice: Art Deco reliefs, terra cotta sculptures, and rooftop ornaments designed for a time when buildings were meant to be admired from every angle. The neighborhood's transformation from peep-show district in the 1970s to family entertainment zone in the 1990s was one of the most dramatic urban reinventions in American history.",
            "A StoryHunt through Times Square strips away the neon and reveals the hidden infrastructure. Your phone sends you past theatrical facades, into lobbies, and toward hidden details that tell the story of the neighborhood before the billboards. Each clue connects to real history — pneumatic tubes, horse markets, and underground stations. You'll decode architectural details most people miss even when they're staring right at them. No guided group — just you, solving a puzzle in the brightest spot in the city.",
        ],
        "links": [("ghosts-of-broadway.html", "Ghosts of Broadway"), ("underground-tunnels-nyc.html", "Underground Tunnels of NYC"), ("midtown.html", "Decode Midtown")],
    },

    "greenwich-village.html": {
        "subtitle": "The intersection of rebellion, poetry, and crooked streets that changed the world.",
        "title": "Greenwich Village: Birthplace of the American Counterculture",
        "paragraphs": [
            "Greenwich Village's irregular street grid exists because the neighborhood predates Manhattan's 1811 grid plan. The lanes follow old property lines, streams, and cow paths from the Dutch colonial era — which is why you can stand at the intersection of West 4th Street and West 10th Street, something that shouldn't be geometrically possible. This disorienting layout attracted outsiders and nonconformists for centuries. Washington Square Park, anchored by Stanford White's triumphal arch (modeled after the Arc de Triomphe), has served as the neighborhood's public living room since the 1820s — a place where chess hustlers, folk musicians, and NYU students have always mixed freely.",
            "The Stonewall Inn on Christopher Street was an unremarkable Mafia-run bar until June 28, 1969, when a police raid triggered the uprising that launched the modern LGBTQ+ rights movement. Cafe Wha?, in the basement at 115 MacDougal Street, hosted early performances by Bob Dylan, Jimi Hendrix, and Bruce Springsteen. The triangle formed by Waverly Place where it crosses Waverly Place — yes, the street intersects itself — is one of the most unusual geographic quirks in Manhattan. Each block in the Village contains layers of cultural history that no other American neighborhood can match.",
            "StoryHunt's Greenwich Village experience turns these crooked streets into an interactive mystery. Your phone sends you through hidden alleyways, past literary landmarks, and to doorways where history was made. You'll decode clues connected to the Beat Generation, the folk music revival, and the civil rights movements that were born here. Each step takes you deeper into the Village's layered story — no guide, no schedule, just you navigating the streets that refuse to follow the rules.",
        ],
        "links": [("haunted-places-greenwich-village.html", "Haunted Places in Greenwich Village"), ("west-village.html", "Decode the West Village"), ("literary-tours-nyc.html", "Literary Tours NYC")],
    },

    "bryant-park.html": {
        "subtitle": "Above ground, a perfect lawn. Below it, seven stories of hidden library stacks.",
        "title": "Bryant Park: The Secret Beneath the Grass",
        "paragraphs": [
            "Bryant Park sits on top of one of the most unusual structures in Manhattan: the New York Public Library's underground book stacks, which extend seven levels beneath the lawn. When the library at the park's eastern edge was built in 1911, the stacks were added below grade to house the library's growing collection. The park above was relandscaped in the 1990s, and today millions of visitors sit on the lawn without realizing they're perched above millions of books. The Josephine Shaw Lowell Memorial Fountain at the park's western entrance, installed in 1912, was the first public monument in New York City dedicated to a woman — a social reformer who championed workers' rights.",
            "Before it was Bryant Park, this ground was a potter's field — a public burial ground for the city's unclaimed dead. When the Croton Reservoir was built on the site in 1842 (a massive Egyptian-style structure that occupied the land where the library now stands), the bodies were moved. Or at least, most of them were. Construction projects in the area have occasionally turned up remains that were missed. The park itself has cycled through identities: from reservoir to Civil War training ground to a neglected drug haven in the 1970s to the immaculate corporate lawn it is today. During Fashion Week, the same grass hosts runway shows and celebrity sightings.",
            "A StoryHunt through Bryant Park and its surroundings turns a Midtown lunch spot into an investigation. Your phone sends you searching for hidden details on the library's facade, coded inscriptions on park monuments, and clues that connect the underground stacks to the surface world. You'll decode the park's layered history — from potter's field to fashion runway — and discover why this small rectangle of green holds more secrets than most neighborhoods. Ninety minutes of immersive exploration in the heart of Manhattan.",
        ],
        "links": [("midtown.html", "Decode Midtown"), ("hidden-places-nyc.html", "Hidden Places in NYC"), ("underground-tunnels-nyc.html", "Underground Tunnels of NYC")],
    },

    "high-line.html": {
        "subtitle": "An abandoned freight rail line reborn as Manhattan's most unexpected park.",
        "title": "The High Line: Walking on Ghost Tracks",
        "paragraphs": [
            "The High Line is a 1.45-mile elevated park built on a former New York Central Railroad freight line on Manhattan's West Side. The rail line was constructed in the 1930s to lift dangerous freight trains off street level — before the elevated tracks, so many pedestrians were killed by ground-level trains on Tenth Avenue that the street was nicknamed \"Death Avenue\" and the railroad hired men on horseback to ride ahead of the trains waving red flags. The original rail tracks are still embedded in the High Line's walkway, curving through plantings designed by Dutch garden designer Piet Oudolf to mimic the wild vegetation that colonized the tracks during the decades the line sat abandoned.",
            "The Spur, a wide overlook at the High Line's midpoint near 30th Street, offers one of the best viewpoints in Manhattan — a panoramic sweep from the Hudson River to the Empire State Building. Below the Spur, at street level, sits the former Nabisco factory (now Chelsea Market), where the High Line once carried raw materials directly into the building's upper floors. The rail line's last train ran in 1980, carrying three carloads of frozen turkeys. For twenty years the structure was slated for demolition, until a group of neighborhood residents formed Friends of the High Line and convinced the city to transform it into a park instead.",
            "StoryHunt's High Line experience adds a layer of mystery to your walk above the city. Your phone delivers clues tied to the railroad's industrial history, challenges you to find the original rail hardware hidden among the plantings, and sends you to viewpoints where the old and new city collide. Each step is part of a narrative that connects Death Avenue to frozen turkeys to one of the most celebrated urban parks in the world. Walk at your own pace — the tracks will guide you.",
        ],
        "links": [("chelsea.html", "Decode Chelsea"), ("architectural-marvels-nyc.html", "Architectural Marvels of NYC"), ("hidden-places-nyc.html", "Hidden Places in NYC")],
    },

    "upper-east-side.html": {
        "subtitle": "Behind the limestone facades: mansions with secrets and a museum mile with hidden rooms.",
        "title": "The Upper East Side: Old Money, Hidden Treasures",
        "paragraphs": [
            "The Upper East Side's Museum Mile — the stretch of Fifth Avenue from 82nd to 105th Street — contains the highest concentration of cultural institutions in the world: the Metropolitan Museum of Art, the Guggenheim, the Neue Galerie, the Jewish Museum, and more. But the neighborhood's cultural wealth extends far beyond its museums. The Frick Collection, housed in the 1914 mansion of steel magnate Henry Clay Frick, is one of the finest small art museums in the world — and the building itself, with its enclosed garden court and Gilded Age interiors, is as much a treasure as the Vermeers and Rembrandts on its walls.",
            "Henderson Place, a cluster of 24 Queen Anne-style row houses built in 1882 near East 86th Street, is one of the most hidden residential enclaves in Manhattan. The tiny cul-de-sac was originally designed as affordable housing for \"persons of moderate means\" — an ironic label given that the surviving houses now sell for millions. The Met's rooftop garden, accessible via elevator from the museum's fifth floor, offers panoramic views of Central Park and a rotating selection of contemporary art installations that most visitors never discover. The Upper East Side rewards patience and curiosity: its best treasures are the ones you have to look for.",
            "A StoryHunt through the Upper East Side peels back the neighborhood's polished surface. Your phone sends you past mansion facades with hidden symbols, into museum rooms that most visitors skip, and along residential blocks that contain architectural secrets from the Gilded Age. You'll decode the connections between robber barons and Renaissance art, investigate hidden gardens, and piece together a puzzle that spans from the Met's rooftop to the basement of a Fifth Avenue townhouse. Elegant exploration — no guide, no group, just discovery.",
        ],
        "links": [("central-park.html", "Decode Central Park"), ("architectural-marvels-nyc.html", "Architectural Marvels of NYC"), ("hidden-places-nyc.html", "Hidden Places in NYC")],
    },

    "grand-central.html": {
        "subtitle": "A whispering gallery, a hidden bar, and a secret power station beneath the world's most famous terminal.",
        "title": "Grand Central: The Terminal Full of Secrets",
        "paragraphs": [
            "Grand Central Terminal's most famous secret is also its most accessible. The whispering gallery, located in the arched passageway near the Oyster Bar on the lower level, allows two people standing in diagonally opposite corners to have a private conversation at a whisper — the sound travels along the curved ceramic tiles of the vaulted ceiling. This acoustic quirk was not intentionally designed; it's a byproduct of the Guastavino tile work created by Spanish-born architect Rafael Guastavino. The Campbell Bar, hidden behind an unmarked door on the mezzanine level, was once the private office of 1920s businessman John W. Campbell, complete with a 25-foot painted ceiling and a massive stone fireplace.",
            "Look up at Grand Central's astronomical ceiling and you'll notice the constellations are painted backward — a mistake that has been debated for over a century. Some say the painter worked from a medieval manuscript that depicted the sky as seen from outside the celestial sphere. Look more carefully and you'll spot a small dark rectangle near the constellation Cancer: this patch was intentionally left unrestored during the 1998 renovation to show how much nicotine and tar had accumulated on the ceiling from decades of cigarette smoke. Beneath the terminal lies M42, a secret sub-basement power station that was considered so critical during World War II that armed guards were stationed to prevent sabotage.",
            "StoryHunt's Grand Central experience transforms your commute — or your visit — into a detective mission. Your phone sends you to the whispering gallery, through hidden corridors, and past architectural details that most of the terminal's 750,000 daily visitors never notice. You'll decode ceiling constellations, investigate the Campbell Bar's hidden history, and piece together clues that lead from the main concourse to secret sub-basements. The terminal is the puzzle — your phone is the decoder.",
        ],
        "links": [("midtown.html", "Decode Midtown"), ("underground-tunnels-nyc.html", "Underground Tunnels of NYC"), ("architectural-marvels-nyc.html", "Architectural Marvels of NYC")],
    },

    # ═══════════════════════════════════════
    # NYC TOPICS (15)
    # ═══════════════════════════════════════

    "hidden-places-nyc.html": {
        "subtitle": "Secret gardens, sealed doorways, and underground rooms the city doesn't advertise.",
        "title": "New York's Best-Kept Hidden Places",
        "paragraphs": [
            "New York City has more hidden places per square mile than any other city in the Western Hemisphere. Behind a service door in the basement of the Woolworth Building, a swimming pool built for the building's tenants in 1913 has sat unused for decades, its tiled walls still intact. The Elevated Acre, a public park built on top of a parking garage at 55 Water Street in the Financial District, is one of the largest public green spaces in Lower Manhattan — and most New Yorkers have never heard of it. In the West Village, a locked gate on Grove Street leads to Grove Court, a cluster of private homes built in the 1850s that is one of the most hidden residential enclaves on the island.",
            "The city's hidden places exist because New York was built in layers. Each generation built on top of the last, sealing off previous versions of the city. Beneath the streets of Chinatown, old Prohibition tunnels connected bars to escape routes. Inside Grand Central Terminal, secret passageways lead to sub-basements that were classified during World War II. On Roosevelt Island, the ruins of a 19th-century smallpox hospital stand in a public park, their Gothic arches slowly crumbling into the East River. Each hidden place is a portal to a version of New York that the surface city has papered over.",
            "StoryHunt is built for exactly this kind of discovery. Each mystery walk sends you to hidden places — not as a tourist on a bus, but as an investigator following clues on your phone. You'll find locked gardens, decode inscriptions on forgotten monuments, and discover rooms that most New Yorkers walk past every day without knowing they exist. Every clue is rooted in real history and real geography. The city is full of secrets. Your job is to find them.",
        ],
        "links": [("secret-spots-nyc.html", "Secret Spots in NYC"), ("underground-tunnels-nyc.html", "Underground Tunnels of NYC"), ("abandoned-places-nyc.html", "Abandoned Places in NYC")],
    },

    "secret-spots-nyc.html": {
        "subtitle": "The doorways, alleys, and passages that don't appear on any tourist map.",
        "title": "Secret Spots the Guidebooks Miss",
        "paragraphs": [
            "The Hess Triangle, a tiny mosaic embedded in the sidewalk at the corner of Seventh Avenue South and Christopher Street, is the smallest piece of private property in New York City. It measures just 25.5 inches on each side and was created in 1922 as an act of spite: when the city seized the Voorhis family property through eminent domain to widen the street, the family's estate discovered this tiny triangle had been overlooked in the seizure documents, and they inscribed it with \"Property of the Hess Estate which has never been dedicated for public purposes.\" It remains to this day.",
            "In the East Village, a community garden called the 6BC Botanical Garden on East 6th Street contains a two-story treehouse, a fishpond, and a performance stage — all built by neighborhood volunteers on a vacant lot the city abandoned in the 1970s. On the Upper West Side, the Pomander Walk, a hidden row of Tudor-style cottages between 94th and 95th Streets, was built in 1921 as a replica of the set from a London stage play. Humphrey Bogart lived there before he became famous. These secret spots aren't hidden underground or behind locked doors — they're hidden by familiarity, overlooked because they don't fit the New York City most people expect to find.",
            "StoryHunt's mystery walks are designed to lead you to exactly these kinds of places. Your phone delivers clues that guide you off the main streets and into the city's secret geography. You'll investigate hidden triangles, decode garden inscriptions, and discover architectural quirks that tell the real story of how New York was built — not by grand planners but by stubborn individuals who carved out small, strange, beautiful spaces in the gaps between the big buildings.",
        ],
        "links": [("hidden-places-nyc.html", "Hidden Places in NYC"), ("weird-places-nyc.html", "Weird Places in NYC"), ("west-village.html", "Decode the West Village")],
    },

    "urban-legends-nyc.html": {
        "subtitle": "Alligators in the sewers, ghosts in the subway, and the stories New York tells about itself.",
        "title": "NYC Urban Legends: Fact, Fiction, and the Gray Zone",
        "paragraphs": [
            "The most famous New York urban legend — that alligators live in the sewers beneath Manhattan — has a surprisingly real origin. In the 1930s, the New York Times reported that a group of teenagers pulled a seven-foot alligator from an open manhole on East 123rd Street. Whether the story was embellished by the reporter is debatable, but alligators have been found in New York waterways multiple times since then, most likely released by owners who bought baby gators as pets. The sewer ecosystem couldn't actually support a breeding population, but the legend persists because it captures something true about the city: beneath the surface, anything seems possible.",
            "The ghosts of the original Penn Station — demolished in 1963 to build the current underground labyrinth and Madison Square Garden — are another legend that blurs the line between myth and fact. The building's pink marble columns were dumped in the Meadowlands, and for years locals reported seeing their outlines at low tide. Old City Hall subway station, sealed since 1945 but still visible through the windows of the 6 train as it loops around at the end of the line, generates its own legends: security guards have reported footsteps, voices, and flickering lights in the abandoned station.",
            "StoryHunt turns urban legends into interactive investigations. Your phone sends you to the real locations behind the myths — the manhole covers, the sealed stations, the buildings where witnesses reported impossible things. Each clue asks you to decide: fact or fiction? The line between history and legend in New York is thinner than you think, and a StoryHunt mystery walk puts you right on that line. No guide telling you what to believe — just evidence, and your own judgment.",
        ],
        "links": [("weird-places-nyc.html", "Weird Places in NYC"), ("haunted-places-nyc.html", "Haunted Places in NYC"), ("underground-tunnels-nyc.html", "Underground Tunnels of NYC")],
    },

    "mysteries-in-nyc.html": {
        "subtitle": "Unsolved cases, vanished landmarks, and the questions New York still can't answer.",
        "title": "The Unsolved Mysteries of New York City",
        "paragraphs": [
            "The Dakota building at 72nd Street and Central Park West is famous as the site of John Lennon's murder in 1980 — but the building has accumulated mysteries since long before that night. Built in 1884, it was so far north of the city's developed areas that it was named \"The Dakota\" as a joke, comparing its remote location to the Dakota Territory. The building's architect, Henry Hardenbergh, included hidden passages, a private courtyard, and apartments with layouts so irregular that residents have reported discovering rooms they didn't know existed. The Dakota's resident list reads like a catalog of New York aristocracy, and the building's co-op board remains one of the most secretive in the city.",
            "New York is full of missing landmarks whose absence is itself a mystery. The original Waldorf-Astoria Hotel on 34th Street was demolished to build the Empire State Building — but photographs of its grand interiors suggest that much of the hotel's ornamental ironwork and stained glass was removed before demolition and simply vanished. No museum or private collection has claimed the pieces. Similarly, Penn Station's demolished eagles — massive stone sculptures that adorned the building's entrance — were never recovered. The city's history is riddled with objects, buildings, and even people who disappeared without satisfactory explanation.",
            "StoryHunt's mystery walks send you to the real locations of New York's unsolved questions. Your phone delivers clues drawn from cold cases, missing landmarks, and architectural puzzles that historians still debate. You'll investigate sealed doorways, decode inscriptions, and piece together evidence scattered across multiple city blocks. Every StoryHunt mission is built on real mysteries — because in New York, the truth is strange enough that you don't need to make anything up.",
        ],
        "links": [("urban-legends-nyc.html", "Urban Legends of NYC"), ("haunted-places-nyc.html", "Haunted Places in NYC"), ("hidden-places-nyc.html", "Hidden Places in NYC")],
    },

    "weird-places-nyc.html": {
        "subtitle": "The city's strangest spots — from a sidewalk triangle of spite to an underground civilization.",
        "title": "The Weirdest Places in New York City",
        "paragraphs": [
            "The old City Hall subway station, sealed since 1945, is arguably the most beautiful room in New York that almost nobody has seen. Its Guastavino tile arches, brass chandeliers, and stained-glass skylights were designed to impress riders on the city's first subway line, which opened in 1904. The station was closed because its curved platform couldn't accommodate modern, longer trains — but the space was never demolished, and it sits beneath City Hall Park in pristine condition. You can catch a glimpse of it by staying on the 6 train past its last stop at Brooklyn Bridge and riding the loop as the train turns around.",
            "Jennifer Toth's 1993 book \"The Mole People\" documented communities living in abandoned tunnels beneath Manhattan — a controversial account that mixed investigative journalism with disputed claims. What's not disputed is that New York's underground contains vast networks of unused spaces: sealed stations, abandoned rail tunnels, Cold War-era shelters, and Prohibition passageways. The Hess Triangle — a 25.5-inch mosaic triangle in the Greenwich Village sidewalk — is the smallest piece of private property in New York, maintained as a monument to a property dispute from 1922.",
            "StoryHunt was built for the weird places. Each mystery walk sends you to spots that defy ordinary explanation — architectural oddities, geographic quirks, and spaces that shouldn't exist but do. Your phone guides you with clues drawn from real history and real geography, challenging you to find the weirdest details hiding in plain sight. You don't need a tour guide to find New York's strangest places — you need a decoder. That's what StoryHunt gives you.",
        ],
        "links": [("secret-spots-nyc.html", "Secret Spots in NYC"), ("abandoned-places-nyc.html", "Abandoned Places in NYC"), ("urban-legends-nyc.html", "Urban Legends of NYC")],
    },

    "true-crime-tours-nyc.html": {
        "subtitle": "Five Points alleys, gangland shootouts, and the real crime scenes hiding in plain sight.",
        "title": "True Crime Walking Tours in New York City",
        "paragraphs": [
            "The Five Points, the intersection of five streets in what is now Chinatown and Civic Center, was the most dangerous neighborhood in 19th-century America. Gangs like the Dead Rabbits and the Bowery Boys fought for control of blocks so overcrowded that single tenement rooms housed a dozen people. The Old Brewery, a converted commercial building on the site of today's Columbus Park, was considered the most dangerous building in the city — police refused to enter it, and an 1852 demolition revealed human remains in the walls. The neighborhood was eventually razed in one of the city's first slum clearance projects, but the streets still follow the same paths.",
            "New York's true crime history extends well beyond the 19th century. The 1906 murder of Stanford White by millionaire Harry Thaw in the rooftop theater of Madison Square Garden was the first \"trial of the century\" in American media. Murder Inc., the Mafia's enforcement arm, operated out of Midnight Rose's candy store in Brownsville, Brooklyn, in the 1930s and 40s. The Son of Sam terrorized the city in 1977, and the addresses where his victims were found are still visible, unmarked, on residential streets in Queens and the Bronx.",
            "StoryHunt's true crime experiences turn notorious neighborhoods into interactive investigations. Your phone sends you to the actual locations where crimes occurred, delivering clues that challenge you to reconstruct the events. You'll walk the same blocks the detectives walked, decode evidence scattered across multiple locations, and piece together stories that are both horrifying and deeply connected to the city's evolution. This isn't a theatrical ghost tour — it's a real investigation, guided by your phone, driven by real history.",
        ],
        "links": [("mob-history-nyc.html", "Mob History NYC"), ("true-crime-lower-east-side.html", "True Crime: Lower East Side"), ("haunted-places-nyc.html", "Haunted Places in NYC")],
    },

    "haunted-places-nyc.html": {
        "subtitle": "The most reported paranormal hotspots in the five boroughs — and the histories behind them.",
        "title": "Haunted Places in New York City",
        "paragraphs": [
            "The Merchant's House Museum at 29 East 4th Street is widely considered the most haunted building in Manhattan. Built in 1832, it's the only 19th-century family home in New York preserved intact with its original furnishings. The house's last resident, Gertrude Tredwell, died there in 1933 at age 93, and staff and visitors have reported seeing her apparition in an upstairs bedroom, smelling her perfume in the parlor, and hearing piano music from a room where no one is playing. The building has been investigated by paranormal researchers multiple times, and it's one of the few haunted locations in New York that is open to the public year-round.",
            "The Morris-Jumel Mansion in Washington Heights, Manhattan's oldest surviving house (built in 1765), served as George Washington's headquarters during the Battle of Harlem Heights. Its residents over the centuries included Aaron Burr's wife Eliza Jumel, whose ghost has been reportedly seen in an upstairs window. The House of Death at 14 West 10th Street — a brownstone in Greenwich Village — has an alleged 22 ghosts, including Mark Twain, who lived there briefly. The New York Public Library's main branch on Fifth Avenue has reports of footsteps in empty reading rooms after closing. Even the Empire State Building has its ghost stories, typically involving Depression-era workers who died during construction.",
            "StoryHunt's haunted walks send you to the city's most reported paranormal locations — not for jump scares, but for investigation. Your phone delivers historical clues about each site, challenges you to find physical evidence of the events that created the legends, and lets you draw your own conclusions. Each haunted place has a real history that's as compelling as any ghost story. You walk the route, you decode the clues, you decide what you believe.",
        ],
        "links": [("ghost-tours-nyc.html", "Ghost Tours NYC"), ("haunted-places-greenwich-village.html", "Haunted Greenwich Village"), ("urban-legends-nyc.html", "Urban Legends of NYC")],
    },

    "ghost-tours-nyc.html": {
        "subtitle": "Where to find New York's ghosts — and how to hunt them with your phone.",
        "title": "Ghost Tours in New York City: A Different Kind of Hunt",
        "paragraphs": [
            "Traditional ghost tours in New York City follow a predictable formula: a guide in a cape leads a group to five or six haunted locations, tells dramatized stories, and maybe throws in a jump scare. They're entertaining, but they barely scratch the surface. The city has hundreds of reported haunting locations — from the Merchant's House Museum in the East Village (where staff regularly report encounters with Gertrude Tredwell's spirit) to the Players Club at 16 Gramercy Park South (where the ghost of Edwin Booth, brother of John Wilkes Booth, allegedly roams the halls). A two-hour guided walk can only cover a fraction of these sites.",
            "The best ghost-hunting experiences go deeper: they connect each haunting to the real historical events that created the legends. The Ear Inn on Spring Street, one of the oldest bars in Manhattan (operating since 1817), has a ghost named Mickey that staff attribute to a sailor who died in the building during the 19th century. The ghost of Peter Stuyvesant — the last Dutch governor of New Amsterdam — has been reported in and around St. Mark's Church in-the-Bowery, where he is buried. Each ghost story is really a history lesson, and the best tours are the ones that treat them that way.",
            "StoryHunt reimagines the ghost tour as an interactive investigation. Instead of following a guide, your phone delivers paranormal case files as clues. You walk the city at your own pace, visiting haunted locations and decoding the historical evidence behind each reported sighting. No one tells you what to believe — you investigate, you find the facts, you decide. It's a ghost tour for people who want to actually hunt, not just listen. Two to three hours across some of the most atmospheric streets in the city.",
        ],
        "links": [("haunted-places-nyc.html", "Haunted Places in NYC"), ("ghosts-of-broadway.html", "Ghosts of Broadway"), ("haunted-places-greenwich-village.html", "Haunted Greenwich Village")],
    },

    "speakeasies-nyc.html": {
        "subtitle": "Prohibition ended in 1933. The hidden bars never went away.",
        "title": "Speakeasies in NYC: The Doors That Stay Hidden",
        "paragraphs": [
            "During Prohibition (1920–1933), New York City had an estimated 30,000 to 100,000 speakeasies — more than double the number of legal bars that had existed before the ban. The sheer density of hidden drinking establishments meant that secret entrances were built into barbershops, laundries, basements, and private homes across every neighborhood. When Prohibition ended, most of these spaces were converted back to their original purposes — but a surprising number survived, either as bars that kept their hidden entrances for atmosphere or as sealed-off rooms that were simply forgotten behind new walls.",
            "Chumley's at 86 Bedford Street in the West Village has operated as a bar since 1922 and famously never had a sign — the expression \"86'd,\" meaning to be thrown out, allegedly comes from its address (though etymologists debate this). Please Don't Tell (PDT) in the East Village requires you to enter through a phone booth inside Crif Dogs, a hot dog restaurant. Employees Only on Hudson Street is marked only by a psychic's neon palm sign. These modern speakeasies preserve the Prohibition-era tradition of concealment, but the real historical hidden bars — the ones that were built to evade federal agents — were far more ingenious, with trapdoors, escape tunnels, and rooms that could be sealed in seconds.",
            "StoryHunt's speakeasy experiences send you hunting for hidden bars — both the historical sites and the modern descendants. Your phone delivers Prohibition-era clues that lead you to unmarked doorways, concealed staircases, and addresses where the hidden entrance is part of the adventure. You'll decode the signs that speakeasy operators used to mark their doors, investigate the tunnels that connected bars to escape routes, and discover how the culture of concealment shaped the way New York drinks to this day.",
        ],
        "links": [("hidden-speakeasies-soho.html", "Hidden Speakeasies of SoHo"), ("mob-history-nyc.html", "Mob History NYC"), ("west-village.html", "Decode the West Village")],
    },

    "mob-history-nyc.html": {
        "subtitle": "Five Families, famous hits, and the buildings that witnessed it all.",
        "title": "Mob History in New York City",
        "paragraphs": [
            "New York's Five Families — the Gambino, Lucchese, Genovese, Bonanno, and Colombo organizations — controlled the city's criminal underworld for most of the 20th century. The structures they operated from are still standing: the Ravenite Social Club at 247 Mulberry Street in Little Italy was John Gotti's headquarters until the FBI bugged the building's upstairs apartment. Sparks Steak House at 210 East 46th Street was where Paul Castellano, boss of the Gambino family, was gunned down in 1985 on Gotti's orders — the hit that made Gotti the most famous mobster in America.",
            "The Mafia's influence on New York extended far beyond violence. The Five Families controlled the Fulton Fish Market for decades, taking a cut of every transaction. They ran concrete companies that built the city's skyscrapers, controlled the garment industry's trucking, and influenced the outcome of labor disputes that shaped the city's economy. The Commission, created by Lucky Luciano in 1931 to settle disputes between the families without bloodshed, met in various locations around the city — including a penthouse on the Upper West Side and a social club in Brooklyn. The infrastructure of organized crime was as complex and far-reaching as the city government itself.",
            "StoryHunt's mob history walks take you to the actual locations where New York's organized crime history unfolded. Your phone delivers clues drawn from court records, FBI surveillance transcripts, and historical accounts. You'll walk past social clubs, investigate former meeting places, and decode the network of locations that connected the Five Families' operations. This isn't a Hollywood version of the mob — it's the real geography of power, violence, and influence that shaped modern New York.",
        ],
        "links": [("mob-history-little-italy.html", "Mob History: Little Italy"), ("true-crime-tours-nyc.html", "True Crime Tours NYC"), ("speakeasies-nyc.html", "Speakeasies of NYC")],
    },

    "abandoned-places-nyc.html": {
        "subtitle": "Ghost stations, ruined hospitals, and military forts reclaimed by nature.",
        "title": "Abandoned Places in New York City",
        "paragraphs": [
            "The old City Hall subway station is the crown jewel of New York's abandoned places. Opened in 1904 as the showpiece of the city's first subway line, it was closed in 1945 because its curved platform couldn't accommodate longer, modern trains. The station's Guastavino tile arches, brass chandeliers, and colored-glass skylights remain intact beneath City Hall Park, preserved in a kind of subterranean time capsule. You can catch a fleeting glimpse of it by staying on the 6 train past Brooklyn Bridge as it loops around — the lights of the abandoned station flash through the windows for a few seconds.",
            "On Roosevelt Island, the Renwick Smallpox Hospital stands as a stabilized ruin in Southpoint Park. Designed by James Renwick Jr. (who also designed St. Patrick's Cathedral) and built in 1856, the hospital treated smallpox patients quarantined from the city. After the hospital closed, the building deteriorated for over a century, and its Gothic Revival walls now frame open sky where ceilings used to be. At Fort Tilden on the Rockaway Peninsula, abandoned military buildings from both World Wars sit among overgrown dunes — concrete gun emplacements, ammunition bunkers, and observation towers slowly being reclaimed by sand and salt air.",
            "StoryHunt leads you to the edges of New York's abandoned spaces through interactive mystery walks. Your phone delivers clues connected to the histories of abandoned stations, hospitals, and military installations, guiding you to viewpoints and access points that are legal and safe while preserving the thrill of discovery. You'll decode the stories behind sealed doors, investigate the reasons each place was abandoned, and piece together the hidden map of New York's forgotten infrastructure.",
        ],
        "links": [("abandoned-stations-nyc-subway.html", "Abandoned Subway Stations"), ("underground-tunnels-nyc.html", "Underground Tunnels of NYC"), ("hidden-places-nyc.html", "Hidden Places in NYC")],
    },

    "movie-locations-nyc.html": {
        "subtitle": "From Ghostbusters to Home Alone 2 — the real buildings behind the reel.",
        "title": "Iconic Movie Locations in New York City",
        "paragraphs": [
            "New York City is the most filmed city in the world, with roughly 50,000 location shoots per year. The Ghostbusters firehouse at 14 North Moore Street in TriBeCa (Hook & Ladder Company 8) is still an active firehouse, and fans still pose outside it daily. The brownstone steps at 64 Perry Street in the West Village stood in for Carrie Bradshaw's apartment in Sex and the City, though the real apartment used for interior shots was on the Upper East Side. The Plaza Hotel — where Eloise lived in the children's books — also served as Kevin McCallister's hotel in Home Alone 2: Lost in New York, and you can still walk through the lobby where Macaulay Culkin slid across the marble floor.",
            "Katz's Delicatessen on Houston Street hosted the most famous fake-orgasm scene in cinema history (When Harry Met Sally), and the table where it was filmed is marked with a sign that reads \"Where Harry met Sally... hope you have what she had!\" The steps of the New York County Courthouse at 60 Centre Street have appeared in so many Law & Order episodes that tourists recognize them on sight. The Bethesda Fountain in Central Park has appeared in films from Angels in America to John Wick. Each of these locations carries a double history: the real story of the building and the fictional story projected onto it.",
            "StoryHunt's movie location experiences send you to the real places behind the films, but with a twist — your phone delivers clues that blend the fictional stories with the real histories of each building. You'll investigate why the Ghostbusters firehouse was chosen (its architectural details), decode the connections between film locations and neighborhood history, and discover spots that appeared on screen but that most fans walk right past. Cinema meets city exploration — no bus tour, just you and a mystery that plays out in real locations.",
        ],
        "links": [("tribeca.html", "Decode TriBeCa"), ("central-park.html", "Decode Central Park"), ("hidden-places-nyc.html", "Hidden Places in NYC")],
    },

    "literary-tours-nyc.html": {
        "subtitle": "The addresses where American literature was written, argued over, and reinvented.",
        "title": "Literary Tours in New York City",
        "paragraphs": [
            "New York has been the home or temporary residence of more important American writers than any other city. The White Horse Tavern on Hudson Street was the regular haunt of Dylan Thomas, who famously drank himself to death after leaving the bar in 1953 (his last words, \"I've had eighteen straight whiskies. I think that's the record,\" are likely apocryphal but have become literary legend). The Algonquin Hotel on 44th Street hosted the Round Table — the lunch club where Dorothy Parker, Robert Benchley, and Harold Ross (founder of The New Yorker) traded barbs through the 1920s. The hotel's lobby still arranges its furniture in a nod to the original table configuration.",
            "The Beat Generation made New York its laboratory before decamping to San Francisco. Allen Ginsberg wrote \"Howl\" while living on the Lower East Side. Jack Kerouac typed the scroll manuscript of On the Road in a Chelsea apartment. The Strand Bookstore on Broadway, with its \"18 miles of books,\" has been a gathering point for literary New York since 1927. In Harlem, Langston Hughes' brownstone at 20 East 127th Street sits quietly on a residential block — the house where he wrote some of the most important poetry of the Harlem Renaissance. These aren't museums; they're working buildings on active streets, hiding in plain sight.",
            "StoryHunt's literary walks connect you to the city's writing history through interactive clues. Your phone sends you to the addresses where manuscripts were written, bars where editors discovered writers, and bookstores that shaped literary movements. You'll decode literary references embedded in building facades, investigate the connections between neighborhoods and the works they inspired, and piece together the map of literary New York — one clue at a time, at your own pace.",
        ],
        "links": [("literary-secrets-west-village.html", "Literary Secrets: West Village"), ("west-village.html", "Decode the West Village"), ("greenwich-village.html", "Decode Greenwich Village")],
    },

    "architectural-marvels-nyc.html": {
        "subtitle": "Art Deco eagles, Beaux-Arts lobbies, and ornamental details most people never look up to see.",
        "title": "Architectural Marvels of New York City",
        "paragraphs": [
            "New York City's architecture is best appreciated from angles most people ignore: straight up. The Chrysler Building's stainless-steel crown, with its triangular windows and eagle gargoyles at the 61st floor, is the finest Art Deco ornament in the world — but the building's lobby, with its African marble walls, Edward Trumbull ceiling murals, and original elevator doors, is equally remarkable and far less visited. The Woolworth Building, when it opened in 1913, was the tallest building in the world and was nicknamed the \"Cathedral of Commerce\" for its Gothic terra cotta exterior. Its lobby — accessible by guided tour only — contains caricature sculptures of the building's architect, Cass Gilbert, cradling a model of the tower.",
            "The Beaux-Arts style dominates Midtown's civic architecture: Grand Central Terminal, the New York Public Library, and the old Custom House at Bowling Green (now the National Museum of the American Indian) all feature the grand columns, sculptural groups, and monumental staircases characteristic of the style. But the city's architectural treasures extend to every era: the cast-iron facades of SoHo, the brownstone rows of Brooklyn Heights, the Art Moderne apartment buildings of the Upper West Side, and the brutalist concrete of the 1960s municipal buildings each represent a distinct chapter in the city's visual history. Hidden details — carved faces, symbolic ornaments, embedded dates — reward anyone willing to slow down and look.",
            "StoryHunt turns architectural appreciation into an interactive mission. Your phone sends you past facades, into lobbies, and up to viewpoints where hidden architectural details become clues in a larger mystery. You'll decode ornamental symbols, investigate the stories behind carved figures, and piece together the connections between architects, patrons, and the buildings they created. No architecture degree required — just a willingness to look up.",
        ],
        "links": [("grand-central.html", "Grand Central Secrets"), ("midtown.html", "Decode Midtown"), ("flatiron.html", "Decode Flatiron")],
    },

    "underground-tunnels-nyc.html": {
        "subtitle": "Beneath the city streets, a hidden network of subway secrets, rail tunnels, and sealed passages.",
        "title": "Underground Tunnels of New York City",
        "paragraphs": [
            "The Atlantic Avenue Tunnel in Brooklyn, built in 1844, is the world's oldest subway tunnel. It was sealed in 1861 and forgotten for over a century until urban explorer Bob Diamond rediscovered it in 1981 by lowering himself through a manhole. The half-mile tunnel, originally built for the Long Island Rail Road, sits beneath Atlantic Avenue in pristine condition — its brick walls and iron rail beds untouched since the Civil War era. The Freedom Tunnel, a former Amtrak rail tunnel beneath Riverside Park on the Upper West Side, earned its name from the graffiti artist Chris \"Freedom\" Pape, who painted murals on the tunnel walls in the 1980s while the space was occupied by a community of homeless residents.",
            "New York's underground extends far beyond its subway system. Prohibition-era tunnels connected speakeasies to escape routes in neighborhoods across Lower Manhattan. Steam pipes — part of the world's largest commercial steam system — run beneath the streets of Midtown, occasionally venting through the iconic orange-and-white street stacks that appear in every New York movie. Beneath the Waldorf Astoria, a private rail siding allowed President Franklin Roosevelt to arrive by armored train without being seen. The city's underground is a parallel world, built over more than 150 years and largely invisible to the millions who walk above it every day.",
            "StoryHunt's underground tunnel experiences bring you as close to these hidden worlds as legally possible. Your phone delivers clues connected to tunnel histories, sealed entrances, and the infrastructure that runs beneath your feet. You'll decode the surface signs that reveal what's below — grates, vents, unmarked doors — and piece together the hidden map of underground New York. Each walk is an investigation into the city beneath the city.",
        ],
        "links": [("abandoned-stations-nyc-subway.html", "Abandoned Subway Stations"), ("hidden-places-nyc.html", "Hidden Places in NYC"), ("grand-central.html", "Grand Central Secrets")],
    },

    # ═══════════════════════════════════════
    # NYC DEEP DIVES (9)
    # ═══════════════════════════════════════

    "haunted-places-greenwich-village.html": {
        "subtitle": "More reported ghost sightings per block than any other neighborhood in Manhattan.",
        "title": "Haunted Places in Greenwich Village",
        "paragraphs": [
            "Greenwich Village is the most haunted neighborhood in New York City by density of reported paranormal activity. The House of Death at 14 West 10th Street — a brownstone that has been divided into apartments since the 19th century — reportedly harbors 22 ghosts, including the spirit of Mark Twain, who lived there in 1900-1901. Residents over the decades have reported seeing a gray-haired man in a white suit in the stairwell, hearing typing from empty rooms, and smelling pipe tobacco. In 1987, a defense attorney living in the building murdered his daughter and claimed a ghostly voice told him to do it — a case that drew national attention to the building's dark reputation.",
            "The Merchant's House Museum at 29 East 4th Street, just on the Village's edge, has been investigated by paranormal researchers more than any other building in Manhattan. Gertrude Tredwell, the house's last occupant, reportedly appears in the bedroom where she died in 1933. The Northern Dispensary at 165 Waverly Place — a triangular building where Edgar Allan Poe was treated for a cold in 1837 — has stood empty since 1998, and neighbors report seeing lights in windows of the sealed building. Washington Square Park itself was a potter's field before it was a park; an estimated 20,000 bodies remain buried beneath the grass.",
            "StoryHunt's haunted Greenwich Village walk leads you through the neighborhood's most reported paranormal locations with historical context delivered to your phone as clues. You'll investigate each site, decode the real events behind the hauntings, and decide for yourself what's happening in these buildings. No theatrical performances, no costumes — just real locations, real history, and the unexplained. A two-to-three-hour investigation through the most atmospherically charged streets in the city.",
        ],
        "links": [("greenwich-village.html", "Decode Greenwich Village"), ("haunted-places-nyc.html", "Haunted Places in NYC"), ("ghost-tours-nyc.html", "Ghost Tours NYC")],
    },

    "true-crime-lower-east-side.html": {
        "subtitle": "Tenement murders, gang wars, and the blocks where crime shaped a neighborhood.",
        "title": "True Crime History of the Lower East Side",
        "paragraphs": [
            "The Lower East Side was the most densely populated place on Earth at the turn of the 20th century. Immigrant families — Jewish, Italian, Chinese, Irish — crowded into tenement apartments so small that an entire family might share a single room with no windows. This density bred desperation, and desperation bred crime. The Eastman Gang, led by Monk Eastman, controlled the blocks below Houston Street through a combination of violence and political patronage. Eastman himself — a squat, scarred man who kept a collection of pigeons on his tenement roof — was eventually murdered in 1920 outside a speakeasy on East 14th Street after surviving years of gang warfare.",
            "The Allen Street murders of the 1890s and 1900s — a series of killings connected to the neighborhood's thriving sex-trafficking industry — went largely unsolved because the victims were immigrant women with no political power. The Triangle Shirtwaist Factory fire of 1911, at the corner of Washington Place and Greene Street (just north of the Lower East Side), killed 146 garment workers, mostly young immigrant women, and exposed the dangerous working conditions that the neighborhood's residents endured daily. The building still stands, now part of NYU, with a small plaque that most passersby ignore.",
            "StoryHunt's Lower East Side true crime walk puts you in the middle of this history. Your phone delivers clues drawn from police records, newspaper accounts, and court transcripts of the era. You'll walk the same blocks the gangs controlled, investigate the addresses where crimes occurred, and decode the connections between poverty, immigration, and violence that shaped the neighborhood. No sensationalism — just the streets, the facts, and a mystery that challenges you to understand how this neighborhood's past lives in its present.",
        ],
        "links": [("true-crime-tours-nyc.html", "True Crime Tours NYC"), ("hidden-places-nyc.html", "Hidden Places in NYC"), ("mob-history-nyc.html", "Mob History NYC")],
    },

    "hidden-speakeasies-soho.html": {
        "subtitle": "Behind SoHo's cast-iron facades, Prohibition-era bars that never closed — and new ones that carry the tradition.",
        "title": "Hidden Speakeasies of SoHo",
        "paragraphs": [
            "SoHo's dense collection of 19th-century cast-iron buildings created an ideal environment for Prohibition-era speakeasies. The buildings' commercial ground floors, deep basements, and interconnected cellar passages allowed bar operators to set up hidden drinking rooms with multiple escape routes. When federal agents came through the front, patrons could exit through basement tunnels that connected to adjacent buildings. Many of these sub-street-level spaces were sealed after Prohibition ended and remained hidden behind walls and false floors for decades. Renovation projects in SoHo buildings regularly uncover blocked-off rooms, vintage bottles, and the remains of old bar fixtures.",
            "Today, SoHo's speakeasy tradition lives on in bars that honor the neighborhood's hidden-drinking heritage. Ear Inn at 326 Spring Street has served drinks since 1817 — making it one of the oldest bars in New York — and survived Prohibition by operating as a restaurant that happened to serve alcohol. The building's original facade, with its faded \"BAR\" sign partially obscured (the owner covered the B to read \"EAR\" during the landmark designation process), is one of the most photographed in the neighborhood. Newer establishments carry on the concealment tradition with unmarked entrances, basement access, and interiors designed to evoke the Prohibition atmosphere.",
            "StoryHunt's SoHo speakeasy walk sends you hunting for hidden bars — both the historical sites and their modern descendants. Your phone delivers Prohibition-era clues that guide you to unmarked doors, concealed basements, and the architectural details that reveal where secret bars once operated. You'll decode the visual language of concealment — the signs, symbols, and design choices that speakeasy operators used to communicate with customers while hiding from the law. A two-to-three-hour investigation into SoHo's secret drinking history.",
        ],
        "links": [("soho.html", "Decode SoHo"), ("speakeasies-nyc.html", "Speakeasies of NYC"), ("hidden-places-nyc.html", "Hidden Places in NYC")],
    },

    "secret-gardens-central-park.html": {
        "subtitle": "Hidden clearings, locked gardens, and quiet corners in the world's most famous park.",
        "title": "Secret Gardens of Central Park",
        "paragraphs": [
            "The Hallett Nature Sanctuary, a four-acre woodland at the park's southeast corner near 59th Street and Sixth Avenue, was closed to the public for over two decades before being partially reopened in 2016. During its closure, the sanctuary evolved into a genuine urban wilderness — a dense thicket of native trees, wildflowers, and wildlife just steps from one of the busiest intersections in Manhattan. Even now that it's accessible, most park visitors walk right past its entrance without noticing it. The sanctuary's trails are narrow, unmarked, and quiet in a way that feels impossible given its location above a subway station.",
            "Shakespeare Garden, on the western slope below Belvedere Castle, is planted exclusively with species mentioned in the works of William Shakespeare — roses, primrose, rue, thyme, and dozens more. Bronze plaques throughout the garden quote the relevant passages. The Conservatory Garden, the only formal garden in the park, is accessed through the ornate Vanderbilt Gate on Fifth Avenue at 105th Street — an entrance so grand that tourists assume it leads to a private property and walk past. Inside, three distinct garden styles — Italian, French, and English — create a sequence of outdoor rooms that bloom from April through October. The Secret Garden fountain, inspired by the Frances Hodgson Burnett novel, is the centerpiece of the English section.",
            "StoryHunt's Central Park garden experience leads you to the park's quietest corners through clues delivered to your phone. You'll investigate hidden entrances, decode botanical inscriptions, and discover garden spaces that most of the park's 42 million annual visitors never find. Each clue connects the gardens to the park's layered history — from the original Olmsted and Vaux design to the volunteer efforts that saved these spaces from neglect. A quiet, immersive walk through the park's most beautiful secrets.",
        ],
        "links": [("central-park.html", "Decode Central Park"), ("hidden-places-nyc.html", "Hidden Places in NYC"), ("secret-spots-nyc.html", "Secret Spots in NYC")],
    },

    "mob-history-little-italy.html": {
        "subtitle": "Mulberry Street social clubs, famous hits, and the neighborhood the Five Families called home.",
        "title": "Mob History of Little Italy",
        "paragraphs": [
            "Little Italy — the few blocks of Mulberry, Mott, and Grand Streets between Canal and Houston — was the epicenter of Italian-American organized crime for most of the 20th century. The Ravenite Social Club at 247 Mulberry Street was the most infamous address in the neighborhood: John Gotti held court there in the 1980s, meeting with captains and associates in full view of FBI surveillance teams parked across the street. The FBI finally cracked Gotti's organization by bugging the apartment above the club, where Gotti retreated for private conversations — not realizing the bureau had installed listening devices in the walls.",
            "The neighborhood's mob history predates Gotti by decades. Joe \"The Boss\" Masseria was shot and killed at the Nuova Villa Tammaro restaurant on Coney Island in 1931, ending the Castellammarese War and ushering in Lucky Luciano's modernization of the American Mafia. Umberto's Clam House on Mulberry Street was the site of Joey Gallo's 1972 assassination — he was shot while celebrating his birthday with his family. The restaurant has since moved to a new location on the same street, but the original site is still identifiable. Little Italy's streets contain more verified mob history per block than any other neighborhood in America.",
            "StoryHunt's Little Italy mob walk takes you to the specific addresses where this history played out. Your phone delivers clues drawn from FBI files, trial testimony, and historical records. You'll stand outside social clubs, investigate former meeting places, and decode the geography of power that the Five Families maintained for decades. Each clue connects to a real event — no Hollywood embellishment, just the documented history of organized crime in its home neighborhood.",
        ],
        "links": [("mob-history-nyc.html", "Mob History NYC"), ("true-crime-tours-nyc.html", "True Crime Tours NYC"), ("speakeasies-nyc.html", "Speakeasies of NYC")],
    },

    "ghosts-of-broadway.html": {
        "subtitle": "Phantom footsteps, flickering lights, and the spirits that never left the stage.",
        "title": "Ghosts of Broadway: Haunted Theaters of New York",
        "paragraphs": [
            "Broadway's theaters are among the most haunted buildings in New York City, which makes sense when you consider that many of them are over a century old and have hosted thousands of performers, stagehands, and audiences — some of whom, according to theater lore, never left. The Belasco Theatre on West 44th Street is considered the most haunted theater on Broadway. David Belasco, the producer who built the theater in 1907, reportedly appears as a ghostly figure in the balcony during performances. He was known for wearing a clerical collar (he called himself \"the Bishop of Broadway\"), and staff and actors have reported seeing a man in a dark coat with a white collar sitting in the same balcony seat.",
            "The New Amsterdam Theatre on 42nd Street — now home to Disney's Aladdin — is reportedly haunted by Olive Thomas, a Ziegfeld Follies performer who died in Paris in 1920 under mysterious circumstances (she drank mercury bichloride, either intentionally or by mistake). Stagehands have reported seeing a woman in a green gown carrying a blue bottle on the theater's upper floors. The Palace Theatre, the most prestigious vaudeville house in America when it opened in 1913, has reports of the ghost of acrobat Louis Borsalino, who died during a performance. The tradition of leaving a \"ghost light\" — a single bare bulb on a stand — on every Broadway stage after the audience leaves is officially a safety measure, but many theater workers maintain it's there to appease the spirits.",
            "StoryHunt's Broadway ghost walk sends you past the most haunted theaters in the district with paranormal case files delivered to your phone. You'll investigate each theater's history, decode the real events behind the reported hauntings, and explore the alleyways and stage doors where sightings have been reported. A two-to-three-hour walk through the theater district that reveals the history behind the ghost light.",
        ],
        "links": [("ghost-tours-nyc.html", "Ghost Tours NYC"), ("haunted-places-nyc.html", "Haunted Places in NYC"), ("times-square.html", "Decode Times Square")],
    },

    "abandoned-stations-nyc-subway.html": {
        "subtitle": "Ghost stations, sealed platforms, and the hidden architecture of the world's largest subway system.",
        "title": "Abandoned Subway Stations of New York City",
        "paragraphs": [
            "New York's subway system has at least 40 abandoned or disused stations, sealed off from the public but still physically present beneath the city's streets. The most famous is the old City Hall station, the crown jewel of the original 1904 Interborough Rapid Transit line. Its Guastavino tile vaults, brass fixtures, and stained-glass skylights were designed to convince skeptical New Yorkers that traveling underground could be elegant. The station closed in 1945 because its curved platform was too short for modern trains, but the space has been maintained by the MTA as an unofficial landmark — visible briefly through the windows of the 6 train as it makes its turnaround loop.",
            "The Myrtle Avenue station on the old Brooklyn-Manhattan Transit line was sealed in 1956 and sits beneath the current DeKalb Avenue station — passengers on B and Q trains pass through it without realizing they're traveling through a ghost station. Worth Street station on the 6 line was closed in 1962, and its platform tiles are visible through train windows as trains pass between Brooklyn Bridge and Canal Street. The 91st Street station on the 1 and 2 lines, closed in 1959, occasionally surfaces in MTA proposals for reopening but remains sealed. Each abandoned station is a time capsule of the era in which it was built — tile patterns, mosaic designs, and architectural details frozen at the moment the lights went off.",
            "StoryHunt's abandoned station experience guides you to the surface locations above these hidden platforms. Your phone delivers clues about what lies beneath your feet — station layouts, architectural details, and the reasons each platform was sealed. You'll decode the visible signs of underground infrastructure (gratings, ventilation shafts, sealed entrances) and piece together the map of New York's ghost subway system. An investigation into the transit network that the city built and then forgot.",
        ],
        "links": [("underground-tunnels-nyc.html", "Underground Tunnels of NYC"), ("abandoned-places-nyc.html", "Abandoned Places in NYC"), ("hidden-places-nyc.html", "Hidden Places in NYC")],
    },

    "weird-history-williamsburg.html": {
        "subtitle": "From the nation's sugar capital to underground punk shows — Williamsburg's strangest chapters.",
        "title": "The Weird History of Williamsburg, Brooklyn",
        "paragraphs": [
            "Williamsburg's strangest historical chapter begins with sugar. The Domino Sugar Factory, which operated on the waterfront from 1882 to 2004, processed more than half the sugar consumed in the United States at its peak. The refinery's working conditions were so harsh — furnace-like heat, sugar dust that coated workers' lungs — that employees called the building \"the Sweathouse.\" When the factory finally closed, artist Kara Walker installed a massive sphinx-like sculpture made of sugar inside the empty refinery as a commentary on the sweetness industry's ties to slavery. The sculpture, called \"A Subtlety,\" drew 130,000 visitors in 2014 before the building was demolished for luxury condos.",
            "Before the sugar and the condos, Williamsburg was a brewery district. In the late 1800s, the neighborhood's German immigrant population supported eleven breweries within a fourteen-block area, making it one of the largest beer-producing districts in the country. The brew houses required massive underground ice cellars to keep the lager cold, and some of these cellar networks still exist beneath current buildings — occasionally discovered during renovation projects. In the 1990s, the cheap rents in the neighborhood's abandoned industrial spaces attracted musicians and artists, and McCarren Park Pool — closed and empty since 1984 — became an unlikely concert venue where bands played to crowds standing in the drained concrete basin.",
            "StoryHunt's weird Williamsburg walk takes you through the neighborhood's strangest episodes. Your phone delivers clues connected to sugar, beer, and punk rock — the three substances that defined Williamsburg across three centuries. You'll decode industrial remnants, investigate hidden cellar entrances, and piece together the puzzle of how a neighborhood can transform so completely while leaving physical evidence of every phase behind.",
        ],
        "links": [("williamsburg.html", "Decode Williamsburg"), ("hidden-places-nyc.html", "Hidden Places in NYC"), ("weird-places-nyc.html", "Weird Places in NYC")],
    },

    "literary-secrets-west-village.html": {
        "subtitle": "The apartments, bars, and basements where American literature was rewritten.",
        "title": "Literary Secrets of the West Village",
        "paragraphs": [
            "The West Village has produced or hosted more significant American writers per block than any other neighborhood in the country. The White Horse Tavern at 567 Hudson Street was the regular drinking spot of Dylan Thomas, Jack Kerouac, and James Baldwin. Thomas drank his last drinks there on November 4, 1953, before collapsing and dying at St. Vincent's Hospital a few blocks away. The bar still has Thomas's corner booth, and the walls are covered with photographs and memorabilia from the literary era when the Village was the center of American writing.",
            "At 75½ Bedford Street — the narrowest house in New York — Edna St. Vincent Millay wrote poetry in a nine-and-a-half-foot-wide building that had previously been a cobbler's shop. E. E. Cummings lived at 4 Patchin Place, a gated mews off West 10th Street, for nearly forty years. The building across from his window was home to Djuna Barnes, who lived there as a recluse for over four decades. Around the corner, the Chumley's speakeasy at 86 Bedford Street was a gathering place for writers during Prohibition — its walls were lined with dust jackets from books by its regulars, including Hemingway, Fitzgerald, and Steinbeck. The tradition continues: the bar still displays book jackets on its walls.",
            "StoryHunt's literary West Village walk turns the neighborhood into a living bibliography. Your phone delivers clues connected to specific addresses, specific books, and the real relationships between writers who lived within blocks of each other. You'll decode literary references on building facades, investigate the bars where publishing deals were made, and piece together the geography of a neighborhood that shaped American literature. A walk for readers, writers, and anyone who believes that streets can tell stories.",
        ],
        "links": [("west-village.html", "Decode the West Village"), ("literary-tours-nyc.html", "Literary Tours NYC"), ("greenwich-village.html", "Decode Greenwich Village")],
    },

    "hidden-art-dumbo.html": {
        "subtitle": "Installations beneath bridges, galleries inside warehouses, and art you have to find to see.",
        "title": "Hidden Art in DUMBO, Brooklyn",
        "paragraphs": [
            "DUMBO's art scene grew directly out of its industrial architecture. In the 1970s and 80s, artists moved into the neighborhood's vacant warehouses — drawn by the cheap rent and the cavernous spaces that could accommodate large-scale work. The neighborhood became an unofficial gallery district decades before the developers arrived. Today, that legacy persists in spaces like the DUMBO Walls project, which commissions large-scale murals on the neighborhood's remaining warehouse facades, and the A.I.R. Gallery (Artists in Residence), one of the first artist-run galleries in the United States, which relocated to DUMBO from SoHo.",
            "The most unexpected art in DUMBO hides in plain sight. Underneath the Manhattan Bridge overpass, where the bridge's steel structure creates a covered plaza, temporary installations appear and disappear with the seasons. The Brooklyn waterfront path between the Manhattan and Brooklyn Bridges passes public sculptures that many walkers mistake for leftover industrial equipment. Inside the Empire Stores — the restored Civil War-era warehouses on the waterfront — the Brooklyn Historical Society's exhibition space presents rotating art and history shows in rooms where coffee and tobacco were stored 150 years ago. Jane's Carousel, the restored 1922 merry-go-round in its Jean Nouvel glass pavilion, is itself a piece of art rescued from demolition.",
            "StoryHunt's DUMBO art walk turns the neighborhood into a scavenger hunt for hidden creativity. Your phone sends you to murals, installations, and gallery spaces that most visitors miss — delivering clues that connect each artwork to the neighborhood's industrial past. You'll decode visual symbols in the street art, investigate the histories embedded in warehouse walls, and discover art spaces that don't advertise their existence. A two-to-three-hour exploration of Brooklyn's most visually dense neighborhood.",
        ],
        "links": [("dumbo.html", "Decode DUMBO"), ("bushwick.html", "Decode Bushwick"), ("hidden-places-nyc.html", "Hidden Places in NYC")],
    },
}


def build_content_section(data):
    """Build the neighborhood content HTML section."""
    links_html = "\n                ".join(
        f'<a href="{slug}">{label}</a>' for slug, label in data["links"]
    )
    paragraphs_html = "\n            ".join(
        f"<p>{p}</p>" for p in data["paragraphs"]
    )
    return f"""
    <!-- Neighborhood Content -->
    <section class="neighborhood-content" id="about">
        <div class="container smaller">
            <div class="content-block reveal-text">
                <h2 class="content-title">{data["title"]}</h2>
                {paragraphs_html}
                <div class="related-hunts mono">
                    <span>RELATED_HUNTS:</span>
                    {links_html}
                </div>
            </div>
        </div>
    </section>
"""


def process_file(filepath, filename, data):
    """Process a single HTML file with SEO upgrades."""
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    changes = []

    # 1. Replace the generic subtitle
    subtitle_match = re.search(
        r'(<p class="subtitle reveal-text">)(.*?)(</p>)', html, re.DOTALL
    )
    if subtitle_match:
        old = subtitle_match.group(0)
        new = f'{subtitle_match.group(1)}{data["subtitle"]}{subtitle_match.group(3)}'
        if old != new:
            html = html.replace(old, new, 1)
            changes.append("subtitle")

    # 2. Add content section before manifesto
    content_section = build_content_section(data)
    manifesto_marker = '<section class="manifesto"'
    if manifesto_marker in html and "neighborhood-content" not in html:
        html = html.replace(manifesto_marker, content_section + "\n        " + manifesto_marker, 1)
        changes.append("content section")

    # 3. Add canonical URL after <meta charset="UTF-8">
    canonical_tag = f'<link rel="canonical" href="https://storyhunt.city/explore/{filename}">'
    if "canonical" not in html:
        charset_marker = '<meta charset="UTF-8">'
        if charset_marker in html:
            html = html.replace(
                charset_marker,
                charset_marker + "\n    " + canonical_tag,
                1,
            )
            changes.append("canonical URL")

    # 4. Fix OG URL from vercel to storyhunt.city
    if "storyhuntweb.vercel.app" in html:
        html = html.replace("storyhuntweb.vercel.app", "storyhunt.city")
        changes.append("OG URL fix")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    return changes


def main():
    if not os.path.isdir(EXPLORE_DIR):
        print(f"ERROR: Directory not found: {EXPLORE_DIR}")
        sys.exit(1)

    print("=" * 60)
    print("StoryHunt SEO Content Upgrade")
    print(f"Processing {len(PAGES)} pages in {EXPLORE_DIR}")
    print("=" * 60)

    processed = 0
    skipped = []
    errors = []

    for filename, data in PAGES.items():
        filepath = os.path.join(EXPLORE_DIR, filename)
        if not os.path.isfile(filepath):
            skipped.append(filename)
            print(f"  SKIP  {filename} — file not found")
            continue

        try:
            changes = process_file(filepath, filename, data)
            processed += 1
            changes_str = ", ".join(changes) if changes else "no changes needed"
            print(f"  OK    {filename} — {changes_str}")
        except Exception as e:
            errors.append((filename, str(e)))
            print(f"  ERR   {filename} — {e}")

    print("=" * 60)
    print(f"Processed: {processed}/{len(PAGES)}")
    if skipped:
        print(f"Skipped (file not found): {len(skipped)}")
        for s in skipped:
            print(f"  - {s}")
    if errors:
        print(f"Errors: {len(errors)}")
        for fn, err in errors:
            print(f"  - {fn}: {err}")
    print("=" * 60)
    print("Done.")


if __name__ == "__main__":
    main()
