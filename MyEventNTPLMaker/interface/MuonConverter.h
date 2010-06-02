// -*- c++ -*-
#ifndef HiggsAnalysis_MyEventNTPLMaker_MuonConverter_h
#define HiggsAnalysis_MyEventNTPLMaker_MuonConverter_h

#include<map>
#include<string>

#include "DataFormats/Common/interface/Handle.h"

#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyJet.h"

namespace reco { class Muon; }
namespace pat { class Muon; }
namespace edm { class InputTag; }
class TransientTrackBuilder;

class TrackConverter;
class ImpactParameterConverter;

class MuonConverter {
public:
  MuonConverter(const TrackConverter&, const ImpactParameterConverter&, const TransientTrackBuilder&);
  ~MuonConverter();

  template <class T> MyJet convert(const edm::InputTag& src, edm::Handle<T>& handle, size_t i) const {
    return convert((*handle)[i]);
  }

  MyJet convert(const reco::Muon&) const;
  MyJet convert(const pat::Muon&) const;

private:
  template <class T> MyJet helper(const T&) const;

  typedef std::map<std::string, double> TagType;

  void tag(const reco::Muon&, TagType&) const;
  void tag(const pat::Muon&, TagType&) const;
  template <class T> void tagHelper(const T&, TagType&) const;

  const TrackConverter& trackConverter;
  const ImpactParameterConverter& ipConverter;
  const TransientTrackBuilder& transientTrackBuilder;
};

#endif