import FWCore.ParameterSet.Config as cms
import HiggsAnalysis.MiniAOD2TTree.tools.git as git #HiggsAnalysis.HeavyChHiggsToTauNu.tools.git as git
from HiggsAnalysis.MiniAOD2TTree.tools.HChOptions import getOptionsDataVersion

process = cms.Process("TTreeDump")

#dataVersion = "76Xmc"
dataVersion = "76Xdata"

options, dataVersion = getOptionsDataVersion(dataVersion)
print dataVersion

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

process.load("FWCore/MessageService/MessageLogger_cfi")
process.MessageLogger.categories.append("TriggerBitCounter")
process.MessageLogger.cerr.FwkReport.reportEvery = 10000 # print the event number for every 100th event
process.MessageLogger.cerr.TriggerBitCounter = cms.untracked.PSet(limit = cms.untracked.int32(10)) # print max 100 warnings

# Set the process options -- Display summary at the end, enable unscheduled execution
process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
       '/store/data/Run2015D/SingleMuon/MINIAOD/PromptReco-v4/000/258/174/00000/5E0232D4-F96C-E511-A1CD-02163E013388.root',
#	'/store/mc/RunIIFall15MiniAODv2/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/10000/044F8A3A-43B8-E511-8F98-0025904CF75A.root',
    ),
    secondaryFileNames = cms.untracked.vstring(
       '/store/data/Run2015D/SingleMuon/AOD/PromptReco-v4/000/258/174/00000/067F479F-F96C-E511-8BED-02163E01464A.root',
       '/store/data/Run2015D/SingleMuon/AOD/PromptReco-v4/000/258/174/00000/0AAF1966-D76C-E511-AEBA-02163E0145C8.root',
    )
)

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, str(dataVersion.getGlobalTag()), '')
print "GlobalTag="+dataVersion.getGlobalTag()

# Set up electron ID (VID framework)
# https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
switchOnVIDElectronIdProducer(process, DataFormat.MiniAOD)
# define which IDs we want to produce and add them to the VID producer
for idmod in ['RecoEgamma.ElectronIdentification.Identification.mvaElectronID_PHYS14_PU20bx25_nonTrig_V1_cff']:
    setupAllVIDIdsInModule(process, idmod, setupVIDElectronSelection)

# Set up HBHE noise filter
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2
print "Setting up HBHE noise filter"   
process.load('CommonTools.RecoAlgos.HBHENoiseFilterResultProducer_cfi')
process.HBHENoiseFilterResultProducer.minZeros = cms.int32(99999)
process.HBHENoiseFilterResultProducer.IgnoreTS4TS5ifJetInLowBVRegion=cms.bool(False)
process.HBHENoiseFilterResultProducer.defaultDecision = cms.string("HBHENoiseFilterResultRun2Loose")
# Do not apply EDfilters for HBHE noise, the discriminators for them are saved into the ttree

process.load("HiggsAnalysis/MiniAOD2TTree/PUInfo_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/TopPt_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/Tau_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/Electron_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/Muon_cfi")
process.load("HiggsAnalysis/MiniAOD2TTree/Jet_cfi")    
process.load("HiggsAnalysis/MiniAOD2TTree/MET_cfi")    

process.dump = cms.EDFilter('MiniAOD2TTreeFilter',
    OutputFileName = cms.string("miniaod2tree.root"),
    PUInfoInputFileName = process.PUInfo.OutputFileName,
    TopPtInputFileName = process.TopPtProducer.OutputFileName,
    CodeVersion = cms.string(git.getCommitId()),
    DataVersion = cms.string(str(dataVersion.version)),
    CMEnergy = cms.int32(13),
    Skim = cms.PSet(
	Counters = cms.VInputTag(
	    "skimCounterAll",
            "skimCounterPassed"
        ),
    ),
    EventInfo = cms.PSet(
	PileupSummaryInfoSrc = process.PUInfo.PileupSummaryInfoSrc,
	LumiScalersSrc = cms.InputTag("scalersRawToDigi"),
	OfflinePrimaryVertexSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
        TopPtProducer = cms.InputTag("TopPtProducer"),
    ),
    Trigger = cms.PSet(
	TriggerResults = cms.InputTag("TriggerResults::HLT"),
#        TriggerResults = cms.InputTag("TriggerResults::HLT25NSV4L1V5"),
#        TriggerResults = cms.InputTag("TriggerResults::TauHLT"),

	TriggerBits = cms.vstring(
	    "HLT_IsoMu16_eta2p1_CaloMET30_LooseIsoPFTau50_Trk30_eta2p1_v",
	    "HLT_IsoMu16_eta2p1_CaloMET30_v",
            "HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_LooseIsoPFTau50_Trk30_eta2p1_v",
            "HLT_IsoMu16_eta2p1_MET30_JetIdCleaned_v",
            "HLT_IsoMu16_eta2p1_MET30_LooseIsoPFTau50_Trk30_eta2p1_v",
            "HLT_IsoMu16_eta2p1_MET30_v",
            "HLT_IsoMu17_eta2p1_v",
            "HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v",
            "HLT_IsoMu17_eta2p1_LooseIsoPFTau20_SingleL1_v",
            "HLT_IsoMu17_eta2p1_MediumIsoPFTau40_Trk1_eta2p1_Reg_v",
            "HLT_IsoMu20_eta2p1_v",
            "HLT_IsoMu24_eta2p1_v",
            "HLT_IsoMu24_eta2p1_LooseIsoPFTau20_v"
        ),
	L1Extra = cms.InputTag("l1extraParticles:MET"),
#        L1Extra = cms.InputTag("l1extraParticles:MET:HLT25NSV4L1V5"),
#	L1Extra = cms.InputTag("l1extraParticles:MET:TauHLT"),
	TriggerObjects = cms.InputTag("selectedPatTrigger"),
	TriggerMatch = cms.untracked.vstring(
	    "LooseIsoPFTau50_Trk30_eta2p1",
	    "LooseIsoPFTau20",
            "MediumIsoPFTau40_Trk1_eta2p1_Reg",
	    "IsoMu16_eta2p1",
            "IsoMu17_eta2p1",
            "IsoMu20_eta2p1"
	),
	filter = cms.untracked.bool(False)
    ),
    METNoiseFilter = cms.PSet(
        triggerResults = cms.InputTag("TriggerResults::"+str(dataVersion.getMETFilteringProcess())),
        printTriggerResultsList = cms.untracked.bool(False),
        filtersFromTriggerResults = cms.vstring(
            "Flag_HBHENoiseFilter",
            "Flag_HBHENoiseIsoFilter",
            "Flag_CSCTightHaloFilter",
            "Flag_CSCTightHalo2015Filter",
            "Flag_EcalDeadCellTriggerPrimitiveFilter",
            "Flag_goodVertices",
            "Flag_eeBadScFilter",
        ),
        hbheNoiseTokenRun2LooseSource = cms.InputTag('HBHENoiseFilterResultProducer','HBHENoiseFilterResultRun2Loose'),
        hbheNoiseTokenRun2TightSource = cms.InputTag('HBHENoiseFilterResultProducer','HBHENoiseFilterResultRun2Tight'),
        hbheIsoNoiseTokenSource = cms.InputTag('HBHENoiseFilterResultProducer','HBHEIsoNoiseFilterResult'),
    ),
    Taus      = process.Taus,
#    Electrons = process.Electrons,
    Muons     = process.Muons,
    Jets      = process.Jets,
    METs      = process.METs,
    GenWeights = cms.VPSet(
        cms.PSet(
            branchname = cms.untracked.string("GenWeights"),
            src = cms.InputTag("generator"),
            filter = cms.untracked.bool(False)
        )
    ),
)

process.load("HiggsAnalysis.MiniAOD2TTree.TauLegSkim_cfi")
process.skim.GenWeights = process.dump.GenWeights

process.skimCounterAll        = cms.EDProducer("HplusEventCountProducer")
process.skimCounterMETFilters = cms.EDProducer("HplusEventCountProducer")
process.skimCounterPassed     = cms.EDProducer("HplusEventCountProducer")

# === Setup customizations
from HiggsAnalysis.MiniAOD2TTree.CommonFragments import produceCustomisations
produceCustomisations(process,dataVersion.isData()) # This produces process.CustomisationsSequence which needs to be included to path

# module execution
process.runEDFilter = cms.Path(process.PUInfo*
                               process.skimCounterAll*
                               process.skim*
                               process.skimCounterPassed*
                               process.CustomisationsSequence*
                               process.dump)

#process.output = cms.OutputModule("PoolOutputModule",
#    outputCommands = cms.untracked.vstring(
#        "keep *",
#    ),
#    fileName = cms.untracked.string("CMSSW.root")
#)
#process.out_step = cms.EndPath(process.output)
