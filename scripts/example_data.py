import json
from pyprojroot import here

email_path = here("data/example_emails.json")

# manual copy and paste from emails
emails = [
    {
        "sender": "alice@example.com",
        "date": "2025-06-08T09:15:00",
        "subject": "Meeting Reminder",
        "body": "Just a reminder about our meeting at 10am.",
        "headers": {
            "X-Email-Translator-Processed": "true",  # triggers loop check
            "X-Loop": "email-translator-1234",
            "X-Forwarded-By-EmailTranslator": "v1.0",
        },
    },
    {
        "sender": "alice@example.com",
        "date": "2025-06-08T09:15:00",
        "subject": "Meeting Reminder",
        "body": "Just a reminder about our meeting at 10am.",
    },
    {
        "sender": "secretaria@escolinhadocampo.com",
        "date": "2025-05-08T09:22:00",
        "subject": "Comprovativo de pagamento",
        "body": "Boa tarde papás,"
        "Agora que bastantes papás já efetuaram os pagamentos e que felizmente, a maior parte nos fez chegar uma cópia por email do respetivo comprovativo, percebemos que, sem os mesmos, é muito complicado alocar corretamente os pagamentos, porque muitos são de igual valor."
        "Assim, pedimos o favor de nos fazerem chegar cópia do mesmo, para o novo email da secretaria, caso ainda não o tenham feito."
        "Grata pela compreensão."
        "Com os melhores cumprimentos,"
        "Daniela Alves",
    },
    {
        "sender": "luism@escolinhadocampo.com",
        "date": "2025-05-01T02:15:00",
        "subject": "A praia com a Escolinha está quase a chegar!!",
        "body": """Boa tarde, papás!

                Este ano, toda a Escolinha vai à praia entre os dias 23 de junho e 4 de julho – um momento muito esperado por todos: crianças e equipa!

                As diferentes salas, da creche ao 1.º ciclo, vão rumar à nossa querida Figueirinha, com a alegria e a energia de sempre.

                Valor da atividade: 200€ (a debitar na mensalidade de julho).

                Inscrição: junto da equipa da sala, até dia 6 de junho.

                ✨ Uma novidade especial – Bata Azul

                Este ano, as professoras da Bata Azul também vão à praia com os seus alunos.

                Não porque fosse preciso mais apoio, mas porque acreditamos que também elas devem ter a oportunidade de estar com as crianças num momento leve e descontraído.

                Aquelas que, ao longo do ano, estão mais próximas das tarefas pedagógicas e das responsabilidades formais, vão agora partilhar um espaço diferente – onde a aprendizagem acontece de forma espontânea, com o mar por perto e a areia nos pés.

                Porque a educação não faz pausas. Educamos no refeitório, no recreio e, claro, também na praia.

                Cada vivência é uma oportunidade: para aprender a respeitar o outro, para valorizar as regras comuns, para descobrir o lado bom das coisas simples. E para cultivar o respeito e a gratidão pela natureza – essa professora silenciosa que tanto nos dá.

                Em anexo, enviaremos a organização prática, com os horários e o que cada criança deverá trazer.

                Até já!

                Margarida del Barco""",
    },
    {
        "sender": "phil@cinesociety.pt",
        "date": "2025-06-24T09:15:00",
        "subject": "Is your calendar ready for Lisbon’s wildest week?",
        "body": """
Society Lisboa

Curating the Best Events in Lisbon

Leia em Português.

Hello People Of Lisbon! 👋

Summer is here, and Lisbon’s event calendar is as diverse as ever. This week, catch open-air cinema with Cine Society, family fun at Festival Panda, live music from global stars, and hands-on workshops for all ages. Whether you’re after film, food, or fresh cultural experiences, there’s something for everyone in the city’s vibrant lineup.
 
FEATURED EVENT

🇯🇵 Japan Festival 2025 @ Vasco da Gama Garden, on June 28th, 2025.

This year’s Festa do Japão centers on the symbolism of koi carps, recreating the vibrant atmosphere of a Japanese summer matsuri.

Experience martial arts demonstrations, traditional dance, and workshops including Japanese calligraphy and origami, immersing yourself in the rich culture of Japan. Don’t miss this unique cultural celebration in Lisbon’s beautiful Jardim Vasco da Gama. Check the Website
WHERE WE’RE GOING THIS WEEK

➡️ Cine Society @ Doca da Marinha and Carmo Rooftop, from June 25th to July 1st, returns with open-air screenings of classics and cult favorites, including 10 Things I Hate About You, The Grand Budapest Hotel, and Black Swan. Get Tickets

➡️ Imagine Dragons @ Luz Stadium, on June 26th, brings the Grammy-winning band’s LOOM World Tour to Lisbon for their first major European stadium tour, celebrating their acclaimed new album. Get Tickets

➡️ Summer Garden @ Calouste Gulbenkian Foundation, from June 21st to July 6th, celebrates Lisbon’s cultural diversity with concerts, DJ sets, dance, cinema, talks, and free exhibitions, curated by leading local artists. Check the Website

➡️ Lisbon Loras Meetup powered by Runway @ RNA Studio, on June 26th, kicks off a new AI community series blending tech, creativity, and culture. Enjoy a special screening of GEN:48 award-winning shorts, explore AI-generated art, and join real conversations about the intersection of video, tech, and creativity. Get Tickets
TOP DJ SETS THIS WEEK

🎧 Riktus With Santøs (NL), Salvyan (BR) & More @ Ministerium Club, on June 26th, brings the summer opening with Dutch sensation Santøs, Brazilian debut Salvyan, and local favorites for a fearless night of pure techno. Get Tickets

🎧 Contratempos Clubbing w/ DJ Patife (BR) @ Duro De Matar, on June 28th, features Brazil’s drum’n’bass legend DJ Patife alongside a powerhouse crew of local and international talent for a night of jungle rhythms. Get Tickets

🎧 Wild Groove @ Micro Burger & Music, on June 28th, launches House Four House with DJ Rohtah and VTD mixing Afro House, tech funk, and global beats for a bold, spicy, and irresistible dancefloor experience. Get Tickets
CULTURAL PICKS

🎭 Summer Garden @ Calouste Gulbenkian Foundation, from June 21st to July 6th, celebrates Lisbon’s cultural diversity with concerts, DJ sets, dance, cinema, talks, and free exhibitions, curated by leading local artists. Check the Website

🎭 After Hours Market @ COMOBÅ, on July 26th, hosts a night market with curated vintage, indie brands, tarot readings, tooth gems, and live DJ sets—perfect for discovering one-of-a-kind finds and creative connections. Get Tickets

🎭 InArt – Community Arts Festival @ Bairro Theater, from June 25th to 28th, returns with shows, films, workshops, and discussions highlighting the power of community art and diverse creative voices. Check the Website

🎭 ArtBeat Fair @ National Cordage, on June 28th and 29th, brings artists and the public together for a vibrant showcase of painting, sculpture, photography, dance, and music in a dynamic, sensory celebration. Check the Website
LIVE MUSIC

🎶 Jardins do Marquês Festival @ Marquês Gardens – Oeiras, from June 28th until July 9th, offers nights of open-air concerts and comedy in a stunning setting and iconic performers. Check the Website

🎶 Imagine Dragons @ Luz Stadium, on June 26th, brings the Grammy-winning band’s LOOM World Tour to Lisbon for their first major European stadium tour, celebrating their acclaimed new album. Get Tickets

🎶 LISB-ON @ Keil do Amaral Garden, from June 27th to 29th, returns with a magical atmosphere and an international lineup of disco, house, and techno, all focused on sustainability and Lisbon’s urban culture. Check the Website

🎶 Evil Live @ Restelo Stadium, from June 27th to 29th, hosts its first open-air edition with three days of heavy music, featuring Slipknot, Judas Priest, Korn, and more icons of the metal scene. Get Tickets

🎶 The Lemon Twigs @ LAV – Lisboa ao Vivo, on June 25th, brings the New York duo’s electrifying mix of rock, nostalgia, and pure energy to Lisbon, with support from Gorjão. Get Tickets
FOOD & DRINKS

🍷 Vegetarian Summer WORKSP with Chef Cátia Roque @ Auchan Academy | Alfragide Store, on June 29th, invites all ages to discover delicious plant-based cooking with Chef Cátia Roque, focusing on macrobiotic and functional cuisine in a fun, hands-on workshop. Get Tickets
BUSINESS & INNOVATION

💼 Idea Night 2025 @ São Luiz Theater, on June 25th, brings together writers, scientists, artists, and philosophers for six hours of debates, performances, and workshops exploring collective action and universal rights. Check the Website

💼 CxSummit 2025 @ Nova School of Business and Economics, on June 26th, explores AI-driven personalization and omnichannel strategies with keynote speakers and industry panels across technology, hospitality, healthcare, and customer service. Get Tickets

💼 Google Cloud Day '25 Lisbon @ Beato Convent, on June 26th, offers Portugal's largest Google Cloud event with product announcements, live demos, success stories, and interactive talks with industry leaders. Check the Website
CINEMA

🎬 48 Hour Film Project Lisboa 2025 @ São Jorge Cinema , on June 28th, challenges filmmakers to create short films in just 48 hours. Catch the premiere of 44 brand-new shorts and vote for your favorite at this high-energy screening night. Get Tickets

🎬 Cine Society @ Doca da Marinha and Carmo Rooftop, from June 25th to July 1st, returns with open-air screenings of classics and cult favorites, including 10 Things I Hate About You, The Grand Budapest Hotel, and Black Swan. Get Tickets
FAMILY-FRIENDLY

🧸 Long Summer Days @ LU.CA – Teatro Luís de Camões, on June 28th and 29th, brings magical adventures for kids with six charming short films—perfect for families to celebrate summer with humor and imagination. Check the Website

🧸 Panda Festival 2025 @ Poetas Park, from June 27th to 29th, returns with three days of music, shows, and playful activities for kids ages 3–8, featuring favorite characters and a superpowers theme. Get Tickets

🧸 The Circus of Dreams @ Estoril Casino, on June 28th, presents a dance spectacle where dreams and reality blend in a magical circus world, filled with poetic clowns, gentle monsters, and enchanting illusions. Get Tickets
        """,
    },
]


with open(email_path, "w", encoding="utf-8") as f:
    print("Saving email data")
    json.dump(emails, f, ensure_ascii=False, indent=4)
