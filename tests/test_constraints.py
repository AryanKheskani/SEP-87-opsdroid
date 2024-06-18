import asynctest
import asynctest.mock as mock

from opsdroid.cli.start import configure_lang
from opsdroid.core import OpsDroid
from opsdroid.events import Message
from opsdroid.matchers import match_regex
from opsdroid import constraints


class TestConstraints(asynctest.TestCase):
    """Test the opsdroid constraint decorators."""

    async def setUp(self):
        configure_lang({})

    async def getMockSkill(self):
        async def mockedskill(opsdroid, config, message):
            pass

        mockedskill.config = {}
        return mockedskill

    async def test_constrain_rooms_constrains(self):
        with OpsDroid() as opsdroid:
            skill = await self.getMockSkill()
            skill = match_regex(r".*")(skill)
            skill = constraints.constrain_rooms(["#general"])(skill)
            opsdroid.skills.append(skill)

            tasks = await opsdroid.parse(
                Message(text="Hello", user="user", target="#random", connector=None)
            )
            self.assertEqual(len(tasks), 3)  # Just match_always and match_event

    async def test_constrain_rooms_skips(self):
        with OpsDroid() as opsdroid, mock.patch("opsdroid.parsers.always.parse_always"):
            skill = await self.getMockSkill()
            skill = match_regex(r".*")(skill)
            skill = constraints.constrain_rooms(["#general"])(skill)
            opsdroid.skills.append(skill)

            tasks = await opsdroid.parse(
                Message(text="Hello", user="user", target="#general", connector=None)
            )
            self.assertEqual(len(tasks), 3)  # match_always, match_event and the skill

    async def test_constrain_rooms_inverted(self):
        with OpsDroid() as opsdroid:
            skill = await self.getMockSkill()
            skill = match_regex(r".*")(skill)
            skill = constraints.constrain_rooms(["#general"], invert=True)(skill)
            opsdroid.skills.append(skill)

            tasks = await opsdroid.parse(
                Message(text="Hello", user="user", target="#general", connector=None)
            )
            self.assertEqual(len(tasks), 3)  # Just match_always and match_event

    async def test_constrain_users_constrains(self):
        with OpsDroid() as opsdroid:
            skill = await self.getMockSkill()
            skill = match_regex(r".*")(skill)
            skill = constraints.constrain_users(["user"])(skill)
            opsdroid.skills.append(skill)

            tasks = await opsdroid.parse(
                Message(
                    text="Hello", user="otheruser", target="#general", connector=None
                )
            )
            self.assertEqual(len(tasks), 3)  # Just match_always and match_event

    async def test_constrain_users_skips(self):
        with OpsDroid() as opsdroid:
            skill = await self.getMockSkill()
            skill = match_regex(r".*")(skill)
            skill = constraints.constrain_users(["user"])(skill)
            opsdroid.skills.append(skill)

            tasks = await opsdroid.parse(
                Message(text="Hello", user="user", target="#general", connector=None)
            )
            self.assertEqual(len(tasks), 3)  # match_always, match_event and the skill

    async def test_constrain_users_inverted(self):
        with OpsDroid() as opsdroid:
            skill = await self.getMockSkill()
            skill = match_regex(r".*")(skill)
            skill = constraints.constrain_users(["user"], invert=True)(skill)
            opsdroid.skills.append(skill)

            tasks = await opsdroid.parse(
                Message(text="Hello", user="user", target="#general", connector=None)
            )
            self.assertEqual(len(tasks), 3)  # Just match_always and match_event

    async def test_constrain_connectors_constrains(self):
        with OpsDroid() as opsdroid:
            skill = await self.getMockSkill()
            skill = match_regex(r".*")(skill)
            skill = constraints.constrain_connectors(["slack"])(skill)
            opsdroid.skills.append(skill)
            connector = mock.Mock()
            connector.configure_mock(name="twitter")

            tasks = await opsdroid.parse(
                Message(
                    text="Hello", user="user", target="#random", connector=connector
                )
            )
            self.assertEqual(len(tasks), 3)  # Just match_always and match_event

    async def test_constrain_connectors_skips(self):
        with OpsDroid() as opsdroid:
            skill = await self.getMockSkill()
            skill = match_regex(r".*")(skill)
            skill = constraints.constrain_connectors(["slack"])(skill)
            opsdroid.skills.append(skill)
            connector = mock.Mock()
            connector.configure_mock(name="slack")

            tasks = await opsdroid.parse(
                Message(
                    text="Hello", user="user", target="#general", connector=connector
                )
            )
            self.assertEqual(len(tasks), 3)  # match_always, match_event and the skill

    async def test_constrain_connectors_inverted(self):
        with OpsDroid() as opsdroid:
            skill = await self.getMockSkill()
            skill = match_regex(r".*")(skill)
            skill = constraints.constrain_connectors(["slack"], invert=True)(skill)
            opsdroid.skills.append(skill)
            connector = mock.Mock()
            connector.configure_mock(name="slack")

            tasks = await opsdroid.parse(
                Message(
                    text="Hello", user="user", target="#general", connector=connector
                )
            )
            self.assertEqual(len(tasks), 3)  # Just match_always and match_event

    async def test_constraint_can_be_called_after_skip(self):
        with OpsDroid() as opsdroid:
            skill = await self.getMockSkill()
            skill = match_regex(r".*")(skill)
            skill = constraints.constrain_users(["user"])(skill)
            opsdroid.skills.append(skill)

            tasks = await opsdroid.parse(
                Message(text="Hello", user="user", target="#general", connector=None)
            )
            self.assertEqual(len(tasks), 3)  # match_always, match_event and the skill

            tasks = await opsdroid.parse(
                Message(
                    text="Hello", user="otheruser", target="#general", connector=None
                )
            )
            self.assertEqual(len(tasks), 3)  # Just match_always and match_event

            tasks = await opsdroid.parse(
                Message(text="Hello", user="user", target="#general", connector=None)
            )
            self.assertEqual(len(tasks), 3)  # match_always, match_event and the skill

    async def test_constraint_callback_with_lookup_target(self):
        # Test case where the message.connector has lookup_target attribute
        mock_message = mock.Mock()
        mock_message.target = "#general"
        mock_message.connector = mock.Mock()
        mock_message.connector.lookup_target = mock.Mock(return_value="#general")

        result = constraints.constraint_callback(mock_message, rooms=["#general"])
        self.assertTrue(result)

    async def test_constraint_callback_without_lookup_target(self):
        # Test case where the message.connector does not have lookup_target attribute
        mock_message = mock.Mock()
        mock_message.target = "#general"
        mock_message.connector = mock.Mock()
        del mock_message.connector.lookup_target

        result = constraints.constraint_callback(mock_message, rooms=["#general"])
        self.assertTrue(result)

    async def test_constraint_callback_without_lookup_target_no_match(self):
        # Test case where the message.connector does not have lookup_target attribute and room doesn't match
        mock_message = mock.Mock()
        mock_message.target = "#random"
        mock_message.connector = mock.Mock()
        del mock_message.connector.lookup_target

        result = constraints.constraint_callback(mock_message, rooms=["#general"])
        self.assertFalse(result)

