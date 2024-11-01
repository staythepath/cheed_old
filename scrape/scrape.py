from newspaper import Article

class ArticleScraper:
    def __init__(self, url):
        self.url = url
        self.article = None

    def scrape(self):
        # Create an Article object
        self.article = Article(self.url)
        
        # Download and parse the article
        self.article.download()
        self.article.parse()
        self.article.nlp()
        
    def get_details(self):
        # Extract details after parsing
        return {
            "title": self.article.title,
            "authors": self.article.authors,
            "publication_date": self.article.publish_date,
            "content": self.article.text,
            "top_image": self.article.top_image,
            "keywords": self.article.keywords,
            "summary": self.article.summary
        }

# Example usage:
if __name__ == "__main__":
    scraper = ArticleScraper("https://flathub.org/apps/net.newpipe.NewPipe")
    scraper.scrape()
    details = scraper.get_details()
    #print(details)
