from dataclasses import dataclass
from typing import Any, List

import streamlit as st
import tiktoken
import torch
from langchain.embeddings import HuggingFaceEmbeddings, HuggingFaceInstructEmbeddings
from InstructorEmbedding import INSTRUCTOR
from langchain.base_language import BaseLanguageModel
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.embeddings.openai import Embeddings, OpenAIEmbeddings
from langchain.llms import GPT4All
from transformers import AutoTokenizer

from ultima.shared_arrtibs import GPT4ALL_BINARY, MODEL_PATH
from ultima.logging import logger


class Enum:
    @classmethod
    def all(cls) -> List[Any]:
        return [v for k, v in cls.__dict__.items() if not k.startswith("_")]


@dataclass
class Model:
    name: str
    mode: str
    embedding: str
    path: str = None  
    def __str__(self) -> str:
        return self.name


class MODES(Enum):
    OPENAI = "API"
    LOCAL = "Local"


class EMBEDDINGS(Enum):
    INSTRUCTOR_XL = "hkunlp/instructor-xl"
    ADA002 = "text-embedding-ada-002"
    HUGGINGFACE = "sentence-transformers/all-MiniLM-L6-v2"
    


class MODELS(Enum):
    # Add more models as needed
    GPT35TURBO = Model(
        name="gpt-3.5-turbo",
        mode=MODES.OPENAI,
        embedding=EMBEDDINGS.INSTRUCTOR_XL,
        )
    GPT4 = Model(name="gpt-4", 
                 mode=MODES.OPENAI, 
                 embedding=EMBEDDINGS.INSTRUCTOR_XL,
                 )
    GPT4ALL = Model(
        name="GPT4All",
        mode=MODES.LOCAL,
        embedding=EMBEDDINGS.HUGGINGFACE,
        path=str(MODEL_PATH / GPT4ALL_BINARY),
    )

    @classmethod
    def for_mode(cls, mode) -> List[Model]:
        return [m for m in cls.all() if isinstance(m, Model) and m.mode == mode]


def get_model(options: dict, credentials: dict) -> BaseLanguageModel:
    match options["model"].name:
        case MODELS.GPT35TURBO.name:
            model = ChatOpenAI(
                model_name=options["model"].name,
                temperature=options["temperature"],
                openai_api_key=credentials["openai_api_key"],
            )
        case MODELS.GPT4.name:
                model = ChatOpenAI(
                    model_name=st.session_state["model"].name,
                    temperature=st.session_state["temperature"],
                    openai_api_key=st.session_state["openai_api_key"],
                )    
        case MODELS.GPT4ALL.name:
            model = GPT4All(
                model=options["model"].path,
                n_ctx=options["model_n_ctx"],
                backend="gptj",
                temp=options["temperature"],
                verbose=True,
                callbacks=[StreamingStdOutCallbackHandler()],
            )

        case _default:
            msg = f"Model {options['model'].name} not supported!"
            logger.error(msg)
            st.error(msg)
            exit
    return model


def get_embeddings(options: dict, credentials: dict) -> Embeddings:
    match options["model"].embedding:
        case EMBEDDINGS.ADA002:
            embeddings = OpenAIEmbeddings(
                model=EMBEDDINGS.ADA002,
                disallowed_special=(),
                openai_api_key=credentials["openai_api_key"],
            )
        case EMBEDDINGS.HUGGINGFACE:
            embeddings = HuggingFaceEmbeddings(
                model_name=EMBEDDINGS.HUGGINGFACE, cache_folder=str(MODEL_PATH)
            )
        case EMBEDDINGS.INSTRUCTOR_XL:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            embeddings = HuggingFaceInstructEmbeddings(
                model_name=EMBEDDINGS.INSTRUCTOR_XL, model_kwargs={"device": device}
                )
        case _default:
            msg = f"Embeddings {options['model'].embedding} not supported!"
            logger.error(msg)
            st.error(msg)
            exit
    return embeddings


def get_tokenizer(options: dict) -> Embeddings:
    match options["model"].embedding:
        case EMBEDDINGS.ADA002:
            tokenizer = tiktoken.encoding_for_model(EMBEDDINGS.ADA002)
        case EMBEDDINGS.HUGGINGFACE:
            tokenizer = AutoTokenizer.from_pretrained(EMBEDDINGS.HUGGINGFACE)
        case EMBEDDINGS.INSTRUCTOR_XL:
            tokenizer = AutoTokenizer.from_pretrained(EMBEDDINGS.INSTRUCTOR_XL)

        case _default:
            msg = f"Tokenizer {options['model'].embedding} not supported!"
            logger.error(msg)
            st.error(msg)
            exit
    return tokenizer
