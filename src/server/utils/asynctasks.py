import abc
import asyncio


class AsyncTask(abc.ABC):
    """
    Abstract class for asynchronous tasks from sycnchronous code
    """

    @abc.abstractmethod
    async def impl(self, *args, **kwargs):
        """Run the task."""
        pass

    def __call__(self, *args, **kwargs):
        """Run the task."""
        asyncio.get_event_loop().create_task(self.impl(*args, **kwargs))
