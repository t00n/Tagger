from Collection import Collection
import gtk

class MainWindow(gtk.Window):
	def __init__(self, config):
		gtk.Window.__init__(self)
		self.connect("delete-event", gtk.main_quit)
		self.show_all()
		gtk.main()