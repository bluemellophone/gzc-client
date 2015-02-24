from __future__ import absolute_import, division, print_function
from PyQt4 import QtGui, QtCore, QtWebKit, QtNetwork
#import matplotlib.pyplot as plt


class gps_map(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.domain = self.parent.domain + '/map/submit'
        self.initComponents()
        self.initLayout()

    def initComponents(self):
        self.pageLayout = QtGui.QVBoxLayout(self)
        self.webView = QtWebKit.QWebView(self)

    def initLayout(self):
        self.pageLayout.addWidget(self.webView)

    def initVisual(self):
        self.webView.resize(1000, 500)
        self.clear()

    def _urlencode_post_data(self, post_data):
        post_params = QtCore.QUrl()
        for (key, value) in post_data.items():
            post_params.addQueryItem(key, unicode(value))
        return post_params.encodedQuery()

    def clear(self, gpx_track=None):
        self.webView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Horizontal, QtCore.Qt.ScrollBarAlwaysOff)
        self.webView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
        # Load track Google Maps from server
        request = QtNetwork.QNetworkRequest()
        request.setUrl(QtCore.QUrl(self.domain))
        data = {}
        if gpx_track is not None:
            data['gps_data_str'] = gpx_track
        encoded_data = self._urlencode_post_data(data)
        request.setRawHeader('Content-Type',
                             QtCore.QByteArray('application/x-www-form-urlencoded'))
        self.webView.load(request,
                           QtNetwork.QNetworkAccessManager.PostOperation,
                           encoded_data)
