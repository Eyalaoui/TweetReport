import tweepy
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# Chargement des variables d'environnement
load_dotenv()

# Configuration des tokens
api_key = os.getenv('TWITTER_API_KEY')
api_secret = os.getenv('TWITTER_API_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

def get_saegus_tweets():
    try:
        # Initialisation du client
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            bearer_token=bearer_token
        )

        # Récupération de l'ID du compte Saegus
        user = client.get_user(username='saegus_france')
        if not user.data:
            print("Compte @saegus_france non trouvé")
            return

        user_id = user.data.id
        print(f"\nRécupération des tweets de @saegus_france (ID: {user_id})")

        # Récupération des tweets
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=100,
            tweet_fields=['created_at', 'public_metrics', 'entities']
        )

        if not tweets.data:
            print("Aucun tweet trouvé")
            return

        # Préparation des données pour le JSON
        tweets_data = []
        for tweet in tweets.data:
            tweet_data = {
                'id': tweet.id,
                'created_at': tweet.created_at.isoformat(),
                'text': tweet.text,
                'public_metrics': {
                    'like_count': tweet.public_metrics['like_count'],
                    'retweet_count': tweet.public_metrics['retweet_count'],
                    'reply_count': tweet.public_metrics['reply_count']
                }
            }
            tweets_data.append(tweet_data)
            print(f"\nTweet récupéré : {tweet.text[:50]}...")

        # Sauvegarde dans un fichier JSON
        output_file = 'saegus_tweets.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'total_tweets': len(tweets_data),
                    'retrieved_at': datetime.now().isoformat()
                },
                'tweets': tweets_data
            }, f, ensure_ascii=False, indent=2)

        print(f"\n{len(tweets_data)} tweets ont été sauvegardés dans {output_file}")

    except tweepy.errors.Unauthorized as e:
        print(f"\nErreur d'authentification : {str(e)}")
    except Exception as e:
        print(f"\nUne erreur est survenue : {str(e)}")

if __name__ == "__main__":
    get_saegus_tweets() 