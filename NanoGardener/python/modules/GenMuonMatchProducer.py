import ROOT
from ROOT import TMVA, TFile, TTree, TCut, TChain
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class GenMuonMatchProducer(Module):
    def __init__(self, collection="Muon"):
        self.collection = collection
    def beginJob(self):
        pass
    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Muon_genmatched", "O" , lenVar="nMuon")
        self.out.branch("Muon_promptgenmatched", "O", lenVar="nMuon")
         
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        muons = Collection(event, self.collection)
        genMuons = Collection(event, "GenPart")
        for muon  in muons:
          mu4 = ROOT.TLorentzVector()
          mu4.SetPtEtaPhiM(muon.pt, muon.eta, muon.phi, 0)
          muon.isMatched = False
          muon.isPromptMatched = False
          for genMuon in genMuons:
            if ( abs(genMuon.pdgId) == 11 and \
                 genMuon.status == 1 and \
                 genMuon.p4().DeltaR(mu4) < 0.3) :
              muon.isMatched = True
              if ((genMuon.statusFlags&1 == 1) or (genMuon.statusFlags&6 == 6)):
                muon.isPromptMatched = True
                
        outGenMatched = []
        outPromptGenMatched = []
	for muon in muons:
	   outGenMatched.append(muon.isMatched)
           outPromptGenMatched.append(muon.isPromptMatched)
        self.out.fillBranch("Muon_genmatched", outGenMatched)
        self.out.fillBranch("Muon_promptgenmatched", outPromptGenMatched)
        return True

