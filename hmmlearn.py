import re
import pickle
import sys

f=open(sys.argv[1],encoding='UTF8')
sent_list=[]
words=[]
tags=['start']

for line in f:
    line=line.rstrip()
    sentence=line.split(' ')
    a=[]
    for i in sentence:
        k=re.search('/\w\w$',i)
        index=k.start()
        word=i[:index]
        words.append(word)
        tagg=i[index+1:]
        a.append([word,tagg])
        if tagg not in tags:
            tags.append(tagg)
    sent_list.append(a)

trans_prob={k:{} for k in tags}
emis_prob={k:{} for k in words}
#print(emis_prob)

for key in trans_prob:
    for item in tags:
        if item!='start':
            trans_prob[key][item]=1

count={k:0 for k in tags}
#print(trans_prob)
for item in sent_list:
    i=0
    while i<len(item):
        if i==0:
            if item[0][1] in tags:
                trans_prob['start'][item[0][1]]+=1
        else:
            if item [i-1][1] in tags and item[i][1] in tags:
                trans_prob[item[i-1][1]][item[i][1]]+=1

        if item[i][1] not in emis_prob[item[i][0]]:
            if item[i][1] in tags:
                emis_prob[item[i][0]][item[i][1]]=1
        else:
            emis_prob[item[i][0]][item[i][1]]+=1
        if item[i][1] in tags:
            count[item[i][1]]+=1

        i=i+1


for key in trans_prob:
    sum=0
    for item in trans_prob[key]:
        sum+=trans_prob[key][item]
    for item in trans_prob[key]:
        trans_prob[key][item]/=sum

for key in emis_prob:
    for item in emis_prob[key]:
        emis_prob[key][item]/=count[item]
# print(trans_prob)
# print(emis_prob)

model_dic={"transition_prob":trans_prob,"emission_prob":emis_prob}
#print(model_dic)

with open('hmmmodel.txt', 'wb') as handle:
  pickle.dump(model_dic, handle)


