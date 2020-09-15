import ROOT
from ROOT import TMVA, TFile, TTree, TCut, TChain
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class GenElectronMatchProducer(Module):
    def __init__(self, collection="Electron"):
        self.collection = collection
    def beginJob(self):
        pass
    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Electron_genmatched", "O" , lenVar="nElectron")
        self.out.branch("Electron_promptgenmatched", "O", lenVar="nElectron")
         
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, self.collection)
        genElectrons = Collection(event, "GenPart")
        for electron  in electrons:
          ele4 = ROOT.TLorentzVector()
          ele4.SetPtEtaPhiM(electron.pt, electron.eta, electron.phi, 0)
          electron.isMatched = False
          electron.isPromptMatched = False
          for genElectron in genElectrons:
            if ( abs(genElectron.pdgId) == 11 and \
                 genElectron.status == 1 and \
                 genElectron.p4().DeltaR(ele4) < 0.3) :
              electron.isMatched = True
              if ((genElectron.statusFlags&1 == 1) or (genElectron.statusFlags&6 == 6)):
                electron.isPromptMatched = True
                
        outGenMatched = []
        outPromptGenMatched = []
	for electron in electrons:
	   outGenMatched.append(electron.isMatched)
           outPromptGenMatched.append(electron.isPromptMatched)
        self.out.fillBranch("Electron_genmatched", outGenMatched)
        self.out.fillBranch("Electron_promptgenmatched", outPromptGenMatched)
        return True

