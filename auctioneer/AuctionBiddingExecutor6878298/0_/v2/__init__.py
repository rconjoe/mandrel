from jina import Executor, requests as jina_requests, DocumentArray
import json

from .microservice import func


class AuctionBiddingExecutor6878298(Executor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @jina_requests()
    def endpoint(self, docs: DocumentArray, **kwargs) -> DocumentArray:
        for d in docs:
            d.text = func(d.text)
        return docs
