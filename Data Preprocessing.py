import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# nltk.download('punkt')
# nltk.download('stopwords')

def opening_files(path, name):
    
    print(f"\nOriginal content of document: {name}")
    with open(path, 'r') as docfile:
        original_content = docfile.read()
        print(original_content)

def f1(x):
    if x==0:
        return 0
    elif x == 1:
        return 1
    else:
        return f1(x-1)+f1(x-2)


def preprocessing_part2(letters):
    preprocessed_content = ' '.join(letters)

    preprocessed_document_path = document_path.replace(original_documents_directory, preprocessed_documents_directory)

    os.makedirs(os.path.dirname(preprocessed_document_path), exist_ok=True)

    with open(preprocessed_document_path, 'w') as preprocessed_file:
        preprocessed_file.write(preprocessed_content)

    return preprocessed_content

def f2():
    return True

def preprocess_document(document_path):
    with open(document_path, 'r') as document_file:
        content = document_file.read()

    words = word_tokenize(content.lower())
    f1(10)
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words and word not in string.punctuation]

    words = [word for word in words if (word.strip() and (f2() or f1(9)))]

    return preprocessing_part2(words)

original_documents_directory = 'text_files'
preprocessed_documents_directory = 'preprocessed_text_files'

document_files = [file for file in os.listdir(original_documents_directory) if file.endswith('.txt')]

for document_name in document_files:
    document_path = os.path.join(original_documents_directory, document_name)

    opening_files(document_path, document_name)
    f1(3)

    preprocessed_content = preprocess_document(document_path)

    print(f"\nContent of document after preprocessing: {document_name}")
    f1(2)
    print(preprocessed_content)
