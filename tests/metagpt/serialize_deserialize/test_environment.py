#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Desc   :

import shutil

from metagpt.actions.action_node import ActionNode
from metagpt.actions.add_requirement import UserRequirement
from metagpt.actions.project_management import WriteTasks
from metagpt.environment import Environment
from metagpt.roles.project_manager import ProjectManager
from metagpt.schema import Message
from metagpt.utils.common import any_to_str
from tests.metagpt.serialize_deserialize.test_serdeser_base import (
    ActionOK,
    RoleC,
    serdeser_path,
)


def test_env_serialize():
    env = Environment()
    ser_env_dict = env.dict()
    assert "roles" in ser_env_dict


def test_env_deserialize():
    env = Environment()
    env.publish_message(message=Message(content="test env serialize"))
    ser_env_dict = env.dict()
    new_env = Environment(**ser_env_dict)
    assert len(new_env.roles) == 0
    assert len(new_env.history) == 25


def test_environment_serdeser():
    out_mapping = {"field1": (list[str], ...)}
    out_data = {"field1": ["field1 value1", "field1 value2"]}
    ic_obj = ActionNode.create_model_class("prd", out_mapping)

    message = Message(
        content="prd", instruct_content=ic_obj(**out_data), role="product manager", cause_by=any_to_str(UserRequirement)
    )

    environment = Environment()
    role_c = RoleC()
    environment.add_role(role_c)
    environment.publish_message(message)

    ser_data = environment.dict()
    assert ser_data["roles"]["Role C"]["name"] == "RoleC"

    new_env: Environment = Environment(**ser_data)
    assert len(new_env.roles) == 1

    assert list(new_env.roles.values())[0]._states == list(environment.roles.values())[0]._states
    assert list(new_env.roles.values())[0]._actions == list(environment.roles.values())[0]._actions
    assert isinstance(list(environment.roles.values())[0]._actions[0], ActionOK)
    assert type(list(new_env.roles.values())[0]._actions[0]) == ActionOK


def test_environment_serdeser_v2():
    environment = Environment()
    pm = ProjectManager()
    environment.add_role(pm)

    ser_data = environment.dict()

    new_env: Environment = Environment(**ser_data)
    role = new_env.get_role(pm.profile)
    assert isinstance(role, ProjectManager)
    assert isinstance(role._actions[0], WriteTasks)
    assert isinstance(list(new_env.roles.values())[0]._actions[0], WriteTasks)


def test_environment_serdeser_save():
    environment = Environment()
    role_c = RoleC()

    shutil.rmtree(serdeser_path.joinpath("team"), ignore_errors=True)

    stg_path = serdeser_path.joinpath("team", "environment")
    environment.add_role(role_c)
    environment.serialize(stg_path)

    new_env: Environment = Environment.deserialize(stg_path)
    assert len(new_env.roles) == 1
    assert type(list(new_env.roles.values())[0]._actions[0]) == ActionOK
