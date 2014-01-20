#!/usr/bin/python
from gi.repository import Gtk, GObject, Gio
import threading
import socket
import gobject

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
        box.add(self.entry)

        self.show_all()

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")
        self.set_border_width(5)
        self.set_default_size(400, 200)

        grid = Gtk.Grid(column_homogeneous=True, column_spacing=10, row_spacing=10)
        self.add(grid)

        # Connect button
        self.connectbutton = Gtk.Button()
        icon = Gio.ThemedIcon(name="gtk-network")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        label = Gtk.Label("Connect...")
        connectbox = Gtk.Box(spacing=5)
        connectbox.pack_start(image, True, True, 0)
        connectbox.pack_start(label, True, True, 0)
        self.connectbutton.add(connectbox)
        self.connectbutton.connect("clicked", self.connect_dialog)

        headericonbox = Gtk.Box(spacing=5)
        headericonbox.add(self.connectbutton)
        grid.attach(headericonbox, 0, 0, 1, 1)

        # Scrollable chat window
        self.chatwindow = Gtk.ScrolledWindow()
        self.chatwindow.set_vexpand(True)
        self.chatwindow.set_hexpand(True)
        # Chatbox
        self.chatbox = Gtk.TextView()
        self.chatbox.set_editable(False)
        self.chatbox.set_cursor_visible(False)
        self.chatwindow.add(self.chatbox)
        grid.attach(self.chatwindow, 0, 1, 2, 1)


        # Message input
        self.chatinputentry = Gtk.Entry()
        self.chatinputentry.set_text("Hello World")
        # Send message button
        self.messagesendbutton = Gtk.Button(label="Send message")
        self.messagesendbutton.connect("clicked", self.on_button_clicked)

        messagebox = Gtk.Box(spacing=5)
        messagebox.pack_start(self.chatinputentry, True, True, 0)
        messagebox.pack_end(self.messagesendbutton, False, False, 0)
        grid.attach(messagebox, 0, 3, 2, 1)

        self.addChatEntry("Press the connect button and specify ip and port to connect")

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
            print(e)
        win.addChatEntry("Connected!")
        self.connected = True

        while self.connected:
            data = self.socket.recv(2048)
            if data:
                win.addChatEntry(data)
        self.socket.close()

    def sendData(self, data):
        if self.connected:
            self.socket.send(data)
            print(data)


if __name__ == '__main__':
    GObject.threads_init()
    win = MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()

    connection = Connection()

    Gtk.main()