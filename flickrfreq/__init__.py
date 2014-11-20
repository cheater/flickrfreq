#!/usr/bin/env python
''' This program makes statistics on Flickr photos. You have to install
    flickr_api to use it.
    '''

import ConfigParser
import flickr_api

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
    flickr_api.set_keys(c('Flickr', 'api_key'), c('Flickr', 'api_secret'))
    photos = findPhotos()


def findPhotos():
    ''' Gets a list of photos that are creative commons. '''

    # content_type 1 means "photo".
    # see https://www.flickr.com/services/api/flickr.photos.search.html
    return flickr_api.Photo.search(content_type=1, is_commons=True)

if '__main__' == __name__:
    main()
