from __future__ import division, print_function
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
import speech_recognition as sr
from moviepy.editor import *
import subprocess
import cv2
import os
import time
import sys

import punc 
import translateLaTeX
import math_s
import txt_tex

from PIL import Image, ImageTk

from skimage import measure
import matplotlib.pyplot as plt
import cv2
import json
import requests
import speech_recognition as sr 


import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks


def video_to_brilliant(): #функция создания конспекта

    # -------------------------------- #
    # СОЗДАЕТСЯ ПРОСТОЙ ТЕКСТ ИЗ ВИДЕО #
    # -------------------------------- #
    
    name_video = file_path.get()
    
    if not os.path.isfile(name_video):
        messagebox.showerror("Подождите", "Файл ошибка")
    else:
        messagebox.showinfo("Подождите", "Подождите, мы пишем конспект")
        
        name_audio = "audio.wav"
        name_file = "t.txt"
        new_name_file = "t_new.txt"
        
        #извлечение аудио-дорожки
        audioclip = AudioFileClip(name_video)
        audioclip.write_audiofile(name_audio)
        
        #разбиение аудио-дорожки на 3 сек (из-за большого веса аудио сразу текст нельзя получить)
        myaudio = AudioSegment.from_file(name_audio , "wav") 
        chunk_length_ms = 30000 
        chunks = make_chunks(myaudio, chunk_length_ms) 
        
        #сохранение каждой дорожки как wav файл
        fh = open(name_file, "a")
        for i, chunk in enumerate(chunks):
            chunk_name = "{0}.wav".format(i)
            print ("exporting", chunk_name)
            chunk.export(chunk_name, format="wav")
        
        #получение текста с каждой аудио-дорожки
        i=0
        for chunk in chunks:
            print ("in chunks")
        
            filename = str(i)+'.wav'
            print("Processing chunk "+str(i))
            file = filename
            r = sr.Recognizer()
            with sr.AudioFile(file) as source:
                r.adjust_for_ambient_noise(source)
                audio = r.record(source)
                
            try:
                rec = r.recognize_google(audio, language = "en-GB")
                print (rec)
                fh.write(rec+" ")
            except:
                rec = r.recognize_google(audio,show_all=True)
                print(rec,type(rec))
                
            i += 1
        fh.write("\n")   
        fh.write("\n")   
        fh.close()
        
        
    
        # ------------------------------------------------------------------------- #
        # СОЗДАНИЕ СКРИНШОТОВ ИЗ ВИДЕО И, В СЛУЧАЕ НЕОХОДИМОСТИ, ОБРЕЗАНИЕ КАРТИНКИ #
        # ------------------------------------------------------------------------- #
        
        
        messagebox.showinfo("Подождите", "Идет создание скриншотов")
        step = 15
        frames_count = 10
        
        currentframe = 0
        frames_captured = 0
        
          
        inputFile = name_video
         
          #reading the video from specified path 
        cam = cv2.VideoCapture(inputFile) 
        
          #reading the number of frames at that particular second
        frame_per_second = cam.get(cv2.CAP_PROP_FPS)
        
        while (True):
              ret, frame = cam.read()
              if ret:
                  if currentframe > (step*frame_per_second):  
                      currentframe = 0
                      
                      #сохрание скрина в нужном формате
                      name = str(frames_captured) + '.jpg'
                      print ('Creating...' + name) 
                      
                      cv2.imwrite(name, frame)  
                      
                      #crop - еслина видео есть стационарная доска - 
                      #можно вырезать чисто ее, чтобы картинка было больше
                      
                      filename = str(frames_captured)+'.jpg'
        #
        #              img1 = Image.open(filename)
        #              area = (200, 90, 600, 300)
        #              cropped_img1 = img1.crop(area)
        #              #cropped_img1.show()
        #              filename1 = ".\\2.5 screen\\"+str(frames_captured)+'.1.1.jpg'
        #              cropped_img1.save(filename1)
                      
                      frames_captured+=1
                                                          
                  currentframe += 1           
              if ret == False:
                  break
        finish_screen = filename
        cam.release()
        cv2.destroyAllWindows()
        
        
        

        # ------------------------------------------------- #
        # ВСТАВКА НУЖНЫХ СКРИНШОТОВ В НУЖНОЕ МЕСТО В ТЕКСТЕ #
        # ------------------------------------------------- #
        
        messagebox.showinfo("Подождите", "Идет сравнение скринов и вставка нужных в текст")
        

        original = cv2.imread("0.jpg")
        contrast = cv2.imread("1.jpg")
        
        original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
        
        i = 1
        filename2 = "1.jpg"
        filename1 = "0.jpg"


        while(filename2 != finish_screen):
            original = cv2.imread(filename1)
            contrast = cv2.imread(filename2)
            original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
            contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
            
            #отбор скиншотов с пронцентом схожести 93
            #если видео статическое можно оставить его,
            #если изначально понятно, что кадр постоянно движется, можно поставить меньше
            
            if (measure.compare_ssim(original, contrast).astype("float") <= 0.93):
                
                original = cv2.imread(filename1)
                contrast = cv2.imread(filename2)
                
                original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
                contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
                
                #поиск нужного фрагмента аудио-дорожки
                s = filename2[0:].split(".")
                p = str(round(int(s[0])/2 + 1)) + ".wav"
                print(p, '  ' , filename2)
                
                filename = p
                file = filename
                r = sr.Recognizer()
                with sr.AudioFile(file) as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.record(source)
                    
                try:
                    rec = r.recognize_google(audio, language = "en-GB")
                    #print (rec)
                except:
                    rec = r.recognize_google(audio,show_all=True)
                    print(rec,type(rec))
                    
                #вставка названия скриншота в текст  
                f_o = open(name_file)
                f_n = open(new_name_file, "w")
                
                for line in f_o:
                       
                    if rec in line:
                        index = line.find(rec)
                        output_line = line[:index] + " " + filename2 + " " + line[index:]
                        f_n.write(output_line)
                    else:
                        f_n.write(line)
                f_o.close()
                f_n.close()
                f_o = open(new_name_file)
                f_n = open(name_file, "w")
                for line in f_o:
                    f_n.write(line)
                f_o.close()
                f_n.close()
                #filename1 = filename2
                
                ##вставка картинки на гугл диск- можно выгружать скрины на гугл диск, если хотите       
                ## "Authorization": "Bearer ... нужно вставить свой ключ к гугл диску
                ##Это можно сделать через сайт OAuth 2.0 Playground
                ## requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",... вставить сслыку до места выгрузки
        
        #        headers = {"Authorization": "Bearer ya29.a0AfH6SMA0dWpM-EGYKddjsf_NpV2wwwV_r9QIAAcjy8VhwT10T_rmIoVDmasmfxjC86ITd1Lz_Xs3DxRtZKi4jvB7s7kQ6yCtTwXE_bPLNo83IyUEi5h4H3kjI-Y6AaZKHT8Bkr8pk4y7o7i0t8dPbqlwwp_Q"}
        #        para = {
        #            "name": filename2,
        #            "parents":["1A-t4tru0Iz1oLGF4o_ZQ8sH79-T-mu7J"]
        #        }
        #        files = {
        #            'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
        #            'file': open(filename2, "rb")
        #        }
        #        r = requests.post(
        #            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        #            headers=headers,
        #            files=files
        #        )
        #        print(r.text)
        
                filename1 = filename2
                
            i = i + 1    
            filename2 = str(i)+'.jpg'
        
            contrast = cv2.imread(filename2)
            contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
            

        # --------------------------------- #
        # ВСТАВКА ЗНАКОВ ПУНКТУАЦИИ В ТЕКСТ #
        # --------------------------------- #  
        
        messagebox.showinfo("Подождите", "Пунктуация")
        punc.pun()
        
        
        # ----------------------------------- #
        # ИЗМЕНЕНИЕ НА МАТЕМАТИЧЕСКИЕ СИМВОЛЫ #
        # ----------------------------------- #
        
        messagebox.showinfo("Подождите", "Идет замена на мат.символы")
        math_s.from_bros()
        
        # ----------------------------------- #
        # ПРЕВРАЩЕНИЕ .TXT ФАЙЛА В .TEX #
        # ----------------------------------- #
        
        messagebox.showinfo("Подождите", "Идет создание .tex файла")
        txt_tex.tex()
            
        messagebox.showinfo("Подождите", "Конец. Итоговый файл result_end.tex")
        
        #после завершения программы удаляем вспомогательные файлы
        os.remove("brilliant.txt")
        os.remove("t.txt")
        os.remove("t_new.txt")
        
        
def clicked_btn1(): #функции для создания перевода

    def clicked_ok():
        if not os.path.isfile(file_path.get()) or (re.search('.tex$', file_path.get())==None):
            messagebox.showerror("Ошибка", "В названии файла ошибка или он не существует")
        else:
            translateLaTeX.trans(lang.get(),file_path.get())
            window_trans.destroy()
            
    window_trans=Tk()
    

    window_trans.title("Перевод")
    window_trans.geometry('290x200')
    window_trans.configure(background='#ed4f5b')
    lbl4=Label(window_trans, text="Выберите язык",font=("Montserrat Classic", 12),background = '#ed4f5b', foreground = "#545454")
    file_path=Entry(window_trans, width=30, background='#ffee95')
    file_path.place(x=60,y=100)
    lbl2=Label(window_trans, text='Введите путь до .tex файла',font=("Arial Bold", 12),background='#ed4f5b', foreground='#545454')
    lbl2.place(x=5, y=70)          
    lang=Combobox(window_trans)
    #узнать, на какие языки можно переводить
    lang['values']=["en","ru",'af', 'sq', 'ar', 'hy', 'zh', 'fr', 'de', 'it']
        
    
    lbl4.place(x=5,y=10)
    #btn2.grid(column=4,row=3)
    lang.place(x=65, y=40)
    
    btn2=Button(window_trans, text='Ok', command=clicked_ok, font=("Montserrat Classic", 10), background = '#545454', foreground = "#ffde59",width=10)    
    btn2.place(x=100,y=150)
    window_trans.mainloop()
    
    


window = Tk()

window.title(" Создание конспектов лекций МИЭМа и синхронизация их с видеолекциями")
window.geometry('1000x300')


l=''

bg = PhotoImage(file = "pic.png")
  
# Show image using label
label1 = Label( window, image = bg)
label1.place(x = 0, y = 0)
#
#lbl1=Label(window, text="",font=("Arial Bold", 12))
lbl6=Label(window, text="0",font=("Arial Bold", 10))
lbl2=Label(window, text='введите путь до видео-файла',font=("Arial Bold", 12),background='#ffffff', foreground='#333333')
#lbl3=Label(window, text='Если вы хотите перевести итоговый конспект \n на другой язык,  нажмите кнопку "Перевести"',font=("Arial", 8))
file_path=Entry(window, width=47, background='#ffee95')

btn1=Button(window, text='Перевести .tex файл', command=clicked_btn1, font=("Arial", 12),background = '#545454', foreground = "#ffde59", width=20)
btn2=Button(window, text='Конвертировать', command=video_to_brilliant, font=("Arial", 12),background = '#545454', foreground = "#ffde59")
#lbl1.grid(column=0, row=0 )
#lbl6.grid(column=2000, row=600)
lbl2.place(x=585, y=60)
file_path.place(x=555,y=100)
#lbl3.place(x=575,y=150)
btn2.place(x=633, y=150)
btn1.place(x=608,y=190)
#lbl2.grid(column=60,row=50, columnspan=10)
#file_path.grid(column=600,row=100)
#lbl3.grid(column=600,row=120)

#btn1.grid(column=600,row=400,ipadx=10, ipady=6, padx=10, pady=10)
#btn2.grid(column = 600, row = 30)
#print(l)


window.mainloop()
