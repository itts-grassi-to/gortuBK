# ## CREATO DA ORTU prof. DANIELE
# ## daniele.ortu@itisgrassi.edu.it

import pre_conf

c = pre_conf.GPre()
c.run()
if not c.continua:
    exit()

HOST = c.IP_HOST
import segnali
import gi
import os
import ast
import socket

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from mainNuovo import MainNuovo
from mainConfig import MainConfig, EventiConfig

CURRDIR = os.path.dirname(os.path.abspath(__file__))
GLADE = os.path.join(CURRDIR, 'danieleRBK.glade')
# PATH_CONF = os.path.join(c.dirLIB, 'ortuBK.conf')

# STRUTTURA_CONFIGURAZIONE={
#            'bks': {},
#            'altro': {'mailFROM': '', 'mailTO': ''}
# }
SPAZI = "    "


class Eventi:
    def __init__(self, conf):
        self.__configurazione = conf

    def on_click_nuovo(self, button):
        print("Click nuovo")
        gestione.on_nuovo_clicked()
        # gestione.on_nuovo_clicked(lstBKS)

    def on_click_modifica(self, button):
        # gestione.on_modifica_clicked()
        lst = gestione.getLstBKS()
        if not lst.get_selected_row():
            dialog = Gtk.MessageDialog(
                transient_for=None,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CLOSE,
                text="Seleziona il backup da modificare",
            )
            dialog.run()
            dialog.destroy()
            return
        builder = Gtk.Builder()
        ch = lst.get_selected_row().get_child().get_children()[1].get_label()
        tit = lst.get_selected_row().get_child().get_children()[0].get_text()
        # print(ch)
        mc = MainConfig(self.__configurazione, ch, builder)
        builder.connect_signals(EventiConfig(HOST, mc))
        window = mc.getWin()
        window.set_title("Modifico " + tit)
        window.set_modal(True)
        # window.set_icon_from_file(ICON)
        window.connect("destroy", Gtk.main_quit)
        window.show_all()
        Gtk.main()

    def on_click_cancella(self, button):
        gestione.on_cancella_clicked()

    def on_show_click_menu(self, button):
        print("clicked onshow")
        gestione.on_show_click()

    def lbl_click(self):
        print("clicked*************")


class GMain:
    def __init__(self, builder):
        # self.path_fconf = PATH_CONF
        self.__builder = builder
        self.__lstBKS = builder.get_object('lstBKS')
        self.__lblLed = builder.get_object('lblLed')
        self.__pop = builder.get_object('popover')

        '''
        if not os.path.isfile(PATH_CONF):
            with open(PATH_CONF, "w") as f:
                # print(str(STRUTTURA_CONFIGURAZIONE))
                f.write(str(STRUTTURA_CONFIGURAZIONE))
        '''

        # self.__configurazione = self.get_impostazioni(PATH_CONF)
        self.__configurazione = self.get_impostazioni()
        self.__builder.connect_signals(Eventi(self.__configurazione))
        # print(self.__configurazione)
        self.__bks = self.__configurazione['bks']

        self.lst_chiavi = []
        self.__attach_rows()
        self.__setLed()

    def getLstBKS(self):
        return self.__lstBKS

    def __setLed(self):
        print("setled")
        if self.invia(segnali.IS_ATTIVO) == segnali.OK:
            self.__lblLed.set_markup("<span background='green'><big>    </big></span>")
        else:
            self.__lblLed.set_markup("<span background='red'><big>    </big></span>")

    def invia(self, richi):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, segnali.PORT))
                s.sendall(richi)
                data = s.recv(segnali.DIM_BUFFER)
                return data
        except:
            return segnali.NOK
        # print(f"Received {data!r}")
    def __send_impostazioni(self, conf):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, segnali.PORT))
            s.sendall(segnali.SEND_CONF)
            d = s.recv(segnali.DIM_BUFFER)
            #print(conf)
            #print(len(str(conf)))
            if d == segnali.OK:
                s.sendall(bytes(str(conf), 'utf-8'))
                s.shutdown(socket.SHUT_WR)
            else:
                print("Errore invio dati")
    def get_impostazioni(self):
        ''''
        with open(f, "r") as data:
            d = ast.literal_eval(data.read())
            data.close()
            return d
        '''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, segnali.PORT))
                s.sendall(segnali.GET_CONF)
                rec =b""
                while True:
                    d = s.recv(segnali.DIM_BUFFER)
                    if not d:
                        break
                    rec += d
                return ast.literal_eval(rec.decode('utf-8'))
            except:
                return {}
    def __attach_rows(self):
        # print("Backup: " + str(self.bks['bks']))
        for chiave in self.__bks:
            self.__lstBKS.add(self.__attach_row(chiave))

    def __attach_row(self, ch):
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        bk = self.__bks[ch]
        label = Gtk.Label(label=bk['titolo'], xalign=0)
        label.set_property("width-request", 450)
        hbox.pack_start(label, False, True, 0)

        check = Gtk.CheckButton(label=ch)
        check.set_active(bk['attivo'])
        check.connect("toggled", self.__on_toggled_ck)
        hbox.pack_start(check, False, True, 0)

        self.lst_chiavi.append(ch)
        # hbox.pack_start(check, False, True, 0)

        return row

    def __on_toggled_ck(self, ck):
        ch = ck.get_label()
        self.__bks[ch]['attivo'] = ck.get_active()
        '''
        with open(PATH_CONF, "w") as data:
            data.write(str(self.__configurazione))
            data.close()
        '''
        self.__send_impostazioni(self.__configurazione)
    def on_cancella_clicked(self):
        # print("Hello, world")
        if not self.__lstBKS.get_selected_row():
            dialog = Gtk.MessageDialog(
                transient_for=None,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CLOSE,
                text="Seleziona il backup da cancellare",
            )
            dialog.run()
            dialog.destroy()
            return

        i = self.__lstBKS.get_selected_row().get_index()
        ch = self.__lstBKS.get_selected_row().get_child().get_children()[1].get_label()
        self.__lstBKS.remove(
            self.__lstBKS.get_row_at_index(i)
        )
        del self.__configurazione['bks'][ch]
        '''
        with open(PATH_CONF, 'w') as f:
            f.write(str(self.__configurazione))
            f.close()
        '''
        self.__send_impostazioni( self.__configurazione)
    def on_nuovo_clicked(self):
        # print("NUOVO")
        nv = MainNuovo(HOST, CURRDIR)
        nv.run()
        self.__configurazione = nv.configurazione
        self.__bks = nv.configurazione['bks']
        if nv.ch != "":
            self.__lstBKS.add(self.__attach_row(nv.ch))
        self.__lstBKS.show_all()

    def on_show_click(self):
        self.__pop.popup()

    def getWin(self):
        return self.__builder.get_object('MainWin')


builder = Gtk.Builder()
builder.add_from_file(GLADE)

# window = builder.get_object('MainWin')
# pop = builder.get_object('popover')
# lstBKS = builder.get_object('lstBKS')
# lblLed=builder.get_object('lblLed')
# window.set_icon_from_file(ICON)

gestione = GMain(builder)
# builder.connect_signals(Eventi())
window = gestione.getWin()
window.connect("destroy", Gtk.main_quit)
window.show_all()

Gtk.main()
