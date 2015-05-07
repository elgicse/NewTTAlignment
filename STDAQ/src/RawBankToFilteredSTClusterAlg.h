#ifndef RAWBANKTOFILTEREDSTCLUSTERALG_H 
#define RAWBANKTOFILTEREDSTCLUSTERALG_H 1

#include "STDecodingBaseAlg.h"
#include "Event/RawBank.h"
#include "Kernel/STDAQDefinitions.h"

#include "Event/STCluster.h"

#include <vector>
#include <string>

/** @class RawBankToFilteredSTClusterAlg RawBankToFilteredSTClusterAlg.h
 *  
 *  Algorithm to create STClusters from RawEvent object skipping central TT modules
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
 class TTNames;
}

class RawBankToFilteredSTClusterAlg : public STDecodingBaseAlg {

public:

  /// Standard constructor
  RawBankToFilteredSTClusterAlg( const std::string& name, ISvcLocator* pSvcLocator );

  virtual ~RawBankToFilteredSTClusterAlg( ); ///< Destructor

  virtual StatusCode initialize();    ///< Algorithm initialization
  virtual StatusCode execute();    ///< Algorithm execution
  virtual StatusCode finalize(); ///< finalize


private:

  LHCb::TTNames* tt_names;// = LHCb::TTNames();

  StatusCode decodeBanks(LHCb::RawEvent* rawEvt, LHCb::STClusters* digitCont ) const;


  void createCluster(const STClusterWord& aWord,
                     const STTell1Board* aBoard,
                     const std::vector<SiADCWord>& adcValues,
                     const STDAQ::version& bankVersion,
                     LHCb::STClusters* clusCont) const;
 
  double mean(const std::vector<SiADCWord>& adcValues) const;
   
  LHCb::STLiteCluster word2LiteCluster(const STClusterWord aWord, 
				       const LHCb::STChannelID chan,
				       const unsigned int fracStrip) const;

    
  double stripFraction(const double interStripPos) const;

  /// Output location for STClusters
  std::string m_clusterLocation;

  unsigned int m_nBits; 

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


};

#include "Event/STLiteCluster.h"
#include "Kernel/STChannelID.h"

inline LHCb::STLiteCluster RawBankToFilteredSTClusterAlg::word2LiteCluster(const STClusterWord aWord,
                                                             const LHCb::STChannelID chan,
                                                             const unsigned int fracStrip) const
{
  return LHCb::STLiteCluster(fracStrip,aWord.pseudoSizeBits(),aWord.hasHighThreshold(), chan, (detType()=="UT"));
}

#endif // RAWBANKTOFILTEREDSTCLUSTERALG_H 
