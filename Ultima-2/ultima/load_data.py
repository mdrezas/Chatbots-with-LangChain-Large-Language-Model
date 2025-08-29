import os
import shutil
from pathlib import Path
from typing import List

from langchain.document_loaders import (
    CSVLoader,
    GitLoader,
    OnlinePDFLoader,
    PDFMinerLoader,
    TextLoader,
    UnstructuredFileLoader,
    WebBaseLoader,
)
from langchain.document_loaders.base import BaseLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter, NLTKTextSplitter,  CharacterTextSplitter
from tqdm import tqdm

from ultima.shared_arrtibs import DATA_PATH, PROJECT_URL
from ultima.logging import logger
from ultima.models import get_tokenizer

FILE_LOADER_MAPPING = {
    ".csv": (CSVLoader, {"encoding": "utf-8"}),
    ".pdf": (PDFMinerLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
}

WEB_LOADER_MAPPING = {
    ".pdf": (OnlinePDFLoader, {}),
}

def load_document(
    file_path: str,
    mapping: dict = FILE_LOADER_MAPPING,
    default_loader: BaseLoader = UnstructuredFileLoader,
) -> Document:
    ext = "." + file_path.rsplit(".", 1)[-1]
    if ext in mapping:
        loader_class, loader_args = mapping[ext]
        loader = loader_class(file_path, **loader_args)
    else:
        loader = default_loader(file_path)
    return loader.load()


def load_directory(path: str, silent_errors=True) -> List[Document]:
    all_files = list(Path(path).rglob("**/[!.]*"))
    results = []
    with tqdm(total=len(all_files), desc="Loading documents", ncols=80) as pbar:
        for file in all_files:
            try:
                results.extend(load_document(str(file)))
            except Exception as e:
                if silent_errors:
                    logger.error(f"failed to load {file}")
                else:
                    raise e
            pbar.update()
    return results


def load_data_source(data_source: str) -> List[Document]:
    is_web = data_source.startswith("http")
    is_dir = os.path.isdir(data_source)
    is_file = os.path.isfile(data_source)
    docs = None
    try:
        if is_dir:
            docs = load_directory(data_source)
        elif is_file:
            docs = load_document(data_source)
        elif is_web:
            docs = load_document(data_source, WEB_LOADER_MAPPING, WebBaseLoader)
        return docs
    except Exception as e:
        error_msg = f"Failed to load your data source '{data_source}'. Consider contributing: {PROJECT_URL}"
        logger.error(error_msg)
        e.args += (error_msg,)
        raise e


def split_docs(docs: List[Document], options: dict) -> List[Document]:
    tokenizer = get_tokenizer(options)

    def length_function(text: str) -> int:
        return len(tokenizer.encode(text))

    text_splitter = RecursiveCharacterTextSplitter(
    #text_splitter = NLTKTextSplitter(
    #text_splitter =  CharacterTextSplitter( 
        chunk_size=options["chunk_size"],
        chunk_overlap=options["chunk_overlap"],
        length_function=length_function,
    )

    splitted_docs = text_splitter.split_documents(docs)
    logger.info(f"Loaded: {len(splitted_docs)} document chucks")
    return splitted_docs

