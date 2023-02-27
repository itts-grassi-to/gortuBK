# ## CREATO DA ORTU prof. DANIELE
# ## daniele.ortu@itisgrassi.edu.it
import os
import gi
import ast
import socket
import segnali

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from pg1 import Pg1
from pg2_3 import Pg23


CURRDIR = os.path.dirname(os.path.abspath(__file__))
# PATH_CONF = os.path.join(CURRDIR, 'danieleReteBK.conf')
GLADE = os.path.join(CURRDIR, 'config.glade')

class EventiConfig:

    def __init__( self, obj):
        self.__mc = obj
    def on_click_salva(self, button):
        self.__mc.salvaPG1()
        self.__mc.pg2.on_salva()
        self.__mc.pg3.on_salva()
        # print(self.__mc._bks)
        with open(self.__mc.path_conf,'w') as f:
            f.write(str(self.__mc._bks))
            f.close()
        dialog = Gtk.MessageDialog(
            transient_for=None,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.CLOSE,
            text="Salvato impostazioni"
        )
        dialog.run()
        dialog.destroy()
        self.__invia(segnali.RESTART)
    def __invia(self, richi):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((segnali.HOST, segnali.PORT))
                s.sendall(richi)
                data = s.recv(1024)
                return data
        except:
            return segnali.NOK
        # print(f"Received {data!r}")

    def on_click_monta(self, button):
        print("click monta")
        r = self.__mc.pg2.on_mount(CURRDIR)
        if r != "":
            dialog = Gtk.MessageDialog(
                transient_for=None,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CLOSE,
                text=r
            )
        else:
            dialog = Gtk.MessageDialog(
                transient_for=None,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.CLOSE,
                text="Ho montato la directory"
            )
        dialog.run()
        dialog.destroy()

    def on_click_rd_origine_loc(self, rd):
       # print("click origine")
        self.__mc.pg2.on_rd_click()
    def on_click_rd_destinazione_loc(self, rd):
        print("Click destinazione")
        self.__mc.pg3.on_rd_click()
    def on__ori_loc_currdir_changed(self,widget):
        #print(self.__mc.pg2.getBtLocPathText())
        self.__mc.pg2.setTxtLocPath(self.__mc.pg2.getBtLocPathText())
    def on__dst_loc_currdir_changed(self,widget):
        #print(self.__mc.pg3.getBtLocPathText())
        self.__mc.pg3.setTxtLocPath(self.__mc.pg3.getBtLocPathText())

    def on_click_annulla(self, button):
        pass

class MainConfig(Pg1):
    def __init__(self, path_conf, ch, builder):
        self.path_conf = path_conf
        self.__builder = builder

        with open(self.path_conf, "r") as f:
            self.__bks = ast.literal_eval(f.read())
            f.close()
        self.__builder.add_from_file(GLADE)
        Pg1.__init__(self, builder, ch, self.__bks)
        self.pg2 = Pg23(2, builder, ch, self.__bks)
        self.pg3 = Pg23(3, builder, ch, self.__bks)

    def getWin(self):
        return self.__builder.get_object('MainWinConfig')


# builder = Gtk.Builder()
# mc = MainConfig("pr", builder)
# builder.connect_signals(EventiConfig())
# pg1 = Pg1("pr", builder, bks)

# window = mc.getWin()


# window.set_title("GIGI")
# window.set_icon_from_file(ICON)
# window.connect("destroy", Gtk.main_quit)
# window.show_all()

# Gtk.main()