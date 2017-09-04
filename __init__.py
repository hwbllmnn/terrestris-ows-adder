# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TerrestrisOwsAdder
                                 A QGIS plugin
 Adds terrestris OWS services to connections
                             -------------------
        begin                : 2017-09-04
        copyright            : (C) 2017 by hwbllmnn
        email                : hwbllmnn@mailbox.org
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load TerrestrisOwsAdder class from file TerrestrisOwsAdder.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .terrestris_ows_adder import TerrestrisOwsAdder
    return TerrestrisOwsAdder(iface)
