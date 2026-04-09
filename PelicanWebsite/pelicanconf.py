AUTHOR = 'A.Jarman & I.Khan'
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

DEFAULT_PAGINATION = False
THEME = "ns_theme"
STATIC_PATHS = ['img','extras','notebooks-html']
#PAGE_PATHS = ['notebooks-html']

EXTRA_PATH_METADATA = {
    'notebooks-html/1a_AppointmentDuration.html': {'path': '1a_AppointmentDuration.html'},
    'notebooks-html/1c_DemographicPopGrowth.html': {'path': '1c_DemographicPopGrowth.html'},
    'notebooks-html/Referral_rate_2_sankey.html': {'path': 'Referral_rate_2_sankey.html'},
    'notebooks-html/Referral_rate_4_sankey.html': {'path': 'Referral_rate_4_sankey.html'},
}

ARTICLE_EXCLUDES = ['notebooks-html']


# # Blogroll
# LINKS = (
#     ("Pelican", "https://getpelican.com/"),
#     ("NHS", "https://www.nhs.uk/"),
#     ("Suffolk County Council", "https://www.suffolk.gov.uk/"),
#     ("Jinja2", "https://palletsprojects.com/p/jinja/")
# )

# # Social widget
# SOCIAL = (
#     ("You can add links in your config file", "#"),
#     ("Another social link", "#"),
# )


# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True