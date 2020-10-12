#!bin/bash

source ../venv/bin/activate
LOCAL_ROOT="/ssd_scratch/cvit/$USER"
REMOTE_ROOT="/home2/$USER"

mkdir -p $LOCAL_ROOT/{data,checkpoints,results}

DATA=$LOCAL_ROOT/data
CHECKPOINTS=$LOCAL_ROOT/checkpoints
RESULTS=$LOCAL_ROOT/results

rsync -rvz $REMOTE_ROOT/checkpoints/checkpoint_{last,best}.pt $CHECKPOINTS/

# IMPORT=directory.tar.xz
rsync --progress $REMOTE_ROOT/datasets/$IMPORT $DATA/
# tar -kxvf $DATA/$IMPORT -C $DATA/

ssh $USER@ada "mkdir -p ada:/share1/$USER/backtranslation_results/"

rsync -rvz $REMOTE_ROOT/datasets/complete-en-ml/ $DATA/complete-en-ml/
# mv $DATA/sample_check/a.txt $DATA/complete-en-ml/test.ml-en.en
export ILMULTI_CORPUS_ROOT=$DATA

python3 preprocess_cvit.py config.yaml

function _backtranslate {
    python3 generate.py config.yaml \
        --task shared-multilingual-translation  \
        --path $CHECKPOINTS/checkpoint_best.pt > $RESULTS/backtranslated.txt
}

function train_mt {
    python3 train.py \
        --task shared-multilingual-translation \
        --num-workers 0 \
        --arch transformer \
        --max-tokens 5000 --lr 1e-4 --min-lr 1e-9 \
        --optimizer adam \
        --save-dir $CHECKPOINTS \
        --log-format simple --log-interval 200 \
        --criterion label_smoothed_cross_entropy \
        --dropout 0.1 --attention-dropout 0.1 --activation-dropout 0.1 \
        --ddp-backend no_c10d \
        --update-freq 2 \
        --reset-optimizer \
        --share-all-embeddings \
        config.yaml 
}

train_mt
