import json
import re

def clean_tweet_text(text):
    # Suppression des URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Suppression des mentions
    text = re.sub(r'@\w+', '', text)
    # Suppression des hashtags
    text = re.sub(r'#\w+', '', text)
    # Nettoyage des espaces multiples
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def process_tweets(input_file='saegus_tweets.json', output_file='cleaned_tweets.json'):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            tweets = data['tweets']
        
        cleaned_tweets = []
        for tweet in tweets:
            cleaned_tweet = {
                'id': tweet['id'],
                'created_at': tweet['created_at'],
                'text': clean_tweet_text(tweet['text']),
                'public_metrics': tweet['public_metrics']
            }
            cleaned_tweets.append(cleaned_tweet)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': data['metadata'],
                'tweets': cleaned_tweets
            }, f, ensure_ascii=False, indent=2)
        
        print(f"Tweets nettoyés et sauvegardés dans {output_file}")
        print(f"Nombre de tweets traités : {len(cleaned_tweets)}")
        
        if cleaned_tweets:
            print("\nExemple de tweet nettoyé :")
            print("Original :", tweets[0]['text'])
            print("Nettoyé :", cleaned_tweets[0]['text'])
            
    except FileNotFoundError:
        print(f"Erreur : Le fichier {input_file} n'existe pas")
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier {input_file} n'est pas un JSON valide")
    except Exception as e:
        print(f"Une erreur est survenue : {str(e)}")

if __name__ == "__main__":
    process_tweets() 