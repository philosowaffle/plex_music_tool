import logging
import sqlite3

from time import sleep

from django.db import transaction
from .models import Task, Async

logger = logging.getLogger(__name__)

EXCEPTION_THRESHOLD = 3

def start():

    # There is already and async task running
    if Async.objects.count() > 0:
        logger.info("Async runner already running, exiting.")
        return

    logger.info("Starting run...")

    # Create an entry to indicate an async runner exists
    async_object = Async()
    async_object.save()

    exception_count = 0
    stop = False
    current_task_id = None
    try:

        while not stop:
            try:
                with transaction.atomic():
                    tasks = Task.objects.filter(executed = False).order_by('id')
                    if len(tasks):
                        task = tasks[0]
                        current_task_id = task.id
                        if task.script == 'ASYNC_STOP':
                            stop = True
                        else:
                            exec(task.script)
                            exception_count = 0
                        # task.executed = True
                        # task.save()
                        # Delete on success
                        Task.objects.filter(id=task.id).delete()
                    else:
                        current_task_id = None
                        Async.objects.first().delete()
                        stop = True
            except:
                logger.exception('Async Crashed')
                exception_count += 1

                # we need to mark the failed task as executed in another DB transaction.
                if current_task_id:
                    with transaction.atomic():
                        tasks = Task.objects.filter(id = current_task_id, executed = False).order_by(id)
                        # tasks = Task.objects.raw('SELECT * FROM async_task at WHERE at.id = %s and at.executed = false ORDER BY at.id FOR UPDATE', [current_task_id])
                        if len(tasks):
                            task = tasks[0]
                            task.executed = True
                            task.save()

            if exception_count >= EXCEPTION_THRESHOLD:
                sleep(10)
            else:
                sleep(0.5)

    except Exception as e:
        logger.error("Async Runner exited early: " + str(e))
        Async.objects.first().delete()

def stop():
    Task.objects.create(script='ASYNC_STOP')