from concurrent.futures import ThreadPoolExecutor, as_completed
from inspect import getmembers, isclass
from typing import List

from utils.db.models import migrate
from worker import tasks
from worker.tasks.base_model import Task


class Worker:
    """
    Class for running tasks.

    Class models imported from `worker.tasks` are accepted as tasks. They should be inherited from `Task`.

        * tasks     - List of tasks
        * run       - Run all tasks.
    """
    tasks: List[Task]

    _thread_pool: ThreadPoolExecutor
    _futures: list

    def __init__(self):
        self.tasks = [task[1]() for task in getmembers(tasks, isclass) if issubclass(task[1], Task)]
        self._thread_pool = ThreadPoolExecutor(max_workers=10)
        self._futures = []

    def run(self):
        """Run all tasks. Each task is run in a separate thread."""
        for task in self.tasks:
            self._futures.append(self._thread_pool.submit(task.start))
        for future in as_completed(self._futures):
            future.result()


if __name__ == '__main__':
    migrate()
    worker = Worker()
    worker.run()
