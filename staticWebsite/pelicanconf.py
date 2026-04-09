AUTHOR = 'Andrew Jarman'
SITENAME = 'Primary Care Demand and Capacity Modelling'
SITEURL = ""

PATH = "content"

TIMEZONE = 'GMT'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("NHS", "https://www.nhs.uk/"),
    ("Suffolk County Council", "https://www.suffolk.gov.uk/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = False

PAGE_ORDER_BY = 'order'

ARTICLE_ORDER_BY = 'order'

THEME = "ns_theme"

FILENAME_METADATA = '(?P<title>.*)'

DEFAULT_DATE = 'fs'

STATIC_PATHS = ['img', 'extras', 'notebooks_html', 'capacity','demand']

EXTRA_PATH_METADATA = {'extras/favicon.ico': {'path': 'favicon.ico'},}

#GITHUB_URL

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True