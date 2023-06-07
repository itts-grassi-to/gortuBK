# ## CREATO DA ORTU prof. DANIELE
# ## daniele.ortu@itisgrassi.edu.it

class Pg1:
    def __init__(self,  builder, ch, bks):
        # print(bks)

        self._bks = bks
        self.__bk = bks['bks'][ch]
        self.__altro = bks['altro']
        self.__txtOra = builder.get_object('txtOra')
        self.__txtMin = builder.get_object('txtMin')
        self.__txtGio = builder.get_object('txtGio')
        self.__txtMese = builder.get_object('txtMese')
        self.__ckLun = builder.get_object('ckLun')
        self.__ckMar = builder.get_object('ckMar')
        self.__ckMer = builder.get_object('ckMer')
        self.__ckGio = builder.get_object('ckGio')
        self.__ckVen = builder.get_object('ckVen')
        self.__ckSab = builder.get_object('ckSab')
        self.__ckDom = builder.get_object('ckDom')
        self.__txtNumeroBK = builder.get_object('txtNumeroBK')
        self.__txtMailFROM = builder.get_object('txtMailFROM')
        self.__txtMailTO = builder.get_object('txtMailTO')
        try:
            self.__txtOra.set_text(self.__bk['cron']['ora'])
            self.__txtMin.set_text(self.__bk['cron']['minuto'])
            self.__txtGio.set_text(self.__bk['cron']['giorno'])
            self.__txtMese.set_text(self.__bk['cron']['mese'])
            # Giorno settimana
            self.__ckLun.set_active(1 in self.__bk['cron']['settimana'])
            self.__ckMar.set_active(2 in self.__bk['cron']['settimana'])
            self.__ckMer.set_active(3 in self.__bk['cron']['settimana'])
            self.__ckGio.set_active(4 in self.__bk['cron']['settimana'])
            self.__ckVen.set_active(5 in self.__bk['cron']['settimana'])
            self.__ckSab.set_active(6 in self.__bk['cron']['settimana'])
            self.__ckDom.set_active(0 in self.__bk['cron']['settimana'])
            #numero backup
            self.__txtNumeroBK.set_text(self.__bk['numeroBK'])
            # email
            self.__txtMailFROM.set_text(self.__altro['mailFROM'])
            self.__txtMailTO.set_text(self.__altro['mailTO'])
        except KeyError as er:
            print(f"warring: chiave di configurazione {er} inesistente")


    def __is_active(self, giorno):
        if self.__bk['cron']['settimana'] == '*':
            return True
        return giorno in self.__bk['cron']['settimana']

    def __salva_cron(self):
        self.__bk['cron']['minuto'] = self.__txtMin.get_text()
        self.__bk['cron']['ora'] = self.__txtOra.get_text()
        self.__bk['cron']['giorno'] = self.__txtGio.get_text()
        self.__bk['cron']['mese'] = self.__txtMese.get_text()
        self.__bk['cron']['settimana'] = []
        if self.__ckDom.get_active():
            self.__bk['cron']['settimana'].append(0)
        if self.__ckLun.get_active():
            self.__bk['cron']['settimana'].append(1)
        if self.__ckMar.get_active():
            self.__bk['cron']['settimana'].append(2)
        if self.__ckMer.get_active():
            self.__bk['cron']['settimana'].append(3)
        if self.__ckGio.get_active():
            self.__bk['cron']['settimana'].append(4)
        if self.__ckVen.get_active():
            self.__bk['cron']['settimana'].append(5)
        if self.__ckSab.get_active():
            self.__bk['cron']['settimana'].append(6)
    def __salva_purge(self):
        self.__bk['numeroBK'] = self.__txtNumeroBK.get_text()
    def __salva_altro(self):
        self._bks['altro']['mailFROM'] = self.__txtMailFROM.get_text()
        self._bks['altro']['mailTO'] = self.__txtMailTO.get_text()


    def salvaPG1(self):
        self.__salva_cron()
        self.__salva_purge()
        self.__salva_altro()
        return self._bks