import glob 
from nltk.tokenize import word_tokenize   
from nltk.stem.snowball import SnowballStemmer

PATH_STOPWORDS = './stopwords/stoplist.txt'

def read_stop_words(filename):
        file = open(filename,"r",encoding = "ISO-8859-1")
        words = file.read().splitlines()
        return words

class InvertedIndex:
    files = []
    inverted_index = {}
    snowball_stemmer = SnowballStemmer('spanish')    
    NUMBER_FRECUENCY = 500
    TRASH = '''!()-[]{};:'"\,«»''``<>./?@#$%^&*_~\n'''


    def load_files(self):
        files_sorted = sorted(glob.glob('./books/*.txt'));
        for i in range(1,len(files_sorted) + 1):
            data_file = open(f"./books/libro{i}.txt").read().lower()
            self.files.append(data_file)


    def clean_stop_words_trash(self,set_words):
        clean_words = [ word for word in set_words if not word in (read_stop_words(PATH_STOPWORDS)) if not word in self.TRASH]
        return clean_words


    def stemming(self,set_words):
        words_stemming = []
        for token in set_words:
            words_stemming.append(self.snowball_stemmer.stem(token))
        return words_stemming
    

    def until_frecuency(self):
        until = sorted(self.inverted_index, key=lambda k:len(self.inverted_index[k]), reverse=True)[:self.NUMBER_FRECUENCY]
        for i in list(self.inverted_index.keys()):
            if(i not in until):
                del self.inverted_index[i]


    def make_diccionary(self, word_list,number_page):
        for word in word_list:
            if word not in self.inverted_index:
                self.inverted_index[word] = []
            if word in self.inverted_index:
                if( number_page not in self.inverted_index[word]):
                    self.inverted_index[word].append(number_page)
    
        
    def make_up_inverted_index(self):
        stop_words = read_stop_words(PATH_STOPWORDS)
        self.load_files()
        todo = []
        for i in range (1,len(self.files) + 1):
            words_tokenize = word_tokenize(self.files[i-1])
            clean_words = self.clean_stop_words_trash(words_tokenize)
            words_stemming = self.stemming(clean_words)
            self.make_diccionary(words_stemming,i)  
        self.until_frecuency()          


    def L(self, string):
        word_reduce = self.snowball_stemmer.stem(string)
        return self.inverted_index[word_reduce]


    def AND_(self,string_one,string_two):
        list_one = self.L(string_one)
        list_two = self.L(string_two)
        and_documents = []
        if(len(list_one)<=len(list_two)):
            for number_page in list_one:
                if number_page in list_two:
                    and_documents.append(number_page)
        else:
            for number_page in list_two:
                if number_page in list_one:
                    and_documents.append(number_page)
        return and_documents
    

    # or ordered
    def OR(self,string_one,string_two):
        list_one = self.L(string_one)
        list_two = self.L(string_two)
        i = 0
        j = 0
        or_ = []
        while(i < len(list_one) and j < len(list_two)):
            if(list_one[i] < list_two[j]):
                or_.append(list_one[i])
                i+=1
            if(list_one[i] == list_two[j]):
                or_.append(list_two[j])
                i+=1
                j+=1
            else:
                or_.append(list_two[j])
                j+=1
        return or_ 

    def AND_NOT(self,string_one,string_two):
        list_one = self.L(string_one)
        list_two = self.L(string_two)
        and_not_ = []

        for page_number in list_one:
            if(page_number not in list_two):
                and_not_.append(page_number)
            else:
                continue
        
        return and_not_

    def AND(self,list_one,list_two):
        and_documents = []
        if(len(list_one)<=len(list_two)):
            for number_page in list_one:
                if number_page in list_two:
                    and_documents.append(number_page)
        else:
            for number_page in list_two:
                if number_page in list_one:
                    and_documents.append(number_page)
        return and_documents

inverted_index = InvertedIndex()
inverted_index.make_up_inverted_index()

word_one = "Frodo"
word_two = "Bilbo"
word_three = "Gandalf"
word_four = "acabado"
word_five = "acompañar"

print(f"OPERACION L({word_one}):", inverted_index.L(word_one))
print(f"OPERACION L({word_two}):", inverted_index.L(word_two))
print(f"OPERACION L({word_three}):", inverted_index.L(word_three))
print(f"OPERACION L({word_four}):", inverted_index.L(word_four))
print(f"OPERACION L({word_five}):", inverted_index.L(word_five))
print(f"OPERACION AND({word_one},{word_three}): ", inverted_index.AND_(word_one, word_three))
print(f"OPERACION OR({word_four},{word_five}): ",inverted_index.OR(word_four,word_five))
print(f"OPERACION AND_NOT({word_one},{word_two}): ",inverted_index.AND_NOT(word_one,word_two))
print(f"OPERACION RECOVERY(AND(AND(L({word_one}),L({word_two})),L({word_three})): ",inverted_index.AND
(inverted_index.AND(inverted_index.L(word_one), inverted_index.L(word_two)),inverted_index.L(word_three)))