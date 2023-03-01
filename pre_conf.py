import os
import gi
import ast

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

CURRDIR = os.path.dirname(os.path.abspath(__file__))
GLADE = os.path.join(CURRDIR, 'pre.glade')
FC = os.path.join(CURRDIR, 'gortuBK.conf')


class Eventi:
    def __init__(self, b):
        self.__build = b
    def on_click_salva(self, button):
        print("on_click_salva")
        d = {
            'pathLib': self.__build.get_object('dirChose').get_filename() ,
            'ipHost':  self.__build.get_object('txt_ipHost').get_text()
        }
        with open(FC, "w") as fc:
            fc.write(str(d))
        dialog = Gtk.MessageDialog(
            transient_for=None,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.CLOSE,
            text="Configurazione salvata"
        )
        dialog.run()
        dialog.destroy()
    def on_click_continua(self, button):
        print("on_click_continua")
    def on_click_esci(self, button):
        print("on_click_esci")


class GPre:
    def __init__(self):
        self.__build = Gtk.Builder()
        self.__build.add_from_file(GLADE)
        self.__build.connect_signals(Eventi(self.__build))

        self.__dirLIB, self.__IP_HOST = self.__caricaFC()
        self.__build.get_object('dirChose').set_filename(self.__dirLIB)
        self.__build.get_object('txt_ipHost').set_text(self.__IP_HOST)
        #self.__dirChose.set_filename(self.__dirLIB)

        self.__obj_win = self.__build.get_object('preWin')

        #print(self.__dirChose.get_filename())
    def __caricaFC(self):
        try:
            with open(FC, "r") as fc:
                d = ast.literal_eval(fc.read())
            return d['pathLib'], d['ipHost']
        except:
            with open(FC, "w") as fc:
                fc.write(str({'pathLib':'', 'ipHost':''}))
            return "", ""
    def configurato(self):
        return True
    def getWin(self):
        return self.__obj_win
    def run(self):
        #w = self.__obj_win.getWin()
        self.__obj_win.connect("destroy", Gtk.main_quit)
        self.__obj_win.show_all()
        Gtk.main()
        return self.__dirLIB, self.__IP_HOST

#builder = Gtk.Builder()
#builder.add_from_file(GLADE)
# objWin = GPre(builder)
# w = objWin.getWin()
# w.connect("destroy", Gtk.main_quit)
# w.show_all()
# Gtk.main()

c = GPre()
print(c.run())