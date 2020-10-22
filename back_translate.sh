#!/bin/bash
#SBATCH --job-name=bt-ml
#SBATCH --partition long
#SBATCH --account cvit_bhaasha
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --mem=40G
#SBATCH --time 0-04:00:00
#SBATCH --signal=B:HUP@600
# Constants

# assuming $DATA/monolingual/ml/monolingual.ml
# assuming $DATA/$DATASET/ (the full parallel dataset)
# Make sure that $DATASET is registered in corpora.py
DATASET="complete-en-ml"

# Basic Setup
source ../venv/bin/activate
LOCAL_ROOT="/ssd_scratch/cvit/$USER"
REMOTE_ROOT="/home2/$USER"
mkdir -p $LOCAL_ROOT/{data,checkpoints}
DATA=$LOCAL_ROOT/data
CHECKPOINTS=$LOCAL_ROOT/checkpoints
CKPT=$CHECKPOINTS/checkpoint_last.pt
export ILMULTI_CORPUS_ROOT=$DATA
mkdir -p $DATA/monolingual/ml

function _copy {
    rsync -rvz $REMOTE_ROOT/checkpoints/checkpoint_{last,best}.pt $CHECKPOINTS/
    rsync -rvz $REMOTE_ROOT/datasets/$DATASET/ $DATA/$DATASET/
    rsync -rvz $REMOTE_ROOT/datasets/monolingual/ml/ $DATA/monolingual/ml/
}

_copy

mv $DATA/$DATASET/test.ml-en.ml "$DATA/$DATASET/test.ml-en.ml_original"
mv $DATA/$DATASET/test.ml-en.en "$DATA/$DATASET/test.ml-en.en_original"

function _backtranslate {
    python3 generate.py config.yaml \
        --task shared-multilingual-translation  \
        --path $CKPT > $DATA/monolingual/ml/_.txt
    cat $DATA/monolingual/ml/_.txt \
        | grep "^H" | sed 's/^H-//g' | sort -n | cut -f 3 \
        | sed 's/ //g' | sed 's/▁/ /g' | sed 's/^ //g' \
            > $DATA/monolingual/ml/bt.hyp
    cat $DATA/monolingual/ml/_.txt \
        | grep "^T" | sed 's/^T-//g' | sort -n | cut -f 2 \
        | sed 's/ //g' | sed 's/▁/ /g' | sed 's/^ //g' \
            > $DATA/monolingual/ml/bt.ref
}

cp $DATA/monolingual/ml/monolingual.ml "$DATA/$DATASET/test.ml-en.ml"
touch "$DATA/$DATASET/test.ml-en.en"
_backtranslate
mv $DATA/monolingual/ml/bt.hyp $DATA/monolingual/ml/bt.en
mv $DATA/monolingual/ml/bt.ref $DATA/monolingual/ml/clean_monolingual.ml

cp $DATA/monolingual/ml/bt.en "$DATA/$DATASET/test.ml-en.en"
touch "$DATA/$DATASET/test.ml-en.ml"
_backtranslate
mv $DATA/monolingual/ml/bt.hyp $DATA/monolingual/ml/bt_bt.ml

# Cleanup backtranslate
rm -rf $DATA/monolingual/ml/bt.ref
rm -rf $DATA/monolingual/ml/_.txt

# Get scores
fairseq-score -s $DATA/monolingual/ml/bt_bt.ml -r $DATA/monolingual/ml/clean_monolingual.ml --sentence-bleu > $DATA/monolingual/ml/scores.txt

# Export
ssh $USER@ada "mkdir -p $REMOTE_ROOT/datasets/monolingual"
rsync -rvz $DATA/monolingual/ml/{clean_monolingual.ml,bt.en,scores.txt} $REMOTE_ROOT/datasets/monolingual/ml/
