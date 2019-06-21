"""Read settings and Metadata from Config file

(c) 2019 Gennaro Calendo, Laboratory of Marla R. Wolfson, MS, PhD at Lewis Katz School of Medicine at Temple University
"""
import configparser


def validate_settings(**kwargs):
    """Validate settings from configuration file

    Arguments:
        **kwargs -- settings read from config file or their defaults from .get
    
    Returns:
        dict -- validated settings
    """
    # check if block_size is odd
    if kwargs['block_size'] % 2 == 0:
        print(f"ERROR: Invalid Block_Size '{kwargs['block_size']}' -- must be odd integer, check your config file")
        print("Setting Block_Size to 251")
        kwargs['block_size'] = 251

    if kwargs['method'] not in ('mean', 'median', 'gaussian'):
        print(f"ERROR: Invalid Method '{kwargs['method']}' -- must be one of 'mean', 'median', or 'gaussian', check your config file")
        print("Setting Method to 'mean'")
        kwargs['method'] = 'mean'

    return kwargs


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

    metadata = config['Image_Metadata']
    threshold_params = config['Threshold_Params']
    morphometry_params = config['Morphology_Params']

    species = metadata.get('Species', 'mouse')
    magnification = metadata.get('Magnification', '10X')
    fixed_field = metadata.get('Fixed_Field', '2560x1920')
    scale = float(metadata.get('Scale', 2.0969))
    block_size = int(threshold_params.get('Block_Size', 251))
    constant = int(threshold_params.get('Constant', 0))
    method = str(threshold_params.get('Method', 'mean'))
    min_alv_size = int(morphometry_params.get('Min_Alveolar_Size', 500))
    max_speckle_size = int(morphometry_params.get('Max_Speckle_Size', 100))

    settings = {"species" : species,
                "magnification" : magnification,
                "fixed_field" : fixed_field,
                "scale" : scale,
                "block_size" : block_size,
                "constant" : constant,
                "method" : method, 
                "min_alv_size" : min_alv_size,
                "max_speckle_size" : max_speckle_size
                }

    validated = validate_settings(**settings)

    return validated