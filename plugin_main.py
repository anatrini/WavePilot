import argparse

#from constants import IN_GUI_PORT, OUT_GUI_PORT
from logger import setup_logger
from plugin_renderer import main as renderer_main
from plugin_controller import main as controller_main


log = setup_logger("Plugin Main")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Unified main entrypoint for plugin communication")

    subparser = parser.add_subparsers(dest="mode", required=True)

    # Renderer parser
    renderer_parser = subparser.add_parser("render", help="Run remote preset renderization pipeline")
    renderer_parser.add_argument("-r", "--render_mode",
                        dest="render_mode",
                        type=str,
                        default="preset",
                        help="Select preset generation mode. If set to 'preset', iterate through available presets; if set to 'random', generate random values for each parameter. Default: 'preset'.")

    renderer_parser.add_argument("-i", "--iterations",
                        dest="no_iterations",
                        type=int,
                        default=1,
                        help="Specify the number of random batches of parameter values to generate. This option is only available when --render_mode is set to 'random'. Default: 1.")

    renderer_parser.add_argument("-d", "--directory",
                        dest="directory",
                        type=str,
                        default="rendered_recordings",
                        help="Name of the sub-directory to store rendered presets. Default: 'rendered_recordings'.")

    renderer_parser.add_argument("-n", "--dataset_filename",
                        dest="dataset_filename",
                        type=str,
                        default="dataset",
                        help="Set the name of .csv, containing the values of rendered presets. Default: 'dataset'.")

    renderer_parser.add_argument("-t", "--silence_thresh",
                        dest="silence_thresh",
                        type=float,
                        default=1e-6,
                        help="Adjust the silence threshold to prevent the recording of silent audio files. Default: 1e-6.")
    
    # Controller parser
    controller_parser = subparser.add_parser("controller", help="Run remote plugin controller pipeline")
    controller_parser.add_argument("-f", "--filepath",
                        dest="filepath",
                        type=str,
                        required=True,
                        help="Path to the JSON file containing the OSC addresses scheme.")
    
    args = parser.parse_args()

    if args.mode == "render":
        try:
            if args.render_mode == "preset" and args.no_iterations != 1:
                raise ValueError("Iterations argument is only available if mode is set to 'random'!")
            if args.render_mode == "random" and args.no_iterations < 1:
                raise ValueError("The number of parameters batches to be generated must be at least 1!")
        except ValueError as e:
            log.error(str(e))
            parser.print_help()
            exit(1)
    

    return args


def main():
    args = parse_arguments()

    try:
        if args.mode == "render":
            renderer_main(
                render_mode=args.render_mode,
                directory=args.directory,
                dataset_filename=args.dataset_filename,
                silence_thresh=args.silence_thresh,
                no_iterations=args.no_iterations)
        elif args.mode == "controller":
            controller_main(filepath=args.filepath)
        else:
            log.error("Invalid mode selected")

    except Exception as e:
        log.error("An error occurred: %s:", str(e))
        exit(1)

if __name__ == "__main__":
    main()
