import os

import deeplake
import openai
import streamlit as st
from dotenv import load_dotenv
from langchain.callbacks import OpenAICallbackHandler, get_openai_callback

from ultima.retrieval_chain import get_chain
from ultima.shared_arrtibs import (
    ACTIVELOOP_HELP,
    AUTHENTICATION_HELP,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    DEFAULT_DATA_SOURCE,
    DISTANCE_METRIC,
    ENABLE_ADVANCED_OPTIONS,
    ENABLE_LOCAL_MODE,
    FETCH_K,
    LOCAL_MODE_DISABLED_HELP,
    MAX_TOKENS,
    MAXIMAL_MARGINAL_RELEVANCE,
    MODE_HELP,
    MODEL_N_CTX,
    OPENAI_HELP,
    PAGE_ICON,
    PROJECT_URL,
    TEMPERATURE,
    K,
)
from ultima.input_output import delete_files, save_files
from ultima.logging import logger
from ultima.models import MODELS, MODES

# loads environment variables
load_dotenv()


def initialize_session_state():
    # Initialise all session state variables with defaults
    SESSION_DEFAULTS = {
        "past": [],
        "usage": {},
        "chat_history": [],
        "generated": [],
        "auth_ok": False,
        "chain": None,
        "openai_api_key": None,
        "activeloop_token": None,
        "activeloop_org_name": None,
        "uploaded_files": None,
        "info_container": None,
        "data_source": DEFAULT_DATA_SOURCE,
        "mode": MODES.OPENAI,
        "model": MODELS.GPT4,
        "k": K,
        "fetch_k": FETCH_K,
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "model_n_ctx": MODEL_N_CTX,
        "distance_metric": DISTANCE_METRIC,
        "maximal_marginal_relevance": MAXIMAL_MARGINAL_RELEVANCE,
    }

    for k, v in SESSION_DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v


def authentication_form() -> None:
    # widget for authentication input form
    st.title("Authentication", help=AUTHENTICATION_HELP)
    with st.form("authentication"):
        openai_api_key = st.text_input(
            f"{st.session_state['mode']} Key",
            type="password",
            help=OPENAI_HELP,
            placeholder="This field is mandatory",
        )
        activeloop_token = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY5MDAyMDU2NiwiZXhwIjoxNjkzNDc2NTM4fQ.eyJpZCI6InB1enpsZTAwNyJ9.UBZdkCROZnZCz-V7CFJNppKrsRdiy1aPQTNFuTqtMWKYgg_AvoHkCJ4SUoOjOyfxsl3EyO65zUawYIlhJzqaKA'
        activeloop_org_name = 'puzzle007'
        submitted = st.form_submit_button("Submit")
        if submitted:
            authenticate(openai_api_key, activeloop_token, activeloop_org_name)

def app_can_be_started():
    return st.session_state["auth_ok"] or st.session_state["mode"] == MODES.LOCAL


def update_model_on_mode_change():
    st.session_state["model"] = MODELS.for_mode(st.session_state["mode"])[0]
    if not st.session_state["chain"] is None and app_can_be_started():
        update_chain()


def authentication_and_options_side_bar():
    with st.sidebar:
        mode='API'
        if mode == MODES.LOCAL and not ENABLE_LOCAL_MODE:
            st.error(LOCAL_MODE_DISABLED_HELP, icon=PAGE_ICON)
            st.stop()
        if mode != MODES.LOCAL:
            authentication_form()

        st.info(f"Learn how it works [here]({PROJECT_URL})")
        if not app_can_be_started():
            st.stop()


def authenticate(
    openai_api_key: str, activeloop_token: str, activeloop_org_name: str
) -> None:
    # Validate all credentials 
    openai_api_key = (
        openai_api_key
        or os.environ.get("OPENAI_API_KEY")
        or st.secrets.get("OPENAI_API_KEY")
    )
    activeloop_token = (
        activeloop_token
        or os.environ.get("ACTIVELOOP_TOKEN")
        or st.secrets.get("ACTIVELOOP_TOKEN")
    )
    activeloop_org_name = (
        activeloop_org_name
        or os.environ.get("ACTIVELOOP_ORG_NAME")
        or st.secrets.get("ACTIVELOOP_ORG_NAME")
    )
    if not (openai_api_key and activeloop_token and activeloop_org_name):
        st.session_state["auth_ok"] = False
        st.error("Credentials neither set nor stored", icon=PAGE_ICON)
        return
    try:
        # Try to access embeddign and deeplake
        with st.spinner("Authentifying..."):
            openai.api_key = openai_api_key
            openai.Model.list()
            deeplake.exists(
                f"hub://{activeloop_org_name}/AREA-Authentication-Check",
                token=activeloop_token,
            )
    except Exception as e:
        logger.error(f"Authentication failed with {e}")
        st.session_state["auth_ok"] = False
        st.error("Authentication failed", icon=PAGE_ICON)
        return
    # store credentials in the session state
    st.session_state["auth_ok"] = True
    st.session_state["openai_api_key"] = openai_api_key
    st.session_state["activeloop_token"] = activeloop_token
    st.session_state["activeloop_org_name"] = activeloop_org_name
    logger.info("Authentification successful!")


def update_chain() -> None:
    # Build chain with parameters
    # delete chat history 
    try:
        with st.session_state["info_container"], st.spinner("Building Chain..."):
            data_source = st.session_state["data_source"]
            if st.session_state["uploaded_files"] == st.session_state["data_source"]:
                data_source = save_files(st.session_state["uploaded_files"])
            st.session_state["chain"] = get_chain(
                data_source=data_source,
                options={
                    "mode": st.session_state["mode"],
                    "model": st.session_state["model"],
                    "k": st.session_state["k"],
                    "fetch_k": st.session_state["fetch_k"],
                    "chunk_size": st.session_state["chunk_size"],
                    "chunk_overlap": st.session_state["chunk_overlap"],
                    "temperature": st.session_state["temperature"],
                    "max_tokens": st.session_state["max_tokens"],
                    "model_n_ctx": st.session_state["model_n_ctx"],
                    "distance_metric": st.session_state["distance_metric"],
                    "maximal_marginal_relevance": st.session_state[
                        "maximal_marginal_relevance"
                    ],
                },
                credentials={
                    "openai_api_key": st.session_state["openai_api_key"],
                    "activeloop_token": st.session_state["activeloop_token"],
                    "activeloop_org_name": st.session_state["activeloop_org_name"],
                },
            )
            if st.session_state["uploaded_files"] == st.session_state["data_source"]:
                delete_files(st.session_state["uploaded_files"])
            st.session_state["chat_history"] = []
            msg = f"Data source **{st.session_state['data_source']}** is ready to go with model **{st.session_state['model']}**!"
            logger.info(msg)
            st.session_state["info_container"].info(msg, icon=PAGE_ICON)
    except Exception as e:
        msg = f"Failed to build chain for data source **{st.session_state['data_source']}** with model **{st.session_state['model']}**: {e}"
        logger.error(msg)
        st.session_state["info_container"].error(msg, icon=PAGE_ICON)


def update_usage(cb: OpenAICallbackHandler) -> None:
    # Accumulate API call 
    logger.info(f"Usage: {cb}")
    callback_properties = [
        "total_tokens",
        "prompt_tokens",
        "completion_tokens",
        "total_cost",
    ]
    for prop in callback_properties:
        value = getattr(cb, prop, 0)
        st.session_state["usage"].setdefault(prop, 0)
        st.session_state["usage"][prop] += value


def generate_response(prompt: str) -> str:
    # call the chain & generate responses and append to chat history
    with st.spinner("Generating response"), get_openai_callback() as cb:
        response = st.session_state["chain"](
            {"question": prompt, "chat_history": st.session_state["chat_history"]}
        )
        update_usage(cb)
    logger.info(f"Response: '{response}'")
    st.session_state["chat_history"].append((prompt, response["answer"]))
    return response["answer"]
