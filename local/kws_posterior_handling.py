'''
@Author: zhyyao
@Date: 2020-01-17 20:09:37
@LastEditTime : 2020-01-17 21:20:03
@LastEditors  : Vim
@Description: Using this script to process neural network output. You can also see paper writen by Chen guoguo
@FilePath: /yao_workspace/kws_mia/local/kws_posterior_handling.py
'''
import numpy as np
import argparse

Wsmooth=5
Wmax=100
label_low=3
label_high=10

def posteriorSmooth(y,j):
    hsmooth= max(1,j-Wsmooth+1)
    return (1.0/float(j-hsmooth+1)*y[hsmooth:j].sum(axis=0))

def confidence(y,j):
    hmax=max(1,j-Wmax+1)
    pp=y[hmax-1:j].max(axis=0)
    conf=1
    for i in range(label_low,label_high):
        conf=conf*pp[i]
    return pow(conf,1.0/(label_high-label_low))

def readFile(filename):
    f=open(filename,"r")
    name=""
    confidenceDic=dict()
    for line in f.readlines():
        if(len(line.split())==2):
            name=line.split()[0]
            y_output=list()
        elif(len(line.split())==10):
            post=[ np.exp(float(x)) for x in line.split() ]
            post= post/np.sum(post)
            y_output.append(post)
        elif(len(line.split())==11):
            post=[ np.exp(float(line.split()[x])) for x in range(10) ]
            post= post/np.sum(post)
            y_output.append(post)
            yp = list()
            for i in range(1,len(y_output)):
                yp.append(posteriorSmooth(np.array(y_output),i))
            confList= list()
            for i in range(1,len(y_output)):
                confList.append(confidence(np.array(yp),i))
            confidenceDic[name]=max(confList)
            print [name,max(confList)]
    f.close()
    return confidenceDic

def writeFile(result, outfilename):
    f = open(outfilename,"w")
    for key in result:
        f.write(key+" "+str(result[key])+"\n")
    f.close()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="decode kws output")
    parser.add_argument('bnf_file',help='output of network')
    
    FLAGS = parser.parse_args()

    result = readFile(FLAGS.bnf_file)

    writeFile(result, "result.txt")
