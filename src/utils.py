import os
import requests

def fetch_poster(id, media_type='movie'):
    """
    Fetches the poster URL from OMDb API based on the title and media type.

    :param title: Title of the movie or TV show
    :param media_type: 'movie' or 'series'
    :return: Poster URL or a placeholder image URL
    """
    api_key = os.getenv('OMDB_API_KEY')
    
    if not api_key:
        print('no api key')
        return 'https://via.placeholder.com/300x450.png?text=No+Image'
    
    try: 
        params = {
            'i': id,
            'type': media_type,
            'apikey': api_key
        }
        response = requests.get('https://www.omdbapi.com/', params=params)
        data = response.json()

        if data.get('Response') == 'True' and data.get('Poster') != 'N/A':
            return data.get('Poster')
        else:
            return 'https://via.placeholder.com/300x450.png?text=No+Image'
        
    except Exception as e:
        print(e)
        return 'https://via.placeholder.com/300x450.png?text=No+Image'