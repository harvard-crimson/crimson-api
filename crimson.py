import requests

BASE_URI = "http://www.thecrimson.com/api/v1/"

class API:
    def __init__(self, key):
        self.results = {}
        self.request_url = ""
        self.key = key

    def search(self, content_type="article", start_date="", end_date = "", 
               ID = [], text = "", title = [], subtitle = [], tags = [], 
               contributors = [], description = [], slug = [], page = 1, 
               fields = []):
        base_url = BASE_URI + content_type + "/?"
        payload = {
            "start_date" : start_date,
            "end_date" : end_date, 
            "ID" : ID,
            "text" : text,
            "title" : title,
            "subtitle" : subtitle,
            "tags" : tags,
            "contributors" : contributors,
            "description" : description,
            "slug" : slug,
            "page" : page,
            "fields" : fields,
            "key" : self.key
        }
        
        self.request_url = create_url(base_url, payload)
#        self.results = requests.get(self.request_url).json()
        print self.request_url
#        return self.results

    def next(self):
        if self.results["next"] != None:
            self.request_url = self.results["next"]
            self.results = requests.get(self.request_url).json()
            return self.results
        else:
            raise MissingPageError("There is no next page of results.")

    def previous(self):
        if self.results["previous"] != None:
            self.request_url = self.results["previous"]
            self.results = requests.get(self.request_url).json()
            return self.results
        else:
            raise MissingPageError("There is no previous page of results.")
        
    def get_articles(self, **kwargs):
        kwargs["content_type"] = "article"
        return self.search(**kwargs)

    def get_images(self, **kwargs):
        kwargs["content_type"] = "image"
        return self.search(**kwargs)

    def get_external_contents(self, **kwargs):
        kwargs["content_type"] = "externalContent"
        return self.search(**kwargs)

    def get_galleries(self, **kwargs):
        kwargs["content_type"] = "gallery"
        return self.search(**kwargs)
        
    def get_videos(self, **kwargs):
        kwargs["content_type"] = "video"
        return self.search(**kwargs)
        
    def get_flash_graphics(self, **kwargs):
        kwargs["content_type"] = "flashGraphic"
        return self.search(**kwargs)
        
    def get_maps(self, **kwargs):
        kwargs["content_type"] = "map"
        return self.search(**kwargs)

def create_url(base_url, payload):
    request_url = base_url
    payload = sanitize(payload)
    
    for key in payload:
        request_url += "{0}={1}&".format(key, payload[key])

    request_url = request_url[:len(request_url) - 1]
    return request_url
    
def sanitize(payload):
    for key in payload:
        value = str(payload[key])
        
        if value == "[]":
            value = "[]"
        elif len(value) > 1 and value[0] == "[" and value[len(value) - 1] == "]":
            value = filter(lambda x : x != "'" and x != "\"", value)
        payload[key] = value
    return payload

class MissingPageError(StandardError):
    pass
    
