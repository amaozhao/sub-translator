import typer
from translator import translator


app = typer.Typer()


@app.command()
def reset_path(path: str):
    translator.reset_path(path, target_path="reset")


@app.command()
def translate_path(path: str):
    translator.translate_path(path, target_path="subtitle", service='baidu', to_lang="zh")


@app.command()
def convert_path(path: str):
    translator.convert_path(path, target_path="convert")


@app.command()
def convert_path_with_reset(path: str):
    translator.convert_path(path, target_path="convert")
    translator.reset_path(path="convert", target_path="reset")


@app.command()
def translate_with_reset(path: str):
    translator.reset_path(path, target_path="reset")
    translator.translate_path(path='reset', target_path="subtitle", service='baidu', to_lang="zh")


@app.command()
def translate_file(file: str):
    translator.translate_sub(file_name=file, target_name=file, service='google', from_lang="en", to_lang="zh")



if __name__ == "__main__":
    app()