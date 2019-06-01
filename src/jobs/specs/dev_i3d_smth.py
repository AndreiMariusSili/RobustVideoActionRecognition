from ignite import metrics
from torch import cuda, nn, optim

import constants as ct
import pipeline as pipe
from models import i3d, options

NUM_DEVICES = cuda.device_count() if cuda.device_count() > 0 else 1

########################################################################################################################
# DATA BUNCH OPTIONS
########################################################################################################################
db_opts = pipe.DataBunchOptions(
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
    keep=4
)
train_so = pipe.SamplingOptions(
    num_segments=4,
    segment_size=1
)
train_ds_opts = pipe.DataSetOptions(
    do=train_do,
    so=train_so
)
train_dl_opts = pipe.DataLoaderOptions(
    batch_size=4,
    shuffle=True,
    num_workers=0,
    pin_memory=False,
    drop_last=False
)
########################################################################################################################
# VALID DATA
########################################################################################################################
valid_do = pipe.DataOptions(
    meta_path=ct.SMTH_META_TRAIN,
    cut=1.0,
    setting='valid',
    keep=4
)
valid_so = pipe.SamplingOptions(
    num_segments=4,
    segment_size=1
)
valid_ds_opts = pipe.DataSetOptions(
    do=valid_do,
    so=valid_so
)
valid_dl_opts = pipe.DataLoaderOptions(
    batch_size=4,
    shuffle=False,
    num_workers=0,
    pin_memory=False,
    drop_last=False
)
########################################################################################################################
# MODEL AND OPTIMIZER
########################################################################################################################
model_opts = options.I3DOptions(
    num_classes=ct.SMTH_NUM_CLASSES,
    dropout_prob=0.5,
)
optimizer_opts = options.AdamOptimizerOptions(
    lr=0.001
)
########################################################################################################################
# TRAINER AND EVALUATOR
########################################################################################################################
trainer_opts = options.TrainerOptions(
    epochs=5,
    optimizer=optim.Adam,
    optimizer_opts=optimizer_opts,
    criterion=nn.CrossEntropyLoss,
    metrics={
        'acc@1': metrics.Accuracy(output_transform=lambda x: x[1:3]),
        'acc@2': metrics.TopKCategoricalAccuracy(k=2, output_transform=lambda x: x[1:3]),
        'loss': metrics.Loss(nn.CrossEntropyLoss(), output_transform=lambda x: x[1:3])
    }
)

evaluator_opts = options.EvaluatorOptions(
    metrics={
        'acc@1': metrics.Accuracy(output_transform=lambda x: x[0:2]),
        'acc@2': metrics.TopKCategoricalAccuracy(k=2, output_transform=lambda x: x[0:2]),
        'loss': metrics.Loss(nn.CrossEntropyLoss(), output_transform=lambda x: x[0:2])
    }
)
########################################################################################################################
# RUN
########################################################################################################################
dev_i3d_smth = options.RunOptions(
    name='dev_i3d_smth',
    mode='discriminative',
    resume=False,
    log_interval=1,
    patience=5,
    model=i3d.I3D,
    model_opts=model_opts,
    data_bunch=pipe.SmthDataBunch,
    db_opts=db_opts,
    train_ds_opts=train_ds_opts,
    valid_ds_opts=valid_ds_opts,
    train_dl_opts=train_dl_opts,
    valid_dl_opts=valid_dl_opts,
    trainer_opts=trainer_opts,
    evaluator_opts=evaluator_opts
)
