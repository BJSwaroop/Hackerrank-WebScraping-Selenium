from sentence_transformers import SentenceTransformer, util
from hackerrank_SQL import SQLprocessor
sql = SQLprocessor()
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# username = "20pa1a5435"
def plagiariseCodes(usernames):
  copied = {}
  for username in usernames:
    sql.user_attempt = []
    sql.user_problems_info = {}
    sql.problems_to_check = {}
    sql.get_user_problems_list(username)
    sql.get_valid_source_codes_for_each_problem(username)
    user_attempts= sql.user_attempt
    # this is a list consists all the user attempts
    user_problems_info= sql.user_problems_info
    # this is a dictionary with user attempts as key and language,time, 
    problems_to_check= sql.problems_to_check

    for attempt in user_attempts:
      curr_attempt = user_problems_info.get(attempt)
      """
        'python-loops': language,score, source_code
      """
      attempt_language = curr_attempt[0]
      attempt_score = curr_attempt[1]
      attempt_source_code = curr_attempt[2]

      if attempt in problems_to_check:
            """
              'python-loops': [('20Pa1a5430', 'python-loops', 'python3', 10, '\nn = int(input())\nfor i in range(n):\n    print(i*i) \n    '), ...]
            """
            max = 99
            max_User = ()
            for individualAttempt in problems_to_check.get(attempt):
              curr_attempt_user = individualAttempt[0]
              curr_attempt_language = individualAttempt[2]
              curr_attempt_score = individualAttempt[3]
              curr_attempt_source_code = individualAttempt[4]
              # if attempt_language == curr_attempt_language:
              # Compute embedding for both lists
              embedding_1= model.encode(attempt_source_code, convert_to_tensor=True)
              embedding_2= model.encode(curr_attempt_source_code, convert_to_tensor=True)
              sim_Score = util.pytorch_cos_sim(embedding_1, embedding_2).item()*100
              if sim_Score > max:
                max = sim_Score
                max_User = individualAttempt
              print(username, curr_attempt_user,attempt ,sim_Score)

            if not len(max_User) == 0:
              if username in copied:
                copiedList = copied.get(username)
                copiedList.append(max_User)
                copied[username] = copiedList
              else:
                copied[username] = [max_User]
              print(max_User[0])
  return copied
