import requests as re
import random
#https://opentdb.com/api.php?amount=10&category=18
async def data():
  res = re.get('https://opentdb.com/api.php?amount=10')
  res = res.json()#convert json in dict
  #print(res.keys())

  #print(len(res['results'][0]))

  #print(res['results'][0]['question'])

  #print(res['results'][0]['incorrect_answers'], res['results'][0]['correct_answer'])

  dictionary=dict()
  for i in range(3):
    tl = res['results'][i]['incorrect_answers']
    tl.append(res['results'][i]['correct_answer'])
    random.shuffle(tl)
    tl.append(res['results'][i]['correct_answer'])
    dictionary[res['results'][i]['question']] = tl

  return dictionary


''' return 
    {'Question':['a','b','c','d','ans'],'Question':['a','b','c','d','ans'],'Question':['a','b','c','d','ans']}
'''