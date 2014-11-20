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

    devices = {}
    for photo in photos:
        device = getCameraInfo(photo)
        cur = devices.get(device, 0)
        devices[device] = cur + 1

    freqs = [(v, k[0], k[1]) for k, v in devices.iteritems()]
    freqs.sort(reverse=True)


def getCameraInfo(photo):
    ''' Takes a Photo from flickr_api and returns the make and model of the
        device it was taken with. Sometimes those may be None. '''

    try:
        exif_tags = photo.getExif()
    except flickr_api.flickrerrors.FlickrAPIError as e:
        if 2 == e.code: # User disabled EXIF access for their photos.
            exif_tags = []
        else: raise

    make = model = None

    # linear search through the tags.
    make_encountered = model_encountered = False
    for e in exif_tags:
        if 'make' == e.tag.lower():
            make = e.raw.strip()
            make_encountered = True
        elif 'model' == e.tag.lower():
            model = e.raw.strip()
            model_encountered = True

        if make_encountered and model_encountered:
            break

    return (make, model)


def findPhotos():
    ''' Gets a list of photos that are creative commons. '''

    # content_type 1 means "photo".
    # see https://www.flickr.com/services/api/flickr.photos.search.html
    return flickr_api.Photo.search(content_type=1, is_commons=True)

if '__main__' == __name__:
    main()
