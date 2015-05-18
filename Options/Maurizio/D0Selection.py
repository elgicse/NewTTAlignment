##################################################################
# Create a selection based on D0->Kpi
##################################################################
def defaultD0Selection():

    from Configurables import Escher, TAlignment
    Escher().RecoSequence = ["Hlt","Decoding","AlignTr","Vertex","RICH" ]
    Escher().MoniSequence = ["Tr","OT"]

    # Tweak a little bit RICH
    from TAlignment.ParticleSelections import MinimalRichSequence
    MinimalRichSequence()

    # now create the D0->K-Pi+ candidates
    from Configurables import FilterDesktop
    from Configurables import ChargedProtoParticleMaker, ChargedProtoParticleAddRichInfo, ChargedProtoCombineDLLsAlg

    # take as much as possible from CommonParticles
    from CommonParticles.StdAllLooseKaons import StdAllLooseKaons
    from CommonParticles.StdAllLoosePions import StdAllLoosePions
    from CommonParticles.StdLooseKaons import StdLooseKaons
    from CommonParticles.StdLoosePions import StdLoosePions
    from CommonParticles.StdLooseD02HH import StdLooseD02KPi
    # remove cuts that require a PV
    StdLooseD02KPi.MotherCut = "((VFASPF(VCHI2)<10) & (ADMASS('D0')<100*MeV))"
    StdLooseKaons.Code = "ALL"
    StdLoosePions.Code = "ALL"

    # add tight PID cuts basically toensure that we don't swap the
    # kaon and pion.
    AlignD02KPiWide = FilterDesktop("AlignD02KPiWide",
                                    Inputs = ["Phys/StdLooseD02KPi"], 
                                    Code = "(ADMASS('D0') < 50.*MeV) & (VFASPF(VCHI2) < 9.)" \
                                    " & (MINTREE('K+'==ABSID, PIDK) > 0)" \
                                    " & (MINTREE('pi+'==ABSID, PIDK) < 0)" )
    
    # tighten the mass window for candidates used in alignment.
    AlignD02KPi = FilterDesktop("AlignD02KPi",
                                Inputs = ["Phys/AlignD02KPiWide"], 
                                Code = "(ADMASS('D0') < 20.*MeV)" )

    # create the sequence that we pass to the alignment
    from Configurables import TrackParticleMonitor, GaudiSequencer
    recoD0Seq= GaudiSequencer("RecoD0Seq")
    recoD0Seq.Members = [ 
        ChargedProtoParticleMaker('ChargedProtoPMaker'),
        ChargedProtoParticleAddRichInfo('ChargedProtoPAddRich'),
        ChargedProtoCombineDLLsAlg('ChargedProtoPCombDLLs'),
        TrackParticleMonitor('StdLooseD02KPiMonitor', 
                              InputLocation = '/Event/Phys/StdLooseD02KPi/Particles',
                              MinMass = 1810, MaxMass = 1930),
        AlignD02KPiWide,
        TrackParticleMonitor('AlignD02KPiWideMonitor', 
                             InputLocation = '/Event/Phys/AlignD02KPiWide/Particles',
                             MinMass = 1810, MaxMass = 1930),
        AlignD02KPi,
        TrackParticleMonitor('AlignD02KPiMonitor', 
                             InputLocation = '/Event/Phys/AlignD02KPi/Particles',
                             MinMass = 1810, MaxMass = 1930)
                        ]

    from TAlignment.ParticleSelections import ParticleSelection
    sel = ParticleSelection( Name = 'D02KPi',
                             Location = '/Event/Phys/AlignD02KPi/Particles',
                             Algorithm = recoD0Seq )
    return sel

# Tracks Selection
from Configurables import TAlignment
from TAlignment.TrackSelections import FavouriteTrackCocktail
TAlignment().TrackSelections = [FavouriteTrackCocktail()]
TAlignment().ParticleSelections = [defaultD0Selection()]
