#!bin/bash

source ../venv/bin/activate
LOCAL_ROOT="/ssd_scratch/cvit/$USER"
REMOTE_ROOT="/home2/$USER"

IMPORT=directory.tar.xz

mkdir -p $LOCAL_ROOT/{data,checkpoints,results}

DATA=$LOCAL_ROOT/data
CHECKPOINTS=$LOCAL_ROOT/checkpoints
RESULTS=$LOCAL_ROOT/results

rsync -rvz $REMOTE_ROOT/checkpoints/checkpoint_best.pt $CHECKPOINTS/

IMPORT=directory.tar.xz
rsync --progress $REMOTE_ROOT/datasets/$IMPORT $DATA/
tar -kxvf $DATA/$IMPORT -C $DATA/

ssh $USER@ada "mkdir -p ada:/share1/$USER/backtranslation_results/"

rsync -rvz $REMOTE_ROOT/datasets/complete-en-ml/ $DATA/complete-en-ml/
mv $DATA/sample_check/a.txt $DATA/complete-en-ml/test.ml-en.en
export ILMULTI_CORPUS_ROOT=$DATA

python3 preprocess_cvit.py config.yaml

function _backtranslate {
    python3 generate.py config.yaml \
        --task shared-multilingual-translation  \
        --path $CHECKPOINTS/checkpoint_best.pt > $RESULTS/backtranslated.txt
}

_backtranslate
