import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, name):
        self.name = name
        self.url = None
        self.similarity_graph = {}
    
    def find_url(self):
        pass 

    def findAssociated(self):
        pass 

    def getGraph(self):
        return self.similarity_graph

    def showGraphImage(self):
        pass

    def getLayeredAssociated(self):
        pass

class WikiScraper(Scraper):
    def __init__(self, name):
        super().__init__(name)
        self.prefix = 'https://en.wikipedia.org/'

    # TODO: Different handling for bands and solo artists (usually there is a (band) next to bands)
    def find_url(self):
        underscored_name = self.name.replace(' ', '_')
        self.url = self.prefix + 'wiki/' + underscored_name
    
    # TODO: Also scrape past/present members of bands, family members, etc
    def findNeighborsOf(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser') 
        
        infobox = soup.find('table', class_='infobox')
        if infobox is None:
            return {}
        
        associated_acts = infobox.find('span', string='Associated acts')
        if associated_acts is None:
            return {}
        associated_acts = associated_acts.parent.next_sibling

        associated_acts = associated_acts.find_all('a')
        links_to_associated = {associated.text.strip(): associated['href'] for associated in associated_acts}
        return links_to_associated

    # Explores the graph similar to BFS for given maximum depth
    def findAssociated(self, depth=2):
        unexplored = {self.name: self.url}

        for _ in range(depth):
            new_unexplored = {}
            # Go to all unexplored
            for name, url in unexplored.items():
                neighbors = self.findNeighborsOf(url)
                self.similarity_graph[name] = neighbors.keys()
                new_unexplored.update({neighbor_name: self.prefix + neighbor_url for neighbor_name, neighbor_url in neighbors.items() if neighbor_name not in unexplored})
            unexplored = new_unexplored


if __name__ == '__main__':
    scraper = WikiScraper('Green Day')
    url = scraper.find_url()
    scraper.findAssociated()
    assocGraph = scraper.getGraph()

    for artist, assoc in assocGraph.items():
        print(f"Artist: {artist}")
        
        assoc = list(assoc)
        if assoc:
            for x in assoc[:-1]:
                print(x, end=', ')
            print(assoc[-1], end='\n')
        else:
            print('No known associated artists')

        print()