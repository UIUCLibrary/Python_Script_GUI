import pytest
from script_gui import script_args


class TestArgumentBuilder:
    @pytest.fixture
    def builder_fixture(self):
        return script_args.ArgumentBuilder()

    def test_add_argument_with_name(self, builder_fixture: script_args.ArgumentBuilder):
        builder_fixture.add_argument(name="Bar")
        args = builder_fixture.build()
        assert isinstance(args["Bar"], script_args.ScriptArgument)
        assert args["Bar"].valid is True

    def test_add_argument_with_name_and_default(self, builder_fixture: script_args.ArgumentBuilder):
        builder_fixture.add_argument(name="Bar", default="aaaaa")
        args = builder_fixture.build()
        assert isinstance(args["Bar"], script_args.ScriptArgument)
        assert args["Bar"].value == "aaaaa"
        assert args["Bar"].valid is True

    def test_add_argument_with_name_and_help(self, builder_fixture: script_args.ArgumentBuilder):
        builder_fixture.add_argument(name="Bar", help="bbb")
        args = builder_fixture.build()
        assert isinstance(args["Bar"], script_args.ScriptArgument)
        assert args["Bar"].help == "bbb"
        assert args["Bar"].valid is True

    def test_add_argument_with_name_and_validator(self, builder_fixture):
        builder_fixture.add_argument(name="Bar", validate=lambda f: f == "myvalue")
        args = builder_fixture.build()
        assert isinstance(args["Bar"], script_args.ScriptArgument)
        assert args["Bar"].valid is False

    def test_build_empty(self, builder_fixture):
        args = builder_fixture.build()
        assert isinstance(args, dict)

    def test_build_multiple(self, builder_fixture):
        builder_fixture.add_argument(name="Foo",
                                     default="f",
                                     validate=lambda user_data: user_data == "f",
                                     help="Must be the letter f")
        builder_fixture.add_argument(name="Bar", default="aaaaa")
        builder_fixture.add_argument(name="Baz", default="aaaa")
        args = builder_fixture.build()
        assert isinstance(args, dict)
