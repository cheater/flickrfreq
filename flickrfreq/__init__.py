#!/usr/bin/env python

import ConfigParser
import flickrapi

def main():
    ''' Runs the search and prints statistics.
        Requires a file called flickr.ini in the pwd, with those contents:

        8<-------------------------------------

        [Flickr]
        api_key=your-api-key
        api_secret=your-api-secret

        8<-------------------------------------

        '''

    cfg = ConfigParser.ConfigParser()
    cfg.read('flickr.ini')
    c = cfg.get

    photos = findPhotos(
        c('Flickr', 'api_key'), c('Flickr', 'api_secret'))


def findPhotos(api_key, api_secret):
    ''' Gets a list of photos that are creative commons. '''
    flickr = flickrapi.FlickrAPI(api_key, api_secret)

    # content_type 1 means "photo".
    # see https://www.flickr.com/services/api/flickr.photos.search.html
    return flickr.walk(content_type=1, is_commons=True)

if '__main__' == __name__:
    main()
