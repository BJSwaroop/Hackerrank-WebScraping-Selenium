from hackerrank_SQL import SQLprocessor
from hackerrank_selenium import *


class HRMain:

    def __init__(self,adminUsername,adminPassword,contest_slug):
        self.adminUsername = adminUsername
        self.adminPassword = adminPassword
        self.contest_slug = contest_slug
    def fetchData(self):
        """
        This function is used to fetch the latest data of all the users of the contest and store it in DB.
        First it will fetch the usernames(All the registered users) then it will get the data of all the users.
        """
        hr_session = HackerrankSession(self.adminUsername, self.adminPassword)
        sql_proc = SQLprocessor() 
        usernames = hr_session.fetch_users(self.contest_slug)
        """
        This will get the all latetst users registered for the contest
        """
        for username in usernames:
            last_fetch_time = sql_proc.fetch_last_attempt_time(username, self.contest_slug)
            # get the max time from current_user_attempts and set it to last_fetch_time.
            contest_submissions = UserContestSubmissions(username, self.contest_slug, hr_session)
            prev_attempts = sql_proc.fetch_user_attempts(username, self.contest_slug)
            current_user_submissions = contest_submissions.fetch_latest_submissions(prev_attempts, last_fetch_time)
            sql_proc.upsert_user_attempts(username, self.contest_slug, current_user_submissions)
        users = sql_proc.fetch_users_list(self.contest_slug)
        probs = sql_proc.fetch_unique_problem_slugs(self.contest_slug)
        userAttempts = sql_proc.fetch_user_attempts_dict(self.contest_slug)
        userAttemptscount = sql_proc.fetch_user_attempts_count_dict(self.contest_slug)
        return {"users":users,"problemsAttempted":probs,"userAttempts":userAttempts,"userAttemptscount":userAttemptscount}
    
    def fetchOldData(self):
        """
        This function is used to fetch the old data of all the users of the contest from DB.
        """
        sql_proc = SQLprocessor() 
        users = sql_proc.fetch_users_list(self.contest_slug)
        probs = sql_proc.fetch_unique_problem_slugs(self.contest_slug)
        userAttempts = sql_proc.fetch_user_attempts_dict(self.contest_slug)
        userAttemptscount = sql_proc.fetch_user_attempts_count_dict(self.contest_slug)
        return {"users":users,"problemsAttempted":probs,"userAttempts":userAttempts,"userAttemptscount":userAttemptscount}


# hr = HRMain("capmentor01","VITBHackers21!","test-contest00")
# # print(cred.username,cred.password,cred.contest)
# users = hr.fetchData()

