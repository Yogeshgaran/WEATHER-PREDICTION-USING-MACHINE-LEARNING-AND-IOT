from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import os
import time
def run_script():
    # Make sure the script is executable and the Python interpreter path is correct
    subprocess.run(["python", "weather3.py"], check=True)
'''
# Create a scheduler instance
scheduler = BlockingScheduler()

# Schedule 'run_script' to be called every day at 6 AM, 12 PM, and 5 PM
scheduler.add_job(run_script, 'cron', hour='6')
scheduler.add_job(run_script, 'cron', hour='12')
scheduler.add_job(run_script, 'cron', hour='17')

# Start the scheduler
scheduler.start()
'''
while True:
    time.sleep(20)
    run_script()
    print("done")
