import requests
from datetime import datetime
from flask import Flask, render_template, request, Response, url_for
from weasyprint import HTML
from io import BytesIO

app = Flask(__name__)

pecados = {
    "1. Amar a Deus sobre todas as coisas": [
        "Negligenciei minha oração diária",
        "Tive dúvidas sobre a fé e critiquei os ensinamentos da Igreja",
        "Senti desânimo espiritual e me revoltei contra Deus",
        "Frequentei cultos ou práticas supersticiosas (ex: cartomantes, horóscopos)",
        "Busquei minha própria glória em vez da vontade de Deus",
        "Fui orgulhoso, vaidoso ou apegado a elogios",
        "Apeguei-me excessivamente ao dinheiro e aos bens materiais",
        "Fui impaciente e pouco tolerante com os outros",
        "Fui indiferente diante do sofrimento alheio",
        "Faltou-me empatia e amor ao próximo",
        "Levei outros ao pecado com meus conselhos, atitudes ou exemplos",
        "Ignorei oportunidades de praticar caridade"
    ],
    "2. Não tomar o nome de Deus em vão": [
        "Usei o nome de Deus ou dos santos de forma desrespeitosa",
        "Ridicularizei símbolos da fé ou religiosos",
        "Fiz promessas sem intenção de cumprir",
        "Fiz juramentos falsos ou desnecessários",
        "Permiti ou ri quando outros zombaram da fé",
        "Usei expressões religiosas com banalidade ou em vão"
    ],
    "3. Guardar domingos e festas de guarda": [
        "Faltei à missa dominical ou em dias santos sem necessidade grave",
        "Cheguei intencionalmente atrasado à missa ou saí antes da bênção final",
        "Comunguei estando em pecado mortal",
        "Deixei de me confessar ao menos uma vez ao ano",
        "Não jejuei ou não fiz abstinência quando mandado pela Igreja",
        "Negligenciei a ajuda material à Igreja",
        "Fui à missa por obrigação, sem esforço de viver a fé no dia a dia"
    ],
    "4. Honrar pai e mãe": [
        "Desobedeci e faltei com respeito aos meus pais ou superiores",
        "Negligenciei os cuidados com meus pais idosos ou doentes",
        "Maltratei meu cônjuge com palavras ou atitudes",
        "Dei mau exemplo aos meus filhos",
        "Permiti influências negativas sobre meus filhos (TV, internet, amizades)",
        "Fui negligente na formação religiosa dos meus filhos",
        "Deixei de corrigir meus filhos por comodismo",
        "Fui ingrato com meus pais ou avós"
    ],
    "5. Não matar": [
        "Alimentei ódio, rancor, inimizade ou desejo de vingança",
        "Recusei-me a perdoar",
        "Desejei a morte ou o mal a alguém (ou a mim mesmo)",
        "Apoiei ou pratiquei aborto, eutanásia ou outras práticas semelhantes",
        "Fui descuidado com minha saúde (excesso de comida, drogas, bebida, sedentarismo)",
        "Assumi riscos desnecessários à minha vida (direção imprudente, vícios)",
        "Dei escândalo ou mau exemplo",
        "Proferi palavrões ou palavras agressivas contra os outros",
        "Feri emocionalmente alguém com minhas palavras ou atitudes",
        "Fui violento, mesmo verbalmente, com pessoas próximas"
    ],
    "6. Não pecar contra a castidade": [
        "Consenti em pensamentos ou desejos impuros",
        "Me masturbei, assisti pornografia ou tive relações sexuais fora do casamento",
        "Fui infiel emocionalmente ou fisicamente",
        "Tive liberdades excessivas no namoro",
        "Usei roupas provocativas com má intenção",
        "Participei de conversas ou fiz piadas imorais",
        "Consumi conteúdo sexualizado (TV, filmes, redes sociais)",
        "Mantive amizades que me levaram ao pecado",
        "Fiz comentários maliciosos sobre o corpo de outras pessoas",
        "Alimentei fantasias sexuais intencionalmente"
    ],
    "7. Não roubar": [
        "Roubei ou fui desonesto em contratos ou negócios",
        "Me apropriei de bens ou dinheiro indevidamente",
        "Deixei de pagar dívidas justas ou salários devidos",
        "Desperdicei tempo no trabalho ou trabalhei com negligência",
        "Fui viciado em jogos de azar",
        "Vivi acima dos meus meios",
        "Fui injusto ao cobrar ou receber valores excessivos",
        "Usei benefícios ou ajudas indevidamente"
    ],
    "8. Não levantar falso testemunho": [
        "Menti habitualmente, mesmo sem prejudicar diretamente",
        "Caluniei, difamei ou exagerei defeitos dos outros",
        "Ouvi ou espalhei boatos",
        "Julguei mal ou condenei injustamente alguém",
        "Causei divisão entre pessoas por fofoca",
        "Não reparei a má reputação causada por mim",
        "Fui hipócrita ou dissimulado para parecer melhor"
    ],
    "9. Não desejar a mulher do próximo": [
        "Alimentei desejos impuros por pessoas casadas ou consagradas",
        "Tive fantasias ou intenções de infidelidade",
        "Assediei verbal ou fisicamente",
        "Flertei com pessoas comprometidas",
        "Tive curiosidade indevida sobre a intimidade de outras pessoas",
        "Usei o olhar de maneira impura ou desrespeitosa"
    ],
    "10. Não cobiçar as coisas alheias": [
        "Invejei os bens, o sucesso ou os talentos dos outros",
        "Desejei tomar ou imitar aquilo que pertence a outros",
        "Fiquei descontente com a minha vida por causa de comparações",
        "Fui ambicioso em excesso, sem gratidão pelo que tenho",
        "Desejei viver a vida dos outros em vez de valorizar a minha"
    ],
    "Mandamentos da Igreja": [
        "Faltei à Missa em festas de guarda",
        "Não me confessei ao menos uma vez por ano",
        "Não comunguei na Páscoa",
        "Comunguei em pecado grave",
        "Não guardei jejum e abstinência nos tempos prescritos",
        "Não ajudei a Igreja materialmente",
        "Desprezei os sacramentos por comodismo ou frieza espiritual"
    ],
    "Pecados relacionados ao casamento e à família": [
        "Fui negligente com meu cônjuge (no diálogo, carinho ou atenção)",
        "Fui violento física ou verbalmente dentro do lar",
        "Desrespeitei meu cônjuge",
        "Guardei mágoas e não perdoei no matrimônio",
        "Priorizei trabalho ou lazer em detrimento da família",
        "Recusei-me a ter filhos sem justa causa",
        "Não dei testemunho cristão dentro do lar",
        "Fui indiferente à vida familiar ou às necessidades dos meus",
        "Usei palavras ofensivas ou humilhantes com meus familiares"
    ],
    "Pecados espirituais e morais": [
        "Fui preguiçoso espiritualmente (não busquei crescer na fé)",
        "Me desinteressei pelas coisas de Deus",
        "Fui indiferente no zelo apostólico (não evangelizei, nem ajudei outros na fé)",
        "Fui conivente com o pecado, meu ou alheio",
        "Busquei o sucesso pessoal acima da vontade divina",
        "Agi por egoísmo, pensando apenas em mim",
        "Fui omisso diante de injustiças ou sofrimentos ao meu redor"
    ],
        "Pecados veniais (faltas leves que enfraquecem minha alma, mas não rompem a amizade com Deus)": [
        "Falei palavras impacientes, com leve irritação ou impolidez",
        "Fui negligente em atos de caridade com os mais próximos",
        "Fiz piadas ou comentários inapropriados, sem intenção grave",
        "Julguei os outros interiormente, mesmo sem espalhar críticas",
        "Tive distrações voluntárias durante a oração, sem esforço para me recolher",
        "Faltei com pequenas responsabilidades no trabalho ou estudo por descuido",
        "Deixei de ajudar alguém por comodismo, ainda que pudesse fazê-lo",
        "Busquei meu conforto ou prazer em coisas pequenas, sem moderação",
        "Fui impaciente com pessoas mais lentas ou com ideias diferentes das minhas",
        "Usei meu tempo de forma egoísta, deixando de servir mais ao próximo"
    ],
    
    "Pecados capitais (raízes do pecado que geram muitas outras faltas)": [
        "Cedi à soberba, agindo com orgulho ou querendo ser superior aos outros",
        "Fui avarento, apegado ao dinheiro ou a bens materiais, sem generosidade",
        "Entreguei-me à luxúria, buscando prazeres impuros nos pensamentos, olhares ou ações",
        "Fui invejoso, entristecendo-me com o bem ou sucesso alheio",
        "Alimentei a gula, comendo ou bebendo além do necessário por puro prazer",
        "Fui irado, permitindo que a raiva dominasse minhas palavras ou atitudes",
        "Fui preguiçoso, negligente no cumprimento dos meus deveres espirituais ou materiais"
    ]

}


# ✅ Rota principal
@app.route("/", methods=["GET", "POST"])
def index():
    resultado = {}
    html_conteudo = ""
    if request.method == "POST":
        for mandamento, lista in pecados.items():
            indices = request.form.getlist(mandamento)
            selecionados = [lista[int(i)] for i in indices if i.isdigit() and int(i) < len(lista)]
            if selecionados:
                resultado[mandamento] = selecionados

        custom = request.form.get("custom", "").strip()
        if custom:
            resultado.setdefault("Outros pecados digitados", []).append(custom)

        html_conteudo = render_template("pdf_template.html", resultado=resultado)

    return render_template("index.html", pecados=pecados, resultado=resultado, html_conteudo=html_conteudo)

# ✅ Rota de download do PDF
@app.route("/download", methods=["POST"])
def download():
    html_renderizado = request.form.get("html_conteudo", "")
    if not html_renderizado:
        return "Conteúdo vazio para gerar PDF", 400

    pdf_io = BytesIO()
    html = HTML(string=html_renderizado, base_url=request.base_url)
    html.write_pdf(target=pdf_io)
    pdf_io.seek(0)

    return Response(pdf_io.read(),
                    mimetype="application/pdf",
                    headers={"Content-Disposition": "attachment;filename=meus_pecados.pdf"})

# ✅ Rota de orações
@app.route("/oracoes")
def oracoes():
    oracoes_lista = [
        {
            "id": 1,
            "titulo": "Oração do Arrependimento",
            "texto": (
                "Meu Jesus, por serdes tão bom, e por me amardes tanto, vos agradeço por me terdes esperado até agora e não terdes permitido que eu morresse em pecado. "
                "Peço-vos, por vossa paixão e morte na cruz, perdoai-me todos os meus pecados e fazei-me verdadeiramente penitente..."
            ),
            "descricao": "Para momentos de reflexão e conversão interior."
        },
        {
            "id": 2,
            "titulo": "Confissão Geral",
            "texto": (
                "Senhor meu Deus, reconheço diante de Vós que pequei muitas vezes por pensamentos, palavras, atos e omissões. "
                "Arrependo-me sinceramente de todas as minhas faltas e ofensas, especialmente daquelas que mais feriram o vosso amor. "
                "Com humildade, suplico a vossa misericórdia e, como o filho pródigo, digo: Pai, pequei contra o Céu e contra Vós. "
                "Não sou digno de ser chamado vosso filho. Tende piedade de mim, Senhor. Amém."
            ),
            "descricao": "Ideal para preparação antes da confissão sacramental."
        },
        {
            "id": 3,
            "titulo": "Miserere Mei Deus",
            "texto": (
                "Tende piedade de mim, ó Deus, segundo a vossa misericórdia; "
                "segundo a grandeza da vossa compaixão, apagai a minha culpa. "
                "Lavai-me totalmente da minha iniquidade, e purificai-me do meu pecado. "
                "Criai em mim, ó Deus, um coração puro e renovai em meu peito um espírito firme."
            ),
            "descricao": "Um dos salmos penitenciais mais conhecidos da tradição cristã."
        },
        {
            "id": 4,
            "titulo": "Do Profundo",
            "texto": (
                "Das profundezas clamo a Vós, Senhor. Senhor, escutai a minha voz! "
                "Estejam atentos os vossos ouvidos às súplicas da minha prece. "
                "Se levardes em conta nossas faltas, Senhor, quem poderá subsistir? "
                "Mas em Vós se encontra o perdão, e por isso Vos teme com reverência."
            ),
            "descricao": "Uma poderosa expressão de esperança na misericórdia divina."
        },
        {
            "id": 5,
            "titulo": "Salmo 6",
            "texto": (
                "Senhor, não me repreendais em vossa ira, nem me castigueis no vosso furor. "
                "Tende piedade de mim, Senhor, pois desfaleço; curai-me, Senhor, pois meus ossos tremem. "
                "A minha alma está profundamente perturbada... Salvai-me por causa da vossa misericórdia!"
            ),
            "descricao": "Suplica o perdão e a cura espiritual e física."
        },
        {
            "id": 6,
            "titulo": "Acto de Contrição",
            "texto": (
                "Meu Deus, arrependo-me de todo o coração de Vos ter ofendido, "
                "porque sois infinitamente bom e digno de ser amado sobre todas as coisas. "
                "Proponho firmemente, com o auxílio da vossa graça, emendar-me e evitar as ocasiões de pecado. "
                "Senhor, pela paixão de Jesus Cristo, tende piedade de mim. Amém."
            ),
            "descricao": "Expressa arrependimento sincero e desejo de mudança."
        },
        {
            "id": 7,
            "titulo": "Oração à Virgem Maria",
            "texto": (
                "Ó Maria Santíssima, Mãe de Deus e minha Mãe, refugio-me sob a vossa proteção maternal. "
                "Vós que sois a Medianeira de todas as graças, intercedei por mim junto a vosso Filho Jesus. "
                "Alcançai-me a graça do verdadeiro arrependimento, uma boa confissão e a perseverança no bem. "
                "Acompanhai-me em todos os momentos da vida, sobretudo na hora da morte. Amém."
            ),
            "descricao": "Peça a intercessão de Nossa Senhora após o exame de consciência."
        }
    ]
    return render_template("oracoes.html", oracoes=oracoes_lista)

# ✅ Rota da Liturgia do Dia
@app.route("/liturgia")
def liturgia():
    try:
        response = requests.get("https://liturgia.up.railway.app/")
        response.raise_for_status()
        dados_api = response.json()

        def extrair_texto(obj):
            if isinstance(obj, dict):
                return {
                    "titulo": obj.get("titulo", ""),
                    "texto": obj.get("texto", "Texto não disponível"),
                    "referencia": obj.get("referencia", "Sem referência"),
                    "refrao": obj.get("refrao", "")  # agora extrai o refrão também
                }
            return {
                "titulo": "",
                "texto": obj or "Texto não disponível",
                "referencia": "Sem referência",
                "refrao": ""
            }

        # Corrige a data para uso na API do Vaticano (Santo do Dia)
        data_api = dados_api.get("data", datetime.now().strftime("%d/%m/%Y"))
        try:
            data_iso = datetime.strptime(data_api, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            data_iso = datetime.now().strftime("%Y-%m-%d")

        dados = {
            "data": dados_api.get("data"),
            "titulo": dados_api.get("liturgia", "Liturgia do Dia"),
            "cor": dados_api.get("cor", "Cor litúrgica não informada"),
            "dia": dados_api.get("dia", ""),
            "oferendas": dados_api.get("oferendas", ""),
            "comunhao": dados_api.get("comunhao", ""),
            "segundaLeitura": dados_api.get("segundaLeitura", ""),
            "antifonas": dados_api.get("antifonas", {}),
            "primeiraLeitura": extrair_texto(dados_api.get("primeiraLeitura")),
            "salmo": extrair_texto(dados_api.get("salmo")),
            "evangelho": extrair_texto(dados_api.get("evangelho")),
        }

        return render_template("liturgia.html", dados=dados)

    except Exception as e:
        return f"Erro ao carregar a liturgia: {e}", 500

@app.route("/terco")
def terco():
    mistérios = {
        "Gozosos": [
            "1. A Anunciação do Anjo a Maria",
            "2. A Visitação de Maria a Isabel",
            "3. O Nascimento de Jesus em Belém",
            "4. A Apresentação do Menino Jesus no Templo",
            "5. O Encontro do Menino Jesus no Templo"
        ],
        "Dolorosos": [
            "1. Jesus agoniza no Horto",
            "2. Jesus é açoitado",
            "3. Jesus é coroado de espinhos",
            "4. Jesus carrega a Cruz",
            "5. Jesus é crucificado"
        ],
        "Gloriosos": [
            "1. Ressurreição de Jesus",
            "2. Ascensão de Jesus",
            "3. Descida do Espírito Santo",
            "4. Assunção de Maria",
            "5. Coroação de Maria"
        ],
        "Luminosos": [
            "1. Batismo de Jesus no Jordão",
            "2. Auto-revelação de Jesus em Caná",
            "3. Anúncio do Reino de Deus",
            "4. Transfiguração de Jesus",
            "5. Instituição da Eucaristia"
        ]
    }

    oracoes = {
        "Sinal da Cruz": "Em nome do Pai, e do Filho e do Espírito Santo. Amém.",
        "Oferecimento": "Divino Jesus, nós vos oferecemos este terço que vamos rezar, meditando nos mistérios da nossa redenção. Concedei-nos, pela intercessão da Virgem Maria, Mãe de Deus e nossa Mãe, as virtudes que nos são necessárias para bem rezá-lo e a graça de ganharmos as indulgências desta santa devoção.",
        "Oração do Anjo": "O Anjo do Senhor anunciou a Maria. E ela concebeu do Espírito Santo. Ave Maria... Eis aqui a serva do Senhor. Faça-se em mim segundo a Vossa palavra. Ave Maria... E o Verbo de Deus se fez carne. E habitou entre nós. Ave Maria... Rogai por nós, Santa Mãe de Deus. Para que sejamos dignos das promessas de Cristo.",
        "Credo": "Creio em Deus Pai todo-poderoso, criador do céu e da terra... (completo)",
        "Mistérios": {
            "Segunda": "Gozosos",
            "Terça": "Dolorosos",
            "Quarta": "Gloriosos",
            "Quinta": "Luminosos",
            "Sexta": "Dolorosos",
            "Sábado": "Gozosos",
            "Domingo": "Gloriosos"
        },
        "Final": {
            "Salve": "Salve, Rainha, Mãe de misericórdia, vida, doçura e esperança nossa, salve! A vós bradamos, os degredados filhos de Eva...",
            "Ladainha": "Senhor, tende piedade de nós... Cristo, tende piedade de nós... Senhor, tende piedade de nós..."
        }
    }

    return render_template("terco.html", mistérios=mistérios, oracoes=oracoes)
# ✅ Execução da aplicação
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
