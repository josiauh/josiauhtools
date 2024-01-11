"""
Grazio, a custom class to do with gradio.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Literal
import gradio as gr
from gradio.components import Component
from gradio.flagging import FlaggingCallback
from gradio.themes import ThemeClass as Theme
import numpy as np


class Themes():
    RedVelvet = gr.themes.Soft(
        primary_hue="rose",
        secondary_hue="cyan",
        neutral_hue="slate",
    )
    Wallet = gr.themes.Base(
        primary_hue="green",
        secondary_hue="yellow",
        neutral_hue="amber",
    ).set(
        embed_radius='*radius_xxl',
        slider_color="#EAB308"
    )

class Interfaces:
    class Examples:
        class News(gr.Interface):
            def __init__(
                    self,
                    examples: list[Any] | list[list[Any]] | str | None = None,
                    cache_examples: bool | None = None,
                    examples_per_page: int = 10,
                    live: bool = False,
                    title: str | None = None,
                    description: str | None = None,
                    article: str | None = None,
                    thumbnail: str | None = None,
                    theme: Theme | str | None = None,
                    css: str | None = None,
                    allow_flagging: str | None = None,
                    flagging_options: list[str] | list[tuple[str, str]] | None = None,
                    flagging_dir: str = "flagged",
                    flagging_callback: FlaggingCallback | None = None,
                    analytics_enabled: bool | None = None,
                    batch: bool = False,
                    max_batch_size: int = 4,
                    api_name: str | Literal[False] | None = "predict",
                    _api_mode: bool = False,
                    allow_duplication: bool = False,
                    concurrency_limit: int | None | Literal["default"] = "default",
                    **kwargs,
            ):
                def news(name):
                    choicesList = ["Amusement park dies in summer due to snow!", "Fluxus being sued by Flies!", "Reporters still setting up live!"]
                    return f"Hey guys! {name} here. Breaking news! {np.random.choice(choicesList)}"
                super().__init__(
                    news,
                    ["text"],
                    ["text"],
                    examples=examples,
                    cache_examples=cache_examples,
                    examples_per_page=examples_per_page,
                    live=live,
                    title=title,
                    description=description,
                    article=article,
                    thumbnail=thumbnail,
                    theme=theme,
                    css=css,
                    allow_flagging=allow_flagging,
                    flagging_options=flagging_options,
                    flagging_dir=flagging_dir,
                    flagging_callback=flagging_callback,
                    analytics_enabled=analytics_enabled,
                    batch=batch,
                    max_batch_size=max_batch_size,
                    api_name=api_name,
                    _api_mode=_api_mode,
                    allow_duplication=allow_duplication,
                    concurrency_limit=concurrency_limit,
                    **kwargs
                )