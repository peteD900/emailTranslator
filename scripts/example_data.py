import json
import os
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
        "sender": "secretaria@aquasetubal.pt",
        "date": "2025-06-01T09:15:00",
        "subject": "Envio fatura e recibo - inscrição",
        "body": "Estimado Pete, boa tarde"
        "Junto remetemos  a nossa fatura e recibo, referente  a inscrição do Ruby Mauldin.  "
        "Com os melhores cumprimentos, ao dispor",
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
        "sender": "climatopservicos@gmail.com",
        "date": "2025-06-22T02:15:00",
        "subject": "Re: AC installation - orçamento",
        "body": """

Boa tarde Sr Marcelo,
Obrigado novamente pelas citações. Temos interesse em fazê-lo com as unidades Mitsubishi, mas temos algumas questões:

1) Todas as unidadesno orçamento têm de ter 9000 BTU? Por exemplo, o quarto da nossa filha é muito mais pequeno que os outros dois. Algo como 5000 seria adequado?
2) Pode enviar-nos o número do modelo das unidades Mitsubishi que procurava? Têm Wi-Fi? Não estamos interessados no Wi-Fi, mas estamos curiosos para saber se o que está incluído no pacote inclui isso.
3) Sei que disse que o multi-split pode ser mais caro, mas poderia dar-nos uma ideia do pacote Mitsubishi se, por exemplo, utilizássemos um único compressor para as duas unidades que ficariam no telhado da varanda da frente?

Obrigada e cumprimentos 
Katie and Pete

On Fri, Jun 6, 2025, 9:03 PM Clima Top <climatopservicos@gmail.com> wrote:

    Dear Customer,

    Please find below the description of the services and materials included in the proposal:

        Air Conditioning System: Mono Split Mitsubishi 9,000 BTUs

        Installation Service: Complete installation of the indoor and outdoor units

        Pressurization: Nitrogen charge for leak testing and line pressurization

        Access Equipment: Rental, assembly, and disassembly of scaffolding required for the execution of the work

    All services will be carried out in accordance with current technical and environmental regulations.

    We remain at your full disposal for any further clarification.

    Best regards,
    Marcelo Almeida
    Climatop
    📧 climatopservicos.pt
    📷 Instagram: @climatopservicos

    	Sem vírus.www.avast.com

    Clima Top <climatopservicos@gmail.com> escreveu (sexta, 6/06/2025 à(s) 04:08):

        Bom dia Sra. Katie Mauldin!

        O técnico está à caminho. 

        Com os melhores cumprimentos,

        Gerente Administrativa
        Roziane Silva 
        Climatop

        Em qui., 5 de jun. de 2025 às 16:39, Clima Top <climatopservicos@gmail.com> escreveu:

            Obrigada por sua confirmação.


            Atentamente,
            Roziane Silva

            Katie Mauldin <mauldin.katie@gmail.com> escreveu (quinta, 5/06/2025 à(s) 13:22):

                Ok. Amanhã ás 9h está bom.

                Katie 

                On Thu, Jun 5, 2025, 10:48 AM Clima Top <climatopservicos@gmail.com> wrote:

                    Amanhã dia 06 às 09 horas.


                    Atenciosamente,
                    Roziane Silva 

                    Katie Mauldin <mauldin.katie@gmail.com> escreveu em qui., 5/06/2025 às 10:45 :

                        Bom dia,
                        Agora não é possìvel. Preciso de ir para Lisboa. Podemos agendar um outro dia?

                        Cumprimentos 
                        Katie 


                        On Thu, Jun 5, 2025, 10:44 AM Clima Top <climatopservicos@gmail.com> wrote:

                            Sra. Katie, bom dia.

                            Tivemos um imprevisto agora pela manhã, por isso o técnico não foi na hora marcada. Ele pode ainda ir fazer a visita mesmo em atraso. Nos confirme.




                            Com melhores cumprimentos,
                            Roziane Silva 
                            Adm. Climatop 

                            Clima Top <climatopservicos@gmail.com> escreveu em ter., 3/06/2025 às 11:12 :

                                Certo, obrigada.



                                Atenciosamnete,
                                Roziane Silva

                                Katie Mauldin <mauldin.katie@gmail.com> escreveu (terça, 3/06/2025 à(s) 10:54):

                                    Sra Roziane bom dia,
                                    Sim. Pode agendar a visita 5 Junho ás 10h. 

                                    A morada é: 
                                    Rua Joao Antonio Moinho 70 
                                    2950-656 Cabanas 

                                    A campainha não está ligada. É necessario ligar quanfo está na casa.

                                    Cumprimentos 
                                    Katie

                                    On Tue, Jun 3, 2025, 10:50 AM Clima Top <climatopservicos@gmail.com> wrote:

                                        Sra. Kate bom dia,

                                        Podemos agendar a visita para dia 05 de junho às 10 horas. Se sim, nos envie seu endereço.
                                        A visita é sem custo.




                                        Atencciosamente,
                                        Roziane Silva
                                        Adm. Climatop


                                        Katie Mauldin <mauldin.katie@gmail.com> escreveu (segunda, 2/06/2025 à(s) 17:32):

                                            Boa tarde Sra Roziane,
                                            O meu telemovel: 964693961.

                                            Cumprimentos 
                                            Katie 


                                            On Mon, Jun 2, 2025, 2:55 PM Clima Top <climatopservicos@gmail.com> wrote:

                                                Sra. Kate boa tarde,

                                                Por favor nos envie seu contato para que possamos agendar uma visita ao local.


                                                Atenciosamente,
                                                Roziane Silva

                                                Katie Mauldin <mauldin.katie@gmail.com> escreveu (sexta, 30/05/2025 à(s) 20:28):

                                                    Boa tarde,
                                                    Tenho interesse em obter um orçamento e falar com alguém sobre a instalação de alguns aparelhos de ar condicionado em nossa casa. Vivemos em Cabanas. Por favor, informe-me qual a melhor forma de proceder e se necessita de mais informações. E peço desculpe....o meu portugues não é muito bom.

                                                    Cumprimentos 
                                                    Katie
                                                    """,
    },
    {
        "sender": "peter.downs@live.co.uk",
        "date": "2025-06-08T09:15:00",
        "subject": "Teatro de Primavera - Creche",
        "body": """
-------- Forwarded Message --------
Subject: 	Mês de Maio - Creche
Date: 	Wed, 7 May 2025 17:49:48 +0100
From: 	Luis Mendão <luism@escolinhadocampo.com>
To: 	Luis Mendão <luism@escolinhadocampo.com>


Queridas Famílias,

Depois de uns meses de março e abril repletos de cores, flores, borboletas e muita energia de primavera - que tanto nos inspira à renovação na Mãe natureza e nos volta a acordar os sentidos -, chegamos ao mês dos Meios de Transportes e da Segurança Rodoviária e da Língua Portuguesa.

Já há muitos anos que escolhemos este mês para explorarmos e acelerarmos por este tema que eles tanto gostam e que atravessa de forma diferente todas as salas da nossa Escolinha. Este ano, juntámos o tema da Língua portuguesa, onde a professora Carina com a ajuda de toda a equipa desenvolverá várias iniciativas e momentos especiais de que irão tendo conhecimento.

Estes temas serão o fio condutor das nossas vivências ao longo do mês, com propostas ajustadas a cada faixa etária, sempre através da exploração, da brincadeira e da descoberta. Queremos ajudar as nossas crianças a reconhecer os diferentes meios de transporte, a compreender para que servem e como podemos circular com mais segurança no nosso dia a dia — seja a pé, de carro, de autocarro, barco, comboio, ou até de bicicleta!

Cada sala terá a sua própria saída ou vivência de campo, especialmente pensada pela equipa educativa, em articulação com os interesses e o desenvolvimento do grupo. Iremos partilhar, mais abaixo, as informações específicas de cada sala.

. Creche

    - Atelier Rita Rovisco, no Prior Velho:

        (Cebolinhas e Batatinhas no dia 26/5 + Bolotinhas no dia 27/5)

         Têm que estar na Escolinha até às 8:30 e trazer equipamento da Escolinha numa mochila, pois deverão levar uma roupa para explorar e sujar sem limites. Voltamos depois de almoço para uma bela sesta!

  - GNR vem à Escolinha:

     (Cebolinhas e Batatinhas + Bolotinhas no dia 20/5)

      Às atividades terão início às 9:30 e haverão circuitos, jogos e diferentes veículos para brincar e explorar.

      Combinem com a equipa da sala quem traz triciclo, trotinete,… e as proteções de segurança.

     Quem pretender inscrever-se nestas atividades práticas dentro e fora da escolinha, deverá fazê-lo junto à equipa da sala. O valor é de 30,00€.

Uma excelente semana para todos e andem a pé!☺️

Margarida del Barco
        """,
    },
]


with open(email_path, "w", encoding="utf-8") as f:
    print("Saving email data")
    json.dump(emails, f, ensure_ascii=False, indent=4)
