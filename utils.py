import Levenshtein
import tiktoken

def sim_find(mot, dico):
    similarites = {mot_dico: Levenshtein.ratio(mot, mot_dico) for mot_dico in dico}
    mot_proche = max(similarites, key=similarites.get)
    return mot_proche if similarites[mot_proche] >= 0.7 else None

def token_count(texte, modele="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(modele)
    tokens = encoding.encode(texte)
    return len(tokens)