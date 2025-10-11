# plugin_main.py
# Orchestrator: CLI entrypoint for "render" (sync) and "controller" (async)

from __future__ import annotations

import argparse
import asyncio
import logging
import sys

from logger import setup_logger

# Render path (sync)
# Adjust the import if your renderer lives elsewhere.
try:
    from plugin_renderer import main as renderer_main  # type: ignore
except Exception:  # pragma: no cover
    renderer_main = None  # will be checked at runtime

# Controller path (async)
# We import the coroutine and run it with asyncio.run(...)
from plugin_controller import _run_async as controller_main  # type: ignore


log = setup_logger("Plugin Main", level=logging.INFO)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plugin orchestrator: render (sync) or controller (async)."
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)

    # ---- render subcommand (sync) ----
    render_parser = subparsers.add_parser(
        "render", help="Run the rendering pipeline (synchronous)"
    )
    render_parser.add_argument(
        "--render-mode",
        dest="render_mode",
        type=str,
        default="default",
        help="Rendering mode/preset to use.",
    )
    render_parser.add_argument(
        "-d",
        "--directory",
        dest="directory",
        type=str,
        required=True,
        help="Base directory for inputs/outputs.",
    )
    render_parser.add_argument(
        "--dataset-filename",
        dest="dataset_filename",
        type=str,
        required=True,
        help="Dataset file name.",
    )
    render_parser.add_argument(
        "--silence-thresh",
        dest="silence_thresh",
        type=float,
        default=-40.0,
        help="Silence threshold (dB).",
    )
    render_parser.add_argument(
        "--no-iterations",
        dest="no_iterations",
        type=int,
        default=1,
        help="Number of iterations.",
    )

    # ---- controller subcommand (async) ----
    controller_parser = subparsers.add_parser(
        "controller",
        help="Run the OSC controller (async) that forwards to ReaLearn.",
    )
    controller_parser.add_argument(
        "-f",
        "--filepath",
        dest="filepath",
        type=str,
        required=True,
        help="Path to the JSON file containing the OSC addresses scheme.",
    )
    controller_parser.add_argument(
        "-i",
        "--ingest",
        dest="ingest",
        type=str,
        choices=["none", "touch", "imu", "orientation"],
        default="none",
        help="Select the pre-processing function applied to incoming data.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    try:
        if args.mode == "render":
            if renderer_main is None:
                log.error("Renderer is unavailable (import failed).")
                sys.exit(1)

            log.info(
                "Starting render | mode=%s dir=%s dataset=%s iterations=%s silence=%s",
                args.render_mode,
                args.directory,
                args.dataset_filename,
                args.no_iterations,
                args.silence_thresh,
            )

            renderer_main(
                render_mode=args.render_mode,
                directory=args.directory,
                dataset_filename=args.dataset_filename,
                silence_thresh=args.silence_thresh,
                no_iterations=args.no_iterations,
            )

        elif args.mode == "controller":
            log.info(
                "Starting controller | filepath=%s ingest=%s",
                args.filepath,
                args.ingest,
            )
            # controller_main is an async coroutine imported from plugin_controller_async
            asyncio.run(controller_main(filepath=args.filepath, proc_mode=args.ingest))

        else:
            log.error("Invalid mode selected: %s", args.mode)
            sys.exit(1)

    except KeyboardInterrupt:
        log.info("Interrupted by user.")
        sys.exit(130)

    except Exception as e:
        log.exception("Fatal error: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
