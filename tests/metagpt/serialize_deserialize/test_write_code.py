# -*- coding: utf-8 -*-
# @Date    : 11/23/2023 10:56 AM
# @Author  : stellahong (stellahong@fuzhi.ai)
# @Desc    :

import pytest

from metagpt.actions import WriteCode
from metagpt.llm import LLM
from metagpt.schema import CodingContext, Document


def test_write_design_serialize():
    action = WriteCode()
    ser_action_dict = action.dict()
    assert ser_action_dict["name"] == "WriteCode"
    # assert "llm" in ser_action_dict  # not export


@pytest.mark.asyncio
async def test_write_code_deserialize():
    context = CodingContext(
        filename="test_code.py", design_doc=Document(content="write add function to calculate two numbers")
    )
    doc = Document(content=context.json())
    action = WriteCode(context=doc)
    serialized_data = action.dict()
    new_action = WriteCode(**serialized_data)

    assert new_action.name == "WriteCode"
    assert new_action.llm == LLM()
    await action.run()
