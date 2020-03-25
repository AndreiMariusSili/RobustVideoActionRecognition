import helpers as hp
import options.experiment_options as eo
import options.job_options as jo


def setup(opts: jo.SetupOptions) -> None:
    if opts.set == 'smth':
        import prepro.smth
        prepro.smth.setup()
    elif opts.set == 'hmdb':
        import prepro.hmdb
        prepro.hmdb.setup()
    else:
        raise ValueError(f'Unknown options: {opts}')


def select_subset(opts: jo.SelectSubsetOptions) -> None:
    if opts.set == 'smth':
        import prepro.smth
        prepro.smth.select_subset(opts)
    else:
        raise ValueError(f'Unknown options: {opts}')


def prepro_set(opts: jo.PreproSetOptions) -> None:
    import prepro
    prepro.common.split_train_dev(opts.set, int(opts.split))
    prepro.common.augment_meta(opts.set, int(opts.split))
    prepro.common.merge_meta(opts.set, int(opts.split))
    prepro.common.gather_stats(opts.set, int(opts.split))
    if opts.jpeg:
        prepro.common.extract_jpeg(opts.set, int(opts.split))


def run_experiment(local_rank: int, opts: jo.RunExperimentOptions):
    spec: eo.ExperimentOptions = hp.build_spec(opts)
    if spec.model.type == 'class':
        import pro.runners.runner_class as rcl
        rcl.ClassRunner(spec, local_rank).run()
    elif spec.model.type == 'ae':
        import pro.runners.runner_ae as rae
        rae.AutoEncoderRunner(spec, local_rank).run()
    elif spec.model.type == 'gsnn':
        import pro.runners.runner_gsnn as rgsnn
        rgsnn.GSNNRunner(spec, local_rank).run()
    elif spec.model.type == 'vae':
        import pro.runners.runner_vae as rvae
        rvae.VariationalAutoEncoderRunner(spec, local_rank).run()


def evaluate_experiment(local_rank: int, opts: jo.EvaluateExperimentOptions):
    spec = hp.load_spec(opts)
    if spec.model.type == 'class':
        import postpro.evaluators.evaluator_class as ecl
        ecl.ClassEvaluator(spec, local_rank).start()
    elif spec.model.type == 'ae':
        import postpro.evaluators.evaluator_ae as eae
        eae.AutoEncoderEvaluator(spec, local_rank).start()
    elif spec.model.type == 'gsnn':
        import postpro.evaluators.evaluator_gsnn as egsnn
        egsnn.GSNNEvaluator(spec, local_rank).start()
    elif spec.model.type == 'vae':
        import postpro.evaluators.evaluator_vae as evae
        evae.VariationalAutoEncoderEvaluator(spec, local_rank).start()


def visualise_model(opts: jo.VisualiseExperimentOptions):
    raise NotImplementedError
