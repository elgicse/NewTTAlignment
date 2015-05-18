###############################################################################
# File for running alignment with J/psi reconstructed from HLT sel reports
###############################################################################
# Syntax is:
#   gaudiiter.py Escher-AlignHltJpsi.py <someDataFiles>.py
###############################################################################

from Configurables import Escher

# Just instantiate the configurable...
theApp = Escher()
theApp.DataType   = "2012"
theApp.InputType  = "MDF"
theApp.PrintFreq = 10000
theApp.EvtMax = 200000
theApp.DatasetName = 'AlignHltD0'
#theApp.DatasetName += '-IgnoreVelo'
#theApp.HltFilterCode = "HLT_PASS_RE( 'Hlt2ExpressDStar2D0PiDecision' )"
theApp.HltFilterCode = "HLT_PASS_RE( 'Hlt2ExpressD02KPiDecision' )"
#theApp.HltFilterCode = "HLT_PASS_RE( 'Hlt2CharmHadD02HH_D02KPiDecision' )"

# COND DB
theApp.DDDBtag = 'head-20120316'
theApp.CondDBtag = 'head-20120316'

# add the filestager
theApp.UseFileStager = True

# specify the input to the alignment
from Configurables import TAlignment
from TAlignment.ParticleSelections import defaultHLTD0Selection
TAlignment().ParticleSelections = [ defaultHLTD0Selection() ]
from TAlignment.TrackSelections import NoPIDTracksFromHlt
TAlignment().TrackSelections = [ NoPIDTracksFromHlt() ]

# specify what we actually align for
from TAlignment.AlignmentScenarios import *
#configurePromptAlignment()
#configureEarlyDataAlignment(True) # with False, you release the constraint in OT3

# Early 2012 data alignment
from TAlignment.Alignables import *
from TAlignment.SurveyConstraints import *
from Configurables import TAlignment
def AlignmentScenarioReprocessing2012( fixQOverPBias = False ) :
    TAlignment().WriteCondSubDetList += ['Velo','TT','IT','OT','MUON']
  
    # define the alignment elements
    elements = Alignables()
    elements.Velo("None")
    elements.VeloRight("Tx")
    elements.VeloLeft("Tx")
    elements.IT("None")
    elements.ITBoxes("TxTzRz")
    elements.ITLayers("TxTz")
    elements.OT("None")
    elements.OTCFrames("Tx")
    elements.OTCFrameLayers("Tz")
    elements.TT("None")
    elements.TTLayers("None")
    elements.TTModules("TxTzRz")
    elements.Tracker("None")
    TAlignment().ElementsToAlign = list(elements)

    # make sure that the velo stays where it was
    TAlignment().Constraints = constraints = []
    constraints.append("VeloHalfAverage : Velo/Velo(Left|Right) : Tx ")
    # fix the q/p scale by not moving T in X. note that you do not
    # want to do this if you use D0 in the alignment
    if fixQOverPBias:
        constraints.append("OT3X : OT/T3X1U.Side : Tx")
 
    # tweak the survey a little bit to fix the z-scale to survey
    surveyconstraints = SurveyConstraints()
    surveyconstraints.All()
    # make sure we fix the z-scale
    surveyconstraints.XmlUncertainties += ["OT/T3X1U : 0.5 0.5 0.00001 0.0001 0.0001 0.0001" ]

def AlignmentScenarioReprocessing2012Bis( fixQOverPBias = False ) :
    TAlignment().WriteCondSubDetList += ['Velo','TT','IT','OT','MUON']
  
    # define the alignment elements
    elements = Alignables()
    elements.Velo("Tz")
    elements.VeloRight("None")
    elements.VeloLeft("None")
    elements.IT("None")
    elements.ITBoxes("TxTzRz")
    elements.ITLayers("None")
    elements.OT("None")
    elements.OTCFrames("TxRz")
    elements.OTCFrameLayers("Tz")
    elements.TT("None")
    elements.TTLayers("None")
    elements.TTModules("TxTzRz")
    elements.Tracker("None")
    TAlignment().ElementsToAlign = list(elements)

    # make sure that the velo stays where it was
    TAlignment().Constraints = constraints = []
    constraints.append("VeloHalfAverage : Velo/Velo(Left|Right) : Tx ")
    # fix the q/p scale by not moving T in X. note that you do not
    # want to do this if you use D0 in the alignment
    if fixQOverPBias:
        constraints.append("OT3X : OT/T3X1U.Side : Tx")
 
    # tweak the survey a little bit to fix the z-scale to survey
    surveyconstraints = SurveyConstraints()
    surveyconstraints.All()
    # make sure we fix the z-scale
    surveyconstraints.XmlUncertainties += ["OT/T3X1U : 0.5 0.5 0.00001 0.0001 0.0001 0.0001" ]

def AlignmentScenarioReprocessing2012Ter( fixQOverPBias = False ) :
    TAlignment().WriteCondSubDetList += ['Velo','TT','IT','OT','MUON']
  
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

    # make sure that the velo stays where it was
    TAlignment().Constraints = constraints = []
    constraints.append("VeloHalfAverage : Velo/Velo(Left|Right) : Tx ")
    # fix the q/p scale by not moving T in X. note that you do not
    # want to do this if you use D0 in the alignment
    if fixQOverPBias:
        constraints.append("OT3X : OT/T3X1U.Side : Tx")
 
    # tweak the survey a little bit to fix the z-scale to survey
    surveyconstraints = SurveyConstraints()
    surveyconstraints.All()
    # make sure we fix the z-scale
    surveyconstraints.XmlUncertainties += ["OT/T3X1U : 0.5 0.5 0.00001 0.0001 0.0001 0.0001" ]


AlignmentScenarioReprocessing2012Ter()
#AlignmentScenarioReprocessing2012Bis()
    #configurePromptAlignment(False)

# Print TES
from Configurables import StoreExplorerAlg
storeExp = StoreExplorerAlg()
#ApplicationMgr().TopAlg += [storeExp]
storeExp.Load = 1
storeExp.PrintFreq = 1.0
storeExp.OutputLevel = 1

##################################################################
# Helper function to create a sequence to fit the tracks and run the hitadder
##################################################################
def configuredFitAndHitAdderSequence( Name, InputLocation, OutputLocation):
    from TrackFitter.ConfiguredFitters import ConfiguredEventFitter
    from Configurables import (TrackHitAdder, TrackContainerCopy, 
                               TrackSelector, GaudiSequencer,
                               TrackStateInitAlg)
    # create the sequence
    if isinstance(Name,GaudiSequencer) :
        seq = Sequence
        Name = seq.name()
        Name.replace( 'Sequence','')
        Name.replace( 'Seq','')
    else:
        seq = GaudiSequencer(Name + 'Seq')

    # I am lazy: use the DOD to get the decoded clusters
    #importOption( "$STDOPTS/DecodeRawEvent.py" )
    # now setup the fitters
    fitBefore = ConfiguredEventFitter(Name + 'FitBeforeHitAdder',TracksInContainer = InputLocation)
    fitBefore.Fitter.MeasProvider.IgnoreVelo = True
    fitBefore.Fitter.MeasProvider.IgnoreVeloPix = True
    fitAfter = ConfiguredEventFitter(Name + 'FitAfterHitAdder',TracksInContainer = InputLocation)
    fitAfter.Fitter.MeasProvider.IgnoreVelo = True
    fitAfter.Fitter.MeasProvider.IgnoreVeloPix = True
    seq.Members += [ 
        TrackStateInitAlg(Name + 'FitInit', TrackLocation = InputLocation),
        fitBefore,
        TrackHitAdder( Name + 'HitAdder', TrackLocation = InputLocation ),
        fitAfter]
    tracksel =  TrackContainerCopy(Name + 'CopyAndSelect',
                                   inputLocation = InputLocation,
                                   outputLocation = OutputLocation,
                                   Selector = TrackSelector())
    # also apply a selection
    tracksel.Selector.MaxChi2Cut = 5
    tracksel.Selector.MaxChi2PerDoFMatch = 5
    tracksel.Selector.MaxChi2PerDoFVelo = 5
    tracksel.Selector.MaxChi2PerDoFDownstream = 5
    seq.Members.append( tracksel )
    return seq


# Add post configuration actions to fix VertexResidualTool
def MyPostConfigurationActions():
    from Configurables import Al__VertexResidualTool
    VtxResTool = Al__VertexResidualTool()
    VtxResTool.parentName = 'D0'
    VtxResTool.daughterNames = ['K+', 'K-', 'pi+', 'pi-']
    from Configurables import AlignAlgorithm
    AlignAlgorithm().VertexResidualTool = VtxResTool
    RecoAlignTrkSeq = GaudiSequencer('HltD0Seq').Members
    # GaudiSequencer('HltD0Seq').Members = [storeExp]
    # for module in RecoAlignTrkSeq:
    #     GaudiSequencer('HltD0Seq').Members += [ module ]

    # redefine TrackFit to ignore VeLo hits
    GaudiSequencer('HltD0Seq').Members=[]
    fitSeq = configuredFitAndHitAdderSequence('HltD0New', 'Rec/Track/AllBest', 'Rec/Track/Best')
    for m in fitSeq.Members: GaudiSequencer('HltD0Seq').Members.append(m)

from GaudiKernel.Configurable import appendPostConfigAction
#appendPostConfigAction(MyPostConfigurationActions)
