from typing import Optional, Dict, Any, Union, Type, Tuple
import dataclasses as dc
from torch import optim
from torch import nn

import pipeline as pipe

__all__ = [
    'TrainerOptions', 'EvaluatorOptions', 'LRCNOptions',
    'OptimizerOptions', 'AdamOptimizerOptions',
    'RunOptions'
]


@dc.dataclass
class OptimizerOptions:
    lr: Optional[float] = 0.001


@dc.dataclass
class AdamOptimizerOptions(OptimizerOptions):
    lr: Optional[float] = 0.001
    betas: Optional[Tuple[float, float]] = (0.9, 0.999)
    eps: Optional[float] = 1e-08
    weight_decay: Optional[float] = 0
    amsgrad: Optional[bool] = False


@dc.dataclass
class CriterionOptions:
    pass


@dc.dataclass
class LRCNOptions:
    num_classes: int
    freeze_features: bool
    freeze_fusion: bool


@dc.dataclass
class I3DOptions:
    num_classes: int
    modality: str = 'rgb'
    dropout_prob: float = 0.0
    name: str = 'inception'


@dc.dataclass
class TADNOptions:
    num_classes: int
    time_steps: int
    growth_rate: int
    drop_rate: float


@dc.dataclass
class TrainerOptions:
    epochs: int
    optimizer: Union[Type[optim.SGD], Type[optim.Adam], Type[optim.RMSprop]]
    criterion: Type[nn.CrossEntropyLoss]
    optimizer_opts: Optional[OptimizerOptions] = OptimizerOptions()
    criterion_opts: Optional[CriterionOptions] = CriterionOptions()


@dc.dataclass
class EvaluatorOptions:
    metrics: Dict[str, Any]


@dc.dataclass
class RunOptions:
    name: str
    resume: bool
    log_interval: int
    patience: int
    model: Type[nn.Module]
    model_opts: Union[LRCNOptions, I3DOptions, TADNOptions]
    data_bunch: Type[pipe.SmthDataBunch]
    db_opts: pipe.DataBunchOptions
    train_ds_opts: pipe.DataSetOptions
    valid_ds_opts: pipe.DataSetOptions
    train_dl_opts: pipe.DataLoaderOptions
    valid_dl_opts: pipe.DataLoaderOptions
    trainer_opts: TrainerOptions
    evaluator_opts: EvaluatorOptions
