# ## CREATO DA ORTU prof. DANIELE
# ## daniele.ortu@itisgrassi.edu.it

import os
import gi
import ast
import socket
import segnali
#import utility

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class EventiNuovo:
    def __init__(self, mn):
        self.__mn = mn
    def on_click_salva(self, button):
        print("Click salva")
        self.__mn.on_salva_clicked()

    def on_click_annulla(self, button):
        print("ANNulla mainnuovo")
        self.__mn.on_annulla()

class MainNuovo:
    def __init__(self,host, currdir):
        # self.__builder = builder
        self.ch = ""
        self.__builder=Gtk.Builder()
        self.__host = host
        self.__builder.add_from_file( os.path.join(currdir, 'nuovo.glade'))
        '''
        with open(self.__path_conf, 'r') as f:
            self.configurazione = ast.literal_eval(f.read())
            f.close()
        '''
        self.configurazione = self.__get_impostazioni()
        self.__txtChiave = self.__builder.get_object('txtChiave')
        self.__txtTitolo = self.__builder.get_object('txtTitolo')

    def __get_impostazioni(self):
        ''''
        with open(f, "r") as data:
            d = ast.literal_eval(data.read())
            data.close()
            return d
        '''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.__host, segnali.PORT))
            s.sendall(segnali.GET_CONF)

            rec = b""
            while True:
                d = s.recv(segnali.DIM_BUFFER)
                if not d:
                    break
                rec += d
            return ast.literal_eval(rec.decode('utf-8'))
    def __send_impostazioni(self, conf):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.__host, segnali.PORT))
            s.sendall(segnali.SEND_CONF)
            d = s.recv(segnali.DIM_BUFFER)
            #print(conf)
            #print(len(str(conf)))
            if d == segnali.OK:
                s.sendall(bytes(str(conf), 'utf-8'))
                s.shutdown(socket.SHUT_WR)
            else:
                print("Errore invio dati")
    def __pulisci(self, s):
        s = s.replace("à", "a")
        s = s.replace("è", "e")
        s = s.replace("é", "e")
        s = s.replace("ì", "i")
        s = s.replace("ò", "o")
        s = s.replace("ù", "u")
        s = s.replace("À", "a")
        s = s.replace("È", "e")
        s = s.replace("É", "e")
        s = s.replace("Ì", "i")
        s = s.replace("Ò", "o")
        s = s.replace("Ù", "o")
        return s
    def __esisteCodice(self, s):
        # print("esisteCodice")
        return s in self.configurazione['bks']
    def __salvaNuovo(self, ch, titolo):
        # print("salvaNuovo")
        # self.bks['bks'] = ch
        self.ch = ch

        self.configurazione['bks'][ch] = {
                'attivo': True ,'titolo': titolo,
                'dirDA': {'remoto': False, 'loc_path': '', 'protocollo': '', 'host': '', 'utente': '', 'rem_path': '', 'mnt': ch+"DA"},
                'dirTO': {'remoto': False, 'loc_path': '', 'protocollo': '', 'host': '', 'utente': '', 'rem_path': '', 'mnt': ch+"TO"},
                'cron': {'minuto': '1', 'ora': '1', 'giorno': '1', 'mese': '1', 'settimana': []}
            }
        # os.system("mkdir -p " + self.configurazione['bks'][ch]['dirDA']['mnt'])
        # os.system("mkdir -p " + self.configurazione['bks'][ch]['dirTO']['mnt'])
        '''
        with open(self.__path_conf, "w") as data:
            data.write(str(self.configurazione))
            data.close()
        '''
        self.__send_impostazioni(self.configurazione)
    def __msg(self, s, tipo):
        dialog = Gtk.MessageDialog(
            transient_for=None,
            flags=0,
            message_type=tipo,
            buttons=Gtk.ButtonsType.CLOSE,
            text=s
        )
        dialog.run()
        dialog.destroy()

    def on_salva_clicked(self):
        # print("Salva")
        if not self.__txtChiave.get_text().isalpha():
            self.__msg("NON puoi inserire nel codice caratteri diversi da quelli dell'alfabeto",Gtk.MessageType.ERROR)
            return
        ch = self.__pulisci(self.__txtChiave.get_text())
        if self.__esisteCodice(ch):
            self.msg("Codice esistente", Gtk.MessageType.ERROR)
            return

        titolo = self.__txtTitolo.get_text()
        if len(titolo) == 0:
            self.__msg("Inserisci il titolo", Gtk.MessageType.ERROR)
            return
        self.__salvaNuovo(ch, titolo)
        self.__msg("Inserito nuovo backup ... configuralo", Gtk.MessageType.INFO)
        self.__w.destroy()

    def run(self):
        self.__builder.connect_signals(EventiNuovo(self))
        self.__w = self.__builder.get_object('NuovoWin')
        self.__w.connect("destroy", Gtk.main_quit)
        self.__w.show_all()
        Gtk.main()
        # self.ch = ""
    def on_annulla(self):
        # self.ch = ""
        self.__w.destroy()

#*********** da commentare
CURRDIR = os.path.dirname(os.path.abspath(__file__))
PATH_CONF = os.path.join(CURRDIR, 'danieleReteBK.conf')
# builder = Gtk.Builder()
# nv = MainNuovo(CURRDIR,PATH_CONF)
# builder.connect_signals(EventiNuovo(nv))
#nv.run()


