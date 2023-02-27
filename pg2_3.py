# ## CREATO DA ORTU prof. DANIELE
# ## daniele.ortu@itisgrassi.edu.it

from utility import Utility_bk
class Pg23:
    def __init__(self,   npg, builder, ch, bks):
        # print(bks)
        self.__bk = bks['bks'][ch]
        self.__lstCombo = ['smb', 'sshfs']
        if npg == 2:
            # print(bks)
            self.__rdLoc = builder.get_object('rdOrigineLoc')
            self.__txtLocPath = builder.get_object('txtOrigineLocPath')
            self.__btLocPath = builder.get_object('btOrigineLocPath')
            self.__cmbProtocollo = builder.get_object('cmbOrigineProtocollo')

            self.__rdRem = builder.get_object('rdOrigineRem')
            self.__cmbProtocollo = builder.get_object('cmbOrigineProtocollo')
            self.__txtUtente = builder.get_object('txtOrigineUtente')
            self.__txtHost = builder.get_object('txtOrigineHost')
            self.__txtRemPath = builder.get_object('txtOrigineRemPath')
            self.__who = 'dirDA'
        else:
            self.__rdLoc = builder.get_object('rdDestinazioneLoc')
            self.__txtLocPath = builder.get_object('txtDestinazioneLocPath')
            self.__btLocPath = builder.get_object('btDestinazioneLocPath')

            self.__rdRem = builder.get_object('rdDestinazioneRem')
            self.__cmbProtocollo = builder.get_object('cmbDestinazioneProtocollo')
            self.__txtUtente = builder.get_object('txtDestinazioneUtente')
            self.__txtHost = builder.get_object('txtDestinazioneHost')
            self.__txtRemPath = builder.get_object('txtDestinazioneRemPath')
            self.__who = 'dirTO'

        print("Carico "+self.__who)
        self.__caricaCampi()
        self.on_rd_click()
            # print("campi caricati ", self.__rdRem.get_active() )
    def setTxtLocPath(self, s):
        self.__txtLocPath.set_text(str(s))
    def setTxtRemPath(self, s):
        self.__txtRemPath.set_text(str(s))
    def getBtLocPathText(self):
        return self.__btLocPath.get_filename()
    #def getBtRemPathText(self):
    #    return \
    #        self.__txtUtente.get_text() + "@" + \
    #        self.__txtHost.get_text() + ":" + \
    #        self.__btRemPath.get_filename()
    def __getCombo(self):
        i = 0
        for t in self.__lstCombo:
            self.__cmbProtocollo.append_text(t)
            if t == self.__bk[self.__who]['protocollo']:
                self.__cmbProtocollo.set_active(i)
                # print(i)
            i = i + 1
    def __caricaCampi(self):
        self.__txtLocPath.set_editable(False)
        self.__txtLocPath.set_text(self.__bk[self.__who]['loc_path'])
        self.__btLocPath.set_filename(self.__bk[self.__who]['loc_path'])

        self.__getCombo()
        self.__txtHost.set_text(self.__bk[self.__who]['host'])
        self.__txtUtente.set_text(self.__bk[self.__who]['utente'])
        self.__txtRemPath.set_text(self.__bk[self.__who]['rem_path'])
        if self.__bk[self.__who]['remoto']:
            self.__rdRem.set_active(True)
        else:
            self.__rdLoc.set_active(True)

    def on_rd_click(self):
        if self.__rdLoc.get_active():
            self.__btLocPath.set_sensitive(True)
            self.__cmbProtocollo.set_sensitive(False)
            self.__txtHost.set_editable(False)
            self.__txtUtente.set_editable(False)
            self.__txtRemPath.set_editable(False)
        else:
            self.__btLocPath.set_sensitive(False)
            #self.__getCombo()
            self.__cmbProtocollo.set_sensitive(True)
            self.__txtHost.set_editable(True)
            self.__txtUtente.set_editable(True)
            self.__txtRemPath.set_editable(True)

    def on_mount(self, currdir):
        u = Utility_bk(currdir)
        r = u.mount(
            self.__cmbProtocollo.get_active_text(),
            self.__txtUtente.get_text() + "@" +
            self.__txtHost.get_text()+":/",
            "tmpConf"
        )
        if r != "":
            return r
        self.__btRemPath.set_filename("tmpConf")
        self.__txtRemPath.set_text(
            self.__btRemPath.get_filename()
        )
        return ""
    def on_salva(self):
        self.__bk[self.__who]['remoto'] = not self.__rdLoc.get_active()
        self.__bk[self.__who]['loc_path'] = self.__txtLocPath.get_text()

        self.__bk[self.__who]['protocollo'] = self.__cmbProtocollo.get_active_text()
        self.__bk[self.__who]['host'] = self.__txtHost.get_text()
        self.__bk[self.__who]['utente'] = self.__txtUtente.get_text()
        self.__bk[self.__who]['rem_path'] = self.__txtRemPath.get_text()
