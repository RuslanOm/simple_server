from pathlib import Path
import yaml 


def load_config(configuration_file=None):
    default_file = Path(__file__).parent / "config.yaml"
    with open(default_file, "r") as f:
        config = yaml.safe_load(f)
    
    cf_dict = {}
    if configuration_file:
        cf_dict = yaml.safe_load(configuration_file)

    config.update(**cf_dict)
    return config        

