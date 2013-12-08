import time
import montecarlotree as mct
from test_tree import *




def time_NumIterations():
    initstate = r
    f = open("timingResultsnumRandMoves.txt",'w')
    f.write( "%-15s%-35s%15s"%("NumIters","Move","Time\n"))   
    for i in range(1,100):
        t1 = time.time()
        res = mct.MonteCarloMethod().TreeSearch(r,i,False)
        t2 = time.time()
        f.write("%-15d%-35s%15f\n"%(i,res,t2-t1))
        
    f.close()

def time_numRandMoves():
    initstate = r
    f = open("timingResultsnumRandMoves.txt",'w')
    f.write( "%-15s%-35s%15s"%("MaxDepth","Move","Time\n"))   
    for i in range(10000,50001,2000):
        total = 0
        for x in range(0,5):
            t1 = time.time()
            res = mct.MonteCarloMethod().TreeSearch(r,10,False,i)
            t2 = time.time()
            total += t2
        f.write("%-15d%-35s%15f\n"%(i,res,(t2-t1)/5.0))
    f.close()
    
