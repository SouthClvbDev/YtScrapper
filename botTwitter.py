import tweepy

# Autenticación
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
api = tweepy.API(auth)

# Postear un tweet
api.update_status("Hola, mundo! Soy un bot 🤖 #Python #TwitterBot")
