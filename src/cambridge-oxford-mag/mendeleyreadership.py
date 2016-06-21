from mendeley import Mendeley
from mendeley.exception import MendeleyException
import yaml
import pandas
import sys
import math
import numpy as np
import copy

class MendeleyRequestor:

    def load_dataset(self):
        oxford = pandas.io.parsers.read_csv("oxford.csv", sep=',')
        cambridge = pandas.io.parsers.read_csv("cambridge.csv", sep=',')

        return (oxford, cambridge)

    def init_mendeley_api(self):
        with open('config.yml') as f:
            config = yaml.load(f)

        # These values should match the ones supplied when registering your application.
        mendeley_object = Mendeley(config['clientId'], config['clientSecret'])

        auth = mendeley_object.start_client_credentials_flow()
        mendeley = auth.authenticate()

        return mendeley

    def get_readership(self, mendeley, dataset):

        total_readers = []
        total_readers_by_country = []
        years = []

        i = 0
        for key, value in dataset.iterrows():
            # we have a doi
            if not pandas.isnull(value['doi']):
                #print('%s' % (value['doi']))
                try:
                    doc = mendeley.catalog.by_identifier(doi=value['doi'], view="stats")
                    total_readers.append(doc.reader_count)
                    total_readers_by_country.append(doc.reader_count_by_country)
                    years.append(doc.year)
                except MendeleyException:
                    print('Document with doi %s not found' % (value['doi']))
                    total_readers.append(np.nan)
                    total_readers_by_country.append(np.nan)
                    years.append(np.nan)
            # we only have the title
            else:
                try:
                    page = mendeley.catalog.advanced_search(title=value['title'], view="stats").list()
                    # we want an exact match
                    #if page.items and page.items[0].title.lower().strip(" .") == value['title'].lower().strip(" ."):
                    if page.items and page.items[0].title == value['title']:
                        total_readers.append(page.items[0].reader_count)
                        total_readers_by_country.append(page.items[0].reader_count_by_country)
                        years.append(page.items[0].year)
                        #print "Matched document %s with %s" % (page.items[0].title, value['title'])
                    else:
                        total_readers.append(np.nan)
                        total_readers_by_country.append(np.nan)
                        years.append(np.nan)
                except MendeleyException:
                    print('Document with title %s not found' % (value['title']))
                    total_readers.append(np.nan)
                    total_readers_by_country.append(np.nan)
                    years.append(np.nan)
            i += 1
            if i % 100 == 0:
                print "Processed %d" % i
                #break

        #doc = mendeley.catalog.by_identifier(doi='10.1186/1471-2180-3-23', view="stats")
        #print "title: %s readers: %d " % (doc.title, doc.reader_count)
        #print doc.reader_count_by_academic_status
        #print doc.reader_count_by_discipline
        #print doc.reader_count_by_country

        return total_readers, total_readers_by_country, years

    def main(self, argv):
        oxford,cambridge = self.load_dataset()
        session = self.init_mendeley_api()

        # total_readers, total_readers_by_country, years = get_readership(session, oxford)
        # #sample
        # #oxford_slice = copy.deepcopy(oxford.head(100))
        # #all
        # oxford_slice = copy.deepcopy(oxford)
        # oxford_slice['year'] = years
        # oxford_slice['total_readers'] = total_readers
        # oxford_slice['total_readers_by_country'] = total_readers_by_country
        # print oxford_slice
        # oxford_slice.to_csv('oxford-results.csv')
        # print oxford_slice.sum()

        total_readers, total_readers_by_country, years = self.get_readership(session, cambridge)
        #sample
        #oxford_slice = copy.deepcopy(oxford.head(100))
        #all
        cambridge_slice = copy.deepcopy(cambridge)
        cambridge_slice['year'] = years
        cambridge_slice['total_readers'] = total_readers
        cambridge_slice['total_readers_by_country'] = total_readers_by_country
        print cambridge_slice
        cambridge_slice.to_csv('cambridge-results.csv')
        print cambridge_slice.sum()


if __name__ == '__main__': sys.exit(main(sys.argv))













