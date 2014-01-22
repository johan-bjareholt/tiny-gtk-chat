#!/usr/bin/python
from gi.repository import Gtk, GObject, Gio
from gi.repository.GdkPixbuf import Pixbuf
import threading
import socket
import gobject

import urllib2

class ConnectDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Connect to server", parent,
            Gtk.DialogFlags.MODAL, buttons=(
            Gtk.STOCK_OK, Gtk.ResponseType.OK,
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

        box = self.get_content_area()

        label = Gtk.Label("Insert server address and port:")
        box.add(label)

        self.entry = Gtk.Entry()
        #self.entry.connect("activate", Gtk.ResponseType.OK)
        box.add(self.entry)

        self.show_all()

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")
        self.set_border_width(5)
        self.set_default_size(400, 200)

        self.grid = Gtk.Grid(column_homogeneous=True, column_spacing=10, row_spacing=10)
        self.add(self.grid)

        # Connect button
        self.connectbutton = self.make_header_icon_button('Connect...', 'gtk-connect')
        self.connectbutton.connect("clicked", self.connect_dialog)
        self.favoritesbutton = self.make_header_icon_button('Favorites', 'gtk-directory')
        self.favoriteaddbutton = self.make_header_icon_button('Add to favorites', 'gtk-add')


        # Create header icon box
        self.headericonbox = Gtk.Box(spacing=5)
        self.grid.attach(self.headericonbox, 0, 0, 2, 1)

        # Add buttons to header icon box
        self.headericonbox.add(self.connectbutton)
        #self.headericonbox.add(self.favoritesbutton)
        #self.headericonbox.add(self.favoriteaddbutton)

        # Scrollable chat window
        self.chatwindow = Gtk.ScrolledWindow()
        self.chatwindow.set_vexpand(True)
        self.chatwindow.set_hexpand(True)
        #self.chatwindow.set
        # Chatbox
        self.chatbox = Gtk.TextView()
        self.chatbox.set_editable(False)
        self.chatbox.set_cursor_visible(False)
        self.chatwindow.add(self.chatbox)
        self.grid.attach(self.chatwindow, 0, 1, 2, 1)
        self.chatbox.set_wrap_mode(Gtk.WrapMode.WORD)

        # Message input
        self.chatinputentry = Gtk.Entry()
        self.chatinputentry.set_text("Hello World")
        self.chatinputentry.connect("activate", self.on_button_clicked)
        # Send message button
        self.messagesendbutton = Gtk.Button(label="Send message")
        self.messagesendbutton.connect("clicked", self.on_button_clicked)

        self.messagebox = Gtk.Box(spacing=5)
        self.messagebox.pack_start(self.chatinputentry, True, True, 0)
        self.messagebox.pack_end(self.messagesendbutton, False, False, 0)
        self.grid.attach(self.messagebox, 0, 3, 2, 1)

        #self.set_picture('http://lolcat.com/images/lolcats/1338.jpg')

        self.addChatEntry("Press the connect button and specify ip and port to connect")

    def make_header_icon_button(self, label, icon):
        iconbutton = Gtk.Button()
        icon = Gio.ThemedIcon(name=icon)
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        label = Gtk.Label(label)
        buttonbox = Gtk.Box(spacing=5)
        buttonbox.pack_start(image, True, True, 0)
        buttonbox.pack_start(label, True, True, 0)
        iconbutton.add(buttonbox)
        return iconbutton

    def set_picture(self, url):
        response = urllib2.urlopen(url) 
        input_stream = Gio.MemoryInputStream.new_from_data(response.read(), None) 
        pixbuf = Pixbuf.new_from_stream(input_stream, None) 
        image = Gtk.Image() 
        image.set_from_pixbuf(pixbuf)
        image.set_pixel_size(50)
        #image = Gtk.Image.new_from_file(image);
        #self.chatbox.draw
        self.grid.attach(image, 3, 1,1,1);

    def connect_dialog(self, widget):
        dialog = ConnectDialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            ip, port = dialog.entry.get_text().split(":")
            connection.connect(ip, int(port))
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

    def addChatEntry(self, messagetext):
    	textbuffer = self.chatbox.get_buffer()
    	textbuffer.insert(textbuffer.get_end_iter(), "\n"+messagetext)


    def on_button_clicked(self, widget):
        text = self.chatinputentry.get_text()
        if text:
            connection.sendData(text)
        self.chatinputentry.set_text("")

class Connection(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.connected = False

    def connect(self, address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.port = port
        self.start()

    def run(self):
        win.addChatEntry("Connecting...")
        try:
            self.socket.connect((self.address, self.port))
        except Exception as e:
            win.addChatEntry(e)
            self.disconnect
        win.addChatEntry("Connected!")
        self.connected = True

        try:
            while self.connected:
                    data = self.socket.recv(2048)
                    if data:
                        win.addChatEntry(data)
        except Exception as e:
            win.addChatEntry(e)
        self.disconnect()
        self.socket.close()

    def disconnect(self):
        self.connected = False
        self.stop()

    def sendData(self, data):
        if self.connected:
            self.socket.send(data)
            print(data)


if __name__ == '__main__':
    GObject.threads_init()
    connection = Connection()
    win = MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.connect("delete-event", connection.disconnect)
    win.show_all()

    Gtk.main()