import sys
sys.path.append("..")
from averageAttack import AverageAttack
from bandwagonAttack import BandWagonAttack
from randomAttack import RandomAttack
from reverseBandwagonAttack import ReverseBandWagonAttack
from loveHateAttack import LoveHateAttack
from hybridAttack import HybridAttack
from segmentAttack import SegmentAttack
#from RR_Attack import RR_Attack

# Random attack
attack = RandomAttack('./config/random_config.conf')
attack.insertSpam()
attack.generateLabels('labels.txt')
attack.generateProfiles('profiles.txt')

# Average attack
attack = AverageAttack('./config/average_config.conf')
attack.insertSpam()
attack.generateLabels('labels.txt')
attack.generateProfiles('profiles.txt')

# Bandwagon attack
attack = BandWagonAttack('./config/bandwagon_config.conf')
attack.insertSpam()
attack.generateLabels('labels.txt')
attack.generateProfiles('profiles.txt')

# Reverse Bandwagon attack
attack = ReverseBandWagonAttack('./config/reverse_bandwagon_config.conf')
attack.insertSpam()
attack.generateLabels('labels.txt')
attack.generateProfiles('profiles.txt')

# Love\Hate attack
attack = LoveHateAttack('./config/love_hate_config.conf')
attack.insertSpam()
attack.generateLabels('labels.txt')
attack.generateProfiles('profiles.txt')

# Hybrid attack
attack = HybridAttack('./config/hybrid_config.conf')
attack.insertSpam()
attack.generateLabels('labels.txt')
attack.generateProfiles('profiles.txt')

# Segment attack
attack = SegmentAttack('./config/segment_config.conf')
attack.insertSpam()
attack.generateLabels('labels.txt')
attack.generateProfiles('profiles.txt')
