import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances
from rank_bm25 import BM25Okapi


def are_titles_same(doc1, doc2):
    title1 = doc1.split(':')[0].strip().lower()  
    title2 = doc2.split(':')[0].strip().lower()
    return 0 if title1 == title2 else 1 



def cosine_similarity_documents(documents,new_document):
    vectorizer = TfidfVectorizer(stop_words='english')
    tf_idf_matrix = vectorizer.fit_transform(documents+new_document)
    cosine_similarities = cosine_similarity(tf_idf_matrix)
    return cosine_similarities


def get_k_shingles(document, k):
    shingles = set()
    words = document.lower().split()
    for i in range(len(words) - k + 1):
        shingle = ' '.join(words[i:i+k])
        shingles.add(shingle)
    return shingles

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

def check_duplicate_jaccard(documents, new_document, k=3, threshold=0.5):
    shingles_documents = get_k_shingles(documents, k)
    shingles_new_document = get_k_shingles(new_document, k)
    similarities = [jaccard_similarity(shingles_new_document, shingle_doc) for shingle_doc in shingles_documents]
    duplicates = [i for i, sim in enumerate(similarities) if sim > threshold]
    return duplicates


def check_duplicate_bm25(documents, new_document, threshold=0.85):
    corpus = documents + new_document
    tokenized_corpus = [doc.lower().split() for doc in corpus]
    bm25 = BM25Okapi(tokenized_corpus)
    similarities = bm25.get_scores(tokenized_corpus[-len(new_document)])
    duplicates = [i for i, sim in enumerate(similarities[:-len(new_document)]) if sim > threshold]
    return duplicates





documents = ['Information requirement: query considers the user feedback as information requirement to search.',
             'Information retrieval: query depends on the model of information retrieval used.',
             'Prediction problem: Many problems in information retrieval can be viewed as prediction problems',
             'Search: A search engine is one of applications of information retrieval models.']

new_document = ['Feedback: feedback is typically used by the system to modify the query and improve prediction',
                'information retrieval: ranking in information retrieval algorithms depends on user query']




def plagiarism_checker(documents, new_document):
    
    title_check = are_titles_same(documents[0], new_document[0])
    if title_check == 0:
        return "Document is duplicate (based on titles)"

    cosine_similarities = cosine_similarity_documents(documents,new_document)
    print(cosine_similarities)
    for idx, similarity in enumerate(cosine_similarities[0]):
        print(f"Cosine Similarity between new_document and document {idx}: {similarity}")
        
    duplicates_jaccard = check_duplicate_jaccard(documents[0], new_document[0])
    if len(duplicates_jaccard) > 0:
        return f"Document is duplicate (based on Jaccard similarity): {duplicates_jaccard}"

    
    duplicates_bm25 = check_duplicate_bm25(documents, new_document)
    if len(duplicates_bm25) > 0:
        return f"Document is duplicate (based on BM25): {duplicates_bm25}"

    return "Document is not duplicate"


result = plagiarism_checker(documents, new_document)
print(result)
