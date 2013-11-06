'''
Created on Nov 5, 2013

@author: KHS
'''

from operator import itemgetter

class Clustering:
    
    #********************** PRIVATE METHODS ****************************
    
    def __init__(self):
        self.similarities   = {}
        self.clusters       = {}
    
    
    def _readSimilarities(self, fileName):
        inp = open(fileName, 'r')
        for line in inp.readlines():
            line = line.strip()
            line = line.split()
            
            if not self.similarities.has_key(line[1]):
                self.similarities[ line[1] ] = {}
            self.similarities[ line[1] ][ line[2] ] = float(line[3]) 
            
        inp.close()
    
    def _getSimilarity(self, dbA, dbB ):
        return self.similarities[ dbA ][ dbB ]
    
    def _clearAll(self):
        self._clearClusters()
        self._clearSimilarities()
        
        
    def _clearClusters(self):
        self.clusters.clear()
        
    def _clearSimilarities(self):
        self.similarities.clear()
    
    def _getKMostSimilarCollections(self, collection, K=-1):
        """
        If K is bigger than number of collections in the set or equals -1
        then function will return all available similarities
        """
        numCollections  = len( self.similarities[collection] )
        similarities    = sorted( self.similarities[collection].iteritems(), key=itemgetter(1), reverse=True )
        if K == -1 or K >= numCollections:
            return similarities
        return similarities[:K]
    
    
    #********************** PUBLIC METHODS ****************************
    
    # compute offline clusters    
    def computeOfflineClusters(self, fileName, clusterSize):
        
        # just in case clear everything
        self._clearAll()
        # read similarities
        self._readSimilarities( fileName )
        # compute clusters
        for collection in self.similarities.iterkeys():
            self.clusters.setdefault(collection, []).append(collection)
            cluster = self._getKMostSimilarCollections(collection, clusterSize)
            #print collection, cluster
            for item in cluster:
                if item[0] != collection:
                    self.clusters[collection].append(item[0])
        
        
    def printClusters(self):
        for coll in self.clusters.iterkeys():
            print coll, self.getCluster(coll)
            
    def getCluster(self, collection):
        return self.clusters.get(collection)
    
    def getCollections(self):
        return self.clusters.iterkeys()
        
        
    def computeOnlineClusters(self, initSet, clusterSize):
        
        # clear from previous results
        self._clearClusters()
        
        # compute cluster for each collection
        for collection in initSet:
            self.clusters.setdefault(collection, []).append(collection)
            # get all available similarities. Note that sims are sorted
            sims    = self._getKMostSimilarCollections( collection, -1 )
            pos     = 0
            while pos < len(sims) and len(self.clusters[collection]) < clusterSize and len(self.clusters[collection])<len(initSet):                
                if sims[pos][0] != collection and sims[pos][0] in initSet:
                    self.clusters[collection].append(sims[pos][0])
                pos += 1
        
        
        
        
    


    
    
        
        