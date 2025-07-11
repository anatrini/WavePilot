import argparse
import asyncio
from optimize import main as optimize_main
from train import main as train_main
from logger import setup_logger


log = setup_logger("Main")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Unified main entrypoint for optimization and training")

    subparsers = parser.add_subparsers(dest="mode", required=True)

    # Optimizer parser
    optimize_parser = subparsers.add_parser("optimize", help="Run optimization pipeline")
    optimize_parser.add_argument("-f", "--filepath",
                        dest="filepath",
                        type=str,
                        required=True,
                        help="Dataset of the presets to be reduced.")

    optimize_parser.add_argument("-n", "--num_entries",
                        dest="num_entries",
                        type=int,
                        default=None,
                        help="Number of random entries to select from the dataset.")

    # optimize_parser.add_argument("-d", "--disable_split",
    #                     dest="disable_split",
    #                     action="store_false",
    #                     help="Disable train/test split and use the entire dataset for both training and validation. Default split enabled.")
    
    # optimize_parser.add_argument("-t", "--test_size",
    #                     dest="test_size",
    #                     type=float,
    #                     default=0.2,
    #                     help="Train test split size, only available if -d flag is not provided. Default size 0.2.")
    
    optimize_parser.add_argument("-m", "--mask_columns",
                        dest="mask_columns",
                        type=str,
                        nargs="+",  # Allows to pass a list of strings 
                        default=None,
                        help="List of parameter names to be masked (excluded) from the dataset.")


    # Train parser
    train_parser = subparsers.add_parser("train", help="Run training pipeline")
    train_parser.add_argument("-f", "--filepath",
                        dest="filepath",
                        type=str,
                        required=True,
                        help="Dataset of presets to be reduced.")

    train_parser.add_argument("-p", "--pretrained-model",
                        dest="pretrained_model",
                        type=str,
                        default=None,
                        help="Pretrained model file.")

    train_parser.add_argument("-o", "--optimizer-session",
                        dest="optimizer_session",
                        type=str,
                        default=None,
                        help="Log file of a previous optimization session.")

    train_parser.add_argument("-s", "--save-model-path", 
                        dest="save_model_path",
                        type=str,
                        default=None, 
                        help="If set save model to this path after training.")

    return parser.parse_args()



async def main():
    args = parse_arguments()

    if args.mode == "optimize":
        optimize_main(
            filepath=args.filepath,
            num_entries=args.num_entries,
            #test_size=args.test_size,
            #disable_split=args.disable_split,
            mask_columns=args.mask_columns)

    elif args.mode == "train":
        await train_main(
            filepath=args.filepath,
            pretrained_model_path=args.pretrained_model,
            optimizer_session=args.optimizer_session,
            save_model_path=args.save_model_path)

    else:
        log.error("Invalid mode selected.")


if __name__ == "__main__":
    asyncio.run(main())