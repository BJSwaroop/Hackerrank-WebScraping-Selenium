from hackerrank_SQL import SQLprocessor
from hackerrank_selenium import *


class HRMain:
    # adminUsername= "capmentor01" 
    # adminPassword=    "VITBHackers21!"
    # contest_slug=   "test-contest00"
    def __init__(self,adminUsername,adminPassword,contest_slug):
        self.adminUsername = adminUsername
        self.adminPassword = adminPassword
        self.contest_slug = contest_slug
    def fetchData(self):
        print("Hello")
        hr_session = HackerrankSession(self.adminUsername, self.adminPassword)
        sql_proc = SQLprocessor() 

        usernames = hr_session.fetch_users(self.contest_slug)
        # usernames = ["a","b"]
        # for username in usernames:
        #     last_fetch_time = sql_proc.fetch_last_attempt_time(username, self.contest_slug)
        #     # get the max time from current_user_attempts and set it to last_fetch_time.
        #     contest_submissions = UserContestSubmissions(username, self.contest_slug, hr_session)
        #     prev_attempts = sql_proc.fetch_user_attempts(username, self.contest_slug)
        #     current_user_submissions = contest_submissions.fetch_latest_submissions(prev_attempts, last_fetch_time)
        #     sql_proc.upsert_user_attempts(username, self.contest_slug, current_user_submissions)
        return usernames

