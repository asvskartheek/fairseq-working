from . import DATASET_REGISTRY
from . import dataset_register, data_abspath
from . import Corpus, sanity_check


@dataset_register('iitb-hi-en', ['train', 'dev', 'test'])
def IITB_meta(split):
    corpora = []
    for lang in ['en', 'hi']:
        sub_path = 'filtered-iitb/{}.{}'.format(split, lang)
        corpus = Corpus('iitb-hi-en', data_abspath(sub_path), lang)
        corpora.append(corpus)
    return corpora

@dataset_register('national-newscrawl', ['train', 'dev', 'test'])
def NationalNewscrawl_meta(split):
    if split in ['dev', 'test']:
        return []
    corpora = []
    for lang in ['en', 'hi']:
        sub_path = 'national-newscrawl/national.{}'.format(lang)
        corpus = Corpus('iitb-hi-en', data_abspath(sub_path), lang)
        corpora.append(corpus)
    return corpora

@dataset_register('wat-ilmpc', ['train', 'dev', 'test'])
def WAT_meta(split):
    corpora = []
    langs = ['bn', 'hi', 'ml', 'si', 'ta', 'te', 'ur']
    for lang in langs:
        for src in [lang, 'en']:
            sub_path = 'indic_languages_corpus/bilingual/{}-en/{}.{}'.format(
                    lang, split, src
            )
            corpus_name = 'wat-ilmpc-{}-{}'.format(lang, 'en')
            corpus = Corpus(corpus_name, data_abspath(sub_path), src)
            corpora.append(corpus)
    return corpora

@dataset_register('ufal-en-tam', ['train', 'dev', 'test'])
def UFALEnTam_meta(split):
    corpora = []
    for lang in ['en', 'ta']:
        sub_path = 'ufal-en-tam/corpus.bcn.{}.{}'.format(split, lang)
        corpus = Corpus('ufal-en-tam', data_abspath(sub_path), lang)
        corpora.append(corpus)
    return corpora

@dataset_register('ilci', ['train', 'dev', 'test'])
def ILCI_meta(split):
    if split in ['dev', 'test']:
        return []
    corpora = []
    langs = [
        'en', 'te', 'hi', 'ml', 
        'ta', 'ud', 'bg', 'mr',
        'gj', 'pj', 'kn'
    ]

    from .utils import canonicalize

    for lang in langs:
        sub_path = 'ilci/complete.{}'.format(lang)
        _lang = canonicalize(lang)
        corpus = Corpus('ilci', data_abspath(sub_path), _lang)
        corpora.append(corpus)
    return corpora

@dataset_register('bible-en-te', ['train', 'dev', 'test'])
def BIBLEEnTe_meta(split):
    corpora = []
    for lang in ['en', 'te']:
        sub_path = 'bible-en-te/bible.{}.{}'.format(split, lang)
        corpus = Corpus('bible-en-te', data_abspath(sub_path), lang)
        corpora.append(corpus)
    return corpora

@dataset_register('mann-ki-baat-test', ['test'])
def MannKiBaat_meta(split):
    corpora = []
    for lang in ['en','hi','ta','te']:
        sub_path = 'mann-ki-baat-test/mkb.{}'.format(lang)
        corpus = Corpus('mann-ki-baat-test', data_abspath(sub_path), lang)
        corpora.append(corpus)
    return corpora

@dataset_register('eenadu-en-te', ['train'])
def EenaduBacktrans_meta(split):
    if split in ['dev', 'test']:
        return []

    corpora = []
    for lang in ['en','te']:
        sub_path = 'eenadu-en-te/train.{}'.format(lang)
        corpus = Corpus('eenadu-en-te', data_abspath(sub_path), lang)
        corpora.append(corpus)
    return corpora
    
@dataset_register('pretrain-en-tam', ['train', 'dev'])
def PretrainEnTam_meta(split):
    corpora = []
    for lang in ['en', 'ta']:
        sub_path = 'pretrain-en-tam/{}.{}'.format(split, lang)
        corpus = Corpus('pib-en-ta', data_abspath(sub_path), lang)
        corpora.append(corpus)
    return corpora
    
@dataset_register('ufal-en-or', ['train', 'dev', 'test'])
def UFALEnOriya_meta(split):
    #print ("This exeuctes when UFALEnTam_meta")
    corpora = []
    for lang in ['en', 'or']:
        sub_path = 'ufal-en-or/{}.{}'.format(split, lang)
        corpus = Corpus('ufal-en-or', data_abspath(sub_path), lang)
        corpora.append(corpus)
    #print ("From inside the corpora file", corpora)
    return corpora

@dataset_register('complete-en-te', ['train', 'dev', 'test'])
def CompleteEnTe_meta(split):
    corpora = []
    for lang in ['en', 'te']:
        sub_path = 'complete-en-te/{}.te-en.{}'.format(split, lang)
        corpus = Corpus('complete-en-te', data_abspath(sub_path), lang)
        corpora.append(corpus)
    #print ("From the corpora file", corpora)
    return corpora
    
@dataset_register('pib-en-mar', ['train', 'dev', 'test'])
def PIBEnMar_meta(split):
    corpora = []
    for lang in ['en', 'mr']:
        sub_path = 'pib-en-mar/{}.{}'.format(split, lang)
        corpus = Corpus('pib-en-mar', data_abspath(sub_path), lang)
        corpora.append(corpus)
    #print ("From the corpora file", corpora)
    return corpora
    
@dataset_register('pib-en-guj', ['train', 'dev', 'test'])
def PIBEnGuj_meta(split):
    corpora = []
    for lang in ['en', 'gu']:
        sub_path = 'pib-en-guj/{}.{}'.format(split, lang)
        corpus = Corpus('pib-en-guj', data_abspath(sub_path), lang)
        corpora.append(corpus)
    #print ("From the corpora file", corpora)
    return corpora



if __name__ == '__main__':
    def merge(*_as):
        _ase = []
        for a in _as:
            _ase.extend(a)
        return _ase

    ls = []
    for key in DATASET_REGISTRY:
        splits, f = DATASET_REGISTRY[key]
        for split in splits:
            ls.append(f(split))

    _all = merge(*ls)
    sanity_check(_all)

