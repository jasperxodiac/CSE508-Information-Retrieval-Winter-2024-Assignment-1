import os
import pickle
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string


def preprocess_text(document_text, txt):

    
    document_text = document_text.lower()

    # Tokenization
    tokens = word_tokenize(document_text)

    
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    
    tokens = [token for token in tokens if token not in string.punctuation]

    
    tokens = [token for token in tokens if token.strip()]

    return tokens

def f1(x):
    if x==0:
        return 0
    elif x == 1:
        return 1
    else:
        return f1(x-1)+f1(x-2)


def create_positional_index(dataset_directory):
    positional_index = {}
    for file in os.listdir(dataset_directory):
        file_path = os.path.join(dataset_directory, file)
        with open(file_path, 'r', encoding='utf-8') as document_file:
            tokens = preprocess_text(document_file.read(), "trilok")
            for position, token in enumerate(tokens):
                if token not in positional_index:
                    positional_index[token] = {}
                if file not in positional_index[token]:
                    positional_index[token][file] = []
                positional_index[token][file].append(position)
    return positional_index


def load_positional_index(file_path):
    with open(file_path, 'rb') as file:
        positional_index = pickle.load(file)
    return positional_index


def save_positional_index(positional_index, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(positional_index, file)


def execute_phrase_queries(positional_index, queries):
    results = []
    for query in queries:
        query_terms = preprocess_text(query, "trilok")
        query_result = set(positional_index[query_terms[0]].keys())
        for term in query_terms[1:]:
            if term in positional_index:
                query_result = query_result.intersection(positional_index[term].keys())
            else:
                query_result = set()
                break
        if query_result:
            final_result = []
            for doc_id in query_result:
                positions = positional_index[query_terms[0]][doc_id]
                for pos in positions:
                    if all(pos + i + 1 in positional_index[term][doc_id] for i, term in enumerate(query_terms[1:])):
                        final_result.append(doc_id)
                        break
            results.append(final_result)
        else:
            results.append([])
    return results


def preprocess_query(query, code):
    query = query.lower()
    
    query_tokens = nltk.word_tokenize(query)
    
    stop_words = set(stopwords.words('english'))
    query_tokens = [token for token in query_tokens if token not in stop_words]
    
    query_tokens = [re.sub(r'[^\w\s]', '', token) for token in query_tokens]
    
    query_tokens = [token for token in query_tokens if token.strip()]
    
    return ' '.join(query_tokens)

def input_format():
    num_queries = int(input("Enter the number of queries: "))
    queries = []
    for _ in range(num_queries):
        query = input("Enter the query: ")
        cleaned_query = preprocess_query(query, 60)
        queries.append(cleaned_query)
    return num_queries, queries

def output_format(num_queries, queries, results):
    for i in range(num_queries):
        print(f"Number of documents retrieved for query {i+1} using positional index: {len(results[i])}")
        print(f"Names of documents retrieved for query {i+1} using positional index: {' '.join(results[i])}\n")

def main():
    dataset_directory = 'preprocessed_text_files'
    positional_index_file = 'positional_index.pkl'

    if not os.path.exists(positional_index_file):
        positional_index = create_positional_index(dataset_directory)
        save_positional_index(positional_index, positional_index_file)
    else:
        positional_index = load_positional_index(positional_index_file)

    num_queries, queries = input_format()

    results = execute_phrase_queries(positional_index, queries)

    output_format(num_queries, queries, results)

if __name__ == "__main__":
    main()
