# import selenium
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
class HackerrankSession:
    """
    Class to manage Hackerrank Session
    """
    flag = True
    def __init__(self, username, password):
        """
        username and password for the gmail admin to be passed
        this method logs in the user with a selenium driver
        """
        # "C:\Hackerrank Plagiarism Checker\Hackerrank-WebScraping-Selenium\Backend\chromedriver.exe"
        # chrome_driver_path = "C:\Hackerrank Plagiarism Checker\Hackerrank-WebScraping-Selenium\Backend\chromedriver.exe"

        # Initialize the Chrome driver with the specified path
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.__driver = webdriver.Chrome()
        print("HELLO its working")
        # self.__driver = webdriver.Chrome()
        # self.__driver = webdriver.Chrome(ChromeDriverManager().install())
        self.__driver.get('https://www.hackerrank.com/auth/login')
        
        # time.sleep(5)
        m = self.__driver.find_element("name", "username")
        m.send_keys(username)
        m = self.__driver.find_element("name", "password")
        m.send_keys(password)
        self.__driver.find_element(
            "css selector", ".ui-btn.ui-btn-primary").click()
    def logout(self):
        pass
    def fetch_link(self, link):
        if link.startswith("http"):
            pass
        else:
            link = f"https://www.hackerrank.com/{link[1:] if link.startswith('/') else link}"
        self.__driver.get(link)
        time.sleep(5)
    
    def check_page_valid(self,page,url):
        """
        Fetch an anticipated page in submissions.
        return true if page exists else return false
        """
        url = url+f"/{page}"
        self.fetch_link(url)
        try:
            self.driver.find_element(
                "css selector", "div.pagination > ul > li.active")
        except:
            self.flag = False
            return True
            #  selenium.common.exceptions.NoSuchElementException
        return True

    def fetch_users(self,contest_slug):
        """
            From leaderboard of a contest this function will fetch all the users who signed up for the contest
        """
        page = 1
        contest_submission_url = f"contests/{contest_slug}/leaderboard"
        usernames = []
        while self.check_page_valid(page,contest_submission_url):
            for submission_item in self.driver.find_elements("class name", "leaderboard-row"):
                list = submission_item.find_elements("tag name","div")
                username = list[1].find_element("tag name","a").get_attribute('href')
                username = username[username.rindex('/')+1:]
                print(username)
                usernames.append(username)
            if not self.flag:
                break 
            page += 1
        return usernames

    
    @property
    def driver(self):
        return self.__driver

class UserContestSubmissions:
    """
    Class to fetch related infor for a user for a particular contest
    """

    def __init__(self, username, contest_slug, hr_session):
        self.contest_slug = contest_slug
        self.username = username
        self.hr_session = hr_session

    def __fetch_code(self, src_link):
        """
        fetches the source code
        """
        self.hr_session.fetch_link(src_link)
        code_elements = self.hr_session.driver.find_elements(
            "class name", "CodeMirror-line")
        return "\n".join([line.text for line in code_elements])

    def __parse_submission_row(self, submission_item):
        """
        Parses a single row of submissions table
        """
        headers = ['problem_slug', 'username', 'id', 'language', 'time',
                   'result', 'score', 'status', 'during_contest', 'srclink']
        not_required = ['status', 'during_contest']
        cols = {}
        # for each column
        for i, column in enumerate(submission_item.find_elements("tag name", "div")):
            # if attribute contains an "a" tag get the href
            # else if it contains a p tag get the text and stript it. check if it has attribute of data_otiginal_title
            # else set the value to be empty
            try:
                val = column.find_element(
                    "tag name", "a").get_attribute('href')
                if i < (len(headers) - 1):
                    val = val[val.rindex('/')+1:]
            except:
                try:
                    val = column.find_element("tag name", "p").text.strip()
                    if headers[i] == 'time':
                        val = int(val)
                    elif headers[i] == 'score':
                        val = float(val)
                    try:
                        testcases = column.get_attribute("data-original-title")
                        cols["total_test_cases"] = len(
                            testcases.strip().split("\n"))
                        cols["test_cases_passed"] = testcases.count("Success")
                    except:
                        pass
                except:
                    val = ""

            if headers[i] not in not_required:
                cols[headers[i]] = val
        return cols

    def __fetch_latest_user_attempts(self, user_attempts, last_fetch_time):
        """
        parses best score recent attempts on a single page
        user_attempts: dict of problems attempted by user from the database
        last_fetch_time: time when the database was last updated for the user
        """
        # for each row.
        current_item_time = last_fetch_time
        for submission_item in self.hr_session.driver.find_elements("class name", "submissions_item"):
            cols = self.__parse_submission_row(submission_item)
            current_item_time = cols["time"]
            # assign only if needed
            problem_slug = cols['problem_slug']
            if problem_slug in user_attempts:  # user already attempted this earlier
                prev_score = user_attempts[problem_slug]["score"]
                if prev_score < cols["score"] or (prev_score == cols["score"] and last_fetch_time < current_item_time):
                    # if not set for insertion then only updates
                    cols["insert"] = user_attempts[problem_slug].get(
                        "insert", False)
                    user_attempts[problem_slug] = cols
            else:  # this is the first ever attempt for this problem
                # insert
                cols["insert"] = True
                user_attempts[problem_slug] = cols
            if current_item_time <= last_fetch_time:
                break
        return current_item_time

    

    """
    The SQL Table will have following columns
    'problem_slug','username','id','language','time','result','score','srclink','source_code']
    """
    def fetch_latest_submissions(self, user_attempts, last_fetch_time):
        """
        fetch the best submissions for problems solved in the given contest
        attempted by the given use after the given last_fetch_time
        """
        page = 1  # start from the first page
        # repeat for every page as long as page entries are above last_fetch_time
        # TODO: fetch from the database the problems done by the user in this contest
        # and store it in user_attempt dict
        contest_submission_url = f"contests/{self.contest_slug}/judge/submissions/team/{self.username}"
        while self.hr_session.check_page_valid(page,contest_submission_url):
            time_processed = self.__fetch_latest_user_attempts(
                user_attempts, last_fetch_time)
            if time_processed <= last_fetch_time:
                break
            if not self.hr_session.flag:
                break
            page += 1
        # if self.check_page_valid(page):
        #   print(self.__fetch_latest_user_attempts(user_attempts, last_fetch_time))

        # print(user_attempts['python-print']["problem_slug"])
        # fetch the source code for user_attempts that do not have the code populated
        final_attempts = {k: user_attempts[k] for k in user_attempts if isinstance(
            user_attempts[k], dict)}
        for problem_slug, attempt in final_attempts.items():
            if not attempt.get("source_code", False) and attempt.get("srclink", False):
                attempt["source_code"] = self.__fetch_code(attempt["srclink"])
        return final_attempts




"""
Above is test code.
Actually we want:
for each contest to be web scraped:
  for each user in our list:
    update the contest submissions

# do plagiarism check for new submissions, i.e. submissions made during this session of scraping only

{'python-loops': {'problem_slug': 'python-loops', 'username': '20PA1A0412', 'id': '1333834691', 'language': 
'python3', 'time': 1976, 'result': 'Accepted', 'score': 10.0, 'srclink': 'https://www.hackerrank.com/contest
s/test-contest00/challenges/python-loops/submissions/code/1333834691', 'source_code': ''}, 

'write-a-function
': {'problem_slug': 'write-a-function', 'username': '20PA1A0412', 'id': '1333833709', 'language': 'python3',
 'time': 1955, 'result': 'Accepted', 'score': 10.0, 'srclink': 'https://www.hackerrank.com/contests/test-con
test00/challenges/write-a-function/submissions/code/1333833709', 'source_code': ''}}

"""
