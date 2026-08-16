import json
import random

def spr(Plansza):
    y = 0
    for i in range(3):

        y1 = str(y)
        x1 = str(0)
        x2 = str(1)
        x3 = str(2)
        dan1 = x1 + "," + y1
        dan2 = x2 + "," + y1
        dan3 = x3 + "," + y1
        if Plansza[dan1] == Plansza[dan2] == Plansza[dan3] == 'X':

            return 1
        if Plansza[dan1] == Plansza[dan2] == Plansza[dan3] == 'O':

            return 2
        y = y + 1
    x = 0
    for i in range(3):

        x1 = str(x)
        y1 = str(0)
        y2 = str(1)
        y3 = str(2)
        dan1 = x1 + "," + y1
        dan2 = x1 + "," + y2
        dan3 = x1 + "," + y3
        if Plansza[dan1] == Plansza[dan2] == Plansza[dan3] == 'X':

            return 1
        if Plansza[dan1] == Plansza[dan2] == Plansza[dan3] == 'O':

            return 2
        x = x + 1
    lit = []
    x = 0
    y = 0
    for i in range(3):
        x1 = str(x)
        y1 = str(y)
        dan1 = x1 + "," + y1
        lit.append(dan1)
        x = x + 1
        y = y + 1
    if Plansza[lit[0]] == Plansza[lit[1]] == Plansza[lit[2]] == 'X':

        return 1
    if Plansza[lit[0]] == Plansza[lit[1]] == Plansza[lit[2]] == 'O':

        return 2
    lit1 = []
    x = 2
    y = 0
    for i in range(3):
        x1 = str(x)
        y1 = str(y)
        dan1 = x1 + "," + y1
        lit1.append(dan1)
        x = x - 1
        y = y + 1
    if Plansza[lit1[0]] == Plansza[lit1[1]] == Plansza[lit1[2]] == 'X':

        return 1
    if Plansza[lit1[0]] == Plansza[lit1[1]] == Plansza[lit1[2]] == 'O':

        return 2
    return 0
def plansza():
    q = 1
    t = str()
    for i in Plansza:
        t = t + Plansza[i]
        if q % 3 == 0:
            print(t)
            t = str()
        q = q + 1

def zam(g):
    k = []
    for h in g:
        k.append(h)
    return k
def zamP(Plan):
    Plan1 = {}
    for j in Plan:
        Plan1[j] = Plan[j]
    return Plan1
def atkx(Plansza):
    Pl = zamP(Plansza)
    for i in Pl:
        if Pl[i] == '|':
            Pl[i] = 'X'
            if spr(Pl) == 1:

                return i
            Pl[i] = '|'
    return 0
def atko(Plansza):
    Pl = zamP(Plansza)

    for i in Pl:
        if Pl[i] == '|':
            Pl[i] = 'O'
            if spr(Pl) == 2:
                return i
            Pl[i] = '|'
    return 0
def atkoR(Plansza,ruch):
    Pl = zamP(Plansza)
    if Pl[ruch] == '|':
        Pl[ruch] = 'O'
        if spr(Pl) == 2:
            return i
    return 0
def atkxR(Plansza,ruch):
    Pl = zamP(Plansza)
    if Pl[ruch] == '|':
        Pl[ruch] = 'X'
        if spr(Pl) == 1:
            return i
    return 0
def obro(Plansza):
    if atkx(Plansza) !=0:
        Pl = zamP(Plansza)
        ruch = atkx(Plansza)
        for i in Pl:
            if Pl[i] == '|':
                Pl[i] = 'O'
                if atkxR(Pl,ruch) == 0:

                    return i
                Pl[i] = '|'
    else:
        return 0
def obrx(Plansza):
    if atko(Plansza) !=0:
        Pl = zamP(Plansza)
        ruch = atko(Plansza)
        for i in Pl:
            if Pl[i] == '|':
                Pl[i] = 'X'
                if atkoR(Pl,ruch) == 0:

                    return i
                Pl[i] = '|'

    return 0
def atk2x(Plansza):
    Pl = zamP(Plansza)
    for i in Pl:
        if Pl[i] == '|':
            Pl[i] = 'X'
            if obro(Pl) != 0:
                g = obro(Pl)
                Pl[g] = 'O'
                if atko(Pl) ==0:
                    for n in Pl:
                        if Pl[n] == '|':
                            Pl[n] = 'X'
                            if obro(Pl) != 0:
                                h = obro(Pl)
                                Pl[h] = 'O'
                                if atkx(Pl) != 0:

                                    return [i, n]
                                Pl[h] = '|'
                            Pl[n] = '|'
                Pl[g] = '|'
            Pl[i] = '|'
    return 0
def atk22x(Plansza):
    Pl = zamP(Plansza)
    for n in Pl:
        if Pl[n] == '|':
            Pl[n] = 'X'
            if obro(Pl) != 0:
                h = obro(Pl)
                Pl[h] = 'O'
                if atkx(Pl) != 0:
                    return n
                Pl[h] = '|'
            Pl[n] = '|'
    return 0
def atk2o(Plansza):
    Pl = zamP(Plansza)
    for i in Pl:
        if Pl[i] == '|':
            Pl[i] = 'O'
            if obrx(Pl) != 0:
                g = obrx(Pl)
                Pl[g] = 'X'
                if atkx(Pl) ==0:
                    for n in Pl:
                        if Pl[n] == '|':
                            Pl[n] = 'O'
                            if obrx(Pl) != 0:
                                h = obrx(Pl)
                                Pl[h] = 'X'
                                if atko(Pl) != 0:

                                    return [i, n]
                                Pl[h] = '|'
                            Pl[n] = '|'
                Pl[g] = '|'
            Pl[i] = '|'
    return 0
def atk22o(Plansza):
    Pl = zamP(Plansza)
    for n in Pl:
        if Pl[n] == '|':
            Pl[n] = 'O'
            if obrx(Pl) != 0:
                h = obrx(Pl)
                Pl[h] = 'X'
                if atko(Pl) != 0:
                    return n
                Pl[h] = '|'
            Pl[n] = '|'
    return 0
def obr2x():
    Pl = zamP(Plansza)
    if atk22o(Pl)!= 0:
        for n in Pl:
            if Pl[n] =='|':
                Pl[n] ='X'
                if atk22o(Pl) ==0:
                    return n
                Pl[n] = '|'
    return 0
def obr2o():
    Pl = zamP(Plansza)
    if atk22x(Pl)!= 0:
        for n in Pl:
            if Pl[n] =='|':
                Pl[n] ='O'
                if atk22x(Pl) ==0:
                    return n
                Pl[n] = '|'
    return 0
def obr22o():
    Pl = zamP(Plansza)
    if atk2x(Pl)!= 0:
        for n in Pl:
            if Pl[n] =='|':
                Pl[n] ='O'
                if atkx(Pl) == 0:
                    if atk22x(Pl) ==0:
                        if atk2x(Pl) ==0:
                            return n
                Pl[n] = '|'
    return 0
def obr22x():
    Pl = zamP(Plansza)
    if atk2o(Pl)!= 0:
        for n in Pl:
            if Pl[n] =='|':
                Pl[n] ='X'
                if atk2o(Pl) ==0:
                    return n
                Pl[n] = '|'
    return 0
def zamiana(s,index,znak):
    return s[:index]+znak+s[index+1:]
def trans(dana):
    dan = dana.split(",")
    return int(dan[1])*3+int(dan[0])
def transR(ruch):
    x = int(ruch)%3
    y = int(ruch)//3
    return str(x)+','+str(y)
def najlep(stan,Q):
    k = -19998
    ruch = str()
    for i in Q[stan]:
        if Q[stan][i]> k:
            k = Q[stan][i]
            ruch = i
    return ruch
def zamQ(Q,stan,ruch,wart):
    if stan in Q and ruch in Q[stan]:
        Q[stan][ruch] = round(Q[stan][ruch]+wart,2)
    else:
        if stan in Q:
            Q[stan][ruch] = 0
        else:
            Q[stan] ={}
            Q[stan][ruch] = 0
def ruchAI(stan,Q):
    if stan in Q:
        if random.random() < Q["E"]:
            return random.choice(dos)
        else:
            return transR(najlep(stan,Q))
    else:
        return random.choice(dos)
def nag(historia,wart):
    gamma = 0.5
    y = 0
    for i in historia:
        stan = i[1]
        ruch = i[0]
        nagroda = wart*(gamma **y)
        zamQ(Q,stan,ruch,nagroda)
        y = y+1
def nagW(historia,wart):
    gamma = 0.8
    y = 0
    for i in historia:
        stan = i[1]
        ruch = i[0]
        nagroda = wart*(gamma **y)
        zamQ(Q,stan,ruch,nagroda)
        y = y+1
remisy = 0
porazki = 0
wygrane = 0
for a in range(1,10001):
    Plansza = {}
    bl=0
    x = 0
    y = 0
    gra = True
    dos = []
    przebieg = []
    przebieg2 = []
    b=[]
    hist = []
    wszs = []
    strat = 0
    rogi = ['0,0', '2,0', '0,2', '2,2']
    boki = ['0,1', '1,0', '1,2', '2,1']
    for i in range(3):
        x = 0
        for t in range(3):
            x1 = str(x)
            y1 = str(y)
            dan = x1 + "," + y1
            Plansza[dan] = "|"
            dos.append(dan)
            wszs.append(dan)
            x = x + 1
        y = y + 1
    dosrog = zam(rogi)
    los = []
    y = 0
    zag = []
    r = 0
    pocz= True

    stan="000000000"
    ostatniStan="000000000"
    while gra == True:
        if pocz == True:
            #zacz = input("kto zaczyna (k - komputer, g - gracz): ")
            zacz = "g"
            if zacz == 'k':
                try:
                    with open("q_O.json", 'r') as f:
                        Q = json.load(f)
                except FileNotFoundError:
                    Q = {}
                    Q["E"] = 0.7
            else:
                try:
                    with open("q_X.json", 'r') as f:
                        Q = json.load(f)
                except FileNotFoundError:
                    Q = {}
                    Q["E"] = 0.7
        if zacz == "g":
            dan = ruchAI(stan, Q)
            zamQ(Q, stan, str(trans(dan)), 0)
            ostatniStan = stan
            hist.append([str(trans(dan)), stan])
            stan = zamiana(stan, trans(dan), "1")
            ostatniRuch = trans(dan)
            Plansza[dan] = 'O'
            dos.remove(dan)
            przebieg.append(dan)
            przebieg2.append(trans(dan))
            Plansza[dan] = 'X'
            y = y+1
            if spr(Plansza) == 1 or spr(Plansza) == 2:
                break
            if y == 8:
                break
            if y == 0:
                los1 = ['0,0', '2,0', '0,2', '2,2', '1,1']
                k = random.choice(los1)
            if y == 1:
                if Plansza["1,1"] == '|':
                    k = "1,1"
                else:
                    k = random.choice(rogi)
            if y>1:
                if atko(Plansza) != 0:
                    k = atko(Plansza)
                    bl =1
                elif obro(Plansza) != 0:
                    k = obro(Plansza)
                    bl=2
                elif atk22o(Plansza) != 0:
                    k = atk22o(Plansza)
                    bl=3
                elif atk2o(Plansza) != 0:
                    k = atk2o(Plansza)[0]
                    r = atk2o(Plansza)[1]
                    bl = 4
                elif obr2o() != 0:
                    k = obr2o()
                    bl =6
                elif obr22o() != 0:
                    k = obr22o()
                    bl = 7
                else:
                    k = random.choice(dos)
                    bl=5
            stan = zamiana(stan, trans(k), "2")
            przebieg.append(k)
            przebieg2.append(trans(k))
            b.append(bl)
            bl = 0
            Plansza[k] = "O"
            dos.remove(k)
            zag.append(k)
            if spr(Plansza) == 1 or spr(Plansza) == 2:
                break
            y = y+1
            if y == 8:
                break
        if zacz == "k":
            if spr(Plansza) == 1 or spr(Plansza) == 2:
                break
            if y == 0:
                los1 = ['0,0', '2,0', '0,2', '2,2', '1,1']
                k = random.choice(los1)
            if y == 1:
                if Plansza["1,1"] == '|':
                    k = "1,1"
                else:
                    k = random.choice(rogi)
            if y>1:
                if atkx(Plansza) != 0:
                    k = atkx(Plansza)
                    bl=1
                elif obrx(Plansza) != 0:
                    k = obrx(Plansza)
                    bl=2
                elif atk22x(Plansza)!= 0:
                    k=atk22x(Plansza)
                    bl=6
                elif atk2x(Plansza) != 0:
                    k = atk2x(Plansza)[0]
                    r = atk2x(Plansza)[1]
                    bl=3
                elif atk22o(Plansza) != 0:
                    k = obr2x()
                elif atk2o(Plansza)!= 0:
                    w = True
                    bl=4
                    while w == True:
                        k = random.choice(dos)
                        if k != atk2o(Plansza):
                            w = False
                else:
                    k = random.choice(dos)
                    bl=5

            Plansza[k] = "X"


            stan = zamiana(stan, trans(k), "1")
            przebieg.append(k)
            przebieg2.append(trans(k))
            b.append(bl)
            bl = 0
            dos.remove(k)
            zag.append(k)
            y =y+1
            if spr(Plansza) == 1 or spr(Plansza) == 2:
                break
            if y == 8:
                break

            dan = ruchAI(stan,Q)
            zamQ(Q, stan, str(trans(dan)), 0)
            ostatniStan = stan
            hist.append([str(trans(dan)), stan])
            stan = zamiana(stan, trans(dan), "2")

            ostatniRuch = trans(dan)
            Plansza[dan] = 'O'
            dos.remove(dan)
            przebieg.append(dan)
            przebieg2.append(trans(dan))

            if spr(Plansza) == 1 or spr(Plansza) == 2:
                break
            y = y+1
            if y == 8:
                break
        pocz= False
    if zacz == 'k':
        if spr(Plansza) ==1:
            porazki = porazki+1
            wart = -1
        elif spr(Plansza) == 2:
            wygrane = wygrane+1
            wart = 1
            print(przebieg, przebieg2,b)
        else:
            remisy = remisy+1
            wart=1
    if zacz == 'g':
        if spr(Plansza) ==2:
            porazki = porazki + 1
            wart=-1
        elif spr(Plansza) == 1:
            wygrane = wygrane + 1
            wart=1
            print(przebieg, przebieg2, b)
        else:
            remisy = remisy+1
            wart = 1

    hist.reverse()
    if wart>0:
        nagW(hist,wart)
    else:
        nag(hist,wart)
    przebieg.clear()
    przebieg2.clear()
    b.clear()
    if a%100==0:
        if Q["E"]>0.2:
            Q["E"] =round(Q["E"]-0.02,2)
        prP = str(porazki)
        prR = str(remisy)
        if zacz == 'k':
            wf = open("wyniki_O.txt", 'a')
        else:
            wf = open("wyniki_X.txt", 'a')
        wf.write("porazki: "+prP+"%    remisy: "+prR+"%     wygrane(niemozliwe): "+str(wygrane)+'\n')
        remisy = 0
        porazki = 0
        wygrane = 0
        wf.close()
    if zacz == 'k':
        with open("q_O.json", 'w') as f:
            json.dump(Q, f)
    else:
        with open("q_X.json", 'w') as f:
            json.dump(Q, f)
