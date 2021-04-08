# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 18:56:55 2021

@author: zotov
"""

import re
import codecs

def from_bros():
    
    #project_math_expr_3_0.py
    
    inFile = open('brilliant.txt', 'r', encoding='utf8')
    outFile = open('daniil_text_end.txt', 'w', encoding='utf8')
    
    OP_DICT_1 = {'plus' : '+',
                 'minus' : '-',
                 'equal' : '=',
                 'equals' : '=',
                 'times' : '*',
                 'over' : '/',
                 'percent' : '%'
                }
    
    OP_DICT_2 = {'to' : '^'}
    
    OP_DICT_3 = {'greater' : '>',
                 'less' : '<'
                }
    
    NM_DICT = {'zero' : '0', 'one' : '1', 'two' : '2', 'three' : '3', 'four' : '4',
               'five' : '5', 'six' : '6', 'seven' : '7', 'eight' : '8', 'nine' : '9',
               'ten' : '10', 'hundred' : '100', 'thousand' : '1000',
              }
    
    operators = ['+', '-', '*', '/', '^', '=', '>', '<']
    
    key_words = ['the', 'power', 'of']
    
    eng_alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
                    'n','o','p','q','r','s','t','u','v','w','x','y','z']
    
    lat_alphabet = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta',
                    'eta ', 'theta', 'iota', 'kappa', 'lambda', 'mu',
                    'nu', 'xi', 'pi', 'rho', 'sigma', 'tau',
                    'upsilon', 'phi', 'chi', 'psi', 'omega']
    
    trig_funcs = ['sin', 'cos', 'tan', 'cot', 'arcsin', 'arcccos', 'arctan', 'arccot']
    
    funcs = ['sqrt']
    
    punctuation = ['.', ',', ';', ':', '!', '?']
    
    brackets = ['(', ')']
    
    
    #Функции для обработки текста === === === === === === === === ===
    
    def read_file(inFile): #считывает файл в список
        text = []
        text.append('IgnoreThisElement')
        for line in inFile:
            line = list(map(str, line.split()))
            line.append('\n')
            for word in line:
                punct = word[-1]
                if punct in punctuation: #отделяет знаки препинания
                    text.append(word[:-1])
                    text.append(punct)
                else:
                    text.append(word)
        text.append('IgnoreThisElement')
        return text
    
    
    def write_file(text, outFile): #записывает список в файл
        print(*text[1:-1], file=outFile)
        return ''
    
    
    def sep_brackets(text): #отделяет скобки от слов
        new_text = []
        for elm in text:
            count1 = 0
            count2 = 0
            while elm[0] == '(' and len(elm) != 1:
                elm = elm[1:]
                count1 += 1
            while elm[-1] == ')' and len(elm) != 1:
                elm = elm[:-1]
                count2 += 1
            for i in range(count1):
                new_text.append('(')
            new_text.append(elm)
            for i in range(count2):
                new_text.append(')')
        return new_text
    
    
    def delete_empty_str(text): #удаляет пустые строки
        new_text = []
        for elm in text:
            if elm != '':
                new_text.append(elm)
        return new_text
    
    
    def punctuation_join(text): #присоединяет знаки препинания
        new_text = []
        for elm in text:
            if elm in punctuation:
                pr_elm = new_text.pop()
                new_text.append(pr_elm + elm)
            else:
                new_text.append(elm)
        return new_text
    
    # === === === === === === === === === === === === === === === ===
    
    
    #Функции для обработки мат. выражений === === === === === === ===
    
    def if_math_expr(array): #проверяет выражение на мат. символы
        answ = False
        answ = answ or any(not(elm.isalpha()) for elm in array)
        answ = answ or any(elm in eng_alphabet or elm in lat_alphabet for elm in array)
        answ = answ or any(elm in funcs or elm in trig_funcs for elm in array)
        for elm in array:
            if elm.find('.jpg') != -1:
                answ = False
        return answ
    
    
    def great_or_less(text): #убирает is и than в выражениях с > или <
        new_text = []
        for i in range(len(text)):
            if text[i] == '>' or text[i] == '<':
                text[i+1] = ''
                if text[i-1] == 'is':
                    new_text.pop()
            new_text.append(text[i])
        return new_text
    
    
    def check_word_in_OP_DICT(text, i): #проверят слово в словарях
        word = text[i]
        new_word = word
        
        if OP_DICT_1.get(word) != None:
            word = OP_DICT_1[word]
            if if_math_expr([text[i-1], text[i+1]]):
                new_word = word
        
        elif OP_DICT_2.get(word) != None:
            word = OP_DICT_2[word]
            if if_math_expr([text[i-1]]):
                count = i + 1
                while text[count] in key_words:
                    text[count] = ''
                    count += 1
                new_word = word
        
        elif OP_DICT_3.get(word) != None:
            word = OP_DICT_3[word]
            if text[i+1] == 'than' and if_math_expr([text[i-2], text[i-1], text[i+2]]):
                new_word = word
        
        return new_word
    
    
    def upgrade_text(text): #заменяет слова по словарям
        new_text = []
        for i in range(len(text)):
            new_word = check_word_in_OP_DICT(text, i)
            new_text.append(new_word)
        return new_text
    
    
    def unite_brackets(text): #объединяет выражения в скобках в один элемент
        new_text = []
        sup_array = []
        count = 0
        for elm in text:
            if elm == '(':
                count += 1
                sup_array.append(elm)
                continue
            if elm == ')':
                count -= 1
                sup_array.append(elm)
                continue
            if count == 0 and len(sup_array) == 0:
                new_text.append(elm)
            if count == 0 and len(sup_array) != 0:
                new_sup_array = minus_join(sup_array)
                new_sup_array = pattern_powers_and_roots(new_sup_array)
                new_sup_array = power_join(new_sup_array)
                new_sup_array = frac_join(new_sup_array)
                new_sup_array = funcs_join(new_sup_array)
                new_text.append(''.join(new_sup_array))
                new_text.append(elm)
                sup_array = []
            if count != 0:
                sup_array.append(elm)
        return new_text
    
    
    def minus_join(text): #соединяет минус с выражением
        new_text = []
        par = 0
        for i in range(len(text)):
            if par == 0:
                if text[i] == '-':
                    bool_par = text[i-1] in punctuation or text[i-1] in operators or text[i-1] in brackets
                    if bool_par or not(if_math_expr([text[i-1]])):
                        new_text.append(text[i] + text[i+1])
                    else:
                        text[i-1] = new_text.pop()
                        new_text.append(text[i-1] + text[i] + text[i+1])
                    par = 1
                else:
                    new_text.append(text[i])
            else:
                par = 0
        return new_text
    
    
    def pattern_powers_and_roots(text): #находит и заменяет шаблоны степеней и корней
        new_text = []
        par = 0
        for i in range(len(text)):
            if par == 0:
                if text[i] == 'squared' and if_math_expr([new_text[-1]]):
                    new_text.append('^')
                    new_text.append('2')
                elif text[i] == 'cubed' and if_math_expr([new_text[-1]]):
                    new_text.append('^')
                    new_text.append('3')
                elif text[i] == 'root' and if_math_expr([text[i+2]]):
                    if text[i-2] == 'the' and text[i-1] == 'square':
                        new_text.pop()
                        new_text.pop()
                    if text[i-2] != 'the' and text[i-1] == 'square' or text[i-1] == 'the':
                        new_text.pop() 
                    new_text.append('sqrt')
                    par = 1
                else:
                    new_text.append(text[i])
            else:
                par -= 1
        return new_text
    
    
    def power_join(text): #соединяет ^ со следующим и предыдущим элементами
        new_text = []
        par = 0
        for i in range(len(text)):
            if par == 0:
                if text[i] == '^':
                    text[i-1] = new_text.pop()
                    if text[i-1][-1] == ')' and text[i+1][0] == '(':
                        new_text.append(text[i-1] + text[i] + text[i+1])
                    elif text[i-1][-1] == ')' and text[i+1][0] != '(':
                        new_text.append(text[i-1] + text[i] + '(' + text[i+1] + ')')
                    elif text[i-1][-1] != ')' and text[i+1][0] == '(':
                        new_text.append('(' + text[i-1] + ')' + text[i] + text[i+1])
                    else:
                        new_text.append('(' + text[i-1] + ')' + text[i] + '(' + text[i+1] + ')')
                    par = 1
                else:
                    new_text.append(text[i])
            else:
                par = 0
        return new_text
    
    
    def frac_join(text): #соединяет / со следующим и предыдущим элементами
        new_text = []
        par = 0
        for i in range(len(text)):
            if par == 0:
                if text[i] == '/':
                    text[i-1] = new_text.pop()
                    if text[i-1][-1] == ')' and text[i+1][0] == '(':
                        new_text.append(text[i-1] + text[i] + text[i+1])
                    elif text[i-1][-1] == ')' and text[i+1][0] != '(':
                        new_text.append(text[i-1] + text[i] + '(' + text[i+1] + ')')
                    elif text[i-1][-1] != ')' and text[i+1][0] == '(':
                        new_text.append('(' + text[i-1] + ')' + text[i] + text[i+1])
                    else:
                        new_text.append('(' + text[i-1] + ')' + text[i] + '(' + text[i+1] + ')')
                    par = 1
                else:
                    new_text.append(text[i])
            else:
                par = 0
        return new_text
    
    
    def funcs_join(text): #записывает следующий элемент в аргумент функции
        new_text = []
        par = 0
        for i in range(len(text)):
            if par == 0:
                if text[i] in trig_funcs or text[i] in funcs:
                    new_text.append(text[i] + '(' + text[i+1] + ')')
                    par = 1
                else:
                    new_text.append(text[i])
            else:
                par = 0
        return new_text
        
    
    # === === === === === === === === === === === === === === === ===
    
    
    #Вызовы функций программы === === === === === === === === === ===
    
    text_arr = read_file(inFile)
    new_text_arr = delete_empty_str(text_arr)
    new_text_arr = sep_brackets(new_text_arr)
    
    new_text_arr = upgrade_text(new_text_arr)
    new_text_arr = great_or_less(new_text_arr)
    new_text_arr = delete_empty_str(new_text_arr)
    new_text_arr = unite_brackets(new_text_arr)
    
    #!!! Эти функции дублируем в функцию unite_brackets !!!
    new_text_arr = minus_join(new_text_arr)
    new_text_arr = pattern_powers_and_roots(new_text_arr)
    new_text_arr = power_join(new_text_arr)
    new_text_arr = frac_join(new_text_arr)
    new_text_arr = funcs_join(new_text_arr)
    
    # new_text_arr = punctuation_join(new_text_arr)
    write_file(new_text_arr, outFile)
    
    # === === === === === === === === === === === === === === === ===
    
    inFile.close()
    outFile.close()