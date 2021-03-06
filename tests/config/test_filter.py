import pytest

from cfripper.config.config import Config
from cfripper.config.filter import Filter
from cfripper.config.rule_config import RuleConfig
from cfripper.model.enums import RuleMode
from cfripper.rule_processor import RuleProcessor
from cfripper.rules import DEFAULT_RULES
from tests.utils import get_cfmodel_from


@pytest.fixture()
def template_cross_account_role_no_name():
    return get_cfmodel_from("config/cross_account_role_no_name.json").resolve()


@pytest.fixture()
def template_cross_account_role_with_name():
    return get_cfmodel_from("config/cross_account_role_with_name.json").resolve()


@pytest.mark.parametrize(
    "filter, args, expected_result",
    [
        (Filter(eval={"eq": ["string", "string"]}), {}, True),
        (Filter(eval={"eq": [1, 1]}), {}, True),
        (Filter(eval={"eq": [-1, -1]}), {}, True),
        (Filter(eval={"eq": [1.0, 1.0]}), {}, True),
        (Filter(eval={"eq": [-1.0, -1.0]}), {}, True),
        (Filter(eval={"eq": [True, True]}), {}, True),
        (Filter(eval={"eq": [False, False]}), {}, True),
        (Filter(eval={"eq": [[1, 2], [1, 2]]}), {}, True),
        (Filter(eval={"eq": ["string", "not_that_string"]}), {}, False),
        (Filter(eval={"eq": [1, 2]}), {}, False),
        (Filter(eval={"eq": [-1, 1]}), {}, False),
        (Filter(eval={"eq": [1.0, 2.0]}), {}, False),
        (Filter(eval={"eq": [1.0, -1.0]}), {}, False),
        (Filter(eval={"eq": [False, True]}), {}, False),
        (Filter(eval={"eq": [True, False]}), {}, False),
        (Filter(eval={"eq": [[1, 2], [2, 1]]}), {}, False),
        (Filter(eval={"ne": ["string", "string"]}), {}, False),
        (Filter(eval={"ne": [1, 1]}), {}, False),
        (Filter(eval={"ne": [-1, -1]}), {}, False),
        (Filter(eval={"ne": [1.0, 1.0]}), {}, False),
        (Filter(eval={"ne": [-1.0, -1.0]}), {}, False),
        (Filter(eval={"ne": [True, True]}), {}, False),
        (Filter(eval={"ne": [False, False]}), {}, False),
        (Filter(eval={"ne": [[1, 2], [1, 2]]}), {}, False),
        (Filter(eval={"ne": ["string", "not_that_string"]}), {}, True),
        (Filter(eval={"ne": [1, 2]}), {}, True),
        (Filter(eval={"ne": [-1, 1]}), {}, True),
        (Filter(eval={"ne": [1.0, 2.0]}), {}, True),
        (Filter(eval={"ne": [1.0, -1.0]}), {}, True),
        (Filter(eval={"ne": [False, True]}), {}, True),
        (Filter(eval={"ne": [True, False]}), {}, True),
        (Filter(eval={"ne": [[1, 2], [2, 1]]}), {}, True),
        (Filter(eval={"lt": [0, 1]}), {}, True),
        (Filter(eval={"lt": [-1, 0]}), {}, True),
        (Filter(eval={"lt": [-float("inf"), float("inf")]}), {}, True),
        (Filter(eval={"lt": [1, 0]}), {}, False),
        (Filter(eval={"lt": [0, -1]}), {}, False),
        (Filter(eval={"lt": [float("inf"), -float("inf")]}), {}, False),
        (Filter(eval={"lt": [1, 1]}), {}, False),
        (Filter(eval={"lt": [0, 0]}), {}, False),
        (Filter(eval={"lt": [-1, -1]}), {}, False),
        (Filter(eval={"lt": [float("inf"), float("inf")]}), {}, False),
        (Filter(eval={"lt": [-float("inf"), -float("inf")]}), {}, False),
        (Filter(eval={"gt": [1, 0]}), {}, True),
        (Filter(eval={"gt": [0, -1]}), {}, True),
        (Filter(eval={"gt": [float("inf"), -float("inf")]}), {}, True),
        (Filter(eval={"gt": [0, 1]}), {}, False),
        (Filter(eval={"gt": [-1, 0]}), {}, False),
        (Filter(eval={"gt": [-float("inf"), float("inf")]}), {}, False),
        (Filter(eval={"gt": [1, 1]}), {}, False),
        (Filter(eval={"gt": [0, 0]}), {}, False),
        (Filter(eval={"gt": [-1, -1]}), {}, False),
        (Filter(eval={"gt": [float("inf"), float("inf")]}), {}, False),
        (Filter(eval={"gt": [-float("inf"), -float("inf")]}), {}, False),
        (Filter(eval={"le": [0, 1]}), {}, True),
        (Filter(eval={"le": [-1, 0]}), {}, True),
        (Filter(eval={"le": [-float("inf"), float("inf")]}), {}, True),
        (Filter(eval={"le": [1, 0]}), {}, False),
        (Filter(eval={"le": [0, -1]}), {}, False),
        (Filter(eval={"le": [float("inf"), -float("inf")]}), {}, False),
        (Filter(eval={"le": [1, 1]}), {}, True),
        (Filter(eval={"le": [0, 0]}), {}, True),
        (Filter(eval={"le": [-1, -1]}), {}, True),
        (Filter(eval={"le": [float("inf"), float("inf")]}), {}, True),
        (Filter(eval={"le": [-float("inf"), -float("inf")]}), {}, True),
        (Filter(eval={"ge": [1, 0]}), {}, True),
        (Filter(eval={"ge": [0, -1]}), {}, True),
        (Filter(eval={"ge": [float("inf"), -float("inf")]}), {}, True),
        (Filter(eval={"ge": [0, 1]}), {}, False),
        (Filter(eval={"ge": [-1, 0]}), {}, False),
        (Filter(eval={"ge": [-float("inf"), float("inf")]}), {}, False),
        (Filter(eval={"ge": [1, 1]}), {}, True),
        (Filter(eval={"ge": [0, 0]}), {}, True),
        (Filter(eval={"ge": [-1, -1]}), {}, True),
        (Filter(eval={"ge": [float("inf"), float("inf")]}), {}, True),
        (Filter(eval={"ge": [-float("inf"), -float("inf")]}), {}, True),
        (Filter(eval={"not": True}), {}, False),
        (Filter(eval={"not": False}), {}, True),
        (Filter(eval={"not": [True]}), {}, False),
        (Filter(eval={"not": [False]}), {}, True),
        (Filter(eval={"or": True}), {}, True),
        (Filter(eval={"or": False}), {}, False),
        (Filter(eval={"or": [True]}), {}, True),
        (Filter(eval={"or": [False]}), {}, False),
        (Filter(eval={"or": [True, True]}), {}, True),
        (Filter(eval={"or": [False, True]}), {}, True),
        (Filter(eval={"or": [True, False]}), {}, True),
        (Filter(eval={"or": [False, False]}), {}, False),
        (Filter(eval={"and": True}), {}, True),
        (Filter(eval={"and": False}), {}, False),
        (Filter(eval={"and": [True]}), {}, True),
        (Filter(eval={"and": [False]}), {}, False),
        (Filter(eval={"and": [True, True]}), {}, True),
        (Filter(eval={"and": [False, True]}), {}, False),
        (Filter(eval={"and": [True, False]}), {}, False),
        (Filter(eval={"and": [False, False]}), {}, False),
        (Filter(eval={"in": ["a", ["a"]]}), {}, True),
        (Filter(eval={"in": ["b", ["a", "b"]]}), {}, True),
        (Filter(eval={"in": ["c", ["a", "b", "c"]]}), {}, True),
        (Filter(eval={"in": ["d", ["a"]]}), {}, False),
        (Filter(eval={"in": ["e", ["a", "b"]]}), {}, False),
        (Filter(eval={"in": ["f", ["a", "b", "c"]]}), {}, False),
        (Filter(eval={"in": ["a", "a"]}), {}, True),
        (Filter(eval={"in": ["b", "ab"]}), {}, True),
        (Filter(eval={"in": ["b", "aba"]}), {}, True),
        (Filter(eval={"in": ["b", "a"]}), {}, False),
        (Filter(eval={"in": ["c", "ab"]}), {}, False),
        (Filter(eval={"in": ["c", "aba"]}), {}, False),
        (Filter(eval={"regex": [r"^\d+$", "5"]}), {}, True),
        (Filter(eval={"regex": [r"pi+", "piiig"]}), {}, True),
        (Filter(eval={"regex": [r"iii", "piiig"]}), {}, False),
        (Filter(eval={"regex": [r"igs", "piiig"]}), {}, False),
        (Filter(eval={"regex": [r"\w*\d\s*\d\s*\d\w*", "xx1 2   3xx"]}), {}, True),
        (Filter(eval={"regex": [r"\w*\d\s*\d\s*\d\w*", "xx12  3xx"]}), {}, True),
        (Filter(eval={"regex": [r"\w*\d\s*\d\s*\d\w*", "xx123xx"]}), {}, True),
        (Filter(eval={"regex": [r"^b\w+", "foobar"]}), {}, False),
        (Filter(eval={"regex": [r"\w*b\w+", "foobar"]}), {}, True),
        (Filter(eval={"exists": None}), {}, False),
        (Filter(eval={"exists": "string"}), {}, True),
        (Filter(eval={"exists": 1}), {}, True),
        (Filter(eval={"exists": -1}), {}, True),
        (Filter(eval={"exists": 1.0}), {}, True),
        (Filter(eval={"exists": -1.0}), {}, True),
        (Filter(eval={"exists": True}), {}, True),
        (Filter(eval={"exists": False}), {}, True),
        (Filter(eval={"empty": []}), {}, True),
        (Filter(eval={"empty": ["string"]}), {}, False),
        (Filter(eval={"empty": [1]}), {}, False),
        (Filter(eval={"empty": [-1]}), {}, False),
        (Filter(eval={"empty": [1.0]}), {}, False),
        (Filter(eval={"empty": [-1.0]}), {}, False),
        (Filter(eval={"empty": [True]}), {}, False),
        (Filter(eval={"empty": [False]}), {}, False),
        (Filter(eval={"ref": "param_a"}), {"param_a": "a"}, "a"),
        (Filter(eval={"ref": "param_a"}), {"param_a": 1}, 1),
        (Filter(eval={"ref": "param_a"}), {"param_a": -1}, -1),
        (Filter(eval={"ref": "param_a"}), {"param_a": 1.0}, 1.0),
        (Filter(eval={"ref": "param_a"}), {"param_a": -1.0}, -1.0),
        (Filter(eval={"ref": "param_a"}), {"param_a": True}, True),
        (Filter(eval={"ref": "param_a"}), {"param_a": False}, False),
        (Filter(eval={"ref": "param_a"}), {"param_a": []}, []),
        (Filter(eval={"ref": "param_a"}), {"param_a": ["a"]}, ["a"]),
        (Filter(eval={"ref": "param_a"}), {"param_a": [1]}, [1]),
        (Filter(eval={"ref": "param_a"}), {"param_a": [-1]}, [-1]),
        (Filter(eval={"ref": "param_a"}), {"param_a": [1.0]}, [1.0]),
        (Filter(eval={"ref": "param_a"}), {"param_a": [-1.0]}, [-1.0]),
        (Filter(eval={"ref": "param_a.param_b"}), {"param_a": {"param_b": "a"}}, "a"),
        (Filter(eval={"ref": "param_a.param_b"}), {"param_a": {"param_b": 1}}, 1),
        (Filter(eval={"ref": "param_a.param_b"}), {"param_a": {"param_b": -1}}, -1),
        (Filter(eval={"ref": "param_a.param_b"}), {"param_a": {"param_b": 1.0}}, 1.0),
        (Filter(eval={"ref": "param_a.param_b"}), {"param_a": {"param_b": -1.0}}, -1.0),
        (Filter(eval={"ref": "param_a.param_b"}), {"param_a": {"param_b": True}}, True),
        (Filter(eval={"ref": "param_a.param_b"}), {"param_a": {"param_b": False}}, False),
        (Filter(eval={"ref": "param_a.param_b"}), {"param_a": {"param_b": []}}, []),
        (Filter(eval={"ref": "param_a.param_b"}), {"param_a": {"param_b": ["a"]}}, ["a"]),
        (Filter(eval={"ref": "param_a.param_b"}), {"param_a": {"param_b": [1]}}, [1]),
        (Filter(eval={"ref": "param_a.param_b"}), {"param_a": {"param_b": [-1]}}, [-1]),
        (Filter(eval={"ref": "param_a.param_b"}), {"param_a": {"param_b": [1.0]}}, [1.0]),
        (Filter(eval={"ref": "param_a.param_b"}), {"param_a": {"param_b": [-1.0]}}, [-1.0]),
        (Filter(eval={"ref": "param_a.param_b.param_c"}), {"param_a": {"param_b": {"param_c": "a"}}}, "a"),
        (Filter(eval={"ref": "param_a.param_b.param_c"}), {"param_a": {"param_b": {"param_c": 1}}}, 1),
        (Filter(eval={"ref": "param_a.param_b.param_c"}), {"param_a": {"param_b": {"param_c": -1}}}, -1),
        (Filter(eval={"ref": "param_a.param_b.param_c"}), {"param_a": {"param_b": {"param_c": 1.0}}}, 1.0),
        (Filter(eval={"ref": "param_a.param_b.param_c"}), {"param_a": {"param_b": {"param_c": -1.0}}}, -1.0),
        (Filter(eval={"ref": "param_a.param_b.param_c"}), {"param_a": {"param_b": {"param_c": True}}}, True),
        (Filter(eval={"ref": "param_a.param_b.param_c"}), {"param_a": {"param_b": {"param_c": False}}}, False),
        (Filter(eval={"ref": "param_a.param_b.param_c"}), {"param_a": {"param_b": {"param_c": []}}}, []),
        (Filter(eval={"ref": "param_a.param_b.param_c"}), {"param_a": {"param_b": {"param_c": ["a"]}}}, ["a"]),
        (Filter(eval={"ref": "param_a.param_b.param_c"}), {"param_a": {"param_b": {"param_c": [1]}}}, [1]),
        (Filter(eval={"ref": "param_a.param_b.param_c"}), {"param_a": {"param_b": {"param_c": [-1]}}}, [-1]),
        (Filter(eval={"ref": "param_a.param_b.param_c"}), {"param_a": {"param_b": {"param_c": [1.0]}}}, [1.0]),
        (Filter(eval={"ref": "param_a.param_b.param_c"}), {"param_a": {"param_b": {"param_c": [-1.0]}}}, [-1.0]),
        # Composed
        (Filter(eval={"eq": [{"ref": "param_a"}, "a"]}), {"param_a": "a"}, True),
        (Filter(eval={"eq": ["a", {"ref": "param_a"}]}), {"param_a": "a"}, True),
        (Filter(eval={"eq": [{"ref": "param_a"}, "b"]}), {"param_a": "a"}, False),
        (Filter(eval={"eq": ["b", {"ref": "param_a"}]}), {"param_a": "a"}, False),
        (Filter(eval={"eq": [{"ref": "param_a"}, {"ref": "param_a"}]}), {"param_a": "a"}, True),
        (Filter(eval={"eq": [{"ref": "param_a"}, {"ref": "param_a"}]}), {"param_a": "a"}, True),
        (Filter(eval={"eq": [{"ref": "param_a"}, {"ref": "param_b"}]}), {"param_a": "a", "param_b": "a"}, True),
        (Filter(eval={"eq": [{"ref": "param_a"}, {"ref": "param_b"}]}), {"param_a": "a", "param_b": "b"}, False),
        (Filter(eval={"eq": [{"ref": "param_a"}, {"ref": "param_b"}]}), {"param_a": "b", "param_b": "a"}, False),
        (
            Filter(eval={"and": [{"exists": {"ref": "param_a.param_b"}}, {"eq": [{"ref": "param_a.param_b"}, "b"]}]}),
            {},
            False,
        ),
        (
            Filter(eval={"and": [{"exists": {"ref": "param_a.param_b"}}, {"eq": [{"ref": "param_a.param_b"}, "b"]}]}),
            {"param_a": {"param_b": "b"}},
            True,
        ),
    ],
)
def test_filter(filter, args, expected_result):
    assert filter(**args) == expected_result


def test_exist_function_and_property_does_not_exist(template_cross_account_role_no_name):
    mock_config = Config(
        rules=["CrossAccountTrustRule"],
        aws_account_id="123456789",
        stack_name="mockstack",
        rules_config={
            "CrossAccountTrustRule": RuleConfig(
                filters=[
                    Filter(
                        rule_mode=RuleMode.WHITELISTED,
                        eval={
                            "and": [
                                {
                                    "and": [
                                        {"exists": {"ref": "resource.Properties.RoleName"}},
                                        {"regex": ["^prefix-.*$", {"ref": "resource.Properties.RoleName"}]},
                                    ]
                                },
                                {"eq": [{"ref": "principal"}, "arn:aws:iam::999999999:role/someuser@bla.com"]},
                            ]
                        },
                    ),
                ]
            )
        },
    )

    rules = [DEFAULT_RULES.get(rule)(mock_config) for rule in mock_config.rules]
    processor = RuleProcessor(*rules)
    result = processor.process_cf_template(template_cross_account_role_no_name, mock_config)
    assert not result.valid


def test_exist_function_and_property_exists(template_cross_account_role_with_name):
    mock_config = Config(
        rules=["CrossAccountTrustRule"],
        aws_account_id="123456789",
        stack_name="mockstack",
        rules_config={
            "CrossAccountTrustRule": RuleConfig(
                filters=[
                    Filter(
                        rule_mode=RuleMode.WHITELISTED,
                        eval={
                            "and": [
                                {
                                    "and": [
                                        {"exists": {"ref": "resource.Properties.RoleName"}},
                                        {"regex": ["^prefix-.*$", {"ref": "resource.Properties.RoleName"}]},
                                    ]
                                },
                                {"eq": [{"ref": "principal"}, "arn:aws:iam::999999999:role/someuser@bla.com"]},
                            ]
                        },
                    ),
                ]
            )
        },
    )

    rules = [DEFAULT_RULES.get(rule)(mock_config) for rule in mock_config.rules]
    processor = RuleProcessor(*rules)
    result = processor.process_cf_template(template_cross_account_role_with_name, mock_config)
    assert result.valid
