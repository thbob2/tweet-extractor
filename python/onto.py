from googletrans import Translator
from textblob import TextBlob

trans = Translator()

result = trans.translate("안녕하세요").text
print(result)

    