from reading_worker import Worker

background_thread = Worker(frequency=2)
background_thread.start()
