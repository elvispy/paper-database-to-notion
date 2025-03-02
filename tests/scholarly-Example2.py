from scholarly import ProxyGenerator, scholarly

# Set up a ProxyGenerator object to use free proxies
# This needs to be done only once per session
pg = ProxyGenerator()
pg.FreeProxies()
scholarly.use_proxy(pg)

# Now search Google Scholar from behind a proxy
search_query = scholarly.search_pubs('Perception of physical stability and center of mass of 3D objects')
scholarly.pprint(next(search_query))