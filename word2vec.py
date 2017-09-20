# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 15:49:12 2017

@author: Java
"""


def word2vec(contentcut,windows=6,dim=300):
    import time
    st=time.time()
    words=contentcut.split(" ")
    appearWord=set(words)
    print("共出現"+str(len(appearWord))+"種字\n總字數"+str(len(words))+'個')
    wordict={word:{} for word in appearWord}
    n=0
    for i in range(len(words)):
        n+=1
        if n%100000==0:
            print("以完成"+str(100*n/len(words))+'%')
        for j in range(i-windows,i+windows):
            try:
                if i<j:
                    if words[j]+"前" not in wordict[words[i]]:
                        if len(wordict[words[i]])<dim:
                            wordict[words[i]][words[j]+"前"]=0
                    wordict[words[i]][words[j]+"前"]+=1
                elif i>j:
                    if words[j]+"後" not in wordict[words[i]]:
                        if len(wordict[words[i]])<dim:
                            wordict[words[i]][words[j]+"後"]=0
                    wordict[words[i]][words[j]+"後"]+=1
            except:
                pass
    try:
        del wordict['']
    except:
        pass
    ed=time.time()
    print("以完成100%")
    print("維度:%s\t找左右相關字個數:%s"%(dim,windows))
    print("共花費"+str(ed-st)+'秒')
    
    return wordict

def like(model,word1,word2):
    publicwords=set(model[word1])&set(model[word2])
    if publicwords==set():
        return {word2:0}
    n=0
    for word in model[word1]:
        n+=model[word1][word]**2
    m=0
    for word in model[word2]:
        m+=model[word2][word]**2
    l=0
    for word in publicwords:
        l+=model[word1][word]*model[word2][word]
    sim=l/((n**(1/2))*(m**(1/2)))
    return {word2:sim}

def checksim(word1,wordict,N=10):
    simi={}
    from collections import Counter
    for word2 in wordict:
        simi.update(like(wordict,word1,word2))
    del simi[word1]
    simi=Counter(simi).most_common(N)
    return simi



import json
with open(r'D:\Data\JsonData\TainanFood\bigtable_1.3.json') as f:
    data=json.load(f)
text=" ".join([dien['contentcut'] for dien in data])

model=word2vec(text,8,dim=300)

print(checksim("同記安平豆花",model,30))




