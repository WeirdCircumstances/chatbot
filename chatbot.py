'''
CODY - TextBot
A simple NLTK Text Chatbot for the CODE{affair} workshop 2019 
based on an example script from Parul Pandey.
'''
import io
import os
import random
import string # (Zur Verarbeitung von Standard Python Strings)
import warnings
#import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from stop_words import get_stop_words
from termcolor import colored, cprint
import nltk
from nltk.stem import WordNetLemmatizer

warnings.filterwarnings('ignore')

# Begrüßungen
GREETING_INPUTS = ("hello", "hi", "greetings", "hey", "what's up", "good morning")
GREETING_RESPONSES = ["Hi", "Hey", "Good morning", "Nice to meet you.", "Hello"]

# Beleidigungen
INDIGNITY_INPUTS = ("fuck", "ass", "idiot", "dumb", "shit")
INDIGNITY_RESPONSES = ["We should communicate friendly.", "If you think so.", "Think twice before saying.", "That isn't nice.", "You shouldn't say something like that", "Oh, it seems you're a very friendly guy..."]

# Für den ersten Start, ansonsten auskommentieren
'''
nltk.download('popular', quiet=True) 
nltk.download('punkt') 
nltk.download('wordnet')'''
# changes in dev


# Corpus einlesen
with open('chatbot_en.txt','r', encoding='utf8', errors ='ignore') as text:
    raw = text.read().lower()

# Tokenisierung
# sent_tokens konvertiert in Liste von Sätzen
sent_tokens = nltk.sent_tokenize(raw)
# word_tokens konvertiert in Liste von Worten (Wird nicht verwendet.)
word_tokens = nltk.word_tokenize(raw)

# Vorverarbeitung (Preprocessing)
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
def trivia(sentence):
    '''Wenn die Nutzereingabe eine Begrüßung ist, Antwortet der Bot mit einer zufälligen Begrüßung als Antwort, 
    gleiches gilt für Beleidigungen'''
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
        if word.lower() in INDIGNITY_INPUTS:
            return random.choice(INDIGNITY_RESPONSES)




# Antwort Erzeugung
def response(user_response):
    stop_words = get_stop_words('english')
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words=stop_words)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        #robo_response= "[tfidf: "+str(round(req_tfidf,2))+"] "+robo_response+ "Tut mir leid, ich verstehe dich nicht."
        robo_response= "[tfidf: "+str(round(req_tfidf,2))+"] "+robo_response+ "Sorry, das habe ich nicht verstanden :'("
        return robo_response
    else:
        robo_response = "[tfidf: "+str(round(req_tfidf,2))+"] "+robo_response+sent_tokens[idx]
        return robo_response

'''
Ausgabe
(Um die Konsolenausgabe übersichtlicher zu gestalten wird die Bibliothek termcolor benutzt)
'''
flag=True
clear = lambda: os.system('clear')
clear()
#print(colored("CODY: ", 'green', attrs=['bold']) + colored("\tHallo, meine Name ist CODY. Ich weiß eine Menge über Chatbots. Frag' mich einfach!\n\tWenn du aufhören willst, tippe 'Bye'.", 'cyan'))
print(colored("CODY: ", 'red', attrs=['bold']) + colored("\tHi, my name is CODY. I want to learn a lot about chatbots and AI. Please train me to get better and better!\n\tTo end this chat, type 'Bye'.", 'cyan'))
while(flag==True):
    user_response = input()
    #stemmer = GermanStemmer()
    #user_response = stemmer.stem(user_response)
    user_response = user_response.lower()
    if(user_response!='bye'):
        if(user_response=='danke dir' or user_response=='danke' ):
            flag=False
            print(colored("CODY: ", 'red', attrs=['bold']) + colored( "You are welcome...", 'cyan'))
        else:
            if(trivia(user_response)!=None):
                print(colored("CODY: ", 'red', attrs=['bold']) + colored(trivia(user_response), 'cyan'))
            else:
                print(colored("CODY: ", 'red', attrs=['bold']), end="")
                print(colored(response(user_response), 'green'))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print(colored("CODY: ", 'red', attrs=['bold']) + colored("See you later.", 'cyan'))    

