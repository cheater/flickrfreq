#!/usr/bin/env python
''' This program makes statistics on Flickr photos. You have to install
    flickr_api to use it.
    '''

import ConfigParser
import flickr_api
import texttable
import sys
import pickle
import os

def main():
    ''' Runs the search and prints statistics.
        Requires a file called flickr.ini in the pwd, with those contents:

        8<-------------------------------------

        [Flickr]
        api_key=your-api-key
        api_secret=your-api-secret
        use=True

        [Local]
        db=flickrfreq.db

        8<-------------------------------------

        'use' is a boolean flag which tells the program if it should load new
        data from Flickr or just use the existing database.

        'db' is the file name for the database.

        '''

    config = ConfigParser.ConfigParser()
    config.read('flickr.ini')

    new_devices = {}
    if config.getboolean('Flickr', 'use'):
        print 'Getting new EXIF data from Flickr...'
        new_devices = getDevices(
            config.get('Flickr', 'api_key'), config.get('Flickr', 'api_secret'))

    db_fname = config.get('Local', 'db')
    old_devices = {}
    if os.path.exists(db_fname):
        db = open(db_fname, 'r+')
        print 'Restoring EXIF data from ' + db_fname
        old_devices = pickle.load(db)
        db.close()

    devices = {}
    for k in set(old_devices.keys() + new_devices.keys()):
        devices[k] = old_devices.get(k, 0) + new_devices.get(k, 0)

    # save data to file
    db = open(db_fname, 'w+')
    db.truncate(0)
    pickle.dump(devices, db)
    db.flush()
    db.close()

    freqs = [(v, k[0], k[1]) for k, v in devices.iteritems()]
    freqs.sort(reverse=True)

    table = texttable.Texttable()
    table.add_rows([('Frequency', 'Make', 'Model')] + freqs)

    print ''
    print table.draw()


def getDevices(api_key, api_secret):
    ''' Gets the frequencies of devices used to make photos from a sample of
        photos obtained from Flickr. '''

    flickr_api.set_keys(api_key, api_secret)
    photos = findPhotos()

    devices = {}
    count = 0
    for photo in photos:
        count = count + 1
        device = getCameraInfo(photo)
        cur = devices.get(device, 0)
        devices[device] = cur + 1
        sys.stdout.write('\rGot EXIF for photo #%d.' % count)
        sys.stdout.flush()
    sys.stdout.write('\r\n')
    sys.stdout.flush()

    return devices


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
    # We need to make the model and make normal strings, or pickle bugs out.
    make_encountered = model_encountered = False
    for e in exif_tags:
        if 'make' == e.tag.lower():
            make = str(e.raw.strip())
            make_encountered = True
        elif 'model' == e.tag.lower():
            model = str(e.raw.strip())
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
