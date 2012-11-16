#from hackday.tasks import add
#from celery import group
#
#jobs = []
#
#for x in range(1,10):
#    st = add.subtask((1, x))
#    jobs.append(st)
#
#job = group(jobs)
#result = job.apply_async()
#result.join()
