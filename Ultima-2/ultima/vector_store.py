import deeplake
from langchain.vectorstores import DeepLake, VectorStore

from ultima.shared_arrtibs import DATA_PATH
from ultima.input_output import clean_string_for_storing
from ultima.load_data import load_data_source, split_docs
from ultima.logging import logger
from ultima.models import MODES, get_embeddings


def get_dataset_path(data_source: str, options: dict, credentials: dict) -> str:
    dataset_name = clean_string_for_storing(data_source)
    dataset_name += f"-{options['chunk_size']}-{options['chunk_overlap']}"
    if options["mode"] == MODES.LOCAL:
        dataset_path = str(DATA_PATH / dataset_name)
    else:
        dataset_path = f"hub://{credentials['activeloop_org_name']}/{dataset_name}"
    return dataset_path

def get_vector_store(data_source: str, options: dict, credentials: dict) -> VectorStore:
    embeddings = get_embeddings(options, credentials)
    dataset_path = get_dataset_path(data_source, options, credentials)
    if deeplake.exists(dataset_path, token=credentials["activeloop_token"]):
        logger.info(f"Dataset '{dataset_path}' exists -> loading")
        vector_store = DeepLake(
            dataset_path=dataset_path,
            read_only=True,
            embedding_function=embeddings,
            token=credentials["activeloop_token"],
        )
    else:
        logger.info(f"Dataset '{dataset_path}' does not exist -> uploading")
        docs = load_data_source(data_source)
        docs = split_docs(docs, options)
        vector_store = DeepLake.from_documents(
            docs,
            embeddings,
            dataset_path=dataset_path,
            token=credentials["activeloop_token"],
        )
    logger.info(f"Vector Store {dataset_path} loaded!")
    return vector_store
