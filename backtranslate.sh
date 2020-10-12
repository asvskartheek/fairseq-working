#!bin/bash

source ../venv/bin/activate
LOCAL_ROOT="/ssd_scratch/cvit/$USER"
REMOTE_ROOT="/home2/$USER"

mkdir -p $LOCAL_ROOT/{data,checkpoints,results}

DATA=$LOCAL_ROOT/data
CHECKPOINTS=$LOCAL_ROOT/checkpoints
RESULTS=$LOCAL_ROOT/results

rsync -rvz $REMOTE_ROOT/checkpoints/checkpoint_best.pt $CHECKPOINTS/

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

ARCH='transformer'
MAX_TOKENS=3500
LR=1e-3
UPDATE_FREQ=4
MAX_EPOCHS=200

function train {
    python3 train.py \
        --task shared-multilingual-translation \
        --share-all-embeddings \
        --num-workers 0 \
        --arch $ARCH \
        --max-tokens $MAX_TOKENS --lr $LR --min-lr 1e-9 \
        --optimizer adam --adam-betas '(0.9, 0.98)' \
        --save-dir $CHECKPOINTS \
        --log-format simple --log-interval 200 \
        --dropout 0.1 --attention-dropout 0.1 --activation-dropout 0.1 \
        --lr-scheduler inverse_sqrt \
        --clip-norm 0.1 \
        --ddp-backend no_c10d \
        --update-freq $UPDATE_FREQ \
        --max-epoch $MAX_EPOCHS \
        --criterion label_smoothed_cross_entropy \
        config.yaml
}

train
