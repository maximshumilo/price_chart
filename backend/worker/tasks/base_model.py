from abc import abstractmethod
from logging import Logger, getLogger


class Task:
    """
    Task base model.

        * _start    - Method containing the main logic of the task.
        * start     - Main method for start task.
    """
    _logger: Logger = getLogger('Task')

    def __init__(self):
        self._logger = self._logger.getChild(self.__class__.__name__)

    @abstractmethod
    def _start(self):
        """Method containing the main logic of the task."""
        raise NotImplementedError

    def start(self):
        """Starting task. Executing private method `_start`."""
        self._logger.info(f'Started task')
        self._start()
        self._logger.info(f'Finished task')
