import typing as t

import ignite.engine as ie
import numpy as np
import sklearn.decomposition as skd
import sklearn.manifold as skm
import torch as th
import torch.nn.functional as func

import constants as ct
import options.experiment_options as eo
import postpro.evaluators._evaluator_base as _base
import pro.engine as pe
import specs.maps as sm


class AutoEncoderEvaluator(_base.BaseEvaluator):
    def __init__(self, opts: eo.ExperimentOptions, local_rank: int):
        super(AutoEncoderEvaluator, self).__init__(opts, local_rank)
        assert self.opts.model.type == 'ae'

    def _init_evaluators(self) -> t.Tuple[ie.Engine, ie.Engine, ie.Engine]:
        evaluator_metrics = sm.Metrics[self.opts.evaluator.metrics].value

        train_evaluator = pe.create_ae_evaluator(self.model, evaluator_metrics, self.device, True)
        dev_evaluator = pe.create_ae_evaluator(self.model, evaluator_metrics, self.device, True)
        test_evaluator = pe.create_ae_evaluator(self.model, evaluator_metrics, self.device, True)

        return train_evaluator, dev_evaluator, test_evaluator

    def _get_model_outputs(self, x: th.Tensor) -> t.Dict[str, th.Tensor]:
        recon, energy, temporal_embed, class_embed, *_ = self.model(x)
        conf = func.softmax(energy, dim=-1)

        return {
            'temporal_embeds': temporal_embed.cpu().numpy(),
            'class_embeds': class_embed.cpu().numpy(),
            'confs': conf.cpu().numpy()
        }

    def _get_projections(self, embed_name: str, sample_embeds: np.ndarray) -> np.ndarray:
        if embed_name == 'class_embeds':
            n, c = sample_embeds.shape
            pca_ndim = min(n, c, 64)
            sample_pca = skd.PCA(pca_ndim, random_state=ct.RANDOM_STATE).fit_transform(sample_embeds)
            sample_tsne = skm.TSNE(2, verbose=1, random_state=ct.RANDOM_STATE).fit_transform(sample_pca)
        elif embed_name == 'temporal_embeds':
            if sample_embeds.ndim == 5:  # sequence models
                n, _t, c, h, w = sample_embeds.shape
                sample_embeds = sample_embeds.reshape([n, _t, c * h * w])
            else:  # hierarchical models
                _t = 1
                n, c, h, w = sample_embeds.shape
                sample_embeds = sample_embeds.reshape([n, _t, c * h * w])
            pca_ndim = min(n, c * h * w, 64)
            sample_pca = np.empty([n, _t, pca_ndim])
            sample_tsne = np.empty([n, _t, 2])
            for i in range(_t):
                sample_pca[:, i, :] = skd.PCA(pca_ndim, random_state=ct.RANDOM_STATE).fit_transform(
                    sample_embeds[:, i, :])
                sample_tsne[:, i, :] = skm.TSNE(2, verbose=1, random_state=ct.RANDOM_STATE) \
                    .fit_transform(sample_pca[:, i, :])
        else:
            raise ValueError(f'Unknown embed name: {embed_name}.')

        return sample_tsne
