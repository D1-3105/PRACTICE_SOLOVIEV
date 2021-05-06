import bs4#парсер
import cfg#файл с конфигом
import wikipedia#wikipedia_api
import requests as r#библиотека загрузки
wikipedia.set_lang('ru')#устанавливаем язык апи википедии
def scrab_main_page():
    contentMain=r.get(cfg.main_page).text#контент страницы википедии
    soup=bs4.BeautifulSoup(contentMain, 'lxml')#создаем суп с контентом из википедии
    names=[]#названия деревьев
    all_species=soup.find('div',class_='mw-category')
    for i in all_species.find_all('a',title=True):#парсим имена
        names.append(i['title'])#поиск по атрибуту 'title'
    cfg.names=names
scrab_main_page()#скрабим страницу википедии
def scrab_current_page(page):
    spice=wikipedia.page(page)
    return spice.content
def find_topic(txt, type):
    txt=txt.split('\n')
    masret=[]
    for topic in txt:
        flag = 0
        for word in topic.split(' '):

            for trigger in cfg.categories['trigger_words_{}'.format(type)]:
                if trigger in word:
                    flag=1
        if flag == 1:
            masret.append(topic)
    if len(masret)>1:
        for topic in masret:
            print(str(masret.index(topic))+') '+topic)
        try:
            num1=int(input('Choose the correct topic(0-{}), if there is no correct topic type "-": '.format(len(masret))))
            return masret[num1]
        except:
            return 'UNKNOWN'
    if len(masret)==0:
        return 'UNKNOWN'
    return masret[0]
def find_latin_name(text:str):#ищем латинское название
    markerstart=text.find('(лат. ')+len('(лат. ')
    markerstop=0
    for letter in text[markerstart:markerstart+100]:
        if(letter!=')'):
            markerstop+=1
        else:
            break
    return (text[markerstart:markerstop+markerstart])
def find_usability(text):
    #[мебель(0), строительство(1), бумага(2), лекарства(3), муз инстр(4), спички(5), хим сырье(6)]
    use_list=[0]*7
    for cat in range(len(use_list)):
        use_list[cat]=conv2d(text=text,
                         trigger_words=cfg.categories['trigger_words_cat{}'.format(cat)],
                        )
    return (use_list)
def conv2d(text, trigger_words):#свертка текста и определение значения по словам триггерам
    textlist=text.split(' ')
    score=0
    for word in textlist:
        if len(word)<3:
            continue
        for i in range(len(trigger_words)):
            if trigger_words[i] in word:
               score+=1
    return score
def find_type(name):
    #[лиственные(0),хвойные(1)]
    cont=r.get('https://ru.wikipedia.org/wiki/'+name).content#страница дерева
    soup=bs4.BeautifulSoup(cont,
                           'lxml')
    type=soup.find_all('td',class_='ts-Taxonomy-rang-name')#ищем раздел с таксономией
    #выделяем название из полученной таксономии
    type=str(type[3])
    marker=type.find('</a>')
    type2return=''
    for letter in range(marker,0,-1):
        if type[letter]!='>':
            type2return+=type[letter]
        else:
            break
    if type2return[::-1]=='Хвойные<':
        return 'Хвойные'
    else:
        return 'Лиственные'
num=0
for name in cfg.names:
    try:
        print(num)#выводим номер текущей страницы
        num+=1
        scrabbed=scrab_current_page(page=name)#скрабим страницу дерева
        cfg.latin_names.append(find_latin_name(scrabbed))#ищем иноязычные названия
        cfg.usability.append(find_usability(scrabbed))#заполняем массив использований
        cfg.types.append(find_type(name))#ищем тип дерева
        print('PROCESSING HEIGHT!')
        cfg.height.append(find_topic(scrabbed, 'h'))
        print('PROCESSING AGE!')
        cfg.ages.append(find_topic(scrabbed,'age'))
    except:
        continue