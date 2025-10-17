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
        "render",
        help="Render plugin presets or random parameter sets to audio and CSV dataset"
    )
    render_parser.add_argument(
        "-m",
        "--mode",
        dest="render_mode",
        type=str,
        choices=["preset", "random"],
        default="preset",
        help="Render mode: 'preset' = export all factory/user presets, 'random' = generate random parameter sets (default: preset)",
    )
    render_parser.add_argument(
        "-d",
        "--device",
        dest="device_id",
        type=int,
        required=False,
        default=None,
        help="Audio input device ID (if not provided, will prompt interactively)",
    )
    render_parser.add_argument(
        "-o",
        "--output",
        dest="dataset_filename",
        type=str,
        required=True,
        help="Output dataset filename (saved to data/ folder as CSV)",
    )
    render_parser.add_argument(
        "-t",
        "--threshold",
        dest="silence_thresh",
        type=float,
        default=0.001,
        help="Silence detection threshold for filtering empty recordings (default: 0.001)",
    )
    render_parser.add_argument(
        "-n",
        "--num-iterations",
        dest="no_iterations",
        type=int,
        default=100,
        help="Number of random presets to generate (only used in 'random' mode, default: 100)",
    )
    render_parser.add_argument(
        "--plugin-dir",
        dest="directory",
        type=str,
        required=False,
        default="default_plugin",
        help="Subfolder name for rendered audio files (default: default_plugin)",
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
                "Starting render | mode=%s dir=%s dataset=%s device=%s iterations=%s silence=%s",
                args.render_mode,
                args.directory,
                args.dataset_filename,
                args.device_id,
                args.no_iterations,
                args.silence_thresh,
            )

            renderer_main(
                render_mode=args.render_mode,
                directory=args.directory,
                dataset_filename=args.dataset_filename,
                silence_thresh=args.silence_thresh,
                no_iterations=args.no_iterations,
                device_id=args.device_id,
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
