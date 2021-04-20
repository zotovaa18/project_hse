# project_hse

0. Установите дополнительные внешние модули: SpeechRecognition, moviepy, opencv-python, Theano, googletrans, google-trans-new, scikit-image v0.17.2, numpy, matplotlib, pydub. Также автоматически должны были установиться модули Pillow, requests (если возникли ошибки, установите их вручную)
1. Скачайте этот репозиторий
2. Скачайте файл Demo-Europarl-EN.pcl с диска https://drive.google.com/drive/folders/0B7BsN5f2F1fZQnFsbzJ3TWxxMms , добавьте ее в папку, скачанную на первом шаге
3. Запустите через командную строку, набрав путь до папки, а также python interface.py. Или через любой IDE для python файл interface.py
4. На появившемся окне, если хотите конвертировать видео, в соответствующей строке введите путь до него (для удобства поместите его в текущую папку и введите только название), и нажмите кнопку "Конвертировать". Имя результирующего файла - result_end.tex *
5. Если хотите перевести .tex файл, то нажмите кнопку "Перевести .tex файл"
      1) В появившемся окне выберите язык
      2) Введите путь до .tex файла, который требуется перевести
      3) Нажмите "Ок"
      4) Результирующий файл будет иметь название <название вашего файла>_0.tex **

Для примера можно использовать файл video.mp4, а для примера перевода - end.tex

* Очень важно при последующих запусках программы предыдуший результирующий файл переименовывать для избежания протери данных
** Если .tex файл на русском языке, то некоторые среды LaTeX требуют добавить в начале файла \usepackage[russian] {babel} 
