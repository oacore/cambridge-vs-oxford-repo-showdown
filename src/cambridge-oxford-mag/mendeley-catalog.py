from mendeley import Mendeley
import yaml
import codecs

with open('config.yml') as f:
    config = yaml.load(f)

mendeley = Mendeley(config['clientId'], config['clientSecret'],"http://localhost:5000/oauth")
auth = mendeley.start_authorization_code_flow()

# mendeley_object = Mendeley(config['clientId'], config['clientSecret'])
# auth = mendeley_object.start_client_credentials_flow()
# mendeley = auth.authenticate()

# page = mendeley.catalog.search('"gaia theory" "gaia hypothesis" geophysiology geofysiology daisyworld').list(100)
page = mendeley.catalog.search('"gaia theory" "gaia hypothesis" geophysiology geofysiology daisyworld "daisy world"')

with codecs.open('results.tsv', 'w', 'utf-8') as f:
        for doc in page.iter(20):
            f.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (unicode(doc.title).replace("\n", " "), unicode(doc.year).replace("\n", " "), unicode(doc.abstract).replace("\n", " "), unicode(doc.source).replace("\n", " "), doc.identifiers, doc.link))

# The user needs to visit this URL, and log in to Mendeley.
login_url = auth.get_login_url()
print "Visit the login url: %s " % login_url


x = raw_input("Insert the whole URL to authenticate: ")

session = auth.authenticate(x)

# doi = raw_input('Enter a DOI: ')

# doc = session.catalog.by_identifier(doi=doi, view='stats')
# print '"%s" has %s readers.' % (doc.title, doc.reader_count)

# search_results = session.catalog.search("link discovery")


# profile.me doesn't seem to work
# my mendeley sqlId: 2855421 uuid: 2a3b5b54-e0b1-3b07-aed4-28176475af87
# profiles = session.profiles
# profile = profiles.get('2a3b5b54-e0b1-3b07-aed4-28176475af87')
# print profile.last_name, profile.first_name


# for search_result in search_results.iter(20):
#     print search_result.title

# for f in session.files.iter():
#     print "filename: %s size: %s download_url %s" % (f.file_name, f.size, f.download_url)


