from collections import defaultdict
from itertools import combinations
from . import DATASET_REGISTRY

def canonicalize(langcode):
    _variations = {
        "ur": ["ur", "ud"],
        "bn": ["bg", "bn"]
    }

    inverse = {}
    for root in _variations:
        for x in _variations[root]:
            inverse[x] = root

    return inverse.get(langcode, langcode)

def select(tags, splits, langs):
    """
    """
    # Filter by split, langs
    registry = dict([
            (k, v)  \
            for k, v in DATASET_REGISTRY.items() \
            if k in tags
    ])

    #print ("THESE ARE THE TAGS INSIDE THE SELECT_UTILS", tags)
    #print ("THESE ARE THE SPLITS INSIDE THE SELECT_UTILS", splits)
    #print ("THESE ARE THE LANGS INSIDE THE SELECT_UTILS", langs)
    #print ("\n")
    #print ("WHY WON'T THIS WORK", DATASET_REGISTRY.items())
    #print ("This is the registry", registry)

    filtered_corpora = []
    #print ("\n")
    for key in registry:
        #print ("INSIDE SELECT FUNCTION", key)
        _splits, f = registry[key]
        #print ("These are the varibles", _splits, f)
        
        #langs = ['ta']
        
        isplits = set(_splits).intersection(set(splits))
        isplits = list(isplits)
        #print ("Isplits", isplits)
        for _split in isplits:
            corpora = f(_split)
            #print ("This is the corpora", corpora)
            
            corpora = [
                c for c in corpora \
                if c.lang in langs
            ]

            #print ("Corpora after filtering", corpora)
            filtered_corpora.extend(corpora)


    def group_by_tag(corpora):
        _dict = defaultdict(list)
        for corpus in corpora:
            _dict[corpus.tag].append(corpus)
        return _dict

    corpora = group_by_tag(filtered_corpora)
    pairs = []
    
    #print ("These are the corpora", corpora)
    
    for key in corpora:
        #print ("This is the key", key)
        #print ("Corpora key", corpora[key])
        #print ("What are the combinations", combinations(corpora[key], 2))
        # TODO(jerin): Sort for determinism
        for dx, dy in combinations(corpora[key], 2):
            #print ("This is dx", dx)
            #print ("This is dy", dy)
            #print ("\n")
            pairs.append((dx, dy))

    #print ("Pairs inside select", pairs)
    return pairs


def pairs_select(corpora_config, split):
    ls = []
    #print ("This is the split inside the utils", split)
    if split == 'valid': split = 'dev'
    #print ("This is the corpora_config", corpora_config)
    for tag, v in corpora_config.items():
        #print ("This is the tag", tag)
        #print ("This is v", v)
        tags = [tag]
        if split in v['splits']:
            #print ("\n")
            #print ("this is executing")
            splits = [split]
            #print ("These are the tags", tags)
            #print ("Langs is wtf", v['langs'])
            #print ("\n")
            #print ("Inside pairs_select of utils", tags, splits, v['langs'])
            pairs = select(tags, splits, v['langs'])
            #print (pairs)
            ls.extend(pairs)

    #print ("This is ls", ls)
    # Set is non-determinism. Sort
    def sort_key(pair):
        first, second = pair
        return (first.path, second.path)

    unique = list(set(ls))
    #print ("What is unique", unique)
    unique = sorted(unique, key=sort_key)
    #print ("After sorting", unique)
    return unique


###################################### MONO PRETRAIN CODE ###########################################
def pretrain_select(tags, splits, langs):
    """
    """
    # Filter by split, langs
    #print ("pretrain_select is executing")
    registry = dict([
            (k, v)  \
            for k, v in DATASET_REGISTRY.items() \
            if k in tags
    ])

    #print ("THESE ARE THE TAGS INSIDE THE SELECT_UTILS", tags)
    #print ("THESE ARE THE SPLITS INSIDE THE SELECT_UTILS", splits)
    #print ("THESE ARE THE LANGS INSIDE THE SELECT_UTILS", langs)
    #print ("\n")
    #print ("WHY WON'T THIS WORK", DATASET_REGISTRY.items())
    #print ("This is the registry", registry)

    filtered_corpora = []
    #print ("\n")
    for key in registry:
        #print ("INSIDE SELECT FUNCTION", key)
        _splits, f = registry[key]
        #print ("These are the varibles", _splits, f)
        
        #langs = ['en','ta']
        
        isplits = set(_splits).intersection(set(splits))
        isplits = list(isplits)
        #print ("Isplits", isplits)
        for _split in isplits:
            corpora = f(_split)
            print ("This is the corpora", corpora)
            
            corpora = [
                c for c in corpora \
                if c.lang in langs
            ]
            #print ("Reached here hello")
            #print ("Corpora after filtering", corpora)
            filtered_corpora.extend(corpora)


    def group_by_tag(corpora):
        _dict = defaultdict(list)
        for corpus in corpora:
            _dict[corpus.tag].append(corpus)
        return _dict

    corpora = group_by_tag(filtered_corpora)
    #print ("This is the corpora line 159", corpora)
    pairs = []
    for key in corpora:
        print ("This is the key", key)
        print ("Corpora key", corpora[key])
        #print ("What are the combinations", combinations(corpora[key], 2))
        #TODO(jerin): Sort for determinism
        #for dx, dy in combinations(corpora[key], 2):
        #pairs.append((dx, dy))
        #pairs.append(corpora[key])
    return corpora[key]

def monoling_select(corpora_config, split):
    #print ("monoling_select is executing")
    ls = []
    #print ("This is the split inside the utils", split)
    if split == 'valid': split = 'dev'
    #print ("This is the corpora_config", corpora_config)
    for tag, v in corpora_config.items():
        #print ("This is the tag", tag)
        #print ("This is v", v)
        tags = [tag]
        if split in v['splits']:
            #print ("\n")
            #print ("this is executing")
            splits = [split]
            #print ("These are the tags", tags)
            #print ("Langs is wtf", v['langs'])
            #print ("\n")
            #print ("Inside pairs_select of utils", tags, splits, v['langs'])
            pairs = pretrain_select(tags, splits, v['langs'])
            #print ("We getting them", pairs)
            ls = pairs

    # Set is non-determinism. Sort
    def sort_key(pair):
        first, second = pair
        return (first.path, second.path)

    #print ("What is ls now", ls)
    unique = list(set(ls))
    #unique = sorted(unique, key=sort_key)
    #print ("What is unique", unique)
    return unique[0]
#######################################################################################################


if __name__ == '__main__':
    tags = ['iitb-hi-en', 'wat-ilmpc']
    splits = ['train']
    langs = ['en', 'hi', 'ta', 'ml']
    pairs = select(tags, splits, langs)
    from pprint import pprint
    pprint(pairs)