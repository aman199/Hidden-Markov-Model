import pickle
import sys

with open('hmmmodel.txt', 'rb') as handle:
  prob = pickle.loads(handle.read())


def viterbi_algo(a,b,items):
    T=len(items)
    probability={k:[] for k in range (1,T+1)}
    backpointer={k:[] for k in range(1,T+1)}
    t=1
    for key in a:
        li_prob=[]
        li_back=[]
        if items[t-1] not in b:
             for tag in a:
                 if tag!='start':
                        dict={}
                        dict2={}
                        dict[tag]=a['start'][tag]
                        dict2[tag]='start'
                        li_prob.append(dict)
                        li_back.append(dict2)
             probability[t]=li_prob
             backpointer[t]=li_back
        else:
            for tag in b[items[t-1]]:
                dict={}
                dict2={}
                dict[tag]=a['start'][tag]*b[items[t-1]][tag]
                dict2[tag]='start'
                li_prob.append(dict)
                li_back.append(dict2)
            probability[t]=li_prob
            backpointer[t]=li_back

    t=2
    while(t<=T):

            li_prob=[]
            li_back=[]
            if items[t-1] not in b:
             for tag in a:
                 if items[t-1][0].isupper():
                         if tag!='NP':
                             continue
                 if tag!='start':
                    dict={}
                    dict2={}
                    max=(float)('-inf')
                    for tag2 in probability[t-1]:
                        for key2 in tag2:
                            val=a[key2][tag]*tag2[key2]
                            if val>max:
                                max=val
                                state=key2

                    dict[tag]=max
                    dict2[tag]=state
                    li_prob.append(dict)
                    li_back.append(dict2)
                 probability[t]=li_prob
                 backpointer[t]=li_back
            else:
                for tag in b[items[t-1]]:
                    dict={}
                    dict2={}
                    max=(float)('-inf')
                    for tag2 in probability[t-1]:
                        for key2 in tag2:
                            val=a[key2][tag]*b[items[t-1]][tag]*tag2[key2]
                            if val>max:
                                max=val
                                state=key2

                    dict[tag]=max
                    dict2[tag]=state
                    li_prob.append(dict)
                    li_back.append(dict2)
                probability[t]=li_prob
                backpointer[t]=li_back
            t=t+1

    # print(probability)
    # print(backpointer)
    i=len(probability)
    for item in probability[i]:
        max=(float)('-inf')
        for key in item:
            if item[key]>max:
                max=item[key]
                tag=key
    tags=[tag]
    i=len(backpointer)
    while i>1:
        a=backpointer[i]
        for item in a:
            for key in item:
                if key==tag:
                    #print(item[key])
                    tags.append(item[key])
        tag=item[key]

        i=i-1
    return tags

emission_prob=prob['emission_prob']
transition_prob=prob['transition_prob']

fw=open('hmmoutput.txt','w',encoding='UTF8')
f=open(sys.argv[1],encoding='UTF8')
for line in f:
    line=line.rstrip()
    items=line.split(' ') #observations
    #print(items)
    tags=viterbi_algo(transition_prob,emission_prob,items)
    #print(tags)
    i=0
    while i<len(items):
        if i==len(items)-1:
            fw.write(items[i]+'/'+tags[0])
        else:
            fw.write(items[i]+'/'+tags[len(items)-1-i]+' ')
        i+=1
    fw.write('\n')
