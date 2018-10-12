import sys
sys.path.append("..")
from averageAttack import AverageAttack
from bandwagonAttack import BandWagonAttack
from randomAttack import RandomAttack
from reverseBandwagonAttack import ReverseBandWagonAttack
#from RR_Attack import RR_Attack
#from hybridAttack import HybridAttack

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
