import abc
import asyncio
import threading


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
        # new thread, create new event loop and run the task
        def _thread():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.impl(*args, **kwargs))

        threading.Thread(target=_thread).start()
