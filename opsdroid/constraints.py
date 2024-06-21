"""Decorator functions to use when creating skill modules.

These decorators are for specifying when a skill should not be called despite
having a matcher which matches the current message.
"""

import logging
from functools import wraps

from opsdroid.helper import add_skill_attributes

branch_coverage = {}

def initialize_coverage(func_name, num_branches):
    branch_coverage[func_name] = [False] * num_branches

def mark_branch(func_name, branch_id):
    branch_coverage[func_name][branch_id] = True

def report_coverage():
    total_branches = 0
    reached_branches = 0
    
    for func_name, branches in branch_coverage.items():
        func_total = len(branches)
        func_reached = sum(branches)
        
        total_branches += func_total
        reached_branches += func_reached
        
        coverage_percentage = (func_reached / func_total) * 100 if func_total > 0 else 0
        
        print(f"Coverage for {func_name}:")
        for i, reached in enumerate(branches):
            print(f"  Branch {i}: {'Reached! ✅' if reached else 'Not Reached ❌'}")
        print(f"  Function coverage: {coverage_percentage:.2f}%\n")
    
    overall_coverage = (reached_branches / total_branches) * 100 if total_branches > 0 else 0
    print(f"Overall branch coverage: {overall_coverage:.2f}%")

initialize_coverage("constraint_decorator", 2)
initialize_coverage("constraint_decorator_users", 2)
initialize_coverage("constraint_decorator_connectors", 2)

_LOGGER = logging.getLogger(__name__)

def invert_wrapper(func):
    """Inverts the result of a function."""

    @wraps(func)
    def inverted_func(*args, **kwargs):
        return not func(*args, **kwargs)

    return inverted_func


def constrain_rooms(rooms, invert=False):
    """Return room constraint decorator."""

    def constraint_decorator(func):
        """Add room constraint to skill."""

        def constraint_callback(message, rooms=rooms):
            """Check if the room is correct."""
            if hasattr(message.connector, "lookup_target"):
                rooms = list(map(message.connector.lookup_target, rooms))

            return message.target in rooms

        func = add_skill_attributes(func)
        if invert:
            mark_branch("constraint_decorator", 0)
            constraint_callback = invert_wrapper(constraint_callback)
        else: 
            mark_branch("constraint_decorator", 1)
        func.constraints.append(constraint_callback)
        return func

    return constraint_decorator


def constrain_users(users, invert=False):
    """Return user constraint decorator."""

    def constraint_decorator(func):
        """Add user constraint to skill."""

        def constraint_callback(message, users=users):
            """Check if the user is correct."""
            return message.user in users

        func = add_skill_attributes(func)
        if invert:
            mark_branch("constraint_decorator_users", 0)
            constraint_callback = invert_wrapper(constraint_callback)
    
        else:
            mark_branch("constraint_decorator_users", 1)
        func.constraints.append(constraint_callback)
        return func

    return constraint_decorator


def constrain_connectors(connectors, invert=False):
    """Return connector constraint decorator."""

    def constraint_decorator(func):
        """Add connectors constraint to skill."""

        def constraint_callback(message, connectors=connectors):
            """Check if the connectors is correct."""
            return message.connector and (message.connector.name in connectors)

        func = add_skill_attributes(func)
        if invert:
            mark_branch("constraint_decorator_connectors", 0)
            constraint_callback = invert_wrapper(constraint_callback)
        else:
            mark_branch("constraint_decorator_connectors", 1)
        func.constraints.append(constraint_callback)
        return func

    return constraint_decorator

# Example usage for coverage testing
if __name__ == "__main__":
    class MockMessage:
        def __init__(self, target, user, connector):
            self.target = target
            self.user = user
            self.connector = connector
    
    class MockConnector:
        def __init__(self, name):
            self.name = name
        def lookup_target(self, target):
            return target

    @constrain_rooms(["room1", "room2"], invert=False)
    def skill_room(message):
        return "Room constraint passed"

    @constrain_users(["user1", "user2"], invert=False)
    def skill_user(message):
        return "User constraint passed"

    @constrain_connectors(["connector1", "connector2"], invert=False)
    def skill_connector(message):
        return "Connector constraint passed"

    # Test the branches
    msg_room = MockMessage(target="room1", user="user1", connector=MockConnector(name="connector1"))
    msg_room_lookup = MockMessage(target="room1", user="user1", connector=MockConnector(name="lookup_target"))
    msg_user = MockMessage(target="room3", user="user1", connector=MockConnector(name="connector3"))
    msg_connector = MockMessage(target="room3", user="user3", connector=MockConnector(name="connector1"))

    print(skill_room(msg_room))  
    print(skill_room(msg_room_lookup))  
    print(skill_user(msg_user))  
    print(skill_connector(msg_connector))  

    # Invert the decorators
    @constrain_rooms(["room1", "room2"], invert=True)
    def skill_room_invert(message):
        return "Inverted room constraint passed"

    @constrain_users(["user1", "user2"], invert=True)
    def skill_user_invert(message):
        return "Inverted user constraint passed"

    @constrain_connectors(["connector1", "connector2"], invert=True)
    def skill_connector_invert(message):
        return "Inverted connector constraint passed"

    print(skill_room_invert(msg_room)) 
    print(skill_user_invert(msg_user))  
    print(skill_connector_invert(msg_connector))  

    report_coverage()