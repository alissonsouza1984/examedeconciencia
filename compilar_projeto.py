import os

# Arquivos principais a incluir
arquivos = [
    "app.py",
    "Dockerfile",
    "README.md",
    "render.yaml",
    "requirements.txt",
    "static/css/style.css"
]

# Arquivos HTML na pasta templates
templates_dir = "templates"
for arquivo in os.listdir(templates_dir):
    if arquivo.endswith(".html"):
        arquivos.append(os.path.join(templates_dir, arquivo))

# Nome do arquivo final
saida = "projeto_compilado.txt"

# Criar o arquivo de saída
with open(saida, "w", encoding="utf-8") as f_out:
    for caminho in arquivos:
        if os.path.exists(caminho):
            f_out.write(f"{'#' * 80}\n")
            f_out.write(f"### ARQUIVO: {caminho}\n")
            f_out.write(f"{'#' * 80}\n\n")
            with open(caminho, "r", encoding="utf-8") as f_in:
                f_out.write(f_in.read())
            f_out.write("\n\n")
        else:
            f_out.write(f"# Arquivo não encontrado: {caminho}\n\n")

print(f"\n✅ Arquivo '{saida}' criado com sucesso.")
