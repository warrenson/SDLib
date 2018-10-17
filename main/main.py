import sys
sys.path.append("..")
from SDLib import SDLib
from tool.config import Config


if __name__ == '__main__':

    print '='*80
    print '   SDLib: A Python library used to collect shilling detection methods.'
    print '='*80
    print 'Supervised Methods:'
    print '1. DegreeSAD   2.CoDetector\n'
    print 'Semi-Supervised Methods:'
    print '3. SemiSAD\n'
    print 'Unsupervised Methods:'
    print '4. PCASelectUsers    5. FAP\n'
    print 'Extra Methods:'
    print '6. Kmeans\n'
    print '-'*80
    algor = -1
    conf = -1
    #order = input('please enter the num of the method to run it:')
    import time
    s = time.time()
    # if order == 0:
    #     try:
    #         import seaborn as sns
    #     except ImportError:
    #         print '!!!To obtain nice data charts, ' \
    #               'we strongly recommend you to install the third-party package <seaborn>!!!'
    #     conf = Config('../config/visual/visual.conf')
    #     Display(conf).render()
    #     exit(0)

# Loop it
    #for order in [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
    #for order in [4, 5, 6, 7, 8, 9, 10, 11, 12]:
    for order in [1, 2, 4, 5, 6]:
        if order == 1:
            conf = Config('../config/DegreeSAD.conf')

        elif order == 2:
            conf = Config('../config/CoDetector.conf')

        elif order == 3:
            conf = Config('../config/SemiSAD.conf')

        elif order == 4:
            conf = Config('../config/PCASelectUsers.conf')

        elif order == 5:
            conf = Config('../config/FAP.conf')

        elif order == 6:
            conf = Config('../config/Kmeans.conf')
        elif order == 7:
            conf = Config('../config/PCASelectUsersk5.conf')
        elif order == 8:
            conf = Config('../config/PCASelectUsersk7.conf')
        elif order == 9:
            conf = Config('../config/Kmeansp2.conf')
        elif order == 10:
            conf = Config('../config/Kmeansp4.conf')
        elif order == 11:
            conf = Config('../config/Kmeansp7.conf')
        elif order == 12:
            conf = Config('../config/Kmeansp10.conf')
        else:
            print 'Error num!'
            exit(-1)
        sd = SDLib(conf)
        sd.execute()
        e = time.time()
        print "Run time: %f s" % (e - s)
