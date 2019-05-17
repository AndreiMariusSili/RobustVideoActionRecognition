import os

from ignite import metrics
from torch import nn, optim

import constants as ct
import pipeline as pipe
from models import options, tadn

########################################################################################################################
# DATA BUNCH OPTIONS
########################################################################################################################
data_bunch_opts = pipe.DataBunchOptions(
    shape='volume',
    frame_size=224
)
########################################################################################################################
# TRAIN DATA
########################################################################################################################
train_do = pipe.DataOptions(
    meta_path=ct.SMTH_META_TRAIN,
    cut=1.0,
    setting='train',
    keep=64
)
train_so = pipe.SamplingOptions(
    num_segments=4,
    segment_size=1
)
train_data_set_opts = pipe.DataSetOptions(
    do=train_do,
    so=train_so
)
train_data_loader_opts = pipe.DataLoaderOptions(
    batch_size=64,
    shuffle=True,
    num_workers=os.cpu_count(),
    pin_memory=True,
    drop_last=False
)
########################################################################################################################
# VALID DATA
########################################################################################################################
valid_do = pipe.DataOptions(
    meta_path=ct.SMTH_META_TRAIN,
    cut=1.0,
    setting='valid',
    keep=64
)
valid_so = pipe.SamplingOptions(
    num_segments=4,
    segment_size=1
)
valid_data_set_opts = pipe.DataSetOptions(
    do=valid_do,
    so=valid_so
)
valid_data_loader_opts = pipe.DataLoaderOptions(
    batch_size=64,
    shuffle=False,
    num_workers=os.cpu_count(),
    pin_memory=True,
    drop_last=False
)
########################################################################################################################
# MODEL AND AUXILIARIES
########################################################################################################################
model_opts = options.TADNOptions(
    num_classes=ct.SMTH_NUM_CLASSES,
    time_steps=4,
    growth_rate=64,
    drop_rate=0.5,
)
optimizer_opts = options.AdamOptimizerOptions(
    lr=0.001
)
trainer_opts = options.TrainerOptions(
    epochs=30,
    optimizer=optim.Adam,
    optimizer_opts=optimizer_opts,
    criterion=nn.CrossEntropyLoss
)
evaluator_opts = options.EvaluatorOptions(
    metrics={
        'acc@1': metrics.Accuracy(output_transform=lambda tpl: tpl[0:2]),
        'acc@2': metrics.TopKCategoricalAccuracy(k=2, output_transform=lambda tpl: tpl[0:2]),
        'loss': metrics.Loss(nn.CrossEntropyLoss(), output_transform=lambda tpl: tpl[0:2])
    }
)
########################################################################################################################
# RUN
########################################################################################################################
dev_tadn_smth = options.RunOptions(
    name='dev_tadn_smth',
    mode='discriminative',
    resume=False,
    log_interval=1,
    patience=10,
    model=tadn.TimeAlignedDenseNet,
    model_opts=model_opts,
    data_bunch=pipe.SmthDataBunch,
    db_opts=data_bunch_opts,
    train_ds_opts=train_data_set_opts,
    valid_ds_opts=valid_data_set_opts,
    train_dl_opts=train_data_loader_opts,
    valid_dl_opts=valid_data_loader_opts,
    trainer_opts=trainer_opts,
    evaluator_opts=evaluator_opts
)