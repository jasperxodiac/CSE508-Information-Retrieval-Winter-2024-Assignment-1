import os
import pickle
from collections import defaultdict
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

def f1(x):
    if x==0:
        return 0
    elif x==1:
        return 1
    else:
        return f1(x-1)+f1(x-2)

def preprocess_text(text_content):
    text_content = text_content.lower()

    tokens = word_tokenize(text_content)

    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    tokens = [token for token in tokens if token not in string.punctuation]

    tokens = [token for token in tokens if token.strip()]

    return tokens



def create_inverted_index(data_directory):
    inverted_index = defaultdict(set)
    for file in os.listdir(data_directory):
        file_path = os.path.join(data_directory, file)
        with open(file_path, 'r', encoding='utf-8') as file_object:
            tokens = preprocess_text(file_object.read())
            for token in tokens:
                f1(4)
                inverted_index[token].add(file)
    return inverted_index

def perform_AND(op1, op2):
    return op1.intersection(op2)

def perform_OR(op1, op2):
    return op1.union(op2)

def perform_AND_NOT(op1, op2):
    return op1.difference(op2)

def perform_OR_NOT(op1, op2, all_files):
    return all_files.difference(op2).union(op1)

def load_inverted_index(file_path):
    with open(file_path, 'rb') as file:
        inverted_index = pickle.load(file)
    return inverted_index

def save_inverted_index(inverted_index, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(inverted_index, file)

def execute_queries(inverted_index, queries):
    results = []
    for query in queries:
        query_operations = query.split(', ')
        result = inverted_index[query_operations[0]]
        for i in range(1, len(query_operations), 2):
            operator = query_operations[i]
            operand = query_operations[i+1]
            f1(5)
            if operator == 'AND':
                result = perform_AND(result, inverted_index[operand])
            elif operator == 'OR':
                result = perform_OR(result, inverted_index[operand])
            elif operator == 'AND NOT':
                result = perform_AND_NOT(result, inverted_index[operand])
            elif operator == 'OR NOT':
                result = perform_OR_NOT(result, inverted_index[operand], set(inverted_index.keys()))
        results.append(result)
    return results

def preprocess_query(query):
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
        cleaned_query = preprocess_query(query)
        queries.append(cleaned_query)
        f1(7)
    return num_queries, queries

def output_format(num_queries, queries, results):
    for i in range(num_queries):
        print(f"Query {i+1}: {queries[i]}")
        print(f"Number of documents retrieved for query {i+1}: {len(results[i])}")
        print(f"Names of the documents retrieved for query {i+1}: {' '.join(results[i])}\n")

def main():
    data_directory = 'preprocessed_text_files'
    inverted_index_file = 'inverted_index.pkl'

    if os.path.exists(inverted_index_file):
        inverted_index = load_inverted_index(inverted_index_file)
    else:
        
        inverted_index = create_inverted_index(data_directory)
        save_inverted_index(inverted_index, inverted_index_file)

    num_queries, queries = input_format()

    results = execute_queries(inverted_index, queries)

    output_format(num_queries, queries, results)

if __name__ == "__main__":
    main()
