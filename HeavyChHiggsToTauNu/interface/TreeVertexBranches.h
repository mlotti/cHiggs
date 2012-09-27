// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TreeVertexBranches_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TreeVertexBranches_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include<vector>

namespace edm {
  class ParameterSet;
  class Event;
}

class TTree;

namespace HPlus {
  class TreeVertexBranches {
  public:
    TreeVertexBranches(const edm::ParameterSet& iConfig);
    ~TreeVertexBranches();

    void book(TTree *tree);
    void setValues(const edm::Event& iEvent);
    void reset();

    const edm::InputTag& getInputTag() const { return fVertexSrc; }

  private:
    void setValues(const edm::View<reco::Vertex>& muons);

    edm::InputTag fVertexSrc;

    unsigned fVertexCount;
  };
}

#endif
