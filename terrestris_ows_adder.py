# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TerrestrisOwsAdder
                                 A QGIS plugin
 Adds terrestris OWS services to connections
                              -------------------
        begin                : 2017-09-04
        git sha              : $Format:%H$
        copyright            : (C) 2017 by hwbllmnn
        email                : hwbllmnn@mailbox.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from builtins import str
from builtins import object
from qgis.PyQt.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
# Initialize Qt resources from file resources.py
#from . import resources
from qgis.core import QgsProject, QgsRasterLayer
import os.path

class TerrestrisOwsAdder(object):
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            '{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = u'&terrestris'
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'TerrestrisOwsAdder')
        self.toolbar.setObjectName(u'TerrestrisOwsAdder')

    def add_action(
        self,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        action = QAction(text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        self.add_action(
            text='OSM',
            callback=self.addOsmWms,
            parent=self.iface.mainWindow())
        self.add_action(
            text='Gray',
            callback=self.addOsmWmsGray,
            parent=self.iface.mainWindow())
        self.add_action(
            text='TOPO',
            callback=self.addTopoWms,
            parent=self.iface.mainWindow())
        self.add_action(
            text='TOPO/OSM',
            callback=self.addTopoOsmWms,
            parent=self.iface.mainWindow())


    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(
                u'&terrestris',
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def addOsmWms(self):
        crs = self.iface.mapCanvas().mapSettings().destinationCrs().authid()
        layer = QgsRasterLayer('url=http://ows.terrestris.de/osm/service&format=image/png&layers=OSM-WMS&styles=&crs=' + str(crs), 'OSM-WMS', 'wms')
        QgsProject.instance().addMapLayer(layer)

    def addOsmWmsGray(self):
        crs = self.iface.mapCanvas().mapSettings().destinationCrs().authid()
        layer = QgsRasterLayer('url=http://ows.terrestris.de/osm-gray/service&format=image/png&layers=OSM-WMS&styles=&crs=' + str(crs), 'OSM-WMS', 'wms')
        QgsProject.instance().addMapLayer(layer)

    def addTopoWms(self):
        crs = self.iface.mapCanvas().mapSettings().destinationCrs().authid()
        layer = QgsRasterLayer('url=http://ows.terrestris.de/osm/service&format=image/png&layers=TOPO-WMS&styles=&crs=' + str(crs), 'TOPO-WMS', 'wms')
        QgsProject.instance().addMapLayer(layer)

    def addTopoOsmWms(self):
        crs = self.iface.mapCanvas().mapSettings().destinationCrs().authid()
        layer = QgsRasterLayer('url=http://ows.terrestris.de/osm/service&format=image/png&layers=TOPO-OSM-WMS&styles=&crs=' + str(crs), 'TOPO-OSM-WMS', 'wms')
        QgsProject.instance().addMapLayer(layer)
