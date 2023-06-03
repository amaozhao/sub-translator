from pysubparser import parser, writer
from pysubparser.classes.subtitle import Subtitle
from googletranslatepy import Translator as GTranslator
import os
from time import sleep


class Translator:
    def __init__(self):
        self.parser = parser.parse
        self.writer = writer.write
        self.translator = GTranslator()

    def translate(self, text, service='google', from_lang="en", to_lang="zh"):
        # _ = ts.preaccelerate_and_speedtest()
        try:
            return self.translator.translate(text, timeout=10)
        except:
            return ''
    
    def subtitle(self, file_name):
        return self.parser(file_name)
    
    def path_subs(self, directory):
        file_list = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.srt') or file.endswith('.ass') or file.endswith('.ssa'):
                    file_path = os.path.join(root, file)
                    file_list.append(file_path)
        file_list.sort()
        return file_list
    
    def translate_sub(self, file_name, target_name, service='google', from_lang="en", to_lang="zh"):
        subtitle = self.subtitle(file_name)
        resutl = []
        index = 1
        for s in subtitle:
            translated = self.translate(s.text, service=service, from_lang=from_lang, to_lang=to_lang)
            _subtitle = Subtitle(index=index, start=s.start, end=s.end, lines=[f'{translated}\n{s.text}'])
            resutl.append(_subtitle)
            index += 1
            sleep(0.2)
            print(index)
        self.writer(resutl, target_name)

    def translate_path(self, path, target_path, service='google', from_lang="en", to_lang="zh"):
        sub_files = self.path_subs(path)
        if not os.path.exists(target_path):  # 判断目录是否存在
            os.makedirs(target_path)
        for f in sub_files:
            print(f'start translate: {f}')
            self.translate_sub(
                f,
                target_name=os.path.join(target_path, os.path.split(f)[-1]),
                service=service
            )
            print(f, 1111)


translator = Translator()
