import typer
from translator import translator


app = typer.Typer()


@app.command()
def translate_path(path: str):
    translator.translate_path(path, target_path="subtitle", service='baidu', to_lang="zh")


@app.command()
def translate_file(file: str):
    translator.translate_sub(file_name=file, target_name=file, service='google', from_lang="en", to_lang="zh")


if __name__ == "__main__":
    app()