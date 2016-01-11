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
#           http://ilastik.org/license.html
###############################################################################
from ilastik.workflow import Workflow

from ilastik.applets.dataSelection import DataSelectionApplet
from ilastik.applets.multicut import MulticutApplet

from lazyflow.graph import Graph

class MulticutWorkflow(Workflow):
    workflowName = "Multicut"
    workflowDescription = "A bare-bones workflow for testing the multicut applet"
    defaultAppletIndex = 1 # show DataSelection by default

    DATA_ROLE_RAW = 0
    DATA_ROLE_PROBABILITIES = 1
    DATA_ROLE_SUPERPIXELS = 2
    ROLE_NAMES = ['Raw Data', 'Probabilities', 'Superpixels']
    EXPORT_NAMES = ['Multicut Segmentation']

    @property
    def applets(self):
        return self._applets

    @property
    def imageNameListSlot(self):
        return self.dataSelectionApplet.topLevelOperator.ImageName

    def __init__(self, shell, headless, workflow_cmdline_args, project_creation_workflow, *args, **kwargs):
        # Create a graph to be shared by all operators
        graph = Graph()

        super(MulticutWorkflow, self).__init__( shell, headless, workflow_cmdline_args, project_creation_workflow, graph=graph, *args, **kwargs)
        self._applets = []

        # Create applets 
        self.dataSelectionApplet = DataSelectionApplet(self, "Input Data", "Input Data", supportIlastik05Import=True, batchDataGui=False)
        self.multicutApplet = MulticutApplet(self, "Multicut Segmentation", "Multicut Segmentation")

        # Dataset inputs
        opDataSelection = self.dataSelectionApplet.topLevelOperator
        opDataSelection.DatasetRoles.setValue( self.ROLE_NAMES )

        # Expose to shell
        self._applets.append(self.dataSelectionApplet)
        self._applets.append(self.multicutApplet)

    def connectLane(self, laneIndex):
        """
        Override from base class.
        """
        opData = self.dataSelectionApplet.topLevelOperator.getLane(laneIndex)
        opMulticut = self.multicutApplet.topLevelOperator.getLane(laneIndex)

        # Connect top-level operators
        opMulticut.RawData.connect( opData.ImageGroup[self.DATA_ROLE_RAW] )
        opMulticut.Probabilities.connect( opData.ImageGroup[self.DATA_ROLE_PROBABILITIES] )
        opMulticut.Superpixels.connect( opData.ImageGroup[self.DATA_ROLE_SUPERPIXELS] )

