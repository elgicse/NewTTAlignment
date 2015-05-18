###############################################################################
# File for running alignment using the default reconstruction sequence.
###############################################################################
# Syntax is:
#   
#   gaudipariter.py -n 4 -p 8 -e 200000 /afs/cern.ch/user/g/gdujany/LHCb/Alignment/align2011/newAlignment/align2halves/align2halves.py | tee output.txt
#  
#   -n <number of iterations>
#   -p <number of processes>
#   -e <number of events>
#
# SetupProject Alignment 
###############################################################################
from Gaudi.Configuration import *
import GaudiKernel.SystemOfUnits as units
from TrackMonitors.BGIRecoConf import BGIRecoConf
from Configurables import CondDB, CondDBAccessSvc, RecSysConf

RecSysConf().RecoSequence = ["Decoding", "VELO", "Tr", "Vertex", "TT"]

from Configurables import Escher
theApp = Escher()
theApp.DataType   = "2012" # Check that this is true
from Configurables import CondDB
CondDB(LatestGlobalTagByDataType=theApp.DataType)
# theApp.CondDBtag = "sim-20130522-vc-md100"#'sim-20111111-vc-md100'
# theApp.DDDBtag = "dddb-20130929"#'MC11-20111102'
theApp.Simulation = True
#theApp.WithMC = True
theApp.InputType  = "DST" #"MDF"
theApp.PrintFreq = 5000
theApp.EvtMax = 20000 #00 #2000#160000 #20000
#theApp.SkipEvents = 20 
theApp.DatasetName = 'Align'
#theApp.UseFileStager = True



### VERTEX SELECTION ##############
from TAlignment.VertexSelections import configuredPVSelection

### TRACK SELECTION ##############
from TAlignment.TrackSelections import GoodLongTracks, NoPIDTracksFromHlt

### PARTICLE SELECTION ##############
from TAlignment.ParticleSelections import defaultHLTD0Selection

### ALIGNABLES & CONSTRAINTS ##############
from TAlignment.Alignables import Alignables
from TAlignment.SurveyConstraints import *


def myconfigureTTAlignment():
#    TAlignment().WriteCondSubDetList  += ['TT']
#
#    elements = Alignables()
#    elements.TT("None")
#    elements.TTLayers("None")
#    elements.TTHalfLayers("None")
#    elements.TTSplitLayers("None")
#    elements.TTBoxes("None")
#    elements.TTHalfModules("None")
#    elements.TTModules("None")
#    TAlignment().ElementsToAlign += list(elements)
    TAlignment().WriteCondSubDetList += ['TT','IT','OT']
 
    # define the alignment elements
    elements = Alignables()
    elements.Velo("None")
    elements.VeloRight("None")
    elements.VeloLeft("None")
    elements.IT("None")
    elements.ITBoxes("TxTzRz")
    elements.ITLayers("None")
    elements.OT("None")
    elements.OTCFrames("TxRz")
    elements.OTCFrameLayers("Tz")
    elements.OTModules("TxRz")
    elements.TT("None")
    elements.TTLayers("Tz")
    elements.TTModules("TxRz")
    elements.Tracker("None")
    TAlignment().ElementsToAlign = list(elements)

    surveyconstraints = SurveyConstraints()

    #    surveyconstraints.All()

    # For MC I have to use different Constraints because Tz is different!
    # surveyconstraints.XmlFiles[:2] = ['../../Modules.xml', '../../Detectors.xml']

    # MC constraints (all zeros)
    # Muon
    #surveyconstraints.Muon()
    # OT
    surveyconstraints.Constraints  = [ "OT/.*?M. : 0 0 0 0 0 0 : 0.05 0.05 0.05 0.00001 0.001 0.00001",
                                       "OTSystem : 0 0 0 0 0 0 : 1 1 1 0.001 0.001 0.001" ]
    # TT
    surveyconstraints.Constraints += [ "TTSystem             : 0 0 0 0 0 0 : 0.5 0.5 0.5 0.001 0.001 0.001",
                                       "TT.                  : 0 0 0 0 0 0 : 0.1 0.1 0.1 0.0005 0.0005 0.0005",
                                       "TT..Layer            : 0 0 0 0 0 0 : 0.1 0.1 0.1 0.0005 0.0005 0.0005",
                                       "TT..Layer.Side       : 0 0 0 0 0 0 : 0.1 0.1 0.1 0.0005 0.0005 0.0005",
                                       "TT..LayerR.Module.*? : 0 0 0 0 0 0 : 0.1 0.1 0.1 0.0005 0.0005 0.0005",
                                       "TT.*?(Low|High)Z     : 0 0 0 0 0 0 : 0.1 0.1 1.0 0.0005 0.0005 0.0005",
                                       "TTASide : 0 0 0 0 0 0 : 0.2 0.2 0.2 0.001 0.001 0.001",
                                       "TTCSide : 0 0 0 0 0 0 : 0.2 0.2 0.2 0.001 0.001 0.001"  ]
    # IT
    surveyconstraints.Constraints += [ "ITSystem                   : 0 0 0 0 0 0 : 1 1 1 0.01 0.01 0.01",
                                       "ITT.                       : 0 0 0 0 0 0 : 0.5 0.5 0.5 0.001 0.001 0.001",
                                       "ITT.*?Box                  : 0 0 0 0 0 0 : 0.5 0.5 0.5 0.001 0.001 0.001",
                                       "ITT.*?Layer.{1,2}          : 0 0 0 0 0 0 : 0.2 0.05 0.05 0.0001 0.0001 0.001",
                                       "ITT.*?Layer(X1U|VX2)       : 0 0 0 0 0 0 : 0.2 0.05 0.05 0.0001 0.0001 0.001",
                                       "ITT.*?Layer.{1,2}Ladder.*? : 0 0 0 0 0 0 : 0.1 0.02 0.02 0.0001 0.0001 0.001" ]
    # Other
    surveyconstraints.Constraints += [ "Tracker : 0 0 0 0 0 0 : 10 10 10 0.1 0.1 0.1",
                                       "TStations : 0 0 0 0 0 0 : 10 10 10 0.1 0.1 0.1" ]

    
    print surveyconstraints
   

# specify the input to the alignment
from Configurables import TAlignment


TAlignment().TrackSelections = [ NoPIDTracksFromHlt() ]#[ GoodLongTracks() ]
TAlignment().ParticleSelections = [ defaultHLTD0Selection() ]


TAlignment().PVSelection = configuredPVSelection()

myconfigureTTAlignment()

#from Configurables import UpdateManagerSvc
#UpdateManagerSvc().ConditionsOverride += [ "Conditions/Alignment/TT/TTaXLayerR1Module1T := double_v dPosXYZ = 0.0 0. 0.; double_v dRotXYZ = 0. 0. 1.;" ]

#########################################

print 'ALIGNABLE:'
print TAlignment().ElementsToAlign
print 'TAlignment():'
print TAlignment().__slots__


# disable the HltErrorFilter
from Configurables import LoKi__HDRFilter as HDRFilter
hltErrorFilter = HDRFilter('HltErrorFilter').Enable = False


# In digi MC do not have trigger infos so remove ...
GaudiSequencer('HltFilterSeq').Enable = False 


dataName = 'myfirsttestMC'
#ntupleDir='/tmp/gdujany'
#ntupleOutputFile = ntupleDir+'KalmanNtuple_'+dataName+'.root'
histoOutputFile = 'KalmanHisto_'+dataName+'.root'
HistogramPersistencySvc().OutputFile = histoOutputFile
#NTupleSvc().Output=["FILE1 DATAFILE='"+ntupleOutputFile+"' TYP='ROOT' OPT='NEW'"]

from GaudiConf import IOHelper

# Da Giulio (probabilmente D02KPi)
prodNumber = 15517 
fileList = ['/lhcb/MC/MC11a/ALLSTREAMS.DST/{0:0>8}/0000/{0:0>8}_{1:0>8}_1.allstreams.dst'.format(prodNumber, i) for i in range(1,190)]
# Dst_D0pi,Kpimumu
prodNumber = 20931 
fileList += ['/lhcb/MC/MC11a/ALLSTREAMS.DST/{0:0>8}/0000/{0:0>8}_{1:0>8}_1.allstreams.dst'.format(prodNumber, i) for i in range(1,50)]
prodNumber = 21334
fileList += ['/lhcb/MC/MC11a/ALLSTREAMS.DST/{0:0>8}/0000/{0:0>8}_{1:0>8}_1.allstreams.dst'.format(prodNumber, i) for i in range(1,89)]
# Dst_D0pi,Kpipipi
prodNumber = 21470
fileList += ['/lhcb/MC/MC11a/ALLSTREAMS.DST/{0:0>8}/0000/{0:0>8}_{1:0>8}_1.allstreams.dst'.format(prodNumber, i) for i in range(1,89)]

IOHelper().inputFiles(['PFN:root://eoslhcb.cern.ch//eos/lhcb/grid/prod'+file for file in fileList], clear=True)



