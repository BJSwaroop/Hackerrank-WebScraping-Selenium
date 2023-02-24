import mysql.connector as connector
class SQLprocessor:
    user_attempt = []
    user_problems_info = {}
    problems_to_check = {}
    def __init__(self):

        self.mydb = connector.connect(
            host="localhost",
            user="root",
            password="swaroop@4468",
            database="test")

        self.cursor = self.mydb.cursor(buffered=True)
        # print(self.cursor)
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
        return {x[0]: {"score": x[1]} for x in self.cursor.fetchall()}

    def upsert_user_attempts(self, username, contest_slug, attempts):
        """
        insert if not exists and passes if same and update if exists
        attempts: dict(problem_slug->attempt) Its a list which contains problem_slug after last fetch time
        """
        print("dbbbbbbbbb", attempts)
        for attempt in attempts:
            i = attempts[attempt]

            query = ''
            print("attempt = ", attempt)
            if attempts[attempt].get('insert', False):
                print("Inserting")
                src_code = i['source_code'].replace("\'", "\\'")
                query = f"""Insert into CAPHRProblemBestAttempt (problem_slug,username,contest_slug,id,language,time,result,score,srclink,source_code) VALUES ('{i["problem_slug"]}','{username}','{contest_slug}','{i["id"]}','{i["language"]}',{i["time"]},'{i["result"]}',{i["score"]},'{i["srclink"]}','{src_code}')"""
                self.cursor.execute(query)
            elif attempts[attempt].get("source_code", False):
                print("Updating")
                src_code = i['source_code'].replace("\'", "\\'")
                query = f"""Update CAPHRProblemBestAttempt set id = {i["id"]},language = '{i["language"]}',time = {i["time"]},score= {i["score"]},srclink = '{i["srclink"]}',source_code= '{src_code}' where username = '{username}' and problem_slug = '{i['problem_slug']}'"""
                self.cursor.execute(query)
            else:
                pass
        self.mydb.commit()
    def get_user_problems_list(self,username):
        """
        TODO: This function will return list, which consists of all the problems or attempts of a user
        """
        query = f""" 
                SELECT problem_slug,language,score, source_code
                from CAPHRProblemBestAttempt
                where username="{username}";
            """
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        self.user_attempt = []
        self.user_problems_info = {}
        for row in records:
            self.user_attempt.append(row[0])
            self.user_problems_info[row[0]] = row[1:]
        # print(user_attempt)
        # print(problems_info)
    def get_valid_source_codes_for_each_problem(self, username):
        """
        TODO: This function is used to get all the valid source quotes which match the problem slug the score the difficulty level the language. 
        And then there will be two cases. One is for easy difficulty level problems where we will compare the string length also string length in the sense, 
        the source code length and another case where the difficulty level is medium or hard. 
        In that case we will just fetch the source codes with same score.
        """

        query = f"""
            Select username, problem_slug, language, score,source_code time from CAPHRProblemBestAttempt c1 
            WHERE problem_slug IN
            (SELECT problem_slug
            from CAPHRProblemBestAttempt c2 
            where username="{username}" 
            and c1.score = c2.score) 
            and not c1.username = "{username}"
            order by problem_slug; 
        """

        self.cursor.execute(query)
        records = self.cursor.fetchall()

        for row in records:
            if row[1] in self.problems_to_check:
                ProbList = self.problems_to_check.get(row[1])
                ProbList.append(row)
                self.problems_to_check[row[1]] = ProbList
            else:
                list = []
                list.append(row)
                self.problems_to_check[row[1]] = list

"""
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
