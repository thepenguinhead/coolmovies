'''
-- White Box Testing --

Description: This small script tests getting links for both trailers and images.
'''

import unittest
from utils import fetch_poster
from ImdbScraper import videoScraper

class FractionTestCase(unittest.TestCase): 

    def test_fetch_poster_func(self):
        movieImageElement = fetch_poster("tt0848228", "movie")
        self.assertEqual(movieImageElement[0:33], "https://m.media-amazon.com/images")

        tvImageElement = fetch_poster("tt32896635", "series")
        self.assertEqual(tvImageElement[0:33], "https://m.media-amazon.com/images")

        noImageElement = fetch_poster("tt4118188", "movie")
        self.assertEqual(noImageElement, "https://via.placeholder.com/300x450.png?text=No+Image")
        
        
    def test_fetch_trailer_func(self): 
        mediaVideoElement = videoScraper("tt0848228")
        self.assertEqual(mediaVideoElement[0:46], "https://imdb-video.media-imdb.com/vi1891149081")

        noVideoElement = videoScraper("tt4118188")
        self.assertIsNone(noVideoElement)

if __name__ == '__main__':
    unittest.main()