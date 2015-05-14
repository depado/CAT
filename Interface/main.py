__author__ = 'Folaefolc'
__lisence__ = "CeCIL"

import interface
import sys
import traceback
import pdb

def pdb_post_mortem(exc_type, exc_val, exc_tb):
    # On affiche l'exception histoire de savoir ce qu'on debug
    print("".join(traceback.format_exception(exc_type, exc_val, exc_tb)))
    # On balance pdb en mode post mortem, c'est à dire qu'il va se lancer
    # malgré le fait que le programme ne marche plus, donnant accès
    # au contexte qu'il y avait juste avant que ça foire
    pdb.post_mortem(exc_tb)
    input("Appuyez sur Entrer pour terminer le programme ...")

# On dit à python de lancer cette fonction quand il plante
sys.excepthook = pdb_post_mortem

def go():
    janiswo = interface.Interface()
    janiswo.start()

if __name__ == '__main__':
    go()

