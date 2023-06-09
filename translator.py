from pysubparser import parser, writer
from pysubparser.classes.subtitle import Subtitle
from google.cloud import translate_v2 as gtranslate
import os
from time import sleep
import webvtt


class Translator:
    def __init__(self):
        self.parser = parser.parse
        self.writer = writer.write
        self.translator = gtranslate.Client()

    def translate(self, text, from_lang="en", to_lang="zh"):
        # _ = ts.preaccelerate_and_speedtest()
        try:
            result = self.translator.translate(text, target_language=to_lang)
            return result["translatedText"]
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
    
    def translate_sub(self, file_name, target_name, from_lang="en", to_lang="zh"):
        subtitle = self.subtitle(file_name)
        result = []
        index = 1
        for s in subtitle:
            translated = self.translate(s.text, from_lang=from_lang, to_lang=to_lang)
            _subtitle = Subtitle(index=index, start=s.start, end=s.end, lines=[f'{translated}\n{s.text}'])
            result.append(_subtitle)
            index += 1
            sleep(0.1)
            print(index)
        self.writer(result, target_name)

    def translate_path(self, path, target_path, service='google', from_lang="en", to_lang="zh"):
        sub_files = self.path_subs(path)
        if not os.path.exists(target_path):  # 判断目录是否存在
            os.makedirs(target_path)
        for f in sub_files:
            print(f'start translate: {f}')
            self.translate_sub(
                f,
                target_name=os.path.join(target_path, os.path.split(f)[-1])
            )
            print(f, 1111)

    def reset_sub(self, file_name):
        subtitles = self.subtitle(file_name)
        result = []
        sub_map = {}
        jumps = set()
        st_idx = 1
        for s in subtitles:
            sub_map[s.index] = s
        for k, s in sub_map.items():
            if s.index in jumps:
                continue
            jumps.add(s.index)
            text = s.text.strip()
            start = s.start
            end = s.end
            if not s.text.endswith('.') or not s.text.endswith(','):
                next_sub = sub_map.get(s.index + 1)
                if next_sub:
                    end = next_sub.end
                    next_text = next_sub.text.strip()
                    jumps.add(next_sub.index)
                    text = text + ' ' + next_text
            _sub = Subtitle(index=st_idx, start=start, end=end, lines=[text])
            st_idx += 1
            result.append(_sub)
        return result
    
    def reset_path(self, path, target_path):
        sub_files = self.path_subs(path)
        if not os.path.exists(target_path):  # 判断目录是否存在
            os.makedirs(target_path)
        for f in sub_files:
            print(f'start reset sub: {f}')
            subtitle = self.reset_sub(f)
            self.writer(
                subtitle,
                os.path.join(target_path, os.path.split(f)[-1])
            )

    def convert_path(self, path, target_path):
        file_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.vtt'):
                    file_path = os.path.join(root, file)
                    file_list.append(file_path)
        file_list.sort()
        if not os.path.exists(target_path):  # 判断目录是否存在
            os.makedirs(target_path)
        for f in file_list:
            vtt = webvtt.read(f)
            vtt.save_as_srt()

            # write to opened file in SRT format
            f_name = os.path.split(f)[-1]
            f_name = f_name[:-4] + '.srt'
            with open(os.path.join(target_path, f_name), 'w') as fd:
                vtt.write(fd, format='srt')



translator = Translator()
