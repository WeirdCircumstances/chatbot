'''
Andy - TextBot
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
<<<<<<< HEAD
GREETING_INPUTS = ("hello", "hi", "Good Day", "Whats Up", "greedings", "hey")
GREETING_RESPONSES = ["hi", "hey", "hello", "Nice to meet you"]

# Beleidigungen
INDIGNITY_INPUTS = ("idiot", "fuck", "dumd", "shit", "asshole")
INDIGNITY_RESPONSES = ["We sould be nice to each other", "you shouldn't say somthing like that", "this isn't very nice", " don't say this", "Oh what a nice Guy"]

# Witze
SADNESS_INPUTS = ("sad")
SADNESS_RESPONSES = ["My Musical knowledge is so poor i thought kanye west was a railway station ans lena del a holiday destination.", "Two fish in a tank. One turns to the other and says: „Do you know how to drive this?"]
=======
GREETING_INPUTS = ("hallo", "hi", "grüße", "tach", "was geht", "hey", "servus", "moin")
GREETING_RESPONSES = ["hi", "hey", "gott zum gruße", "tach", "hallo", "Es freut mich, mit dir sprechen zu dürfen.", "Servus"]

# Beleidigungen
INDIGNITY_INPUTS = ("arsch", "sau", "depp", "doof", "dumm", "kacke")
INDIGNITY_RESPONSES = ["Wir sollten nett zueinander sein.", "Wenn du meinst.", "Überleg mal, was du sagst.", "Das finde ich nicht nett.", "Du solltest sowas nicht sagen", "Ohje, du bist ja ein besonders netter Zeitgenosse...", "Ich hoffe du kriegst husten"]
>>>>>>> 3da919dd61bb2b5dd7e635c0a05a252c3377fe40

# Für den ersten Start, ansonsten auskommentieren
#'''
#nltk.download('popular', quiet=True) 
#nltk.download('punkt') 
#nltk.download('wordnet')'''
# changes in dev


# Corpus einlesen
with open('chatbot_en_andy_1.txt','r', encoding='utf8', errors ='ignore') as text:
    raw = text.read().lower()

# familien antworten laden (MM)
with open('chatbot_family.txt','r', encoding='utf8', errors ='ignore') as text:
    raw_fam = text.read().lower()

# Tokenisierung
# sent_tokens konvertiert in Liste von Sätzen
sent_tokens = nltk.sent_tokenize(raw)
# familien antworten hinzufuegen (MM)
sent_tokens.extend(nltk.sent_tokenize(raw_fam))
# word_tokens konvertiert in Liste von Worten (Wird nicht verwendet.)
word_tokens = nltk.word_tokenize(raw)
#print (word_tokens)

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
        if word.lower() in SADNESS_INPUTS:
            return random.choice(SADNESS_RESPONSES)




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
    #print(flat)
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
andy_print_color = "yellow"
flag=True
clear = lambda: os.system('clear')
clear()
<<<<<<< HEAD
#print(colored("ANDY: ", 'green', attrs=['bold']) + colored("\tHallo, meine Name ist ANDY. Ich weiß eine Menge über Chatbots. Frag' mich einfach!\n\tWenn du aufhören willst, tippe 'Bye'.", 'cyan'))
print(colored("ANDY: ", 'green', attrs=['bold']) + colored("\tHi, my name is ANDY. I want to help you!\n\tTo end this chat, type 'Bye'.", 'cyan'))
=======

#print(colored("Andy: ", andy_print_color, attrs=['bold']) + colored("\tHallo, meine Name ist Andy. Ich weiß eine Menge über Chatbots. Frag' mich einfach!\n\tWenn du aufhören willst, tippe 'Bye'.", 'cyan'))
print(colored("Andy: ", andy_print_color, attrs=['bold']) + colored("\tHi I'm Andy. I want to help you. Please tell me your issue!\n\tTo end this conversation, type 'Bye'.", 'cyan'))
user_input = input(colored("Name your favorite color!\n", "cyan"))
if user_input in "grey red green yellow blue magenta cyan white":
    andy_print_color = user_input
    print(colored("Color changed!", "cyan"))
else:
    print(colored("Unfortenaly this isn't a color.", "cyan"))

>>>>>>> 3da919dd61bb2b5dd7e635c0a05a252c3377fe40
while(flag==True):
    user_response = input()
    #stemmer = GermanStemmer()
    #user_response = stemmer.stem(user_response)
    user_response = user_response.lower()
    if(user_response!='bye'):
        if(user_response=='danke dir' or user_response=='danke' ):
            flag=False
<<<<<<< HEAD
            print(colored("ANDY: ", 'green', attrs=['bold']) + colored( "You are welcome...", 'cyan'))
        else:
            if(trivia(user_response)!=None):
                print(colored("ANDY: ", 'green', attrs=['bold']) + colored(trivia(user_response), 'cyan'))
            else:
                print(colored("ANDY: ", 'green', attrs=['bold']), end="")
=======
            print(colored("Andy: ", andy_print_color, attrs=['bold']) + colored( "You are welcome...", 'cyan'))
        else:
            if(trivia(user_response)!=None):
                print(colored("Andy: ", andy_print_color, attrs=['bold']) + colored(trivia(user_response), 'cyan'))
            else:
                print(colored("Andy: ", andy_print_color, attrs=['bold']), end="")
>>>>>>> 3da919dd61bb2b5dd7e635c0a05a252c3377fe40
                print(colored(response(user_response), 'cyan'))
                sent_tokens.remove(user_response)
    else:
        flag=False
<<<<<<< HEAD
        print(colored("ANDY: ", 'green', attrs=['bold']) + colored("Smell you later.", 'cyan'))    
=======
        print(colored("Andy: ", andy_print_color, attrs=['bold']) + colored("Smell you later.", 'cyan'))    
>>>>>>> 3da919dd61bb2b5dd7e635c0a05a252c3377fe40

