import requests
import json

BASE_URI = "http://www.thecrimson.com/api/v1/"


class API(object):
    def __init__(self, key):
        self.results = {}
        self.request_url = ""
        self.key = key

    def search(self, content_type="article", start_date=None, end_date=None,
               ID=None, text=None, title=None, subtitle=None, tags=None,
               contributors=None, description=None, slug=None, page=1,
               fields=None, section=None, contributor_ids=None, tag_ids=None,
               sort=None, name=None):
        base_url = BASE_URI + content_type
        payload = {
            "start_date": start_date,
            "end_date": end_date,
            "id": ID,
            "text": text,
            "title": title,
            "subtitle": subtitle,
            "tags": tags,
            "contributors": contributors,
            "description": description,
            "slug": slug,
            "page": page,
            "fields": fields,
            "key": self.key,
            "section": section,
            "contributor_ids": contributor_ids,
            "tag_ids": tag_ids,
            "sort": sort,
            "name": name
        }

        payload = sanitize(payload)
        request = requests.get(base_url, params=payload)
        if request.status_code == 403:
            raise InvalidKeyError("The API key is not valid.")
        self.results = request.json()

        return self.results

    def next(self):
        if self.results["next"] is not None:
            self.results = requests.get(self.results["next"]).json()
            return self.results
        else:
            raise MissingPageError("There is no next page of results.")

    def previous(self):
        if self.results["previous"] is not None:
            self.results = requests.get(self.results["previous"]).json()
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
        kwargs["content_type"] = "externalcontent"
        return self.search(**kwargs)

    def get_galleries(self, **kwargs):
        kwargs["content_type"] = "gallery"
        return self.search(**kwargs)

    def get_videos(self, **kwargs):
        kwargs["content_type"] = "video"
        return self.search(**kwargs)

    def get_flash_graphics(self, **kwargs):
        kwargs["content_type"] = "flashgraphic"
        return self.search(**kwargs)

    def get_maps(self, **kwargs):
        kwargs["content_type"] = "map"
        return self.search(**kwargs)

    def get_contributors(self, **kwargs):
        kwargs["content_type"] = "contributor"
        return self.search(**kwargs)

    def get_tags(self, **kwargs):
        kwargs["content_type"] = "tag"
        return self.search(**kwargs)

    def get_sections(self, **kwargs):
        kwargs["content_type"] = "section"
        return self.search(**kwargs)


def sanitize(payload):
    for key in payload:
        value = payload[key]
        if type(value) == list or type(value) == tuple:
            payload[key] = json.dumps(value)
    return payload


class MissingPageError(StandardError):
    pass


class InvalidKeyError(StandardError):
    pass
