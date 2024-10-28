# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys

sys.path.append(os.curdir)

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITENAME = 'Primary Care Demand and Capacity Modelling'
SITEURL = "http://snee-ics.github.io/primarycaredemandandcapacity"
RELATIVE_URLS = False

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

DELETE_OUTPUT_DIRECTORY = True
THEME = "snee_theme"
PATH = 'content'
TIMEZONE = 'GMT'
STATIC_PATHS = ['img','extras','notebooks-html']
#PAGE_PATHS = ['notebooks-html']
PAGE_ORDER_BY = 'order'
ARTICLE_ORDER_BY = 'order'

TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 5

EXTRA_PATH_METADATA = {
    'notebooks-html/1a_AppointmentDuration.html': {'path': '1a_AppointmentDuration.html'},
    'notebooks-html/1c_DemographicPopGrowth.html': {'path': '1c_DemographicPopGrowth.html'},
    'notebooks-html/Referral_rate_2_sankey.html': {'path': 'Referral_rate_2_sankey.html'},
    'notebooks-html/Referral_rate_4_sankey.html': {'path': 'Referral_rate_4_sankey.html'},
}

ARTICLE_EXCLUDES = ['notebooks-html']


# Following items are often useful when publishing

# DISQUS_SITENAME = ""
# GOOGLE_ANALYTICS = ""