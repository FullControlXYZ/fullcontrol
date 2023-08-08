# this __init__ file should import lab functions/classes that supplement
# those that already exist in fullcontrol. if the lab functions overwrite
# existing fullcontrol features, it's likely best to have them in a
# separate import statement (e.g. like multiaxis stuff is currently)
from lab.fullcontrol.geometry import *
from lab.fullcontrol.p_r import setup_p, setup_r
