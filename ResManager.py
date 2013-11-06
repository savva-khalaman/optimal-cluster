'''
Created on Nov 5, 2013

@author: KHS
'''

'''
Class ResManager is going to hold results of
a retrieval
'''

class ResManager():
    def __init__(self):
        self.qryDocs   = {}
        self.qryScores = {}
    
    
    def clean(self):
        """Clean previous results"""
        self.qryDocs.clear()
        self.qryScores.clear()
        
        
    def readResults(self, fileName, colNum = 6, ext = False):
        """Read original scores"""
        if colNum == 3:
            self._readThreeColumn(fileName)
        elif colNum == 4:
            self._readFourColumn(fileName)
        else:
            self._readSixColumn(fileName)
    
    def _readThreeColumn(self, fileName):
        inp = open(fileName, 'r')
        for line in inp.readlines():
            line = line.strip()
            line = line.split()
            self.qryDocs.setdefault( line[0], [] ).append( line[1] )
            self.qryScores.setdefault( line[0], [] ).append( float(line[2]) )
        inp.close()
    
    def _readFourColumn(self, fileName):
        """
        Reads extended result files; E.g.:
        qid counter doc1 score1
        qid counter doc2 score2
        """
        inp = open(fileName, 'r')
        for line in inp.readlines():
            line = line.strip()
            line = line.split()
            
            if line[0] not in self.qryDocs.keys():
                self.qryDocs.setdefault(line[0], {} )
                self.qryScores.setdefault(line[0], {} )
            #---->     --> qryid <--            --> counter <--        --> docid <--
            self.qryDocs[ line[0] ].setdefault( int(line[1]), [] ).append( line[2] )
            self.qryScores[ line[0] ].setdefault( int(line[1]), [] ).append( float(line[3]) )
        inp.close()
    
    
    def _readSixColumn(self, fileName):
        inp = open(fileName, 'r')
        for line in inp.readlines():
            line = line.strip()
            line = line.split()
            self.qryDocs.setdefault( line[0], [] ).append( line[2] )
            self.qryScores.setdefault( line[0], [] ).append( float(line[4]) )
        inp.close()
    
    def getQueries(self):
        """Returns a sorted list of query ids"""
        return sorted( self.qryDocs.keys() )
    
    def getDocs(self, qryid, counter = None):
        """Returns a list of the retrieved documents for the query"""
        if counter is None:
            return self.qryDocs[qryid]
        else:
            return self.qryDocs[qryid][counter]
    
    def getScores(self, qryid, counter = None):
        """Returns a list of the retrieved documents' scores"""
        if counter is None:
            return self.qryScores[qryid]
        else:
            return self.qryScores[qryid][counter]
    
    def getDocInfo(self, qryid, pos):
        """Returns a couple: doc & score"""
        return ( self.qryDocs[qryid][pos], self.qryScores[qryid][pos] )
    
    def getNumRetDocs(self, qryid):
        return len( self.qryDocs[qryid] )
    
    
    def setCuttoff(self, qryid,  lvl):
        if lvl < len( self.qryDocs[qryid] ):
            self.qryDocs[ qryid ][lvl:] = []
            self.qryScores[qryid][lvl:] = []
        else:
            print qryid, ":", lvl, "vs",len( self.qryDocs[qryid] )
    
    def getDocScore(self, qryid, docid):
        """
        Return document retrieval score. If docid doesn't exist in the
        list, then method returns 0 score.
        NOTE: current implementation is inefficient; quicker version
        needs a change in the data-structure
        """
        retrievedDocs = self.getDocs(qryid)
        for pos in range(len(retrievedDocs)):
            if docid == retrievedDocs[pos]:
                return self.qryScores[qryid][pos]
        return 0
            
