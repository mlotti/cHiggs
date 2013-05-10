// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_METSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_METSelection_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  class METSelection: public BaseSelection {
  public:
    /**
     * Class to encapsulate the access to the data members of
     * TauSelection. If you want to add a new accessor, add it here
     * and keep all the data of TauSelection private.
     */
    class Data {
    public:
      // The reason for pointer instead of reference is that const
      // reference allows temporaries, while const pointer does not.
      // Here the object pointed-to must live longer than this object.
      Data();
      ~Data();

      const bool passedEvent() const { return fPassedEvent; }
      const edm::Ptr<reco::MET> getSelectedMET() const { return fSelectedMET; }
      const edm::Ptr<reco::MET> getRawMET() const { return fRawMET; }
      const edm::Ptr<reco::MET> getType1MET() const { return fType1MET; }
      const edm::Ptr<reco::MET> getType2MET() const { return fType2MET; }
      const edm::Ptr<reco::MET> getCaloMET() const { return fCaloMET; }
      const edm::Ptr<reco::MET> getTcMET() const { return fTcMET; }
      const  std::vector<reco::MET> getType1METCorrected() const { return fType1METCorrected; }

      friend class METSelection;

    private:
      bool fPassedEvent;
      // MET objects
      edm::Ptr<reco::MET> fSelectedMET;
      edm::Ptr<reco::MET> fRawMET;
      edm::Ptr<reco::MET> fType1MET;
      edm::Ptr<reco::MET> fType2MET;
      edm::Ptr<reco::MET> fCaloMET;
      edm::Ptr<reco::MET> fTcMET;
      // For type I/II correction
      std::vector<reco::MET> fType1METCorrected;
      //std::vector<reco::MET> fType2METCorrected;

    };

    METSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, const std::string& label, const std::string& tauIsolationDiscriminator);
    ~METSelection();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    // Here tau is always assumed isolated for type 1 correction
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Candidate>& selectedTau, const edm::PtrVector<pat::Jet>& allJets);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Candidate>& selectedTau, const edm::PtrVector<pat::Jet>& allJets);

    // Here non-isolated taus are taken as jets, if
    // fNonIsolatedTausAsJetsEnabled is true (from python
    // configuration)
    Data silentAnalyzeWithPossiblyIsolatedTaus(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Candidate>& selectedTau, const edm::PtrVector<pat::Jet>& allJets);
    Data analyzeWithPossiblyIsolatedTaus(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Candidate>& selectedTau, const edm::PtrVector<pat::Jet>& allJets);

    const double getCutValue() const { return fMetCut; }

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Candidate>& selectedTau, const edm::PtrVector<pat::Jet>& allJets, bool possiblyIsolatedTaus);

    enum Select {kRaw, kType1, kType2};

    enum PossiblyIsolatedTauMode { // Do TypeI (residual) correction for possibly isolated taus?
      kDisabled,       // equivalent to always
      kNever,          // Taus in (silent)analyzeWithPossiblyIsolatedTaus are always considered as jets
      kAlways,         // Taus in (silent)analyzeWithPossiblyIsolatedTaus are always considered as isolated taus
      kForIsolatedOnly // Taus in (silent)analyzeWithPossiblyIsolatedTaus are treated according to their isolation status (non-isolated as jets, isolated as taus)
    };

    reco::MET undoJetCorrectionForSelectedTau(const edm::Ptr<reco::MET>& met, const edm::Ptr<reco::Candidate>& selectedTau, const edm::PtrVector<pat::Jet>& allJets, Select type, bool possibltyIsolatedTaus);

    // Input parameters
    edm::InputTag fRawSrc;
    edm::InputTag fType1Src;
    edm::InputTag fType2Src;
    edm::InputTag fCaloSrc;
    edm::InputTag fTcSrc;
    Select fSelect;

    // For type I/II correction
    const double fMetCut;
    const double fTauJetMatchingCone;
    const double fJetType1Threshold;
    std::string fJetOffsetCorrLabel;
    //double fType2ScaleFactor;
    std::string fTauIsolationDiscriminator;
    PossiblyIsolatedTauMode fDoTypeICorrectionForPossiblyIsolatedTaus;


    // Counters
    Count fTypeIAllEvents;
    Count fTypeITauIsolated;
    Count fTypeITauRefJetFound;
    Count fMetCutCount;

    // Histograms
    WrappedTH1 *hMet;
    WrappedTH1 *hMetPhi;
    WrappedTH1 *hMetSignif;
    WrappedTH1 *hMetSumEt;
    WrappedTH1 *hMetDivSumEt;
    WrappedTH1 *hMetDivSqrSumEt;

  };
}

#endif
