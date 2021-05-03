#[Русское название0, Латинское название1, Тип2, [мебель3, строительство4, целлюлоза5,медицина6,музыкальныеибыт7,горюч8,химия9]]
import cfg
import pickle#библиотека для сериализации
import scrab
bd=[]
for i in range(0,min(len(cfg.latin_names),len(cfg.usability),len(cfg.names),len(cfg.types))):
    bd.append([cfg.names[i],(cfg.latin_names[i]),cfg.types[i],
               cfg.usability[i]])#объединяем данные в большой массив
with open(file='trees',mode='wb') as f:
    pickle.dump(bd,f)#сохранение данных