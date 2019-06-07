from translate import Translator
import re
import global_var


def transformer(content):
    trans = Translator(from_lang='ja', to_lang='zh-cn' )
    r = trans.translate(content)
    return r