################################################################################
# Package: STDAQ
################################################################################
gaudi_subdir(STDAQ v4r6)

gaudi_depends_on_subdirs(DAQ/DAQUtils
                         Det/DetDesc
                         Det/STDet
                         Event/DAQEvent
                         Event/DigiEvent
                         Event/RecEvent
                         GaudiAlg
                         GaudiKernel
                         Kernel/LHCbKernel
                         ST/STKernel
                         ST/STTELL1Event
                         Si/SiDAQ)

find_package(GSL)

gaudi_add_module(STDAQ
                 src/*.cpp
                 INCLUDE_DIRS GSL DAQ/DAQUtils Event/DigiEvent Si/SiDAQ
                 LINK_LIBRARIES GSL DetDescLib STDetLib DAQEventLib RecEvent GaudiAlgLib GaudiKernel LHCbKernel STKernelLib STTELL1Event)

