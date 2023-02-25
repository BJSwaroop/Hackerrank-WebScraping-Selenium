from hackerrank_SQL import SQLprocessor
from hackerrank_selenium import *

adminUsername = "capmentor01"
adminPassword = "VITBHackers21!"
contest_slug = "test-contest00"

hr_session = HackerrankSession(adminUsername, adminPassword)
sql_proc = SQLprocessor()

usernames = hr_session.fetch_users(contest_slug)
print(usernames)
for username in usernames:
    last_fetch_time = sql_proc.fetch_last_attempt_time(username, contest_slug)
    # get the max time from current_user_attempts and set it to last_fetch_time.
    contest_submissions = UserContestSubmissions(username, contest_slug, hr_session)
    prev_attempts = sql_proc.fetch_user_attempts(username, contest_slug)
    current_user_submissions = contest_submissions.fetch_latest_submissions(prev_attempts, last_fetch_time)
    sql_proc.upsert_user_attempts(username, contest_slug, current_user_submissions)


