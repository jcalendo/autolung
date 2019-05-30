"""Read settings and Metadata from Config file

(c) 2019 Gennaro Calendo, Laboratory of Marla R. Wolfson, MS, PhD at Lewis Katz School of Medicine at Temple University
"""
import configparser


def load_settings(config_file):
    """Read contents of config file and pass on as settings for image processing
    
    Arguments:
        config_file {str} -- path to config file
    
    Returns:
        dict -- image metadata from config file
    """
    config = configparser.ConfigParser()
    
    try:
        config.read(config_file)
    except FileNotFoundError:
        print("Could not find configuration file")

    # read the config sections
    metadata = config['Image_Metadata']
    threshold_params = config['Threshold_Params']
    morphometry_params = config['Morphology_Params']

    # extract the settings from the sections
    # use .get method to set defaults if setting is missing
    species = metadata.get('Species', 'mouse')
    magnification = metadata.get('Magnification', '10X')
    fixed_field = metadata.get('Fixed_Field', '2560x1920')
    scale = float(metadata.get('Scale', 2.0969))
    block_size = int(threshold_params.get('Block_Size', 641))
    constant = int(threshold_params.get('Constant', 1))
    min_alv_size = int(morphometry_params.get('Min_Alveolar_Size', 500))
    max_speckle_size = int(morphometry_params.get('Max_Speckle_Size', 100))

    settings = {"species" : species,
                "magnification" : magnification,
                "fixed_field" : fixed_field,
                "scale" : scale,
                "block_size" : block_size,
                "constant" : constant, 
                "min_alv_size" : min_alv_size,
                "max_speckle_size" : max_speckle_size
                }

    return settings