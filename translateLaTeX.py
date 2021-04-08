import sys
import pickle
import argparse
import re
import googletrans
from googletrans import Translator
from google_trans_new import google_translator 
#parser = argparse.ArgumentParser()
#parser.add_argument('nameOfFile')
#args = parser.parse_args()
#
#if(re.search('.tex$', args.nameOfFile)==None):
#    sys.exit('The input file must be a .tex file.')
#print('The LaTeX document is:', args.nameOfFile)

def trans(lang, name_file):
    #print(lang)
    #name_file = 'end.tex'
    with open(name_file, 'r') as originalFile:
        origin = originalFile.read()
    
    #Поиск возможных конфликтов токенов
    struggles = re.findall('\[ *[012][\.\,][0-9]+\]', origin)
    if(struggles!=[]):
        print('Token struggles found: ', struggles)
        sys.exit('Tokens can overlap with content. Change the tokens or remove the source of the conflict.')
    else:
        print('No token conflicts were found.')
    
    #Скрыть все, что находится за пределами \begin{document}...\end{document}
    LaTeX = []
    beginDoc = re.search(r'\\begin{document}', origin)
    endDoc = re.search(r'\\end{document}', origin)
    if(beginDoc!=None):
        preface = origin[:beginDoc.end()]
        LaTeX.append(preface)
        if(endDoc!=None):
            content = '[1.0]' + origin[beginDoc.end():endDoc.start()]
            postamble = origin[endDoc.start():]
        else:
            content = '[1.0]' + origin[beginDoc.end():]
            postamble = []
    else:
        content = origin
        postamble = []
    
    #Скрыть все комментарии
    reAssert = re.compile(r'(?<!\\)[%].*')
    remarks = []
    for m in reAssert.finditer(content):
        remarks.append(m.group())
    nRemark = 0
    def repl_comment(obj):
        global nRemark
        nRemark += 1
        return '___COMMENT%d___'%(nRemark-1)
    content = reAssert.sub(repl_comment, content)
    with open('Comments', 'wb') as fp:
        pickle.dump(remarks, fp)
    
    #Скрыть латексные конструкции \begin{...}...\end{...}
    initialValues = []
    finalValues = []
    for m in re.finditer(r'\\begin{ *equation\** *}|\\begin{ *figure\** *}|\\begin{ *eqnarray\** *}|\\begin{ *multline\** *}' + r'|\\begin{ *thebibliography *}|\\begin{ *verbatim\** *}|\\begin{ *table\** *}|\\begin{ *subequations\** *}|\\begin{ *align\** *}' + r'|\\begin{ *displaymath\** *}|\\begin{ *gather\** *}|\\\[', content):
        initialValues.append(m.start())
    for m in re.finditer(r'\\end{ *equation\** *}|\\end{ *figure\** *}|\\end{ *eqnarray\** *}|\\end{ *multline\** *}' + r'|\\end{ *thebibliography *}|\\end{ *verbatim\** *}|\\end{ *table\** *}|\\end{ *subequations\** *}|\\end{ *align\** *}' + r'|\\end{ *displaymath\** *}|\\end{ *gather\** *}|\\\]', content):
        finalValues.append(m.end())
    nElements = len(initialValues)
    assert(len(finalValues)==nElements)
    if(nElements>0):
        newContent = content[:initialValues[0]]
        for neq in range(nElements-1):
            LaTeX.append(content[initialValues[neq]:finalValues[neq]])
            newContent += '[1.%d]'%(len(LaTeX)-1) + content[finalValues[neq]:initialValues[neq+1]]
        LaTeX.append(content[initialValues[nElements-1]:finalValues[nElements-1]])
        newContent += '[1.%d]'%(len(LaTeX)-1) + content[finalValues[nElements-1]:]
        content = newContent
    
    if(postamble!=[]):
        LaTeX.append(postamble)
        content += '[1.%d]'%(len(LaTeX)-1)
    with open('LaTeX', 'wb') as fp:
        pickle.dump(LaTeX, fp)
    
    #Заменить латексные формулы, комментарии и команды токенами.
    #Регулярное выражение r'(\$+)(?:(?!\1)[\s\S])*\1' для обработки $...$ и $$...$$ из:
    #https://stackoverflow.com/questions/54663900/how-to-use-regular-expression-to-remove-all-math-expression-in-latex-file
    reCommand = re.compile(r'___COMMENT[0-9]*___|\\title|\\chapter\**|\\section\**|\\subsection\**|\\subsubsection\**|~*\\footnote[0-9]*|(\$+)(?:(?!\1)[\s\S])*\1|~*\\\w*\s*{[^}]*}\s*{[^}]*}|~*\\\w*\s*{[^}]*}|~*\\\w*')
    instructions = []
    for m in reCommand.finditer(content):
        instructions.append(m.group())
    nc = 0
    def repl_f(obj):
        nonlocal nc
        nc += 1
        return '[2.%d]'%(nc-1)
    content = reCommand.sub(repl_f, content)
    with open('Commands', 'wb') as fp:
        pickle.dump(instructions, fp)
    
    #Сохранить обработанный вывод в файл .txt
    maximum = 30000 #Расчетный лимит символов Google Translate
    fileBase = re.sub('.tex$', '', name_file)
    begin = 0
    nPart = 0
    for m in re.finditer(r'\.\n', content):
        if(m.end()-begin<maximum):
            end = m.end()
        else:
            nameOfOutputFile = fileBase + '_%d.txt'%nPart
            nPart += 1
            with open(nameOfOutputFile, 'w') as txtFile:
    	        txtFile.write(content[begin:end])
            print('Output file:', nameOfOutputFile)
            begin = end
            end = m.end()
    nameOfOutputFile = fileBase + '_%d.txt'%nPart
    with open(nameOfOutputFile, 'w') as txtFile:
        txtFile.write(content[begin:])
    
    f = open(nameOfOutputFile, 'r', encoding='utf-8')
    contents = f.read()
    
    #translator = Translator()
    #translation = translator.translate(contents, dest='fr')
    
    
    translator = google_translator()  
    translate_text = translator.translate(contents, lang_tgt=lang)  
    
    
    
    with open(nameOfOutputFile, 'w', encoding='utf-8') as f:
    #    f.write(translation.text)
        f.write(translate_text)
    
    #Загрузка данных LaTeX из двоичных файлов.
    with open(nameOfOutputFile, 'r', encoding='utf-8') as fin:
        origin = fin.read()
    with open ('Comments', 'rb') as fp:
        remarks = pickle.load(fp)
    with open ('Commands', 'rb') as fp:
        instructions = pickle.load(fp)
    with open ('LaTeX', 'rb') as fp:
        LaTeX = pickle.load(fp)
    
    #Заменить странные символы, введенные переводом.
    translatedText = re.sub('\u200B', ' ', origin)
    
    #Исправить интервал.
    translatedText = re.sub(r'\\ ', r'\\', translatedText)
    translatedText = re.sub(' ~ ', '~', translatedText)
    translatedText = re.sub(' {', '{', translatedText)
    
    #Восстановить LaTeX и формулы.
    spot = 0
    newContent = ''
    nl = 0
    nc = 0
    corruptedTokens = []
    for m in re.finditer('\[ *[012][\.\,][0-9]+\]', translatedText):
        t = int(re.search('(?<=[\[ ])[012](?=[\.\,])', m.group()).group())
        n = int(re.search('(?<=[\.\,])[0-9]+(?=\])', m.group()).group())
        if(t==1):
            if(n<nl):
                print('Token ', m.group(), 'found in place of [%d.%d]. Revise manually and run again.'%(t, nl))
                break
            while(nl!=n):
                corruptedTokens.append('[%d.%d]'%(t,nl))
                nl += 1
            newContent += translatedText[spot:m.start()] + LaTeX[n]
            nl += 1
        elif(t==2):
            if(n<nc):
                print('Token ',m.group(),'found in place of [%d.%d]. Revise manually and run again.'%(t,nc))
                break
            while(nc!=n):
                corruptedTokens.append('[%d.%d]'%(t,nc))
                nc += 1
            newContent += translatedText[spot:m.start()] + instructions[n]
            nc += 1
        spot = m.end()
    newContent += translatedText[spot:]
    translatedText = newContent
    
    #Восстановление комментариев.
    spot = 0
    nRemark = 0
    newContent = ''
    for m in re.finditer('___COMMENT[0-9]*___', translatedText):
        n = int(re.search('[0-9]+', m.group()).group())
        if(n!=nRemark):
            print('Comment token ',m.group(),'is broken.')
            break
        newContent += translatedText[spot:m.start()] + remarks[n]
        nRemark += 1
        spot = m.end()
    newContent += translatedText[spot:]
    translatedText = newContent
    
    #Сохранить обработанный вывод в файл .tex.
    nameOfOutputFile = re.sub('.txt$', '.tex', nameOfOutputFile)
    with open(nameOfOutputFile, 'w', encoding='utf-8') as translation_file:
    	translation_file.write(translatedText)
    print('Output file:', nameOfOutputFile)
    
    #Сообщить о поврежденных токенах.
    if(corruptedTokens==[]):
        print('No damaged tokens. The translation is ready.')	
    else:
        print('Damaged tokens found:', end=' ')
        for c in corruptedTokens:
            print(c, end=' ')
        print()
        print('To improve the output, manually change the damaged tokens in the file', nameOfOutputFile, 'and run FromTranslation again.')
