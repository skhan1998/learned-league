# learned-league
This respository contains code for scraping LearnedLeague history and training classifiers on it. The code in scraper.py does the scraping, in neighbors.py does embedding and nearest-neighbor searches, and in publisher.py formats and outputs the results. The code in defense.py combines all of these, and be called as

```
python defense.py SEASON_NUMBER DAY_NUMBER OPPONENT_NAME USERNAME PASSWORD
``` 

This code relies on the [sent2vec sentence embeddings](https://github.com/epfml/sent2vec) and the wiki_unigrams.bin model available available there, as well as pdflatex for compiling the PDF output. 
