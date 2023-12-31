# -*- coding: utf-8 -*-
# @Date    : 2023/7/22 02:40
# @Author  : stellahong (stellahong@deepwisdom.ai)
#
import os

from metagpt.config import CONFIG
from metagpt.tools.sd_engine import SDEngine


def test_sd_engine_init():
    sd_engine = SDEngine()
    assert sd_engine.payload["seed"] == -1


def test_sd_engine_generate_prompt():
    sd_engine = SDEngine()
    sd_engine.construct_payload(prompt="test")
    assert sd_engine.payload["prompt"] == "test"


async def test_sd_engine_run_t2i():
    sd_engine = SDEngine()
    await sd_engine.run_t2i(prompts=["test"])
    img_path = CONFIG.workspace_path / "resources" / "SD_Output" / "output_0.png"
    assert os.path.exists(img_path)
