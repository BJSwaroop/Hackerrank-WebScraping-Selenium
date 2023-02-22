import selenium
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
import requests
import mysql.connector as connector


class HackerrankSession:
  """
  Class to manage Hackerrank Session
  """
  def __init__(self, username, password):
    """
    username and password for the gmail admin to be passed
    this method logs in the user with a selenium driver
    """
    self.__driver = webdriver.Chrome(ChromeDriverManager().install())
    self.__driver.get('https://www.hackerrank.com/auth/login')
    m = self.__driver.find_element("name","username")
    m.send_keys(username)
    m = self.__driver.find_element("name","password")
    m.send_keys(password)
    self.__driver.find_element("css selector",".ui-btn.ui-btn-primary").click()

  def logout(self):
    pass

  def fetch_link(self, link):
    if link.startswith("http"):
      pass
    else:
      link = f"https://www.hackerrank.com/{link[1:] if link.startswith('/') else link}"
    
    self.__driver.get(link)
    time.sleep(5)

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
      code_elements = self.hr_session.driver.find_elements("class name","CodeMirror-line")
      return "\n".join([line.text for line in code_elements])

    def __parse_submission_row(self, submission_item):
      """
      Parses a single row of submissions table
      """
      headers = ['problem_slug','username','id','language','time','result','score','status','during_contest','srclink']
      not_required = ['status','during_contest']
      cols = {}
      # for each column
      for i, column in enumerate(submission_item.find_elements("tag name","div")):
        # if attribute contains an "a" tag get the href
        # else if it contains a p tag get the text and stript it. check if it has attribute of data_otiginal_title
        # else set the value to be empty
        try:
          val = column.find_element("tag name","a").get_attribute('href')
          if i < (len(headers) - 1):
            val = val[val.rindex('/')+1:]
        except:
          try:
            val = column.find_element("tag name","p").text.strip()
            if headers[i] == 'time':
              val = int(val)
            elif headers[i] == 'score':
              val = float(val)
            try:
              testcases = column.get_attribute("data-original-title")
              cols["total_test_cases"] = len(testcases.strip().split("\n"))
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
      for submission_item in self.hr_session.driver.find_elements("class name","submissions_item"):
        # list = submission_item.find_elements("tag name","div")
        # print("list ",list)
        # print("question ",list[0].find_element("tag name","a").get_attribute('href'))
        # print("time ",list[4])
        # print("score ",list[6])
        cols = self.__parse_submission_row(submission_item)
        current_item_time = cols["time"]
        # assign only if needed

        problem_slug = cols['problem_slug']
        if problem_slug in user_attempts: # user already attempted this earlier
          prev_score = user_attempts[problem_slug]["score"]
          
          # print("prev_score = ", prev_score)
          if prev_score < cols["score"] or (prev_score == cols["score"] and last_fetch_time < current_item_time):
            #if not set for insertion then only updates
            cols["insert"] = user_attempts[problem_slug].get("insert", False)
            user_attempts[problem_slug] = cols

        else: # this is the first ever attempt for this problem
          # insert
          cols["insert"] = True
          user_attempts[problem_slug] = cols


        if current_item_time <= last_fetch_time:
          break
      return current_item_time

    def __fetch_submission_page(self, page_number):
      """
      Fetch an anticipated page in submissions.
      return true if page exists else return false
      """
      contest_submission_url = f"contests/{self.contest_slug}/judge/submissions/team/{self.username}/{page_number}"
      self.hr_session.fetch_link(contest_submission_url)
      try: 
        self.hr_session.driver.find_element("css selector","div.pagination > ul > li.active")
      except: #
        #  selenium.common.exceptions.NoSuchElementException
        return False

      return True

    """
    The SQL Table will have following columns
    'problem_slug','username','id','language','time','result','score','srclink','source_code']
    """
    def fetch_latest_submissions(self, user_attempts, last_fetch_time):
      """
      fetch the best submissions for problems solved in the given contest
      attempted by the given use after the given last_fetch_time
      """
      page = 1 # start from the first page
      # repeat for every page as long as page entries are above last_fetch_time
      # TODO: fetch from the database the problems done by the user in this contest
      # and store it in user_attempt dict
      while self.__fetch_submission_page(page):
        time_processed = self.__fetch_latest_user_attempts(user_attempts, last_fetch_time)
        if time_processed <= last_fetch_time:
          break
        page +=1
      # if self.__fetch_submission_page(page):
      #   print(self.__fetch_latest_user_attempts(user_attempts, last_fetch_time))
      
      # print(user_attempts['python-print']["problem_slug"])
      # fetch the source code for user_attempts that do not have the code populated
      final_attempts = {k: user_attempts[k] for k in user_attempts if isinstance(user_attempts[k], dict)}
      print(final_attempts)
      for problem_slug, attempt in final_attempts.items():
        if not attempt.get("source_code", False) and attempt.get("srclink", False):
          attempt["source_code"] = self.__fetch_code(attempt["srclink"])

      return final_attempts

class SQLprocessor:
  def __init__(self):
    
    self.mydb = connector.connect(
                                host="localhost",
                                user="root",
                                password="swaroop@4468",
                                database = "test")

    self.cursor = self.mydb.cursor(buffered = True)
    #print(self.cursor)
    # code to create a sql connector handle AND create table
    self.cursor.execute("CREATE TABLE if not exists CAPHRProblemBestAttempt (problem_slug VARCHAR(255),username VARCHAR(255),contest_slug VARCHAR(255), id VARCHAR(255),language VARCHAR(255),time int,result VARCHAR(255),score int,srclink VARCHAR(255),source_code VARCHAR(2000))")
    self.cursor.execute("CREATE TABLE if not exists CAPHRContestAttempt (username VARCHAR(255),contest_slug VARCHAR(255),score int)")
    self.cursor.execute("CREATE TABLE if not exists CAPHRContestProblem (contest_slug VARCHAR(255),username VARCHAR(255),score int,difficulty VARCHAR(20))")
     
    
  def fetch_last_attempt_time(self, username, contest_slug):
    """
    returns last fetch time
    """
    
    query = f"Select max(time) from CAPHRProblemBestAttempt where username = '{username}' and contest_slug = '{contest_slug}'"
    print(query)
    try:
      self.cursor.execute(query)
      time = int(self.cursor.fetchone()[0])
      submission_list = [f'{time}']
      return int(submission_list[0])
    except:
      return 0

  def fetch_user_attempts(self, username, contest_slug):
    query1 = f"select problem_slug,score from CAPHRProblemBestAttempt where username = '{username}' and contest_slug = '{contest_slug}'"
    self.cursor.execute(query1)
    return {x[0]:{"score":x[1]} for x in self.cursor.fetchall()}

  def upsert_user_attempts(self, username, contest_slug, attempts):
    """
    insert if not exists and passes if same and update if exists
    attempts: dict(problem_slug->attempt) Its a list which contains problem_slug after last fetch time
    """
    print("dbbbbbbbbb",attempts)
    for attempt in attempts:
      i = attempts[attempt]

      query = ''
      print("attempt = ",attempt)
      if attempts[attempt].get('insert', False):
        print("Inserting")
        src_code = i['source_code'].replace("\'","\\'")
        query =f"""Insert into CAPHRProblemBestAttempt (problem_slug,username,contest_slug,id,language,time,result,score,srclink,source_code) VALUES ('{i["problem_slug"]}','{username}','{contest_slug}','{i["id"]}','{i["language"]}',{i["time"]},'{i["result"]}',{i["score"]},'{i["srclink"]}','{src_code}')"""
        self.cursor.execute(query)
      elif attempts[attempt].get("source_code", False):
        print("Updating")
        src_code = i['source_code'].replace("\'","\\'")
        query = f"""Update CAPHRProblemBestAttempt set id = {i["id"]},language = '{i["language"]}',time = {i["time"]},score= {i["score"]},srclink = '{i["srclink"]}',source_code= '{src_code}' where username = '{username}' and problem_slug = '{i['problem_slug']}'"""
        self.cursor.execute(query)
      else: 
        pass
    self.mydb.commit()

hr_session = HackerrankSession("capmentor01","VITBHackers21!" )
sql_proc = SQLprocessor()
username = "20PA1A0412"
contest_slug = "test-contest00"
last_fetch_time = sql_proc.fetch_last_attempt_time(username,contest_slug)
# last_fetch_time = 0
# print("Last fetch time = ",last_fetch_time)
# get the max time from current_user_attempts and set it to last_fetch_time.
contest_submissions = UserContestSubmissions(username,contest_slug , hr_session)
prev_attempts = sql_proc.fetch_user_attempts(username, contest_slug)
# prev_attempts = {}
# print("Prev attempts = ",prev_attempts)
current_user_submissions = contest_submissions.fetch_latest_submissions(prev_attempts, last_fetch_time)
# print(current_user_submissions[0],current_user_submissions[1])
sql_proc.upsert_user_attempts(username, contest_slug, current_user_submissions)
# sql_proc.insert_data(current_user_submissions)

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



The Database
------------
--
-- Table structure for table `CAPHRCustomContestWise`
--

DROP TABLE IF EXISTS `CAPHRCustomContestWise`;
CREATE TABLE `CAPHRCustomContestWise` (
  `sno` int(1) DEFAULT '0',
  `contestname` varchar(150) NOT NULL DEFAULT '',
  `hrmarks` int(1) DEFAULT '0',
  `lbmarks` int(1) DEFAULT '0',
  `display_status` int(1) DEFAULT '1',
  `sync_status` int(1) DEFAULT '1',
  PRIMARY KEY (`contestname`),
  UNIQUE KEY `contestname_UNIQUE` (`contestname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `capcompeteprog`
--

DROP TABLE IF EXISTS `capcompeteprog`;
CREATE TABLE `capcompeteprog` (
  `rollnumber` varchar(10) NOT NULL DEFAULT '',
  `name` varchar(150) DEFAULT NULL,
  `hrun` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`rollnumber`),
  UNIQUE KEY `rollnumber_UNIQUE` (`rollnumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table to store hackerrank contest cumulative scores
--
CREATE TABLE `CAPHRContestAttempt` (
    `hrun` varchar(150) NOT NULL,
    `contestname` varchar(150) NOT NULL,
    `score` int(1) NOT NULL DEFAULT 0
);

--
-- Table structure to store contest problem details
--
CREATE TABLE `CAPHRContestProblem` (
    `slug` varchar(150) NOT NULL,
    `max_Score` int(1) NOT NULL,
    `difficulty` ENUM('Easy', 'Medium', 'High') NOT NULL,
);

--
-- Table to store CAPHRProblemBestAttempt attempts for hackerrank problems (direct or contest)
--
CREATE TABLE `CAPHRProblemBestAttempt` (
    `hrun` varchar(150) NOT NULL,
    `problem_slug` varchar(150) NOT NULL,
    `contestname` varchar(150),
    `lang` varchar(30) NOT NULL,
    `status` varchar(100) NOT NULL,
    `num_testcases_passed` int(1) NOT NULL,
    `num_testcases_failed` int(1) DEFAULT 0,
    `sourcecode` varchar(5000) NOT NULL DEFAULT '',
    `score` int(1) NOT NULL DEFAULT 0,
    `max_score` int(1) NOT NULL
);
"""  
            
            



