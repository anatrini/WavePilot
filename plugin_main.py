# plugin_main.py
# Orchestrator: CLI entrypoint for "render" (sync) and "controller" (async)

from __future__ import annotations

import argparse
import asyncio
import logging
import sys

from logger import setup_logger
from constants import FORWARD_PORT, SEND_PORT, WEBAPP_HOST

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
    render_parser.add_argument(
        "--osc-host",
        dest="osc_host",
        type=str,
        default=WEBAPP_HOST,
        help=f"OSC target host for REAPER communication (default: {WEBAPP_HOST})",
    )
    render_parser.add_argument(
        "--osc-port",
        dest="osc_port",
        type=int,
        default=SEND_PORT,
        help=f"OSC target port for REAPER communication (default: {SEND_PORT})",
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
    controller_parser.add_argument(
        "--osc-host",
        dest="osc_host",
        type=str,
        default=WEBAPP_HOST,
        help=f"OSC target host for forwarding (default: {WEBAPP_HOST})",
    )
    controller_parser.add_argument(
        "--osc-port",
        dest="osc_port",
        type=int,
        default=FORWARD_PORT,
        help=f"OSC target port for forwarding (default: {FORWARD_PORT})",
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
                "Starting render | mode=%s dir=%s dataset=%s device=%s iterations=%s silence=%s osc_target=%s:%d",
                args.render_mode,
                args.directory,
                args.dataset_filename,
                args.device_id,
                args.no_iterations,
                args.silence_thresh,
                args.osc_host,
                args.osc_port,
            )

            renderer_main(
                render_mode=args.render_mode,
                directory=args.directory,
                dataset_filename=args.dataset_filename,
                silence_thresh=args.silence_thresh,
                no_iterations=args.no_iterations,
                device_id=args.device_id,
                osc_host=args.osc_host,
                osc_port=args.osc_port,
            )

        elif args.mode == "controller":
            log.info(
                "Starting controller | filepath=%s ingest=%s osc_target=%s:%d",
                args.filepath,
                args.ingest,
                args.osc_host,
                args.osc_port,
            )
            # controller_main is an async coroutine imported from plugin_controller_async
            asyncio.run(controller_main(
                filepath=args.filepath,
                proc_mode=args.ingest,
                osc_host=args.osc_host,
                osc_port=args.osc_port
            ))

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
