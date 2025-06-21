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
]


with open(email_path, "w", encoding="utf-8") as f:
    print("Saving email data")
    json.dump(emails, f, ensure_ascii=False, indent=4)
