"""Class for persisting information in opsdroid."""

import logging

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

initialize_coverage("_get_from_database", 3)

_LOGGER = logging.getLogger(__name__)


class Memory:
    """A Memory object.

    An object to obtain, store and persist data outside of opsdroid.

    Attributes:
        databases (:obj:`list` of :obj:`Database`): List of database objects.
        memory (:obj:`dict`): In-memory dictionary to store data.

    """

    def __init__(self):
        """Create object with minimum properties."""
        self.databases = []

    async def get(self, key, default=None):
        """Get data object for a given key.

        Gets the key value found in-memory or from the database(s).

        Args:
            key (str): Key to retrieve data.

        Returns:
            A data object for the given key, otherwise `None`.

        """
        _LOGGER.debug("Getting %s from memory.", key)
        result = await self._get_from_database(key)
        return result or default

    async def put(self, key, data):
        """Put a data object to a given key.

        Stores the key and value in memory and the database(s).

        Args:
            key (str): Key for the data to store.
            data (obj): Data object to store.

        """
        _LOGGER.debug("Putting %s to memory.", key)
        await self._put_to_database(key, data)

    async def delete(self, key):
        """Delete data object for a given key.

        Deletes the key value found in-memory or from the database(s).

        Args:
            key (str): Key to delete data.

        """
        _LOGGER.debug("Deleting %s from memory.", key)
        await self._delete_from_database(key)

    async def _get_from_database(self, key):
        """Get updates from databases for a given key.

        Gets the first key value found from the database(s).

        Args:
            key (str): Key to retrieve data from a database.

        Returns:
            The first key value (data object) found from the database(s).
            Or `None` when no database is defined or no value is found.

        Todo:
            * Handle multiple databases

        """
        if not self.databases:
            mark_branch("_get_from_database", 0)
            return None
        else:
            mark_branch("_get_from_database", 1)

        results = []
        for database in self.databases:
            results.append(await database.get(key))
            mark_branch("_get_from_database", 2)
        return results[0]

    async def _put_to_database(self, key, data):
        """Put updates into databases for a given key.

        Stores the key and value on each database defined.

        Args:
            key (str): Key for the data to store.
            data (obj): Data object to store.

        """
        if self.databases:
            for database in self.databases:
                await database.put(key, data)

    async def _delete_from_database(self, key):
        """Delete data from databases for a given key.

        Deletes the key and value on each database defined.

        Args:
            key (str): Key for the data to delete.

        """
        if self.databases:
            for database in self.databases:
                await database.delete(key)


if __name__ == "__main__":
    import asyncio

    class MockDatabase:
        def __init__(self):
            self.storage = {}

        async def get(self, key):
            return self.storage.get(key)

        async def put(self, key, value):
            self.storage[key] = value

        async def delete(self, key):
            if key in self.storage:
                del self.storage[key]


    async def main():
        memory = Memory()
        memory.databases.append(MockDatabase())

        #async def test_empty_memory(memory):
        assert await memory.get("test") is None

        #Test _get_from_database when not self.databases
        memory.databases = []  
        await memory.get("key2", "default")  # Expected: default

    asyncio.run(main())

    # Run coverage report
    report_coverage()
