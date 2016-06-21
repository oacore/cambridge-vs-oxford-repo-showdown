from mendeley import Mendeley
from mendeley.exception import MendeleyException
import yaml
import logging
import csv
import sys
import codecs

class ArticleLookup:

    def init_mendeley_api(self):
        with open('config.yml') as f:
            config = yaml.load(f)

        # These values should match the ones supplied when registering your application.
        mendeley_object = Mendeley(config['clientId'], config['clientSecret'])

        auth = mendeley_object.start_client_credentials_flow()
        mendeley = auth.authenticate()

        return mendeley

    def get_metadata(self, mendeley, path, output_path, skip_lines, logfilename):

        with codecs.open(output_path, 'a', 'utf-8') as output_file:

            with open(path) as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',')

                i = 0
                for row in reader:

                    if i < skip_lines:
                        i += 1
                        continue

                    try:
                        doc = mendeley.catalog.by_identifier(doi=row['DOI'], view="stats")
                        if doc.abstract:
                            abstract = doc.abstract
                        else:
                            abstract = ""

                        if doc.title:
                            title = doc.title
                        else:
                            title = ""

                        if doc.reader_count:
                            reader_count = doc.reader_count
                        else:
                            reader_count = -1

                        if doc.year:
                            year = doc.year
                        else:
                            year = -1

                        # print "abstract: %s" % doc.abstract
                        output_file.write("%s\t%s\t%s\t%s\t%d\t%d\n" % (row['DOI'].decode('utf-8'), row['MAGID'].decode('utf-8'), unicode(title).replace("\n", " "), unicode(abstract).replace("\n", " "), reader_count, year))
                    except MendeleyException:
                        abstract = ""

                    with open(logfilename, 'w') as logfile:
                        logfile.write("%d" % i)

                    i += 1

                    if i % 1 == 0:
                        print "Processed %d" % i

        return

def main(config):
    al = ArticleLookup()
    session = al.init_mendeley_api()

    al.get_metadata(session, config['dois_path'], config['output_path'], config['skip_lines'], config['logfilename'])
    print "Success!"

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format='[%(asctime)s] %(levelname)s: %(message)s')

    with open(sys.argv[1]) as f:
        config = yaml.load(f)

    main(config)














