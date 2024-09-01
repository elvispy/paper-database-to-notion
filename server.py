from fastapi import FastAPI
from main import auto_fetch_workflow, make_bibtex, refresh_bib
import logging
logging.basicConfig(level=logging.INFO, filename="fetch.log", filemode="a", format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")


app = FastAPI()


@app.get("/autofetch")
def process_qeury(q:str):
    return auto_fetch_workflow(q)


@app.get("/bibtex")
def get_bibtex_api(refresh:bool=False, all=False):
    if refresh:
        return refresh_bib(all=all)
    else:
        return make_bibtex()