from Collection import Collection
import gtk

class MainWindow(gtk.Window):
	def __init__(self, tagger):
		self.tagger = tagger
		gtk.Window.__init__(self)
		# self.show_all()
		# gtk.main()