# Траффик авто на фоне Авроры СПб

<a href="https://vkvideo.ru/video-18901857_456254570?ref_domain=guide-spb.fontanka.ru" target="_blank">*Источник видео*</a>

Целью данного репозитория будем считать подсчет машин с выводом в базу данных данных (Windows 10).

![Пример](content_for_readme/1_img283.png)

## Для этого:

### 1. Обучим модель YOLOv8m, будет включать классификацию (ну тут только один класс, но она есть), детекцию и треккинг.
### 2. Затем определим поле на дороге, при пересечении которого машина будет засчитываться (возможно для точности потребуется несколько полей, т.к. машины перекрывают друг друга время от вмемени).
### 3. Подсоединимся к базе данных.
### 4. Попробуем подсоединить дашборд, может быть типа grafana с выводом статистики через порт в браузер.
### 5. Пока до этого пункта доберемся, еще что-нибудь придумаем ...)

>Важно! Установка пакетов requirements.txt, прежде чем егозапускать с помощью pip install -r requirements.txt, нужно создать файлик .py и .ipynb, после чего создаем среду .conda выбираем ее для .py (не забываем добавить среду в переменные окружения windows), в файлике .ipynb создаем простую мат. операцию и запускаем, после чего появится запрос на подключение kernel, выбираем нашу среду .conda. После этих манипуляций проблем с requirements.txt не должно возникнуть.

## 1. Обучение модели.
**1.1 Записываем видео с [сайта](https://guide-spb.fontanka.ru/peterburg-veb-kamery "Источник видео") в формате mp.4.**

Заходим на сайт включаем трансляцию, с момощью кнопок _Windows + Alt + R_ создаем видеофайл, от которого и будем плясать. Нужно отметить, что моделька будет хорошо работать в таких же условиях, как на видео, т.е. зима, снег, ночь, огоньки, для иных условий, например день, или лето, потребуется дообучение.

**1.2 Разбиваем видео на кадры, получая картинки в формате png**

Для этого используем программку [FFmpeg](https://ffmpeg.org/download.html).
Чтобы она работала в командной строке, необходимо в "Переменных среды" прописать путь _C:\\ffmpeg\bin_. После этого в командной сроке пишем:
```
ffmpeg -i train.mp4 -vf fps=1.5 images_train/1_img%03d.png
```
>* ffmpeg -  это команда для запуска программы FFmpeg, которая используется для обработки
видео и аудио файлов
>* --i train.mp4 - это опция для указания входного файла train.mp4
>* -vf fps=1.5 - это опция для указания фильтрации видео с заданной частотой кадров в 1.5 кадра
в секунду
>* images_train/img%03d.png - это опция для указания выходной директории и формата имени
файлов, где %03d означает использование трех цифр для нумерации файлов

У меня получилось где-то 250 картинок.

**1.3 Разметка картинок с помощью [CVAT](https://www.cvat.ai/).**

 Очень удобный редактор, в моем случае я его поднял локально, используя [образ Docker](https://docs.cvat.ai/docs/administration/basics/installation/).

Т.к. размечать все картинки очень лень, я разметил около 16-ти картинок, дообучил модель 
YOLOv8m, прогнал всю пачку картинок через модель и получил неплохую разметку, после чего убрал
 лишние боксы, добавил недостающие и уточнил полезные. Далее будет описание обработки основной 
 парии картинок, но такую стратегию надо выбирать и для обучения предварительных 16-ти картинок.

 > > ! При экспорте размеченных картинок из CVAT нужно выбрать формат YOLO 1.1

**1.4 Формирование картинок с аннотациями для подачи в модель YOLO.**

Сильно много писать здесь не буду, есть 
[хороший репозиторий](https://github.com/ankhafizov/CVAT2YOLO) на GitHub,
 в котором все подробно объяснено. Единственное, что хотельсь бы добавить,
 виртуальную среду лучше ставить на python 3.10, иначе вроде там разные
 ошибки будут вылетать.

**1.5 Обучаем модель.**

У меня нет карты с GPU, но обучать быстро очень хочется, поэтому обучение проводилось 
с помощью GPU _Google Colab_ с подгрузкой данных на _Google Диск_.

Я выложил в папку _study файлик _Обучение_YOLO_данные_с_googgledisk.ipynb_, который я использовал для обучения. Там понадобятся первых 
3 блока. Первый загружает _Google Диск_ (нужно его завести), второй подгружает модели 
ultralytics (включает и YOLOv8m), в третьем уже происходит обучение модели (нужно не забыть
выбрать GPU, а то будет обучаться до второго пришествия). Я обучал на протяжении 250-ти эпох.

После обучения скачиваем из папки _/content/runs/detect/train/weights_ файл best.pt, это 
файлик с лучшими весами, т.е. весами которые выдали лучший результат по статистикам.
Т.е. в дальнейшем вместо файлика yolov8m.pt используем best.pt (можно переименовать, если
 не нравится.)

**1.6 Пропускаем видео через модель.**

В папке _study есть файлик tracker.ipynb, там только нужно указать путь до модели, путь до файла видео входного и путь до файла видео выходного (файлик создастся в процессе обучения).

Результат моего обучения показан на видео ниже, Аврора красивая). Дальше уже будем внедрять hydra, бузу данных и пр.

__Пример демонстрации трекинга машин:__
![Traffic statistics 1](content_for_readme/1_out_3_short.gif)
## 2. Определяем поле для считывания машин.
**2.1 Создание поля регистрации с помощью [CVAT](https://www.cvat.ai/).**

Загружаем любую из картинок на которых обучали модель. В режиме редактирования кликаем на значек похожий на солнце с планетами, там выбираем area -> shape, после чего, как показано ниже, выделяем область для регистрации машин:

![Пример](content_for_readme/area.png)

**2.2 Создание файлиск с полями.**

После выделенияя нужных областей сохраняем данные и делаем экпорт в формате COCO Keypoints 1.0 (возможно есть лучшие форматы, но я не нашел, хотя сильно и не искал), затем выдергиваем из полученного файлика координаты областей и оформляем как в configs/entry_exit_lanes.json.
P.S. Нужные данные находятся под ключиком "keypoints", там просто удаляем двойки, сохраняя последовательность, и остаются координаты вершин.

**2.3 Регистрация полей в общей структуре.**

Прописываем путь до файла с полями в файлик configs/app_config.yaml, как значение с ключем roads_info

Создали поле при пересечении которого середины bboxа, он засчитывается:
![Traffic statistics 2](content_for_readme/aurora_short.gif)
vbr9vb9bv9rb9vb9ii