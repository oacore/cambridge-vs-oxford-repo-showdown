from mendeley import Mendeley
from mendeley.exception import MendeleyException
import yaml
import pandas
import sys
import math
import numpy as np
import copy


def load_dataset():
    oxford = pandas.io.parsers.read_csv("oxford.csv", sep=',')
    cambridge = pandas.io.parsers.read_csv("cambridge.csv", sep=',')

    return (oxford, cambridge)


def init_mendeley_api():
    with open('config.yml') as f:
        config = yaml.load(f)

    # These values should match the ones supplied when registering your application.
    mendeley_object = Mendeley(config['clientId'], config['clientSecret'])

    auth = mendeley_object.start_client_credentials_flow()
    mendeley = auth.authenticate()

    return mendeley


def get_readership(mendeley, dataset):
    total_readers = []
    total_readers_by_country = []
    years = []
    dois = []

    i = 0
    for key, value in dataset.iterrows():
        # we have a doi
        if not pandas.isnull(value['DOI']):
            # print('%s' % (value['doi']))
            try:
                doc = mendeley.catalog.by_identifier(doi=value['DOI'], view="stats")
                total_readers.append(doc.reader_count)
                total_readers_by_country.append(doc.reader_count_by_country)
                years.append(doc.year)
                dois.append(np.nan)
            except MendeleyException:
                print('Document with doi %s not found' % (value['DOI']))
                total_readers.append(np.nan)
                total_readers_by_country.append(np.nan)
                years.append(np.nan)
                dois.append(np.nan)
        # we only have the title
        else:
            try:
                page = mendeley.catalog.advanced_search(title=value['title'], view="stats").list()
                # we want an exact match
                # if page.items and page.items[0].title.lower().strip(" .") == value['title'].lower().strip(" ."):
                if page.items and page.items[0]:
                    titleMendeley = page.items[0].title.replace("[^A-Za-z]", "").lower().encode('ascii', 'ignore')
                    titleCore = str(value["Title"]).replace("[^A-Za-z]", "").lower().encode('ascii', 'ignore')
                    # print titleMendeley
                    # print titleCore
                    ratio = SequenceMatcher(None, titleMendeley, titleCore).ratio()
                    # print ratio
                    identifiers = page.items[0].identifiers
                    if ratio > 0.8:
                        total_readers.append(page.items[0].reader_count)
                        total_readers_by_country.append(page.items[0].reader_count_by_country)
                        years.append(page.items[0].year)
                        if identifiers and "doi" in identifiers:
                            dois.append(identifiers['doi'])
                            print ("DOI!")
                    else:
                        total_readers.append(np.nan)
                        total_readers_by_country.append(np.nan)
                        years.append(np.nan)
                        dois.append(np.nan)
                        # print "Matched document %s with %s" % (page.items[0].title, value['title'])
                else:
                    total_readers.append(np.nan)
                    total_readers_by_country.append(np.nan)
                    years.append(np.nan)
                    dois.append(np.nan)
            except MendeleyException:
                print('Document with title %s not found' % (value['Title']))
                total_readers.append(np.nan)
                total_readers_by_country.append(np.nan)
                years.append(np.nan)
                dois.append(np.nan)
        i += 1
        if i % 100 == 0:
            print ("Processed %d" % i)
            # break

            # doc = mendeley.catalog.by_identifier(doi='10.1186/1471-2180-3-23', view="stats")
            # print "title: %s readers: %d " % (doc.title, doc.reader_count)
            # print doc.reader_count_by_academic_status
            # print doc.reader_count_by_academic_status
            # print doc.reader_count_by_discipline
            # print doc.reader_count_by_country

    return total_readers, total_readers_by_country, years, dois


def main(argv):
    oxford, cambridge = load_dataset()
    session = init_mendeley_api()

    # total_readers, total_readers_by_country, years = get_readership(session, oxford)
    # #sample
    # oxford_slice = copy.deepcopy(oxford.head(100))
    # #all
    # oxford_slice = copy.deepcopy(oxford)
    # oxford_slice['year'] = years
    # oxford_slice['total_readers'] = total_readers
    # oxford_slice['total_readers_by_country'] = total_readers_by_country
    # print oxford_slice
    # oxford_slice.to_csv('oxford-results.csv')
    # print oxford_slice.sum()

    total_readers, total_readers_by_country, years, dois = get_readership(session, cambridge)
    # sample
    # oxford_slice = copy.deepcopy(oxford.head(100))
    # all
    cambridge_slice = copy.deepcopy(cambridge)
    cambridge_slice['year'] = years
    cambridge_slice['total_readers'] = total_readers
    cambridge_slice['total_readers_by_country'] = total_readers_by_country
    cambridge_slice["discovered_doi"] = dois
    print (cambridge_slice)


# cambridge_slice.to_csv('cambridge-results.csv')
# print cambridge_slice.sum()


if __name__ == '__main__': sys.exit(main(sys.argv))

