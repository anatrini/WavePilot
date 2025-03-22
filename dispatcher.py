# Global dispatcher
SUGGEST_DISPATCH = {
    "categorical": lambda trial, name, cfg: trial.suggest_categorical(name, cfg["values"]),
    "float": lambda trial, name, cfg: trial.suggest_float(name, cfg["low"], cfg["high"], log=cfg.get("log", False)),
    "int": lambda trial, name, cfg: trial.suggest_int(name, cfg["low"], cfg["high"])
}