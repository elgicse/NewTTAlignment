#ifndef RAWBANKTOFILTEREDSTLITECLUSTERALG_H 
#define RAWBANKTOFILTEREDSTLITECLUSTERALG_H 1

#include "STDecodingBaseAlg.h"
#include "Event/RawBank.h"
#include "Kernel/STDAQDefinitions.h"

#include "Event/STLiteCluster.h"

#include <vector>
#include <string>
#include <utility>

/** @class RawBankToFilteredSTLiteClusterAlg RawBankToFilteredSTLiteClusterAlg.h
 *  
 *  Algorithm to create STLiteClusters from RawEvent object skipping central TT modules
 * 
 *  @author E. Graverini
 *  @date   2015-05-06
 */


#include "Kernel/STClusterWord.h"
#include "Kernel/TTNames.h"

class SiADCWord;
class STTell1Board;

namespace LHCb{
 class STChannelID;
 class STLiteCluster;
}

class RawBankToFilteredSTLiteClusterAlg : public STDecodingBaseAlg {

public:

  /// Standard constructor
  RawBankToFilteredSTLiteClusterAlg( const std::string& name, ISvcLocator* pSvcLocator );

  virtual ~RawBankToFilteredSTLiteClusterAlg( ); ///< Destructor

  virtual StatusCode initialize();    ///< Algorithm initialization
  virtual StatusCode execute();    ///< Algorithm execution
  virtual StatusCode finalize(); ///< finalize

private:

  // Used to filter hits in the central TT modules
  unsigned int min_TTaULayerR2Module2T = 2697217;
  unsigned int min_TTaULayerR2Module2B = 2694145;
  unsigned int min_TTaXLayerR2Module2T = 2435073;
  unsigned int min_TTaXLayerR2Module2B = 2432001;
  unsigned int min_TTbVLayerR2Module3T = 4536321;
  unsigned int min_TTbVLayerR2Module3B = 4533249;
  unsigned int min_TTbXLayerR2Module3T = 4798465;
  unsigned int min_TTbXLayerR2Module3B = 4795393;

  unsigned int max_TTaULayerR2Module2T = 2699776;
  unsigned int max_TTaULayerR2Module2B = 2696704;
  unsigned int max_TTaXLayerR2Module2T = 2437632;
  unsigned int max_TTaXLayerR2Module2B = 2434560;
  unsigned int max_TTbVLayerR2Module3T = 4538880;
  unsigned int max_TTbVLayerR2Module3B = 4535808;
  unsigned int max_TTbXLayerR2Module3T = 4801024;
  unsigned int max_TTbXLayerR2Module3B = 4797952;

  LHCb::TTNames* tt_names;

  // create Clusters from this type
  StatusCode decodeBanks(LHCb::RawEvent* rawEvt, LHCb::STLiteCluster::STLiteClusters* fCont) const;

  // add a single cluster to the output container
  void createCluster(const STTell1Board* aBoard,  const STDAQ::version& bankVersion, 
                     const STClusterWord& aWord, LHCb::STLiteCluster::STLiteClusters* fCont) const;


  std::string m_clusterLocation;  
  
  class Less_by_Channel : public std::binary_function<LHCb::STLiteCluster,LHCb::STLiteCluster ,bool>{
  public:

    /** compare the channel of one object with the
     *  channel of another object
     *  @param obj1   first  object
     *  @param obj2   second object
     *  @return  result of the comparision
     */
    //
    inline bool operator() ( LHCb::STLiteCluster obj1 , LHCb::STLiteCluster obj2 ) const
    {
      return obj1.channelID() < obj2.channelID() ;
    }
  };

   
  class Equal_Channel : public std::binary_function<LHCb::STLiteCluster,LHCb::STLiteCluster ,bool>{
  public:

    /** compare the channel of one object with the
     *  channel of another object
     *  @param obj1   first  object
     *  @param obj2   second object
     *  @return  result of the comparision
     */
    //
    inline bool operator() ( LHCb::STLiteCluster obj1 , LHCb::STLiteCluster obj2 ) const
    {
      return obj1.channelID() == obj2.channelID() ;
    }
  };

  
};

#include "Kernel/STTell1Board.h"
#include "Kernel/ISTReadoutTool.h"
//#include <iostream>
//#include <string>

inline void RawBankToFilteredSTLiteClusterAlg::createCluster(const STTell1Board* aBoard,  const STDAQ::version& bankVersion,
                                                     const STClusterWord& aWord, LHCb::STLiteCluster::STLiteClusters* fCont) const{
   
  const unsigned int fracStrip = aWord.fracStripBits();     
  const STTell1Board::chanPair chan = aBoard->DAQToOffline(fracStrip, bankVersion, STDAQ::StripRepresentation(aWord.channelID()));
  LHCb::STLiteCluster liteCluster(chan.second,
                            aWord.pseudoSizeBits(),
                            aWord.hasHighThreshold(),
                            chan.first,
                            detType() == "UT");

  // Mask the central modules of the TT
  LHCb::STChannelID thisChannelID = liteCluster.channelID();
  unsigned int chID = thisChannelID.channelID();

  if (!( (chID >= min_TTaULayerR2Module2T && chID <= max_TTaULayerR2Module2T) ||
         (chID >= min_TTaULayerR2Module2B && chID <= max_TTaULayerR2Module2B) ||
         (chID >= min_TTaXLayerR2Module2T && chID <= max_TTaXLayerR2Module2T) ||
         (chID >= min_TTaXLayerR2Module2B && chID <= max_TTaXLayerR2Module2B) ||  
         (chID >= min_TTbVLayerR2Module3T && chID <= max_TTbVLayerR2Module3T) ||
         (chID >= min_TTbVLayerR2Module3B && chID <= max_TTbVLayerR2Module3B) ||  
         (chID >= min_TTbXLayerR2Module3T && chID <= max_TTbXLayerR2Module3T) ||
         (chID >= min_TTbXLayerR2Module3B && chID <= max_TTbXLayerR2Module3B) )){
    fCont->push_back(liteCluster);
  }
  else {
    if( UNLIKELY( msgLevel(MSG::DEBUG) ) ){
      std::string thisSector = tt_names->UniqueSectorToString((const LHCb::STChannelID &)thisChannelID);
      debug() << "Cluster in TT central module filtered out: " << thisSector << endmsg;          
      //debug() << "Cluster in TT central module filtered out: " << aBoard->boardID()<< " " <<  aWord.channelID() << endmsg;  
    }
    //info() << "Cluster in TT central module filtered out: " << aBoard->boardID()<< " " <<  aWord.channelID() << endmsg;  
    //info() << "Cluster in TT central module filtered out: " << thisSector << endmsg;
    //Warning("Failed to insert cluster --> cluster filtered out", StatusCode::SUCCESS , 100);
    //delete liteCluster; 
  }

}

#endif //  RAWBANKTOFILTEREDSTLITECLUSTERALG_H 
