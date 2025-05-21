import arxiv
from typing import List, Dict

def search_arxiv(query: str, max_results: int = 5) -> List[Dict]:
    results = []
    pdf_urls = []
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    for result in client.results(search):
        results.append({
            "title": result.title,
            "paper_id": result.get_short_id(),
            "authors": [author.name for author in result.authors],
            "published": result.published.date(),
            "pdf_url": result.pdf_url,
            "entry_id": result.entry_id,
            "source": "arXiv",
            "abstract": result.summary,
            # "obj": result,
        })
        pdf_urls.append({"pdf_url": result.pdf_url})

    return results, pdf_urls
