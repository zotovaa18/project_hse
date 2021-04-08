# -*- coding: utf-8 -*-
from __future__ import division, print_function
import subprocess
import sys
sys.argv=['punctuator.py', 'Demo-Europarl-EN.pcl', 'new.txt']
import models
import data
import theano
from io import open
import theano.tensor as T
import numpy as np


MAX_SUBSEQUENCE_LEN = 200
def pun():
    print("!")
    def punct(name):
        def to_array(arr, dtype=np.int32):
        # minibatch of 1 sequence as column
            return np.array([arr], dtype=dtype).T
    
        def convert_punctuation_to_readable(punct_token):
            if punct_token == data.SPACE:
                return " "
            else:
                return punct_token[0]
    
        def restore_with_pauses(output_file, text, pauses, word_vocabulary, reverse_punctuation_vocabulary, predict_function):
            i = 0
            with open(output_file, 'w', encoding='utf-8') as f_out:
                while True:
        
                    subsequence = text[i:i+MAX_SUBSEQUENCE_LEN]
                    subsequence_pauses = pauses[i:i+MAX_SUBSEQUENCE_LEN]
        
                    if len(subsequence) == 0:
                        break
        
                    converted_subsequence = [word_vocabulary.get(w, word_vocabulary[data.UNK]) for w in subsequence]
        
                    y = predict_function(to_array(converted_subsequence), to_array(subsequence_pauses, dtype=theano.config.floatX))
        
                    f_out.write(subsequence[0])
        
                    last_eos_idx = 0
                    punctuations = []
                    for y_t in y:
        
                        p_i = np.argmax(y_t.flatten())
                        punctuation = reverse_punctuation_vocabulary[p_i]
        
                        punctuations.append(punctuation)
        
                        if punctuation in data.EOS_TOKENS:
                            last_eos_idx = len(punctuations) # we intentionally want the index of next element
        
                    if subsequence[-1] == data.END:
                        step = len(subsequence) - 1
                    elif last_eos_idx != 0:
                        step = last_eos_idx
                    else:
                        step = len(subsequence) - 1
        
                    for j in range(step):
                        f_out.write(" " + punctuations[j] + " " if punctuations[j] != data.SPACE else " ")
                        if j < step - 1:
                            f_out.write(subsequence[1+j])
        
                    if subsequence[-1] == data.END:
                        break
        
                    i += step
        
        def restore(output_file, text, word_vocabulary, reverse_punctuation_vocabulary, predict_function):
            i = 0
            with open(output_file, 'w', encoding='utf-8') as f_out:
                while True:
        
                    subsequence = text[i:i+MAX_SUBSEQUENCE_LEN]
        
                    if len(subsequence) == 0:
                        break
        
                    converted_subsequence = [word_vocabulary.get(w, word_vocabulary[data.UNK]) for w in subsequence]
        
                    y = predict_function(to_array(converted_subsequence))
        
                    f_out.write(subsequence[0])
        
                    last_eos_idx = 0
                    punctuations = []
                    for y_t in y:
        
                        p_i = np.argmax(y_t.flatten())
                        punctuation = reverse_punctuation_vocabulary[p_i]
        
                        punctuations.append(punctuation)
        
                        if punctuation in data.EOS_TOKENS:
                            last_eos_idx = len(punctuations) # we intentionally want the index of next element
        
                    if subsequence[-1] == data.END:
                        step = len(subsequence) - 1
                    elif last_eos_idx != 0:
                        step = last_eos_idx
                    else:
                        step = len(subsequence) - 1
        
                    for j in range(step):
                        f_out.write(" " + punctuations[j] + " " if punctuations[j] != data.SPACE else " ")
                        if j < step - 1:
                            f_out.write(subsequence[1+j])
        
                    if subsequence[-1] == data.END:
                        break
        
                    i += step
        
        #if __name__ == "__main__":
        print("in processsss")
    
        if len(sys.argv) > 1:
            model_file = sys.argv[1]
            print("1:   ",sys.argv[1])
        else:
            sys.exit("Model file path argument missing")
    
        if len(sys.argv) > 2:
            output_file = sys.argv[2]
            print ("2      ",sys.argv[2])
        else:
            sys.exit("Output file path argument missing")
    
        use_pauses = len(sys.argv) > 3 and bool(int(sys.argv[3]))
        print ("all:   ",sys.argv)
        x = T.imatrix('x')
        
        if use_pauses:
        
            p = T.matrix('p')
    
            print("Loading model parameters...")
            net, _ = models.load(model_file, 1, x, p)
    
            print("Building model...")
            predict = theano.function(
                inputs=[x, p],
                outputs=net.y
            )
    
        else:
    
            print("Loading model parameters...")
            net, _ = models.load(model_file, 1, x)
    
            print("Building model...")
            predict = theano.function(
                inputs=[x],
                outputs=net.y
            )
    
        word_vocabulary = net.x_vocabulary
        punctuation_vocabulary = net.y_vocabulary
    
        reverse_word_vocabulary = {v:k for k,v in word_vocabulary.items()}
        reverse_punctuation_vocabulary = {v:k for k,v in punctuation_vocabulary.items()}
    
        #input_text = open(sys.stdin.fileno(), 'r', encoding='utf-8').read()
        
        input_text=open(name,'r',encoding='utf-8').read()
        if len(input_text) == 0:
            sys.exit("Input text from stdin missing.")
    
        text = [w for w in input_text.split() if w not in punctuation_vocabulary and w not in data.PUNCTUATION_MAPPING and not w.startswith(data.PAUSE_PREFIX)] + [data.END]
        pauses = [float(s.replace(data.PAUSE_PREFIX,"").replace(">","")) for s in input_text.split() if s.startswith(data.PAUSE_PREFIX)]
    
        if not use_pauses:
            restore(output_file, text, word_vocabulary, reverse_punctuation_vocabulary, predict)
        else:
            if not pauses:
                pauses = [0.0 for _ in range(len(text)-1)]
            restore_with_pauses(output_file, text, pauses, word_vocabulary, reverse_punctuation_vocabulary, predict)

    t=open("t_new.txt").read()
    j=0
    k=0
    m=0
    print(t)
    nt=t.split("\n")
    i=0
    for i in range(len(nt)):
        path="text_p"+str(i)+".txt"
        file=open(path,"w")
        file.write(nt[i])
        file.close()
    for k in range(i+1):
        path2="new_text_p"+str(k)+".txt"
        f=open(path2,"w")
        f.close()
    while m in range (i):
        new_file_path="new_text_p"+str(m)+".txt"
        sys.argv[2]=new_file_path
        file_path="text_p"+str(m)+".txt"
        if open(file_path).read()!="":
            punct(file_path)
        m=m+1
    m=0
    while m<=i:
        file_path="new_text_p"+str(m)+".txt"
        txt=open(file_path).read()
        pt=txt.split(" ")
        j=0
        for j in range(len(pt)):
            if pt[j]==".PERIOD":
                pt[j]="."
            if pt[j]==",COMMA":
                pt[j]=","
            if pt[j]=="?QUESTIONMARK":
                pt[j]="?"
            if pt[j]=="!EXCLAMATIONMARK":
                pt[j]="!"
            if pt[j]==":COLON":
                pt[j]=":"
            if pt[j]==";SEMICOLON":
                pt[j]=";"
            j=j+1
        l=0  
        n_data = ' '.join(str(l) for l in pt)
        file=open(file_path,"w")
        file.write(n_data)
        file.close()
        m=m+1
     
     
    m=0
    brilliant_text=open("brilliant.txt","a")
    while m<=i:
        file_path="new_text_p"+str(m)+".txt"
        brilliant_text.write("\n")
        if open(file_path).read()=="":
            brilliant_text.write("\n")
        else:
            text=open(file_path).read()
            brilliant_text.write(text)
        m=m+1
    brilliant_text.close()
    