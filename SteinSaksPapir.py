import random
import matplotlib.pyplot as plt


class Spiller(): #Superklasse

    _historie = []
    _resultater = []
    _playertype = 0
    _aksjoner = ['Stein', 'Saks', 'Papir']
    _motstander = 0
    _poengresultater = []
    _poengsum = 0

    def __init__(self): #Init er forskjellig for hver subklasse
        self._playertype = "Spiller" #Hvis man lager av superklassen, så vet vi det

    def velg_aksjon(self): #Superklassen velger tilfeldig
        valgt_aksjon = self._aksjoner[random.randint(0,2)]
        #self._historie.append(valgt_aksjon)
        return valgt_aksjon

    def motta_resultat(self, resultat, poengresultat): #Mottar tekstlig resultat og eget poengresultat per runde
        self._resultater.append(resultat)
        self._poengresultater.append(poengresultat)

    def oppgi_navn(self): #Returnerer eget navn, benyttes ved representasjon av resultat
        return self._playertype


class Tilfeldig(Spiller): #Velger på lik måte med superklassen, men instansierer egne lokale variabler

    def __init__(self):
        self._playertype = 'Tilfeldig'
        self._historie = []
        self._poengsum = 0
        self._resultater = []
        self._poengresultater = []


class Sekvensiell(Spiller):

    def __init__(self):
        self._playertype = 'Sekvensiell'
        self._historie = []
        self._poengsum = 0
        self._resultater = []
        self._poengresultater = []

    def velg_aksjon(self): #Velger 'Stein, Saks, Papir' på "repeat"
        if not self._historie:
            valgt_aksjon = self._aksjoner[0]
        else:
            valgt_aksjon = self._aksjoner[len(self._historie) % 3]

        #self._historie.append(valgt_aksjon)
        return valgt_aksjon


class MestVanlig(Spiller):

    def __init__(self):
        self._playertype = 'MestVanlig'
        self._historie = []
        self._poengsum = 0
        self._resultater = []
        self._poengresultater = []

    def velg_aksjon(self): #Velger basert på det fremst forekommende valget til motstanderen
        if not self._motstander._historie:

            valgt_aksjon = self._aksjoner[random.randint(0,2)]

        else:

            steinCount = 0
            saksCount = 0
            papirCount = 0

            for i in self._motstander._historie:
                if i == self._aksjoner[0]:
                    steinCount += 1
                elif i == self._aksjoner[1]:
                    saksCount += 1
                elif i == self._aksjoner[2]:
                    papirCount += 1

            #print("Stein:" + str(steinCount) + " Saks:" + str(saksCount) + " Papir:" + str(papirCount))

            if steinCount > saksCount and steinCount > papirCount:
                valgt_aksjon = self._aksjoner[2]
            elif saksCount > steinCount and saksCount > papirCount:
                valgt_aksjon = self._aksjoner[0]
            elif papirCount > steinCount and papirCount > saksCount:
                valgt_aksjon = self._aksjoner[1]

            else:
                valgt_aksjon = self._aksjoner[random.randint(0,2)] #Dersom det ikke er klart hva som er valgt oftest, velger klassen tilfeldig

        #self._historie.append(valgt_aksjon)
        return valgt_aksjon

class Historiker(Spiller):

    def __init__(self, historyCount):
        self._playertype = 'Historiker' + '(' + str(historyCount) + ')'
        self._historie = []
        self._poengsum = 0
        self._resultater = []
        self._poengresultater = []
        self._husk = historyCount

    def velg_aksjon(self): #Velger basert på sekvensen til motstanderen
        if len(self._motstander._historie) < self._husk or self._husk < 2:
            print("Random")
            valgt_aksjon = self._aksjoner[random.randint(0,2)]
        else:
            sekvens = []
            steinCount = 0
            saksCount = 0
            papirCount = 0

            for j in range(-(self._husk),0):
                sekvens.append(self._motstander._historie[j])

            print("Sekvens: ",sekvens)

            for k in range(0, len(self._motstander._historie)):
                if k < len(self._motstander._historie)-(self._husk)-1:

                    if sekvens == self._motstander._historie[k:k+self._husk]:
                        nesteValg = self._motstander._historie[k+self._husk]
                        if nesteValg == self._aksjoner[0]:
                            steinCount += 1
                        elif nesteValg == self._aksjoner[1]:
                            saksCount += 1
                        elif nesteValg == self._aksjoner[2]:
                            papirCount += 1

            if steinCount > saksCount and steinCount > papirCount:
                valgt_aksjon = self._aksjoner[2]
            elif saksCount > steinCount and saksCount > papirCount:
                valgt_aksjon = self._aksjoner[0]
            elif papirCount > steinCount and papirCount > saksCount:
                valgt_aksjon = self._aksjoner[1]

            #Metoden teller antall ganger et av de tre valgene forekommer etter den funnede sekvensen

            else:
                valgt_aksjon = self._aksjoner[random.randint(0,2)]

            #print("Stein:" + str(steinCount) + " Saks:" + str(saksCount) + " Papir:" + str(papirCount))
            #self._historie.append(valgt_aksjon)
        return valgt_aksjon


class EnkeltSpill(): #Klasse for å håndtere én kjørt runde

    def __init__(self, spiller1, spiller2):
        self._spiller1 = spiller1
        self._spiller1._motstander = spiller2
        self._spiller1_valg = 0
        self._spiller2 = spiller2
        self._spiller2._motstander = spiller1
        self._spiller2_valg = 0
        self._resultat = 0

    def gjennomfoer_spill(self):
        self._spiller1_valg = self._spiller1.velg_aksjon() #Lokal variabel som husker på valget til spilleren
        self._spiller2_valg = self._spiller2.velg_aksjon()
        self._spiller1._historie.append(self._spiller1_valg)#Historie inneholder valgene til en spiller i rekkefølge
        self._spiller2._historie.append(self._spiller2_valg)

        if self._spiller1_valg == self._spiller2_valg: #Uavgjort
            self._spiller1._poengsum += 0.5
            self._spiller2._poengsum += 0.5
            self._resultat = 'uavgjort'

            returnString = self.__str__()
            self._spiller1.motta_resultat(returnString, 0.5)
            self._spiller2.motta_resultat(returnString, 0.5)
            return returnString

        elif self.__gt__(self._spiller1_valg, self._spiller2_valg): #Spiller 1 vinner
            self._spiller1._poengsum += 1
            self._resultat = 'spiller1'

            returnString = self.__str__()
            self._spiller1.motta_resultat(returnString, 1)
            self._spiller2.motta_resultat(returnString, 0)
            return returnString

        elif self.__gt__(self._spiller2_valg, self._spiller1_valg): #Spiller 2 vinner
            self._spiller2._poengsum += 1
            self._resultat = 'spiller2'

            returnString = self.__str__()
            self._spiller1.motta_resultat(returnString, 0)
            self._spiller2.motta_resultat(returnString, 1)
            return returnString

    def __gt__(self, s1, s2): #Denne metoden definerer hvilke aksjoner som slår hvilke
        if s1 == self._spiller1._aksjoner[0] and s2 == self._spiller1._aksjoner[1]:
            return True
        elif s1 == self._spiller1._aksjoner[1] and s2 == self._spiller1._aksjoner[2]:
            return True
        elif s1 == self._spiller1._aksjoner[2] and s2 == self._spiller1._aksjoner[0]:
            return True
        else:
            return False


    def __str__(self): #En 'toString()-metode' som representerer rundene tekstlig

        if self._resultat == 'uavgjort':
            return str(self._spiller1.oppgi_navn()) + ':  ' + self._spiller1_valg + '.  ' + str(self._spiller2.oppgi_navn()) + ':  ' + self._spiller2_valg + '.  ->  Uavgjort'

        elif self._resultat == 'spiller1':
            return str(self._spiller1.oppgi_navn()) + ':  ' + self._spiller1_valg + '.  ' + str(self._spiller2.oppgi_navn()) + ':  ' + self._spiller2_valg + '.  ->  ' + str(self._spiller1.oppgi_navn()) + ' vinner'

        elif self._resultat == 'spiller2':
            return str(self._spiller1.oppgi_navn()) + ':  ' + self._spiller1_valg + '.  ' + str(self._spiller2.oppgi_navn()) + ':  ' + self._spiller2_valg + '.  ->  ' + str(self._spiller2.oppgi_navn()) + ' vinner'


class MangeSpill(): #Klasse for å håndtere turneringer

    def __init__(self, spiller1, spiller2, antall_spill):
        self._spiller1 = spiller1
        self._spiller2 = spiller2
        self._antall_spill = antall_spill
        self._enkelt_spill = EnkeltSpill(spiller1, spiller2)

    def arranger_enkeltspill(self): #All funksjonaliteten kan benyttes fra EnkelSpill klassen
        return self._enkelt_spill.gjennomfoer_spill()

    def arranger_turnering(self):
        x_values = []
        y_values = [] #y-values skal inneholde gjennomsnittlig poeng for spiller 1 per runde
        y_values.append(0) #Hverken av spillerne har fått poeng på "runde 0"
        currentsum = 0

        for i in range(0, self._antall_spill): #Kjører en rekke enkeltspill til turneringen er ferdig
            print(self.arranger_enkeltspill())

        for j in range (1, self._antall_spill+1): #Her tilegnes x- og y-variable til den grafiske representasjonen
            currentsum += self._spiller1._poengresultater[j-1]
            print(currentsum/j)
            x_values.append(j-1)
            y_values.append(currentsum/j)

        x_values.append(self._antall_spill) #Setter på siste indeks til x_values
        print(y_values)
        print(len(y_values))
        print(x_values)
        print(len(x_values))

        plt.plot(x_values, y_values) #x_values og y_values er lagt opp slik at y_values er et bilde av x_values
        plt.plot([0, self._antall_spill], [0.5, 0.5])
        plt.axis([0, self._antall_spill, 0, 1])
        plt.show()

        return ("Spiller 1: " + str(self._spiller1._poengsum) + "   Spiller 2: " + str(self._spiller2._poengsum))