
import translator
import profanity_check
import data
import log

import file
import nltk
import lib_hate

# by Jakub Grzana

###################################################################################

classifier = file.Load(lib_hate.GetClassifierDir()+lib_hate.name_classifier)
important_words = file.Load(lib_hate.GetClassifierDir()+lib_hate.name_important_words)

def jg_scan(text):
    global classifier
    text = lib_hate.PreprocessMessage(text)
    features = lib_hate.feature_extractor(text,important_words)
    if classifier.classify(features) == 'hate':
        return 1
    return 0

###################################################################################

def Detect(text):
    # translating to english, if it's not english by default
    try:
        text = EnsureEnglish(text)
    except:
        return 0
    # Hate detection
    if profanity_check.predict([text]) == [1]:
        return 1
    if jg_scan(text):
        return 1
    return 0

def EnsureEnglish(text):
    src = translator.DetectLanguage(text)
    if src != 'en':
        text = translator.RawTranslate(src,'en',text)
    return text

async def Pass(bot, local_env, message):
    if message.author.bot:
        return
    if len(message.content) < 5:
        return
    try:
        if Detect(message.content) == 1:
            user_env = data.GetUserEnvironment(local_env, message.author)
            user_env['infamy'] = user_env['infamy'] + 1
    except Exception as e:
        await log.Error(bot, e, message.guild, local_env, { 'content' : message.content } )