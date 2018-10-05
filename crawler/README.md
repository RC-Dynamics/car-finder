# Car Finder - Crawler
System to find cars

## How to run

To install dependencies run:

```
pip3 install beautifulsoup4 requests tqdm pandas selenium nltk pprint scikit-learn -U

sudo apt-get install phantomjs -y
```

and using python3 run

```
import nltk
nltk.download('punkt')
```

To run the crawler run:

```
python3 crawler.py
```

This script read the `../site.txt` file as input with the links.
