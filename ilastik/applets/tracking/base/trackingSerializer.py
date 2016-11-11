###############################################################################
#   ilastik: interactive learning and segmentation toolkit
#
#       Copyright (C) 2011-2014, the ilastik developers
#                                <team@ilastik.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# In addition, as a special exception, the copyright holders of
# ilastik give you permission to combine ilastik with applets,
# workflows and plugins which are not covered under the GNU
# General Public License.
#
# See the LICENSE file for details. License information is also available
# on the ilastik web site at:
#		   http://ilastik.org/license.html
###############################################################################
from ilastik.applets.base.appletSerializer import AppletSerializer,\
    SerialDictSlot, SerialSlot, SerialHdf5BlockSlot, SerialPickleableSlot, SerialPickledValueSlot


try:
    import pgmlink
except:
    import pgmlinkNoIlpSolver as pgmlink

class TrackingSerializer(AppletSerializer):
    
    def __init__(self, mainOperator, projectFileGroupName):
        slots = [SerialDictSlot(mainOperator.Parameters, selfdepends=True),
                 SerialDictSlot(mainOperator.EventsVector, transform=str, selfdepends=True),
                 SerialDictSlot(mainOperator.FilteredLabels, transform=str, selfdepends=True),
                 SerialPickledValueSlot(mainOperator.ExportSettings),
                 SerialPickledValueSlot(mainOperator.HypothesesGraph)
                 ]

        super( TrackingSerializer, self ).__init__( projectFileGroupName, slots=slots )
        
