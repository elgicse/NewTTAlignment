def doIt():
    from Configurables import RawBankToFilteredSTClusterAlg, RawBankToFilteredSTLiteClusterAlg
    GaudiSequencer("RecoDecodingSeq").Members[1] = RawBankToFilteredSTClusterAlg("createTTClustersFiltered")
    GaudiSequencer("RecoDecodingSeq").Members[2] = RawBankToFilteredSTLiteClusterAlg("createTTLiteClustersFiltered")
    GaudiSequencer("RecoDecodingSeq").Members[1].OutputLevel = DEBUG
    GaudiSequencer("RecoDecodingSeq").Members[2].OutputLevel = DEBUG

from Gaudi.Configuration import *
from Configurables import Brunel

Brunel().DataType   = "2012"
Brunel().InputType = "MDF"
Brunel().EvtMax = 300
Brunel().PrintFreq = 1
Brunel().WithMC = False
Brunel().Simulation= False
Brunel().OutputLevel = FATAL#ERROR#INFO#DEBUG
MessageSvc().OutputLevel = 8

Brunel().DDDBtag = 'dddb-20120831'
Brunel().CondDBtag = 'cond-20120831'

##############################################################################

EventSelector().Input = [
  "DATAFILE='mdf:root://castorlhcb.cern.ch//castor/cern.ch/user/e/evh/131883/131883_0x0046_NB_L0Phys_00.raw' SVC='LHCb::MDFSelector'"
  ]

appendPostConfigAction( doIt )
