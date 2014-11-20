flickrfreq downloads 100 Flickr photos and prints statistics on what devices (cameras) were used.

You have to install flickr_api and texttable to use it.


Requires a file called flickr.ini in the pwd, with those contents:

	[Flickr]
	api_key=your-api-key
	api_secret=your-api-secret
	use=True
	
	[Local]
	db=flickrfreq.db

Execute with python -m flickrfreq.
