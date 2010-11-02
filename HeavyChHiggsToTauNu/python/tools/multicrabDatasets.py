pattuple_dbs = "http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_01/servlet/DBSServlet"

datasets = {
    ############################################################
    # Collision data
    #
    # BTau PD (for signal analysis)
    "BTau_141950-144114": {
        "dataVersion": "38XdataRun2010A",
        "trigger": "HLT_SingleIsoTau20_Trk5",
        "data": {
            "RECO": {
                "datasetpath": "/BTau/Run2010A-Sep17ReReco_v2/RECO",
                "luminosity": 0,
                "lumis_per_job": 200,
                "lumiMaskRequired": True
            },
            "AOD": {
                "fallback": "RECO",
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010A_Sep17ReReco_v2_RECO-pattuple_v3_3-1a3cae4f0de91fe807e595c3536a6777/USER",
                "luminosity": 1.951264571,
                "number_of_jobs": 5
            }
        }

    },
    "BTau_146240-147454": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET20",
        "runs": (146240, 147454),
        "data": {
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/BTau/local-Run2010B_PromptReco_V2_RECO-pattuple_v3_3-ca0cc7472f6f10c326285176dfa5387f/USER",
                "luminosity": 7.390799812,
                "number_of_jobs": 5
            }
        },
    },
    "BTau_146240-148107": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET20",
        "runs": (146240, 148107),
        "data": {
            "RECO": {
                "datasetpath": "/BTau/Run2010B-PromptReco-v2/RECO",
                "luminosity": 0,
                "lumis_per_job": 200,
                "lumiMaskRequired": True
            },
            "AOD": {
                "fallback": "RECO",
            }
        },
    },
    "BTau_148108-148864": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_SingleIsoTau20_Trk15_MET25",
        "runs": (148108, 148864),
        "data": {
            "RECO": {
                "datasetpath": "/BTau/Run2010B-PromptReco-v2/RECO",
                "luminosity": 0,
                "lumis_per_job": 100,
                "lumiMaskRequired": True
            },
            "AOD": {
                "fallback": "RECO",
            }
        },
    },
    # Mu PD (for electroweak background analysis)
    "Mu_135821-144114": {
        "dataVersion": "38XdataRun2010A",
        "trigger": "HLT_Mu9",
        "data": {
            "RECO": {
                "datasetpath": "/Mu/Run2010A-Sep17ReReco_v2/RECO",
                "luminosity": 0,
                "lumis_per_job": 500,
                "lumiMaskRequired": True
            },
            "AOD": {
                "fallback": "RECO",
            }
        }
    },
    "Mu_146240-147116": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_Mu9",
        "runs": (146240, 147116),
        "data": {
            "AOD": {
                "datasetpath": "/Mu/Run2010B-PromptReco-v2/AOD",
                "luminosity": 0,
                "lumis_per_job": 600,
                "lumiMaskRequired": True
            }
        }
    },
    "Mu_147196-148058": {
        "dataVersion": "38XdataRun2010B",
        "trigger": "HLT_Mu15_v1",
        "runs": (147116, 148058),
        "data": {
            "AOD": {
                "datasetpath": "/Mu/Run2010B-PromptReco-v2/AOD",
                "luminosity": 0,
                "lumis_per_job": 500,
                "lumiMaskRequired": True
            }
        }
    },
    ############################################################
    # Monte Carlo
    #
    # Signal MC
    "TTbar_Htaunu_M80": {
        "dataVersion": "35Xredigi",
        "crossSection": 16.1356,
        "data": {
            "RECO": {
                "datasetpath": "/TTbar_Htaunu_M80/Spring10-START3X_V26_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 4,
            },
            "AOD": {
                "fallback": "RECO",
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTbar_Htaunu_M80/local-Spring10_START3X_V26_S09_v1_GEN-SIM-RECO-pattuple_v3-302407b8f1cbc62b8079a153c5ccc8bf/USER",
                "number_of_jobs": 1
            }
        }
    },
    "TTToHpmToTauNu_M90": {
        "dataVersion": "35X",
        "crossSection": 14.6835,
        "data": {
            "RECO": {
                "datasetpath": "/TTToHpmToTauNu_M-90_7TeV-pythia6-tauola/Spring10-START3X_V26-v1/GEN-SIM-RECO",
                "number_of_jobs": 40
            },
            "AOD": {
                "fallback": "RECO",
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTToHpmToTauNu_M-90_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3-1c883eb3798701ca362caa0e5457977b/USER",
                "number_of_jobs": 4
            }
        }
    },
    "TTToHpmToTauNu_M100": {
        "dataVersion": "35X",
        "crossSection": 12.5288,
        "data": {
            "RECO": {
                "datasetpath": "/TTToHpmToTauNu_M-100_7TeV-pythia6-tauola/Spring10-START3X_V26-v1/GEN-SIM-RECO",
                "number_of_jobs": 4,
            },
            "AOD": {
                "fallback": "RECO",
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTToHpmToTauNu_M-100_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3-1c883eb3798701ca362caa0e5457977b/USER",
                "number_of_jobs": 1
            }
        }
    },
    "TTToHpmToTauNu_M120": {
        "dataVersion": "35X",
        "crossSection": 7.9790,
        "data": {
            "RECO": {
                "datasetpath": "/TTToHpmToTauNu_M-120_7TeV-pythia6-tauola/Spring10-START3X_V26-v1/GEN-SIM-RECO",
                "number_of_jobs": 4,
            },
            "AOD": {
                "fallback": "RECO",
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTToHpmToTauNu_M-120_7TeV-pythia6-tauola/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3-1c883eb3798701ca362caa0e5457977b/USER",
                "number_of_jobs": 1
            }
        }
    },
    "TTbar_Htaunu_M140": {
        "dataVersion": "35Xredigi",
        "crossSection": 3.7389,
        "data": {
            "RECO": {
                "datasetpath": "/TTbar_Htaunu_M140/Spring10-START3X_V26_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 4,
            },
            "AOD": {
                "fallback": "RECO",
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTbar_Htaunu_M140/local-Spring10_START3X_V26_S09_v1_GEN-SIM-RECO-pattuple_v3-302407b8f1cbc62b8079a153c5ccc8bf/USER",
                "number_of_jobs": 1
            }
        }
    },
    "TTbar_Htaunu_M160": {
        "dataVersion": "35Xredigi",
        "crossSection": 0.71923,
        "data": {
            "RECO": {
                "datasetpath": "/TTbar_Htaunu_M160/Spring10-START3X_V26_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 4,
            },
            "AOD": {
                "fallback": "RECO",
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTbar_Htaunu_M160/local-Spring10_START3X_V26_S09_v1_GEN-SIM-RECO-pattuple_v3-302407b8f1cbc62b8079a153c5ccc8bf/USER",
                "number_of_jobs": 1
            }
        }
    },
    # Background MC

    # QCD Summer10
    "QCD_Pt30to50": {
        "dataVersion": "36X",
        "crossSection": 5.018e+07,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt-30to50_7TeV-pythia8/Summer10-START36_V10_S09-v2/GEN-SIM-RECO",
                "number_of_jobs": 60
            },
            "AOD": {
                "datasetpath": "/QCD_Pt-30to50_7TeV-pythia8/Summer10-START36_V10_S09-v2/AODSIM",
                "number_of_jobs": 60,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-30to50_7TeV-pythia8/local-Summer10_START36_V10_S09_v2_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 3
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-30to50_7TeV-pythia8/local-Summer10_START36_V10_S09_v2_GEN-SIM-RECO-pattuple_v6-5e21a9973c3d4d9694aee43cc878ac05/USER",
                "number_of_jobs": 3
            }
        },
    },
    "QCD_Pt50to80": {
        "dataVersion": "36X",
        "crossSection": 6.035e+06,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt-50to80_7TeV-pythia8/Summer10-START36_V10_S09-v2/GEN-SIM-RECO",
                "number_of_jobs": 60
            },
            "AOD": {
                "datasetpath": "/QCD_Pt-50to80_7TeV-pythia8/Summer10-START36_V10_S09-v2/AODSIM",
                "number_of_jobs": 50,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-50to80_7TeV-pythia8/local-Summer10_START36_V10_S09_v1_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 2
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-50to80_7TeV-pythia8/local-Summer10_START36_V10_S09_v1_GEN-SIM-RECO-pattuple_v6-5e21a9973c3d4d9694aee43cc878ac05/USER",
                "number_of_jobs": 2
            }
        },
    },
    "QCD_Pt80to120": {
        "dataVersion": "36X",
        "crossSection": 7.519e+05,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt-80to120_7TeV-pythia8/Summer10-START36_V10_S09-v2/GEN-SIM-RECO",
                "number_of_jobs": 60
            },
            "AOD": {
                "datasetpath": "/QCD_Pt-80to120_7TeV-pythia8/Summer10-START36_V10_S09-v2/AODSIM",
                "number_of_jobs": 60,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-80to120_7TeV-pythia8/local-Summer10_START36_V10_S09_v1_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 3
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-80to120_7TeV-pythia8/local-Summer10_START36_V10_S09_v1_GEN-SIM-RECO-pattuple_v6-5e21a9973c3d4d9694aee43cc878ac05/USER",
                "number_of_jobs": 3
            }
        },
    },
    "QCD_Pt120to170": {
        "dataVersion": "36X",
        "crossSection": 1.120e+05,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt-120to170_7TeV-pythia8/Summer10-START36_V10_S09-v2/GEN-SIM-RECO",
                "number_of_jobs": 60
            },
            "AOD": {
                "datasetpath": "/QCD_Pt-120to170_7TeV-pythia8/Summer10-START36_V10_S09-v2/AODSIM",
                "number_of_jobs": 60,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-120to170_7TeV-pythia8/local-Summer10_START36_V10_S09_v1_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 2
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-120to170_7TeV-pythia8/local-Summer10_START36_V10_S09_v1_GEN-SIM-RECO-pattuple_v6-5e21a9973c3d4d9694aee43cc878ac05/USER",
                "number_of_jobs": 2
            }
        },
    },
    "QCD_Pt170to230": {
        "dataVersion": "36X",
        "crossSection": 1.994e+04,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt-170to230_7TeV-pythia8/Summer10-START36_V10_S09-v2/GEN-SIM-RECO",
                "number_of_jobs": 60
            },
            "AOD": {
                "datasetpath": "/QCD_Pt-170to230_7TeV-pythia8/Summer10-START36_V10_S09-v2/AODSIM",
                "number_of_jobs": 60,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-170to230_7TeV-pythia8/local-Summer10_START36_V10_S09_v2_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 2
            }
        },
    },
    "QCD_Pt230to300": {
        "dataVersion": "36X",
        "crossSection": 4.123e+03,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt-230to300_7TeV-pythia8/Summer10-START36_V10_S09-v2/GEN-SIM-RECO",
                "number_of_jobs": 60
            },
            "AOD": {
                "datasetpath": "/QCD_Pt-230to300_7TeV-pythia8/Summer10-START36_V10_S09-v2/AODSIM",
                "number_of_jobs": 60,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-230to300_7TeV-pythia8/local-Summer10_START36_V10_S09_v2_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 2
            },
            "pattuple_v6": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt-230to300_7TeV-pythia8/local-Summer10_START36_V10_S09_v2_GEN-SIM-RECO-pattuple_v6-5e21a9973c3d4d9694aee43cc878ac05/USER",
                "number_of_jobs": 2
            }
        },
    },

    # QCD Fall10
    "QCD_Pt30to50_Fall10": {
        "dataVersion": "38X",
        "crossSection": 5.312e+07,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt_30to50_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 150
            },
            "AOD": {
                "datasetpath": "/QCD_Pt_30to50_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/AODSIM",
                "number_of_jobs": 100,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt_30to50_TuneZ2_7TeV_pythia6/local-Fall10_START38_V12_v1_AODSIM-pattuple_v3-77a027b4f9e83a8f0edf7612e8721105/USER",
                "number_of_jobs": 10
            }
        },
    },
    "QCD_Pt50to80_Fall10": {
        "dataVersion": "38X",
        "crossSection": 6.359e+06,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt_50to80_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 150
            },
            "AOD": {
                "datasetpath": "/QCD_Pt_50to80_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/AODSIM",
                "number_of_jobs": 100,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt_50to80_TuneZ2_7TeV_pythia6/local-Fall10_START38_V12_v1_AODSIM-pattuple_v3-77a027b4f9e83a8f0edf7612e8721105/USER",
                "number_of_jobs": 10
            }
        },
    },
    "QCD_Pt80to120_Fall10": {
        "dataVersion": "38X",
        "crossSection": 7.843e+05,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt_80to120_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 150
            },
            "AOD": {
                "datasetpath": "/QCD_Pt_80to120_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/AODSIM",
                "number_of_jobs": 150,
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt_80to120_TuneZ2_7TeV_pythia6/local-Fall10_START38_V12_v1_AODSIM-pattuple_v3-77a027b4f9e83a8f0edf7612e8721105/USER",
                "number_of_jobs": 10
            }
        },
    },
    "QCD_Pt120to170_Fall10": {
        "dataVersion": "38X",
        "crossSection": 1.151e+05,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt_120to170_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 150
            },
            "AOD": {
                "datasetpath": "/QCD_Pt_120to170_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/AODSIM",
                "number_of_jobs": 100,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt_120to170_TuneZ2_7TeV_pythia6/local-Fall10_START38_V12_v1_AODSIM-pattuple_v3-77a027b4f9e83a8f0edf7612e8721105/USER",
                "number_of_jobs": 10
            }
        },
    },
    "QCD_Pt170to300_Fall10": {
        "dataVersion": "38X",
        "crossSection": 2.426e+04,
        "data": {
            "RECO": {
                "datasetpath": "/QCD_Pt_170to300_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/GEN-SIM-RECO",
                "number_of_jobs": 150
            },
            "AOD": {
                "datasetpath": "/QCD_Pt_170to300_TuneZ2_7TeV_pythia6/Fall10-START38_V12-v1/AODSIM",
                "number_of_jobs": 100,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/QCD_Pt_170to300_TuneZ2_7TeV_pythia6/local-Fall10_START38_V12_v1_AODSIM-pattuple_v3-77a027b4f9e83a8f0edf7612e8721105/USER",
                "number_of_jobs": 10
            }
        },
    },

    # Electroweak
    "TTbar": {
        "dataVersion": "36X",
        "crossSection": 165,
        "data": {
            "RECO": {
                "datasetpath": "/TTbar/Summer10-START36_V9_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 50
            },
            "AOD": {
                "datasetpath": "/TTbar/Summer10-START36_V9_S09-v1/AODSIM",
                "number_of_jobs": 50,
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTbar/local-Summer10_START36_V9_S09_v1_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 3
            }
        },
    },
    "TTbarJets": {
        "dataVersion": "36X",
        "crossSection": 165,
        "data": {
            "RECO": {
                "datasetpath": "/TTbarJets_Tauola-madgraph/Summer10-START36_V9_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 80
            },
            "AOD": {
                "datasetpath": "/TTbarJets_Tauola-madgraph/Summer10-START36_V9_S09-v1/AODSIM",
                "number_of_jobs": 60,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/TTbarJets_Tauola-madgraph/local-Summer10_START36_V9_S09_v1_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 6
            }
        },
    },
    "WJets": {
        "dataVersion": "36X",
        "crossSection": 25090,
        "data": {
            "RECO": {
                "datasetpath": "/WJets_7TeV-madgraph-tauola/Summer10-START36_V9_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 400
            },
            "AOD": {
                "datasetpath": "/WJets_7TeV-madgraph-tauola/Summer10-START36_V9_S09-v1/AODSIM",
                "number_of_jobs": 350,
                "se_white_list": ["T2_FI_HIP"]
            },
            "pattuple_v3": {
                "dbs_url": pattuple_dbs,
                "datasetpath": "/WJets_7TeV-madgraph-tauola/local-Summer10_START36_V9_S09_v1_AODSIM-pattuple_v3-350234694fe4ac3e4a7c59f3d58cf538/USER",
                "number_of_jobs": 40
            }
        },
    },

    # Backgrounds for electroweak background measurement
    "ZJets": {
        "dataVersion": "37X",
        "crossSection": 2400,
        "data": {
            "AOD": {
                "datasetpath": "/ZJets-madgraph/Summer10-START37_V5_S09-v1/AODSIM",
                "number_of_jobs": 15,
            }
        },
    },
    "SingleTop_sChannel": {
        "dataVersion": "37X",
        "crossSection": 0.99,
        "data": {
            "RECO": {
                "datasetpath": "/SingleTop_sChannel-madgraph/Summer10-START37_V5_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 10,
            },
            "AOD": {
                "fallback": "RECO"
            }
        },
    },
    "SingleTop_tChannel": {
        "dataVersion": "37X",
        "crossSection": 20.16,
        "data": {
            "RECO": {
                "datasetpath": "/SingleTop_tChannel-madgraph/Summer10-START37_V5_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 15,
            },
            "AOD": {
                "fallback": "RECO"
            }
        },
    },
    "SingleTop_tWChannel": {
        "dataVersion": "37X",
        "crossSection": 10.56,
        "data": {
            "RECO": {
                "datasetpath": "/SingleTop_tWChannel-madgraph/Summer10-START37_V5_S09-v1/GEN-SIM-RECO",
                "number_of_jobs": 10,
            },
            "AOD": {
                "fallback": "RECO"
            }
        },
    },
}