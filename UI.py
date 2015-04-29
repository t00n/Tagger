from Collection import Collection
from Config import Config
import gtk

class MainWindow(gtk.Window):
	def __init__(self, config):
		gtk.Window.__init__(self)
		self.connect("delete-event", gtk.main_quit)
		self.show_all()
		gtk.main()

if __name__ == '__main__':
	config = Config()
	window = MainWindow(config)