import json
import spacy
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from tqdm import tqdm

def load_tweets(file_path='cleaned_tweets.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_main_topic(tweets):
    # Charger le modèle français
    nlp = spacy.load("fr_core_news_sm")
    
    # Extraire les textes des tweets
    text_data = [tweet["text"] for tweet in tweets]
    
    # Traitement NLP
    all_tokens = []
    for text in tqdm(text_data, desc="Traitement des tweets"):
        doc = nlp(text.lower())
        tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
        all_tokens.extend(tokens)
    
    # Analyse TF-IDF
    vectorizer = TfidfVectorizer(max_features=100)
    X = vectorizer.fit_transform([" ".join(all_tokens)])
    terms = vectorizer.get_feature_names_out()
    scores = X.toarray().flatten()
    
    # Trouver les termes les plus pertinents
    ranked_terms = sorted(zip(terms, scores), key=lambda x: x[1], reverse=True)
    
    # Créer un dictionnaire des sujets principaux
    topics = {term: score for term, score in ranked_terms[:20]}
    
    return topics

def analyze_tweets():
    data = load_tweets()
    tweets = data['tweets']
    topics = extract_main_topic(tweets)
    
    for tweet in tweets:
        tweet_text = tweet['text'].lower()
        tweet_topics = []
        for topic in topics:
            if topic in tweet_text:
                tweet_topics.append({
                    'topic': topic,
                    'score': topics[topic]
                })
        tweet['main_topics'] = tweet_topics
    
    with open('tweets_with_topics.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Créer un DataFrame avec les résultats
    df = pd.DataFrame(list(topics.items()), columns=['Topic', 'Score'])
    
    # Sauvegarder les résultats
    df.to_csv('topics_analysis.csv', index=False)
    
    # Générer un rapport
    with open('topics_report.txt', 'w', encoding='utf-8') as f:
        f.write("Analyse des sujets principaux des tweets Saegus\n")
        f.write("==========================================\n\n")
        
        f.write("Top 10 des sujets les plus fréquents :\n")
        for topic, score in list(topics.items())[:10]:
            f.write(f"- {topic}: {score:.4f}\n")
        
        f.write("\nExemples de tweets par sujet principal :\n")
        for topic in list(topics.keys())[:5]:
            f.write(f"\n{topic}:\n")
            # Trouver des tweets contenant ce sujet
            for tweet in tweets:
                if topic in tweet['text'].lower():
                    f.write(f"- {tweet['text'][:100]}...\n")
                    break

if __name__ == "__main__":
    analyze_tweets()
    print("L'analyse des sujets est terminée. Les résultats ont été sauvegardés dans 'tweets_with_topics.json', 'topics_analysis.csv' et 'topics_report.txt'")