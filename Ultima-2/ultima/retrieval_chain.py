from langchain.chains import ConversationalRetrievalChain

from ultima.vector_store import get_vector_store
from ultima.logging import logger
from ultima.models import get_model


def get_chain(
    data_source: str, options: dict, credentials: dict
) -> ConversationalRetrievalChain:
    # create the langchain 
    vector_store = get_vector_store(data_source, options, credentials)
    retriever = vector_store.as_retriever()
    # "fetch_k" and "k" define how many documents are pulled from the hub
    search_kwargs = {
        "maximal_marginal_relevance": options["maximal_marginal_relevance"],
        "distance_metric": options["distance_metric"],
        "fetch_k": options["fetch_k"],
        "k": options["k"],
    }
    retriever.search_kwargs.update(search_kwargs)
    model = get_model(options, credentials)
    chain = ConversationalRetrievalChain.from_llm(
        model,
        retriever=retriever,
        chain_type="stuff",
        verbose=True,
        # limit the maximum number of used tokens
        max_tokens_limit=options["max_tokens"],
    )
    logger.info(f"Chain for data source {data_source} and settings {options} build!")
    return chain
