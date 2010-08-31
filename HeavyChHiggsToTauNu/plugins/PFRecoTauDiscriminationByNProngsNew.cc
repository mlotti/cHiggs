#include "RecoTauTag/RecoTau/interface/TauDiscriminationProducerBase.h"
//#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "RecoTauTag/TauTagTools/interface/PFTauQualityCutWrapper.h"
#include "FWCore/Utilities/interface/InputTag.h"

/* class PFRecoTauDiscriminationByNProngsNew
 * created : August 30 2010,
 * contributors : Sami Lehti (sami.lehti@cern.ch ; HIP, Helsinki)
 * based on H+ tau ID by Lauri Wendland
 */

#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"
#include "RecoBTag/SecondaryVertex/interface/SecondaryVertex.h"

#include "TLorentzVector.h"

using namespace reco;
using namespace std;

class PFRecoTauDiscriminationByNProngsNew : public PFTauDiscriminationProducerBase  {
    public:
	explicit PFRecoTauDiscriminationByNProngsNew(const ParameterSet& iConfig):PFTauDiscriminationProducerBase(iConfig){
//                                                                               qualityCuts_(iConfig.getParameter<ParameterSet>("qualityCuts")){  // retrieve quality cuts    
		nprongs			= iConfig.getParameter<uint32_t>("nProngs");
	}

      	~PFRecoTauDiscriminationByNProngsNew(){}

	void beginEvent(const edm::Event&, const edm::EventSetup&);
	double discriminate(const reco::PFTauRef&);

    private:

//	PFTauQualityCutWrapper qualityCuts_;

	uint32_t nprongs;
};

void PFRecoTauDiscriminationByNProngsNew::beginEvent(const Event& iEvent, const EventSetup& iSetup){}

double PFRecoTauDiscriminationByNProngsNew::discriminate(const PFTauRef& tau){

	bool accepted = false;
	int np = tau->signalTracks().size();

	if((np == 1 && (nprongs == 1 || nprongs == 0)) ||
           (np == 3 && (nprongs == 3 || nprongs == 0)) ) accepted = true;

	if(!accepted) np = 0;
	return np;
}

DEFINE_FWK_MODULE(PFRecoTauDiscriminationByNProngsNew);

