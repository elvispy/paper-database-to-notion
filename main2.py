"""
given title or arxiv id, search the paper using arxiv api,

"""

import os, re, logging
import arxiv
from arxiv import Client, HTTPError, UnexpectedEmptyPageError
from datetime import datetime, timedelta
import feedparser
import requests
import rich.pretty
import json
import time

rich.pretty.install()

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a file handler
file_handler = logging.FileHandler("fetch.log", mode="a")
file_handler.setLevel(logging.INFO)

# Create a console (stream) handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Define a common formatter
formatter = logging.Formatter(
    "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

CONFIG_FILE = os.path.expanduser("~/.paper-database-to-notion/config.json")
def load_configs():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return {}
CONFIGS = load_configs()


http_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"}

class MyClient(Client):
    def __init__(self, *args, headers=None,**kwargs):
        super().__init__(*args, **kwargs)
        self.headers = headers or {}
    
    def __try_parse_feed(
        self,
        url: str,
        first_page: bool,
        try_index: int,
    ) -> feedparser.FeedParserDict:
        """
        Recursive helper for _parse_feed. Enforces `self.delay_seconds`: if that
        number of seconds has not passed since `_parse_feed` was last called,
        sleeps until delay_seconds seconds have passed.
        """
        # If this call would violate the rate limit, sleep until it doesn't.
        if self._last_request_dt is not None:
            required = timedelta(seconds=self.delay_seconds)
            since_last_request = datetime.now() - self._last_request_dt
            if since_last_request < required:
                to_sleep = (required - since_last_request).total_seconds()
                logging.info("Sleeping: %f seconds", to_sleep)
                time.sleep(to_sleep)

        logging.info("Requesting page (first: %r, try: %d): %s", first_page, try_index, url)

        resp = self._session.get(url, headers=self.headers)
        self._last_request_dt = datetime.now()
        if resp.status_code != requests.codes.OK:
            raise HTTPError(url, try_index, resp.status_code)

        feed = feedparser.parse(resp.content)
        if len(feed.entries) == 0 and not first_page:
            raise UnexpectedEmptyPageError(url, try_index, feed)

        if feed.bozo:
            logging.warning(
                "Bozo feed; consider handling: %s",
                feed.bozo_exception if "bozo_exception" in feed else None,
            )

        return feed

def auto_fetch_workflow(params):
    query = params['query']
    project = params.get('project', 'uncategorized')
    result = search(query)
    if result.status_code == 200:
        CONFIGS = load_configs() if CONFIGS == {} else CONFIGS
        dirpath = os.path.join(CONFIGS.get("download_dir", "./papers"), project)
        os.makedirs(dirpath, exist_ok=True)
        filename = result.entry_id.split("/")[-1] + ".pdf"
        try:
            if not os.path.exists(os.path.join(dirpath, filename)):
                download_response = requests.get(result.pdf_url, headers=http_headers)
                with open(os.path.join(dirpath, filename), "wb") as f:
                    f.write(download_response.content)
                download_log = f"downloaded {filename}"
            else:
                download_log = f"file {filename} already exists"
        except Exception as e:
            download_log = f"Couldnt download because of {e}"
        logging.info(download_log)
        notion_log = push_to_notion(result, tags=params.get("tags", []))

        return "\n\n".join([download_log, notion_log])
    return result.msg

def search(text: str) -> arxiv.Result:
    """given title or arxiv id, search the paper using arxiv api,

    Args:
        text str: the query

    Returns:
        reults type or None
    """
    client = MyClient(headers=http_headers)
    logging.info(f"searching for {text}")
    results = MyClient(); results.msg = ""; results.status_code = 200
    arxiv_bool = True
    if "semanticscholar" in text or "doi.org" in text:
        arxiv_bool = False
        if "doi.org" in text:
            paperId = f"doi:{re.sub(r'https://doi\.org/', '', text)}"
        else:
            paperId = re.search(r'/([a-f0-9])$', text).group(1)
        # Define the API endpoint URL
        url = f"http://api.semanticscholar.org/graph/v1/paper/{paperId}"
        # Define the query parameters
        query_params = {"fields": "title,url,publicationDate,abstract,openAccessPdf,tldr,citationStyles"}
        # Send the API request
        response = requests.get(url, params=query_params)
        # Check response status
        if response.status_code == 200:
            response_data = response.json()
            # Process and print the response data as needed
            results.entry_id = response_data['url']
            results.title = response_data['title']
            results.summary = next((x for x in [response_data['abstract'], (response_data['tldr'] or {}).get('text', '-')] if x not in [None, '']), None)
            results.updated = datetime.strptime(response_data['publicationDate'], "%Y-%m-%d") if response_data['publicationDate'] else datetime.today()
            results.pdf_url = response_data['openAccessPdf']['url'] if (response_data['openAccessPdf'] is not None) else None            
            results.bibtex = response_data['citationStyles']['bibtex']
        else:
            results.status_code = response.status_code
            results.msg = f"Request failed with status code {response.status_code}: {response.text}"
            logging.info(f"Request failed with status code {response.status_code}: {response.text}")
        #return results

        
    elif re.search(r"arxiv", text): #re.match(r".+?(abs|pdf|html)\/\d+.\w+", text):
        # case of url, abs/arxiv_id or pdf/arxiv_id
        arxiv_id = re.search(r'arxiv\.org/(abs|pdf)/((\d{4}\.\d{4,5})|([a-z\-]+/\d{7}))(v\d+)?', text).group(2)
        search_by_id = arxiv.Search(id_list=[arxiv_id])
        results = client.results(search_by_id)
    else:
        search = arxiv.Search(
            query=text, max_results=1, sort_by=arxiv.SortCriterion.Relevance
        )
        results = client.results(search)

    if arxiv_bool == True:
        try:
            results = next(results)
            if results.doi != None:
                res = search(f"https://doi.org/{results.doi}")
                results.bibtex = res.bibtex
            else:
                results.bibtex = ""
            results.status_code = 200
        except Exception as e:
            logging.error(f"search error: {e}")
            results.status_code = 404
            results.msg = f"search error: {e}"
    return results



def semantic_scholar_title_search(text, sleep=10, max_retry=3):
    query_url = (
        "https://api.semanticscholar.org/graph/v1/paper/search/match?query={query}"
    )
    SS_KEY = CONFIGS.get("ss_key", None)
    headers = {"x-api-key": SS_KEY} if SS_KEY else {}
    try:
        response = requests.get(query_url.format(query=text), headers=headers).json()
        if response.get("data", False) and response["data"]:
            logging.info(
                f"SS search title found for {text}, paper id is {response['data'][0]['paperId']}"
            )
            return response["data"][0]["paperId"]
        elif response.get("error", False):
            logging.error(f"SS search title error: {response['error']} for {text}")
            return None
        elif response.get("message", False):
            logging.warning(f"SS search title error: {response['message']} for {text}")
            if "Too Many Requests" in response["message"]:
                time.sleep(sleep)
                return (
                    semantic_scholar_title_search(text, sleep, max_retry - 1)
                    if max_retry > 0
                    else None
                )
        else:
            return None
    except Exception as e:
        logging.error(f"SS search title error: {e} for {text}")
        return None


def semantic_scholar_get_paper(paperId, sleep=10, max_retry=3):
    SS_KEY = CONFIGS.get("ss_key", None)
    headers = {"x-api-key": SS_KEY} if SS_KEY else {}
    try:
        detail_query = f"https://api.semanticscholar.org/graph/v1/paper/{paperId}?fields=citationStyles"
        detail_response = requests.get(detail_query, headers=headers).json()
        if detail_response.get("citationStyles", False):
            logging.info(f"SS citation found for {paperId}")
            return detail_response
        elif detail_response.get("message", False):
            logging.warning(f"SS error: {detail_response['message']} for {paperId}")
            if "Too Many Requests" in detail_response["message"]:
                time.sleep(sleep)
                return (
                    semantic_scholar_get_paper(paperId, sleep, max_retry - 1)
                    if max_retry > 0
                    else None
                )
        else:
            logging.error(f"SS error: {detail_response} for {paperId}")
            return None
    except Exception as e:
        logging.error(f"semantic_scholar error: {e} for {paperId}")
        return None


def semantic_scholar_search(text, sleep=10, max_retry=3):
    """api doc
    https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/get_graph_get_paper
    search title first to get paperId, then get the citationStyles
    """
    logging.info(f"semantic_scholar searching for {text}")
    paperId = semantic_scholar_title_search(text, sleep, max_retry)
    return semantic_scholar_get_paper(paperId, sleep, max_retry) if paperId else None


def push_to_notion(result, tags=[]):
    """push the result to notion

    Args:
        result (arxiv.Result): the result from arxiv api
    """
    NOTION_TOKEN = CONFIGS.get("notion_token", None)
    NOTION_DATABASE_ID = CONFIGS.get("notion_database_id", None)
    assert NOTION_TOKEN, "NOTION_TOKEN not found"
    assert NOTION_DATABASE_ID, "NOTION_DATABASE_ID not found"

    query_url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    #shema_url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}"
    create_url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }


    # query if database already have items
    query = {
        "filter": {
            "property": "URL",
            "url": {"equals": result.entry_id},
        }
    }
    response = requests.post(query_url, headers=headers, data=json.dumps(query)).json()
    if len(response["results"]) > 0:
        notion_log = "already exists in notion"
        logging.info(notion_log)
        return notion_log

    item_data = {
        "Date": {"type": "date", "date": {"start": str(result.updated.date())}},
        "level": {
            "type": "select",
            "select": None,
        },
        "abs": {
            "type": "rich_text",
            "rich_text": [{"type": "text", "text": {"content": result.summary}}],
        },
        "bib": {
            "type": "rich_text",
            "rich_text": [{"type": "text", "text": {"content": result.bibtex}}],
        },
        "alias": {"type": "rich_text", "rich_text": []},
        "my summary": {
            "type": "rich_text",
            "rich_text": [],
        },
        "review": {"type": "url", "url": None},
        "URL": {"type": "url", "url": result.entry_id},
        "pub": {"type": "rich_text", "rich_text": []},
        "Tags": {
            "type": "multi_select",
            "multi_select": [{"name": tag} for tag in tags],
        },
        "path": {
            "type": "rich_text",
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": result.entry_id.split("/")[-1] + ".pdf"},
                }
            ],
        },
        "status": {
            "type": "select",
            "select": {
                "name": "toread",
                "color": "red",
                "description": None,
            },
        },
        "Name": {
            "type": "title",
            "title": [{"type": "text", "text": {"content": result.title}}],
        },
    }

    response = requests.post(
        create_url,
        headers=headers,
        data=json.dumps(
            {
                "parent": {"type": "database_id", "database_id": NOTION_DATABASE_ID},
                "properties": item_data,
            }
        ),
    )

    if response.status_code == 200:
        notion_log = "pushed to notion successfully"
        logging.info(notion_log)
    else:
        notion_log = f"pushed to notion failed, {response.text}"
        logging.error(notion_log)
    return notion_log


if __name__ == '__main__':
    
    auto_fetch_workflow(
        {
            "query":'https://doi.org/10.1016/j.bej.2024.109523',
            "project": "Bioreactor",
            "tags": ["CFD", "Bioreactor"]
        })
    
    #auto_fetch_workflow('https://arxiv.org/abs/cond-mat/0212151')
    #auto_fetch_workflow('https://doi.org/10.1016/j.cma.2007.07.016')
    
    #auto_fetch_workflow(r'https://www.semanticscholar.org/paper/Isogeometric-analysis-of-free-surface-flow-Akkerman-Bazilevs/da79e397f4445827b02c138f9e1c5c993b0aecbf')
