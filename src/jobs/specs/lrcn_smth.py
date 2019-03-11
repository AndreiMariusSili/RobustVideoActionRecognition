from torch import optim, nn
from ignite import metrics
import os

from models import options
import pipeline as pipe
from models import lrcn
import constants as ct

data_bunch_opts = pipe.DataBunchOptions(
    shape='volume',
    frame_size=224
)
data_set_opts = pipe.DataSetOptions(
    cut=1.00,
    sample_size=16
)
data_loader_opts = pipe.DataLoaderOptions(
    batch_size=16,
    shuffle=True,
    num_workers=os.cpu_count(),
    pin_memory=True,
    drop_last=False
)
model_opts = options.LRCNOptions(
    num_classes=10,
    freeze_feature_extractor=True
)
optimizer_opts = options.AdamOptimizerOptions(
    lr=0.01
)
trainer_opts = options.TrainerOptions(
    epochs=100,
    optimizer=optim.Adam,
    optimizer_opts=optimizer_opts,
    criterion=nn.CrossEntropyLoss
)
evaluator_opts = options.EvaluatorOptions(
    metrics={
        'acc@1': metrics.Accuracy(),
        'acc@3': metrics.TopKCategoricalAccuracy(k=3),
        'loss': metrics.Loss(nn.CrossEntropyLoss())
    }
)
lrcn_smth = options.RunOptions(
    name=f'{ct.SETTING}@lrcn@smth',
    resume=False,
    resume_from=None,
    log_interval=10,
    patience=10,
    model=lrcn.LRCN,
    model_opts=model_opts,
    data_bunch=pipe.SmthDataBunch,
    data_bunch_opts=data_bunch_opts,
    data_set_opts=data_set_opts,
    data_loader_opts=data_loader_opts,
    trainer_opts=trainer_opts,
    evaluator_opts=evaluator_opts
)