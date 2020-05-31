#Rectal - budesh smeyatsya, no eto odin iz perevodov(pomimo osnovnih) na eng slova "voencomat"
import random

# Input Data
fileNameMale = open('name_male.csv', 'r', encoding="windows-1251")
nameMale = fileNameMale.read().split() # Chitaem data iz faila i razbivaem po elementam
fileNameMale.close()

with open('name_fmale.csv', 'r', encoding="windows-1251") as fileNameFmale: 
    nameFmale = fileNameFmale.read().split() # Var 2 open/input data pokrashe


fileSurNameAndFrqncy = open('sur_name.csv', 'r', encoding="windows-1251")
surNameAndFrqncy = fileSurNameAndFrqncy.read().split()
surName = surNameAndFrqncy[4::3] # vibiraem list familij iz raw data
frqncy = surNameAndFrqncy[5::3] # Chastota familii v Rus
frqncy = [elem.replace(',', '.') for elem in frqncy] # podgonyaem razdelitel pod sistemnij dlya float
frqncy = [float(elem) for elem in frqncy]
fileSurNameAndFrqncy.close()
city = ['Томск', 'Северс','Кемерово', 'Барнаул'] # ravnoveroyatnij sibirskij gorodskoi prizivnik

# 1 Generate list of recruiters
def old(): # generiruem vozrast po krasote soglasno dannim Rosstat_old.xls v faile opisanie
    chance = random.randint(0, 109032)
    if chance < 23157:
        year = random.randint(0, 19)
    elif chance < 48294:
        year = random.randint(20, 49)
    else:
        year = random.randint(50, 80)
    return(year)

recruitersList=[]
for i in range(99):
    gender = random.random()
    year = old()
    hight = int(random.gauss(175, 6)) # srednee 175 sm, sigma 6 sm
    wight = int(random.gauss(83, 15)) # srednij ves muzhchini 
    if year < 20: # toporno ponijaem rost i wes dlya molodih rostushih (koeficenti kostilnie priblezitelnie)
        hight -= 100 - 5*year
        wight -= int(0.955*wight*(1 - 0.033*year))
    imt = wight/(hight/100)**2 # index massi tela 
    if year < 18 or wight < 45 or imt > 40 or imt < 19: # usloviya godnosti
        godnost ='не '
    else:
        godnost =''

    if gender < 0.9:
        recruitersList.append(['муж', nameMale[random.randrange(len(nameMale))], 
                                str(random.choices(surName, weights = frqncy)).strip("[']"),
                                year, random.choice(city), str(wight) + ' Кг', 
                                str(hight) + ' См', godnost +'годен'
                            ])
    else:
        recruitersList.append(['жен', nameFmale[random.randrange(len(nameFmale))],
                                str(random.choices(surName, weights = frqncy) ).strip("[']") +'а',
                                year, random.choice(city), str(wight) + ' Кг', 
                                str(hight) + ' См', godnost + 'годна'
                            ])

print('Список кандидатов\n','\n'.join(str(elem) for elem in recruitersList))

popName = []
godniki = avrWihgt = man = 0
for recrut in recruitersList:
    popName.append(recrut[1])
    if recrut[0] == 'муж':
        man += 1
    if recrut[7] == 'годен' or recrut[7] == 'годна':
        godniki += 1
        avrWihgt += int(''.join(x for x in recrut[5] if x.isdigit())) #Razleplyaem ot 'Kg'

from collections import Counter # podclichaem shitalku dlya spiskov vozvrashaet tuple(elem, kol povtorov)

print('Три самых популярных имени(сколько раз встречается)', Counter(popName).most_common(3))
# print metodom f strok
print(f'Годны к службе: {godniki}\nСоотношение ж/м {(((len(recruitersList) - man)/man)):.2f}\n'
    f'Средний вес призывника: {avrWihgt/godniki:.2f}'
    )
    
with open("recruitersList.txt", "w") as file:
    file.write(str(recruitersList)) #Zapis v fail spiska kondidatov 