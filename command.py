import typer
from translator import translator


app = typer.Typer()


@app.command()
def translate_path(path: str):
    translator.translate_path(path, target_path="subtitle", service='baidu')


@app.command()
def translate_file(file: str):
    print(f"Hello {file}")


if __name__ == "__main__":
    app()