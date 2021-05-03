import pickle
import cfg
def separate():
    dataset=pickle.load(open(file='trees',mode='rb'))#загрузка объед файла
    type0=[]#хвойные
    type1=[]#лиственные
    for treeMas in dataset:
        if treeMas[2]!='Лиственные':
            type0.append(treeMas)
        else:
            type1.append(treeMas)
    with open('treesType0.pkl','wb') as f:
        pickle.dump(type0,f)#записываем хвойные
        f.close()
    with open('treesType1.pkl','wb') as f:
        pickle.dump(type1,f)#записываем лиственные
        f.close()
def find(t,c):#тип,характеристика
    trees=[]#деревья
    masret=[]#массив на возврат
    with open('treesType{}.pkl'.format(t),'rb') as f:
        trees=pickle.load(f)#загружаем данные из файла
    for tree_ in trees:
        if tree_[3][cfg.categotieslist.index(c)]>1:#ищем индекс в категориях
            masret.append(tree_)#добавляем элемент
    return masret#возврат
if __name__ == '__main__':
    separate()#вызов разделения файла
    find_trees=input("Enter the characteristic ('мебель','строительство','бумага','медицина','быт','горючее','химия'): ")#выбрать характеристику
    try:#обрабатываем исключения
        ans=[]#ответ от find_trees
        for i in range(2):
            ans.append(find(i,find_trees))
        a=[]#массив для сортировки имен
        for t in ans:
            for tree in t:
                a.append(tree[0])
        a.sort()#сортируем по алфавиту
        for name in a:
            print(name)#выводим названия деревьев.
    except:
        print('FILES ARE EMPTY!')#сообщение об ошибке
