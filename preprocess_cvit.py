from argparse import ArgumentParser
from fairseq.data.cvit.utils import pairs_select
from fairseq.data.cvit.dataset import _CVITIndexedRawTextDataset
from fairseq.data.cvit.lmdb import LMDBCorpusWriter, LMDBCorpus
import yaml
from multiprocessing import Pool
from functools import partial
import os
from ilmulti.sentencepiece import SentencePieceTokenizer
    
    
def read_config(path):
    with open(path) as config:
        contents = config.read()
        data = yaml.load(contents)
        return data

def build_corpus(corpus, config, rebuild=False):
    #print ("We above")
    tokenizer = SentencePieceTokenizer(config)
    print ("We below")
    if not LMDBCorpus.exists(corpus):
        print("LMDB({}) does not exist. Building".format(corpus.path))
        raw_dataset = _CVITIndexedRawTextDataset(corpus, tokenizer)
        writer = LMDBCorpusWriter(raw_dataset)
        writer.close()
        print("Built LMDB({})".format(corpus.path))
    else:
        print ("Heyo this is built already")


def get_pairs(data):
    corpora = []
    for split in ['train', 'dev', 'test']:
        pairs = pairs_select(data['corpora'], split) 
        #pairs = monoling_select()
        #print("pairs inside the preprocess file are", pairs)
        if (pairs != []):
            srcs,tgts = list(zip(*pairs))
            corpora.extend(srcs)
            corpora.extend(tgts)
        
    return list(set(corpora))

def main(config_file, rebuild):
    data = read_config(config_file)
    print (data)
    corpora = get_pairs(data)
    hard_code_dict = {
    'en': 4000, 
    'mr': 4000
    }
    
    build_corpus_ = partial(build_corpus, config=hard_code_dict,  rebuild=rebuild)

    # Create pool of processes eqvt to cores
    # Parallel call build_corpus on corpora
    cores = os.cpu_count()
    pool = Pool(processes=cores)
    pool.map_async(build_corpus_, corpora)
    pool.close()
    pool.join()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('config_file', help='config file')
    parser.add_argument('--rebuild', action='store_true')
    
    args = parser.parse_args()
    main(args.config_file, args.rebuild)
